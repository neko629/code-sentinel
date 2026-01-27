from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from code_sentinel.agents.graph_state import ReviewState
from code_sentinel.core.llm_factory import llm_service
from code_sentinel.agents.tools import retrieve_related_code
from code_sentinel.agents.prompts import (
    SECURITY_PROMPT, PERFORMANCE_PROMPT, STYLE_PROMPT, SUMMARY_PROMPT
)

def _call_agent(system_prompt: str, state: ReviewState) -> List[str]:
    """public helper"""
    diff = state["diff_content"]
    lang = state["language"]

    context = state.get("repo_context", "")

    if not context:
        context = "No additional context available."

    # build prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "请审查以下代码变更 (Diff):\n\n{diff}\n\n代码语言: {lang},\n相关上下文:{context}"),
    ])

    # build a chain
    chain = prompt | llm_service | StrOutputParser()
    responses = chain.invoke({"diff": diff, "lang": lang, "context": context})

    # if no comments, return null list
    # if len(responses) < 20:
    #     return []

    return [responses]

def retrieve_context_node(state: ReviewState):
    """RAG retrieve node: retrieve related code snippets from knowledge base"""
    diff = state["diff_content"]

    # 暂时简单处理, 后续考虑通过 deepagent 实现 ReAct
    lines = diff.split("\n")
    keywords = []
    for line in lines:
        if line.startswith("+") and ("class " in line or 'def ' in line):
            clean_line = line.replace("+", "").replace("class ", "").replace("def ", "")
            keywords.append(clean_line)

    if not keywords:
        print("[Retriever] No related code found, skip")
        return {"repo_context": ""}

    query = " ".join(keywords[:3])
    print(f"[Retriever] 提取到关键词: {query}")

    context_str = retrieve_related_code.invoke({"query": query})
    return {"repo_context": context_str}

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