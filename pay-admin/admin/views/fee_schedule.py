"""Copyright 2021 Province of British Columbia.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from flask_admin.contrib.sqla.filters import BaseSQLAFilter, FilterEqual
from flask_admin.contrib import sqla
from flask import has_request_context
from pay_api.models import CorpType, db, FeeSchedule, FeeCode

from .secured_view import SecuredView


class FeeScheduleConfig(SecuredView):
    """Fee Schedule config."""

    # Allow export as a CSV file.
    can_export = False

    # Allow the user to change the page size.
    can_set_page_size = True

    column_display_pk = True

    can_delete = False

    column_list = ['corp_type_code', 'filing_type_code', 'fee', 'future_effective_fee', 'priority_fee', 'service_fee']

    column_labels = {
        'corp_type': 'Corp Type',
        'corp_type_code': 'Corp Type',
        'filing_type': 'Filing Type',
        'filing_type_code': 'Filing Type',
        'fee': 'Filing Fee',
        'fee_start_date': 'Fee effective start date',
        'fee_end_date': 'Fee End Date',
        'future_effective_fee': 'Future Effective Fee',
        'priority_fee': 'Priority Fee',
        'service_fee': 'Service Fee',
        'distribution_codes': 'Distribution Code'
    }
    column_searchable_list = ('corp_type_code', 'filing_type_code')
    column_sortable_list = ('corp_type_code',)

    column_default_sort = 'corp_type_code'

    form_args = {
        # 'fee_code': get_fee_codes(('ss'))
        # 'fee_code': {
        #     'query_factory': lambda: FeeCode.query.filter(FeeCode.code.like('EN%'))
        # }
    }

    form_columns = ['corp_type', 'filing_type', 'fee', 'fee_start_date',
                    'fee_end_date', 'future_effective_fee', 'priority_fee', 'service_fee',
                    'distribution_codes']
    edit_columns = ['corp_type', 'filing_type', 'fee_start_date',
                    'fee_end_date', 'priority_fee', 'service_fee',
                    'distribution_codes']

    def _change_labels(self, form):
        form.fee.label.text = 'Filing Fee (Starts with \'EN\')'
        form.future_effective_fee.label.text = 'Future Effective Fee (Starts with \'FUT\')'
        form.priority_fee.label.text = 'Priority Fee (Starts with \'PRI\')'
        form.service_fee.label.text = 'Service Fee (Starts with \'TRF\')'

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        self._change_labels(form)
        return form

    def create_form(self, obj=None):
        form = super().create_form(obj)
        self._change_labels(form)
        return form


# If this view is going to be displayed for only special roles, do like below
FeeScheduleView = FeeScheduleConfig(FeeSchedule, db.session)
