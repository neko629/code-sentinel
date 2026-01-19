import os

from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")

# graph config
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

if __name__ == "__main__":
    print(f"DEEPSEEK_API_KEY: {DEEPSEEK_API_KEY}")
    print(f"OPENROUTER_API_KEY: {OPENROUTER_API_KEY}")
    print(f"OPENROUTER_BASE_URL: {OPENROUTER_BASE_URL}")
    print(f"LANGSMITH_API_KEY: {LANGSMITH_API_KEY}")
