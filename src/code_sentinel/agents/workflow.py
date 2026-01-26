from langgraph.graph import StateGraph, END, START

from code_sentinel.agents.graph_state import ReviewState
from code_sentinel.agents.nodes import (
    security_node,
    performace_node,
    style_node,
    summary_node
)

# 1. init graph
workflow = StateGraph(ReviewState)

# 2. add nodes
workflow.add_node("security_agent", security_node)
workflow.add_node("performance_agent", performace_node)
workflow.add_node("style_agent", style_node)
workflow.add_node("summary_agent", summary_node)

# 3 set edges

# set entry
workflow.set_entry_point("security_agent")

# add edges
workflow.add_edge(START, "security_agent")
workflow.add_edge(START, "performance_agent")
workflow.add_edge(START, "style_agent")
workflow.add_edge("security_agent", "summary_agent")
workflow.add_edge("performance_agent", "summary_agent")
workflow.add_edge("style_agent", "summary_agent")
workflow.add_edge("summary_agent", END)

# 4 compile
app = workflow.compile()
