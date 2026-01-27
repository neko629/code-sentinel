from typing import List, TypedDict, Annotated, Optional
import operator

def merge_comments(left: List[str], right: List[str]) -> List[str]:
    """merge two lists of comments"""
    return left + right

class ReviewState(TypedDict):
    """state of graph"""

    # input data
    diff_content: str
    language: str

    # related code snippets retrieved from knowledge base
    repo_context: Optional[str]

    style_check_tool_result: Optional[str]

    security_comments: Annotated[List[str], operator.add]
    performance_comments: Annotated[List[str], operator.add]
    style_comments: Annotated[List[str], operator.add]

    final_report: str