from langgraph.graph import StateGraph, END, START

from code_sentinel.agents.graph_state import ReviewState
from code_sentinel.agents.nodes import (
    security_node,
    performance_node,
    style_node,
    summary_node
)

def route_diff(state: ReviewState):
    """filter some content that not need to comment"""
    diff = state["diff_content"]
    if "Process finished with exit code" in diff:
        return END
    return ["security_agent", "performance_agent", "style_agent"]

# 1. init graph
workflow = StateGraph(ReviewState)

# 2. add nodes
workflow.add_node("security_agent", security_node)
workflow.add_node("performance_agent", performance_node)
workflow.add_node("style_agent", style_node)
workflow.add_node("summary_agent", summary_node)

# 3 set edges

workflow.set_conditional_entry_point(
    route_diff
)

workflow.add_edge("security_agent", "summary_agent")
workflow.add_edge("performance_agent", "summary_agent")
workflow.add_edge("style_agent", "summary_agent")
workflow.add_edge("summary_agent", END)

# 4 compile
app = workflow.compile()
