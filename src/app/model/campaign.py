"""Campaign module"""

# Third-party library imports
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

@dataclass
class Campaign:
    id: Optional[int]
    name: str
    type: str
    start_date: date
    end_date: date
    advertiser: str
    impressions_delivered: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        # Automatically set created_at and updated_at if not provided
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()