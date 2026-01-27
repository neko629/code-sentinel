from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# init SQLite
DATEBASE_URL = "sqlite:///./feedback_memory.db"
engine = create_engine(
    DATEBASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# db model
class FalsePositiveCase(Base):
    __tablename__ = "false_positives"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, index=True)
    code_snippet = Column(Text)
    ai_comment = Column(Text)
    user_feedback = Column(Text)

# create table
Base.metadata.create_all(bind=engine)

def add_feedback(file_path, code, comment, feedback):
    session = SessionLocal()
    case = FalsePositiveCase(
        file_path=file_path,
        code_snippet=code,
        ai_comment=comment,
        user_feedback=feedback
    )
    session.add(case)
    session.commit()
    session.close()

def get_similar_mistakes(k=5) -> str:
    """先展示取最近的 k 条, 后续考虑改成向量数据库做语言搜索"""
    session = SessionLocal()

    cases = session.query(FalsePositiveCase).order_by(FalsePositiveCase.id.desc()).limit(k).all()
    session.close()

    if not cases:
        return ''

    examples = "\n".join(
        [
            f"File: {case.file_path}\nCode Snippet: {case.code_snippet}\nAI Comment: {case.ai_comment}\nUser Feedback: {case.user_feedback}\n" for case in cases
        ]
    )

    return f"Here are some examples of previous false positive cases:\n{examples}"
