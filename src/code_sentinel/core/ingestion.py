from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_community.document_loaders import TextLoader
import os

from code_sentinel.core.knowledge_base import knowledge_base

def load_and_index_codebase(root_path: str):
    """scan repo, build index"""
    print(f"\n\n>>> start scan code repo...")
    documents = []

    # 1. walk
    for dirpath, _, filenames in os.walk(root_path):
        # ignore hidden dir and v-env
        if any(part.startswith(".") for part in dirpath.split(os.sep)):
            continue

        for file in filenames:
            if file.endswith(".py"):
                full_path = os.path.join(dirpath, file)
                try:
                    loader = TextLoader(full_path, encoding="utf-8")
                    documents.extend(loader.load())
                except Exception as e:
                    print(f"skip file {full_path} due to error: {e}")

    print(f">>> load {len(documents)} files")

    # 2. chunking
    splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=1000,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)
    print(f">>> split {len(chunks)} documents")

    # 3. indexing
    knowledge_base.clear()
    knowledge_base.add_documents(chunks)

    print(f">>> build knowledge base complete.")

if __name__ == "__main__":
    current_dir = os.getcwd()
    load_and_index_codebase(current_dir)
