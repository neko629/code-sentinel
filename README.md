# Code Sentinel

**Code Sentinel** is an AI-powered code review agent designed to automate and enhance the code review process, particularly for Pull Requests. It leverages advanced Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) to provide intelligent feedback, integrate seamlessly with Git platforms like GitHub, and capture user feedback for continuous improvement.

## Features

*   **AI-Powered Code Reviews**: Automatically review code changes in pull requests using state-of-the-art LLMs.
*   **GitHub Webhook Integration**: Listen for GitHub `pull_request` (opened, synchronize) and `pull_request_review_comment` events to trigger automated reviews and process user feedback.
*   **Customizable LLM Providers**: Supports various LLM providers (DeepSeek, OpenAI, OpenRouter, Google GenAI) via LangChain.
*   **Knowledge Base with RAG**: Utilizes ChromaDB for maintaining a knowledge base, potentially for contextual code analysis or storing past feedback.
*   **User Feedback Mechanism**: Captures explicit user feedback from PR review comments to improve model performance and accuracy.
*   **Persisted Data**: Uses Docker volumes for persistent storage of the vector database (ChromaDB) and feedback memory (SQLite).

## Technologies Used

*   **FastAPI**: High-performance web framework for building the API.
*   **LangChain / LangGraph**: Frameworks for developing applications powered by LLMs.
*   **ChromaDB**: Open-source embedding database for knowledge base management.
*   **Uvicorn**: ASGI server for running the FastAPI application.
*   **Python-dotenv**: For managing environment variables.
*   **PyGithub**: Python library to access the GitHub API.
*   **Pydantic**: Data validation and settings management using Python type hints.
*   **SQLAlchemy**: ORM for database interactions (e.g., feedback memory).

## Getting Started

### Prerequisites

Ensure you have the following installed:

*   **Python 3.11+**
*   **Poetry**: For dependency management. Install it via `curl -sSL https://install.python-poetry.org | python3 -`
*   **Docker & Docker Compose**: For containerized deployment.

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-org/code-sentinel.git
    cd code-sentinel
    ```

2.  **Initialize Poetry and install dependencies**:
    ```bash
    poetry init # if not already initialized
    poetry install
    ```
    This will install all required dependencies including FastAPI, LangChain components, ChromaDB, etc.

3.  **Configuration**:
    Create a `.env` file in the project root by copying `.env.example` and fill in your credentials and settings:
    ```bash
    cp .env.example .env
    ```
    Edit the `.env` file:
    ```ini
    # llm config
    # provider deepseek or openai
    LLM_PROVIDER = deepseek # or openai, openrouter, google_genai

    # Example API Keys - fill with your actual keys
    DEEPSEEK_API_KEY=your_deepseek_api_key_here
    OPENROUTER_API_KEY=your_openrouter_api_key_here
    OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
    GOOGLE_API_KEY=your_google_api_key_here
    OPENAI_API_KEY=your_openai_api_key_here

    # LangSmith (LangChain Tracing) config (optional but recommended for debugging)
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
    LANGCHAIN_API_KEY=lsv2_xxxxxxxxxxxxxxxxxxxx # Your LangSmith API key
    LANGCHAIN_PROJECT="code-review-agent-dev" # Your LangSmith project name

    # GitHub Integration
    GIT_WEBHOOK_SECRET=your_webhook_secret_here # A secret phrase for GitHub webhook verification
    GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxx # A GitHub Personal Access Token with repo scope
    ```
    *Note: Ensure your GitHub Token has the necessary permissions (e.g., `repo` scope) to fetch PR diffs and post comments.*

## Running the Application

### Locally with Poetry

To run the FastAPI application directly using Poetry:

```bash
poetry run uvicorn src.code_sentinel.main:app --host 0.0.0.0 --port 8000 --reload
```
The API will be available at `http://0.0.0.0:8000`.

### Using Docker Compose

For a containerized setup, use Docker Compose:

```bash
docker-compose up -d
```
This will build the Docker image and start the `code-sentinel` service in the background, exposing it on port `8000`. Persistent data for `chroma_db` and `feedback_memory.db` will be stored in the `./chroma_db` and `./feedback_memory.db` directories on your host.

## API Endpoints

The API provides endpoints for manual code review requests and automated GitHub webhook processing.

### 1. `POST /api/v1/review`

Manually trigger a code review for a given code snippet.

*   **Description**: Receives code content and its language, and returns AI-generated review comments.
*   **Request Body**:
    ```json
    {
        "diff_content": "string",  # The code snippet or diff content to review
        "language": "string"       # The programming language (e.g., "Python", "Java", "Markdown")
    }
    ```
*   **Response Body**:
    ```json
    {
        "comments": "string"       # AI-generated review comments
    }
    ```

### 2. `POST /api/v1/webhook`

Receives and processes GitHub webhook events.

*   **Description**: This endpoint is configured as a webhook listener in your GitHub repository settings. It processes `pull_request` events to trigger automated reviews and `pull_request_review_comment` events for feedback.
*   **Headers**:
    *   `X-GitHub-Event`: Type of GitHub event (e.g., `pull_request`, `pull_request_review_comment`).
    *   `X-Hub-Signature-256`: HMAC hex digest of the request body, used for signature verification with `GIT_WEBHOOK_SECRET`.
*   **Event Handling**:
    *   **`pull_request` (actions: `opened`, `synchronize`)**: Triggers an AI code review for the PR's changes and posts comments back to the PR.
    *   **`pull_request_review_comment` (action: `created`)**: Processes comments that contain specific trigger phrases (e.g., "false positive", "wrong", "误报") as user feedback and records them.

## Development & Contributing

### Environment Setup & Code Standards

#### 1. Poetry Initialization (Already covered in Installation)

#### 2. Configure Code Formatter and Linter (Ruff)

Ruff is used for both linting and formatting the codebase. Configuration is defined in `pyproject.toml`.

To check for issues:
```bash
poetry run ruff check .
```
To automatically format and fix linting issues:
```bash
poetry run ruff format .
```

#### 3. Configure Pre-commit Hooks

Pre-commit hooks are used to automatically run Ruff checks and formatting before each commit, ensuring code quality.

1.  **Install pre-commit hooks**:
    ```bash
    poetry run pre-commit install
    ```
    The `.pre-commit-config.yaml` file in the root directory defines the hooks.

2.  **Hooks in use**:
    *   `ruff`: Checks for linting errors.
    *   `ruff-format`: Automatically formats code according to `pyproject.toml` settings.
