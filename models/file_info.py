from enum import IntEnum
from typing import List

from pydantic import BaseModel, Field


class ClaimMode(IntEnum):
    """Enumeration of file claim modes."""
    UNCLAIMED = 0
    EXCLUSIVE = 1
    SHARED = 2


class FileInfo(BaseModel):
    """File information model for tracking and managing files."""
    file_id: str
    file_hash: str
    user_ids: List[str]
    branch_name: str
    claim_mode: ClaimMode
