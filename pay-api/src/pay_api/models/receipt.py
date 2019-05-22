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
"""Model to handle all operations related to Receipt."""

from sqlalchemy import ForeignKey

from .base_model import BaseModel
from .db import db, ma


class Receipt(db.Model, BaseModel):
    """This class manages all of the base data about Receipt."""

    __tablename__ = 'receipt'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    invoice_id = db.Column(db.Integer, ForeignKey('invoice.id'), nullable=False)
    receipt_number = db.Column(db.String(50), nullable=False)
    receipt_date = db.Column(db.DateTime)
    receipt_amount = db.Column(db.Integer)


class ReceiptSchema(ma.ModelSchema):
    """Main schema used to serialize the Receipt."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Returns all the fields from the SQLAlchemy class."""

        model = Receipt
