from enum import IntEnum

from pydantic import BaseModel, Field


class ClaimMode(IntEnum):
    """Enumeration of file claim modes."""
    UNCLAIMED = 0
    EXCLUSIVE = 1
    SHARED = 2


class FileInfo(BaseModel):
    """File information model for tracking and managing files."""
    file_id: str = Field(serialization_alias="fileId")
    file_hash: str = Field(serialization_alias="fileHash")
    user_ids: int = Field(serialization_alias="userIds")
    branch_name: str = Field(serialization_alias="branchName")
    claim_mode: ClaimMode = Field(serialization_alias="claimMode")


class ListFilesResponse(BaseModel):
    """Response model for listing files."""
    nextCursor: int = Field(serialization_alias="nextCursor")
    files: list[FileInfo] = Field(serialization_alias="files")
