from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from code_sentinel.agents.graph_state import ReviewState
from code_sentinel.core.llm_factory import llm_service
from code_sentinel.agents.prompts import (
    SECURITY_PROMPT, PERFORMANCE_PROMPT, STYLE_PROMPT, SUMMARY_PROMPT
)

def _call_agent(system_prompt: str, state: ReviewState) -> List[str]:
    """public helper"""
    diff = state["diff_content"]
    lang = state["language"]

    # build prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "请审查以下代码变更 (Diff):\n\n{diff}\n\n代码语言: {lang}"),
    ])

    # build a chain
    chain = prompt | llm_service | StrOutputParser()
    responses = chain.invoke({"diff": diff, "lang": lang})

    # if no comments, return null list
    # if len(responses) < 20:
    #     return []

    return [responses]

def security_node(state: ReviewState):
    """comments from security agent"""
    print("\n\n>>>>Executing security node...")
    return {"security_comments": _call_agent(SECURITY_PROMPT, state)}

def performance_node(state: ReviewState):
    """comments from  performance agent"""
    print("\n\n>>>>Executing performance node...")
    return {"performance_comments": _call_agent(PERFORMANCE_PROMPT, state)}

def style_node(state: ReviewState):
    """comments from  code style agent"""
    print("\n\n>>>>Executing style node...")
    return {"style_comments": _call_agent(STYLE_PROMPT, state)}

def summary_node(state: ReviewState):
    """comments from  summary agent"""
    print("\n\n>>>>Executing summary node...")
    security_comments = state.get("security_comments", [])
    performace_comments = state.get("performance_comments", [])
    style_comments = state.get("style_comments", [])

    # build input prompt
    inputs = f"""
    [Security Report]: {security_comments},
    [Performance Report]: {performace_comments},
    [Style Report]: {style_comments}
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SUMMARY_PROMPT),
            ("human", "各方意见汇总:\n{inputs}")
        ]
    )

    chain = prompt | llm_service | StrOutputParser()
    final_report = chain.invoke({"inputs": inputs})

    return {"final_report": final_report}