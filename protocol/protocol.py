from enum import IntEnum
from typing import List

from pydantic import BaseModel, Field


class ClaimMode(IntEnum):
    """Enumeration of file claim modes."""
    UNCLAIMED = 0
    EXCLUSIVE = 1
    SHARED = 2


class FileInfoResponse(BaseModel):
    """File information model for tracking and managing files."""
    file_id: str = Field(alias="fileId")
    file_hash: str = Field(alias="fileHash")
    user_ids: List[str] = Field(alias="userIds")
    branch_name: str = Field(alias="branchName")
    claim_mode: ClaimMode = Field(alias="claimMode")


class ListFilesResponse(BaseModel):
    """Response model for listing files."""
    nextCursor: int = Field(alias="nextCursor")
    files: List[FileInfoResponse] = Field(alias="files")
