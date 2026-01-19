import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

from code_sentinel.config import config

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")


class LLMFactory:
    """
    factory class
    return gpt or deepseek model based on provider
    """

    @staticmethod
    def get_llm():
        if LLM_PROVIDER == "openai":
            return init_chat_model(
                model="gpt-4o",
                api_key=config.OPENROUTER_API_KEY,
                base_url=config.OPENROUTER_BASE_URL,
                model_provider=LLM_PROVIDER,
                temperature=0.1,
                timeout=300,
            )
        elif LLM_PROVIDER == "deepseek":
            return init_chat_model(
                model="deepseek-chat",
                model_provider=LLM_PROVIDER,
                temperature=0.1,
                timeout=300,
            )
        else:
            raise ValueError("Unknown LLM provider")


llm_service = LLMFactory.get_llm()

if __name__ == "__main__":
    LLM_PROVIDER = "openai"
    print(f"=========test {LLM_PROVIDER} llm==========")
    openai_llm = LLMFactory.get_llm()
    openai_result = openai_llm.invoke("Where is Beijing?")
    print(f"OpenAI LLM Response: {openai_result}")

    LLM_PROVIDER = "deepseek"
    print(f"=========test {LLM_PROVIDER} llm==========")
    deepseek_llm = LLMFactory.get_llm()
    deepseek_result = deepseek_llm.invoke("Where is Beijing?")
    print(f"DeepSeek LLM Response: {deepseek_result}")
