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

@tool
def run_java_lint(code_content: str) -> str:
    """
    对 Java 代码运行静态代码分析 (Linter)。
    当需要检查代码格式、命名规范、行长度限制时，请调用此工具。

    Args:
        code_content: 需要检查的 Java 源代码内容。
    """

    print("[Java Linter Tool] start....")
    # subprocess.run(
    #     ["java", "-jar", "checkstyle.jar", "-c", "google_checks.xml", tmp_file])

    report = []
    lines = code_content.split("\n")

    for i, line in enumerate(lines):
        line_num = i + 1

        if len(line) > 120:
            report.append(f"[CheckStyle] Line {line_num}: 行长度超过 120 个字符。")

        if "System.out.println" in line:
            report.append(f"[CheckStyle] Line {line_num}: 避免使用 System.out.println 进行调试。")

        if "class " in line:
            parts= line.split("class ")
            if len(parts) > 1 and parts[1]:
                class_name = parts[1].strip().split(" ")[0]
                if class_name and class_name[0].islower():
                    report.append(f"[CheckStyle] Line {line_num}: 类名 '{class_name}' 应以大写字母开头。")

    if not report:
        return "[CheckStyle] 未发现代码风格问题。"

    return "[CheckStyle] 发现以下代码风格问题:\n" + "\n".join(report)

