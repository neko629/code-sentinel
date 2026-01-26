from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from code_sentinel.core.llm_factory import llm_service
from code_sentinel.agents.workflow import app as graph_app


class ReviewService:
    """main logic for review code"""

    def __init__(self):
        # define prompt template
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
            你是一位拥有 15 年经验的资深 {language} 架构师。
            你的任务是审查代码变更(Git Diff)，并从以下三个维度给出专业的改进建议：
            1. 代码规范与风格 (Clean Code)
            2. 潜在的 Bug 与 安全漏洞 (Security)
            3. 性能优化 (Performance)
            请保持客观、严厉但建设性。
            如果代码没有明显问题，请直接回复"LGTM"(Looks Good To Me)。
            """,
                ),
                ("human", "请审查以下代码变更:\n\n{code_diff}"),
            ]
        )

        # build a chain
        self.chain = self.prompt_template | llm_service | StrOutputParser()

    def review_code(self, language: str, code_diff: str) -> str:
        """review code diff and return suggestions"""
        response = self.chain.invoke({"language": language, "code_diff": code_diff})
        return response

    async def review_code_async(self, code_diff: str, language: str = 'python') -> str:
        """call agent asynchronously"""
        inputs = {
            "diff_content": code_diff,
            "language": language,
            "security_comments": [],
            "performance_comments": [],
            "style_comments": []
        }
        result = await graph_app.ainvoke(inputs)
        return result.get("final_report", "Review generation failed!")


review_service = ReviewService()
