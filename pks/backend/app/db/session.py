"""
数据库会话管理

提供数据库会话的依赖注入
"""
from typing import Generator
from sqlalchemy.orm import Session
from app.db.base import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话

    Yields:
        Session: SQLAlchemy会话对象

    Example:
        @app.get("/cards")
        def get_cards(db: Session = Depends(get_db)):
            return db.query(Card).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
