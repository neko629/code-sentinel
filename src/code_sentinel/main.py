import os

from dotenv import load_dotenv

from code_sentinel.core.review_service import review_service

# 加载环境变量
load_dotenv()


def test_llm_layer():
    print(">>> 正在初始化 AI 审查员...")

    # 模拟一段很烂的 Java 代码 Diff
    bad_java_code = """
    + public class UserController {
    +     public User getUser(String id) {
    +         // TODO: fix later
    +         String sql = "SELECT * FROM users WHERE id = '" + id + "'";
    +         return db.query(sql);
    +     }
    + }
    """

    print(">>> 发送代码给 AI (Provider: {})...".format(os.getenv("LLM_PROVIDER")))

    try:
        # 调用服务
        result = review_service.review_code(language="Java", code_diff=bad_java_code)

        print("\n=== AI 审查意见 ===")
        print(result)
        print("===================")

    except Exception as e:
        print(f"❌ 调用失败: {e}")


if __name__ == "__main__":
    test_llm_layer()
