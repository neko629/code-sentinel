import time
import logging
from langchain_chroma import Chroma
from langchain.embeddings import init_embeddings
from dotenv import load_dotenv

load_dotenv(verbose=True)

from code_sentinel.config import config

logger = logging.getLogger(__name__)

class CodeKnowledgeBase:
    """Wrapper for ChromaDB"""
    def __init__(self, persist_dir: str = "./chroma_db"):
        print(f">>> open router config: key {config.OPENROUTER_API_KEY}, url {config.OPENROUTER_BASE_URL}")
        # init embedding
        self.embedding_model = init_embeddings(
            model="gemini-embedding-001",
            provider="google_genai",
            timeout=60
        )

        self.persist_dir = persist_dir

        # init vector db
        self._initialize_vector_store()

    def _initialize_vector_store(self):
        """初始化向量存储"""
        try:
            self.vector_store = Chroma(
                collection_name="project_codebase",
                embedding_function=self.embedding_model,
                persist_directory=self.persist_dir)
            # 测试集合是否可用
            self.vector_store._collection.count()
        except Exception as e:
            logger.warning(
                f"Vector store initialization failed: {e}. Creating new collection...")
            # 如果失败,删除旧数据并重新创建
            try:
                Chroma(
                    collection_name="project_codebase",
                    embedding_function=self.embedding_model,
                    persist_directory=self.persist_dir
                ).delete_collection()
            except:
                pass

            self.vector_store = Chroma(
                collection_name="project_codebase",
                embedding_function=self.embedding_model,
                persist_directory=self.persist_dir
            )

    def add_documents(self, documents: list):
        """insert code block into vector db"""
        if not documents:
            return

        valid_docs = [doc for doc in documents if doc.page_content.strip()]
        if not valid_docs:
            print("No valid documents to add")
            return

        print(f"\n\n>>>>> insert {len(documents)} documents into vector db...")

        batch_size = 10
        for i in range(0, len(valid_docs), batch_size):
            batch = valid_docs[i:i + batch_size]
            try:
                self.vector_store.add_documents(batch)
                print(f"Processed batch {i//batch_size + 1} / {(len(valid_docs) + batch_size - 1)//batch_size}")
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error adding documents to vector store: {e}")
                continue
        print(">>>>> insert completed.\n\n")

    def search_related_code(self, query: str, k: int = 4):
        """search related code blocks from vector db"""
        results = self.vector_store.similarity_search(query, k=k)
        return results

    def clear(self):
        """empty db"""
        self.vector_store.delete_collection()
        self._initialize_vector_store()

# singleton instance
knowledge_base = CodeKnowledgeBase()
