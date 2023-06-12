from pydantic import BaseModel, conint
from enum import Enum
from datetime import datetime
from typing import TypedDict, Optional


class OperatorEnum(Enum):
    EQ = 'eq'
    GT = 'gt'
    LT = 'lt'
    GE = 'ge'
    LE = 'le'


class SearchBody(BaseModel):
    """Model of data for request body for search."""
    text: Optional[str] = None
    file_mask: Optional[str] = None
    size: Optional[TypedDict(
        "size", {"value": conint(ge=0), "operator": OperatorEnum})] = None
    creation_time: Optional[TypedDict(
        "creation_time", {"value": datetime, "operator": OperatorEnum})] = None
