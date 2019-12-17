# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests to assure the Receipt Service.

Test-Suite to ensure that the Receipt Service is working as expected.
"""

from datetime import datetime

import pytest

from pay_api.exceptions import BusinessException
from pay_api.models import FeeSchedule
from pay_api.services.payment_service import PaymentService
from pay_api.services.receipt import Receipt as ReceiptService
from tests.utilities.base_test import (
    factory_invoice, factory_invoice_reference, factory_payment, factory_payment_account, factory_payment_line_item,
    factory_payment_transaction, get_payment_request)


def test_receipt_saved_from_new(session):
    """Assert that the receipt is saved to the table."""
    payment_account = factory_payment_account()
    payment = factory_payment()
    payment_account.save()
    payment.save()
    i = factory_invoice(payment_id=payment.id, account_id=payment_account.id)
    i.save()
    factory_invoice_reference(i.id).save()

    receipt_service = ReceiptService()
    receipt_service.receipt_number = '1234567890'
    receipt_service.invoice_id = i.id
    receipt_service.receipt_date = datetime.now()
    receipt_service.receipt_amount = 100
    receipt_service = receipt_service.save()

    receipt_service = ReceiptService.find_by_id(receipt_service.id)

    assert receipt_service is not None
    assert receipt_service.id is not None
    assert receipt_service.receipt_date is not None
    assert receipt_service.invoice_id is not None

    receipt_service = ReceiptService.find_by_invoice_id_and_receipt_number(i.id, receipt_service.receipt_number)

    assert receipt_service is not None
    assert receipt_service.id is not None


def test_receipt_invalid_lookup(session):
    """Test invalid lookup."""
    receipt = ReceiptService.find_by_id(999)

    assert receipt is not None
    assert receipt.id is None

    receipt = ReceiptService.find_by_invoice_id_and_receipt_number(999, '1234567890')

    assert receipt is not None
    assert receipt.id is None


def test_create_receipt_without_invoice(session):
    """Try creating a receipt without invoice number."""
    payment_account = factory_payment_account()
    payment = factory_payment()
    payment_account.save()
    payment.save()
    invoice = factory_invoice(payment.id, payment_account.id)
    invoice.save()
    factory_invoice_reference(invoice.id).save()
    fee_schedule = FeeSchedule.find_by_filing_type_and_corp_type('CP', 'OTANN')
    line = factory_payment_line_item(invoice.id, fee_schedule_id=fee_schedule.fee_schedule_id)
    line.save()
    transaction = factory_payment_transaction(payment.id)
    transaction.save()

    PaymentService.update_payment(payment.id, get_payment_request(), {'preferred_username': 'test'})
    input_data = {
        'corpName': 'Pennsular Coop ',
        'filingDateTime': '1999',
        'fileName': 'coopser'
    }
    response = ReceiptService.create_receipt(payment.id, '', input_data, skip_auth_check=True)
    assert response is not None


def test_create_receipt_with_invoice(session, app, client):
    """Try creating a receipt with invoice number."""
    payment_account = factory_payment_account()
    payment = factory_payment()
    payment_account.save()
    payment.save()
    invoice = factory_invoice(payment.id, payment_account.id)
    invoice.save()
    factory_invoice_reference(invoice.id).save()
    fee_schedule = FeeSchedule.find_by_filing_type_and_corp_type('CP', 'OTANN')
    line = factory_payment_line_item(invoice.id, fee_schedule_id=fee_schedule.fee_schedule_id)
    line.save()
    transaction = factory_payment_transaction(payment.id)
    transaction.save()

    PaymentService.update_payment(payment.id, get_payment_request(), {'preferred_username': 'test'})
    input_data = {
        'corpName': 'Pennsular Coop ',
        'filingDateTime': '1999',
        'fileName': 'coopser'
    }
    response = ReceiptService.create_receipt(payment.id, invoice.id, input_data, skip_auth_check=True)
    assert response is not None


def test_create_receipt_with_no_receipt(session):
    """Try creating a receipt with invoice number."""
    payment_account = factory_payment_account()
    payment = factory_payment()
    payment_account.save()
    payment.save()
    invoice = factory_invoice(payment.id, payment_account.id)
    invoice.save()
    factory_invoice_reference(invoice.id).save()
    fee_schedule = FeeSchedule.find_by_filing_type_and_corp_type('CP', 'OTANN')
    line = factory_payment_line_item(invoice.id, fee_schedule_id=fee_schedule.fee_schedule_id)
    line.save()

    PaymentService.update_payment(payment.id, get_payment_request(), {'preferred_username': 'test'})
    input_data = {
        'corpName': 'Pennsular Coop ',
        'filingDateTime': '1999',
        'fileName': 'coopser'
    }

    with pytest.raises(BusinessException) as excinfo:
        ReceiptService.create_receipt(payment.id, '', input_data, skip_auth_check=True)
    assert excinfo.type == BusinessException
