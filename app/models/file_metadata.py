from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class FileMetadata(BaseModel):
    user_id: Optional[str] = None
    file_id: Optional[str] = None
    file_extension: Optional[str] = None
    size: int
    bucket: Optional[str] = None
    is_committed: bool = False
    version: Optional[int] = 0
    created_at: datetime = Field(default_factory=datetime.now)
