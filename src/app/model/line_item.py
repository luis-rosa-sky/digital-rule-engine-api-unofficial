"""Line Item module"""

# Third-party library imports
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, List, Dict

@dataclass
class LineItem:
    id: Optional[int]
    order_id: int
    name: str
    status: str
    type: str
    skippable_ad: bool = False
    impressions_delivered: int = 0
    impression_goal: Optional[int] = None
    start_date: date = None
    end_date: date = None
    priority_level: int = None
    delivery_type: str = None
    bookies: List[str] = None
    cpm: Optional[float] = None
    pacing_osi: Optional[float] = None
    targetting_attributes: Optional[Dict] = None
    creative_dimensions: Optional[Dict] = None
    vast_error_codes: Optional[Dict] = None
    ad_unit_mapping: Optional[Dict] = None
    assets_assigned: List[str] = None
    platform: str = None
    fill_rate: Optional[float] = None
    campaign_id: int = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        # Automatically set created_at and updated_at if not provided
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()