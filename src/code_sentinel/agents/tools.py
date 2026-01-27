from langchain.tools import tool

from code_sentinel.core.knowledge_base import knowledge_base

@tool
def retrieve_related_code(query: str) -> str:
    """
    检索项目代码库中的相关代码片段。

    当你发现代码 Diff 中调用了某个未知的函数、类或变量，且你想查看其定义时，
    必须使用此工具。

    Args:
        query: 搜索关键词，例如函数名 "verify_signature" 或类名 "UserManager"。
    """
    print(f"[RAG Tool] 正在搜索: {query}")

    results = knowledge_base.search_related_code(query, k=3)
    if not results:
        return "未找到相关代码片段。"

    # 格式化结果
    formatted_results = []
    for doc in results:
        source = doc.metadata.get("source", "unknown")
        content = doc.page_content
        formatted_results.append(f"--- 来源: {source} ---\n --- 内容: \n{content} \n\n")

    return "\n".join(formatted_results)