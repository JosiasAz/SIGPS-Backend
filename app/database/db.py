from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


motor_db = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessaoLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor_db)


def obter_sessao_db():
    db = SessaoLocal()
    try:
        yield db
    finally:
        db.close()