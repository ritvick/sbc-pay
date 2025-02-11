# Copyright © 2022 Province of British Columbia
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
"""Class to record the settlement file information for a payment."""

from datetime import datetime

from pay_api.models.base_model import BaseModel
from .db import db


class CasSettlement(BaseModel):  # pylint: disable=too-few-public-methods
    """This class keeps track of the settlements from CAS, usually provided in CSV format."""

    __tablename__ = 'cas_settlements'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    received_on = db.Column('received_on', db.DateTime, nullable=False, default=datetime.now)
    file_name = db.Column(db.String, nullable=False)
    processed_on = db.Column('processed_on', db.DateTime, nullable=True)
