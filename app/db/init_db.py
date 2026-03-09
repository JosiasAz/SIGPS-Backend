from sqlalchemy.orm import Session
from app.db.base_models import Base
from app.core.config import settings
from app.schemas.user import UserCreate
from app.services.user_service import user_service
from app.repositories.user_repository import user_repository
from app.utils.enums import UserRole

def init_db(db: Session) -> None:
    # Espaço para criar dados iniciais (Seed)
    admin_email = "admin@sigps.com.br"
    user = user_repository.get_by_email(db, email=admin_email)
    if not user:
        user_in = UserCreate(
            email=admin_email,
            password="adminpassword123", # Altere conforme a necessidade ou via variável de ambiente
            role=UserRole.ADMIN
        )
        user_service.create(db, obj_in=user_in)

if __name__ == "__main__":
    from app.db.session import SessionLocal
    db = SessionLocal()
    init_db(db)
    db.close()
    print("Database Initialized com admin.")
