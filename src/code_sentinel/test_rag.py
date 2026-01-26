from code_sentinel.core.knowledge_base import knowledge_base

query = "How is the GitHub signature verification implemented?"

print(f"正在搜索问题: {query}\n")

results = knowledge_base.search_related_code(query, k=2)

for i, doc in enumerate(results):
    print(f"--- 结果 {i + 1} (来源: {doc.metadata['source']}) ---")
    print(doc.page_content[:300] + "...\n")
