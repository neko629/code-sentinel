from typing import Optional

from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    """request dto for code review"""
    diff_content: str = Field(..., description="Git diff content to be reviewed")
    file_path: Optional[str] = Field(None, description="Git diff file path")
    language: str = Field("python", description="Git diff language")

class ReviewResponse(BaseModel):
    """response dto for code review"""
    comments: str = Field(..., description="Review comments from AI")
    status: str = Field("success", description="Review status")
