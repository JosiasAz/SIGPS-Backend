from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.models import QueueEntry


def get_queue_ordered(db: Session) -> list[QueueEntry]:
    # Maior prioridade primeiro, depois mais antigo
    q = select(QueueEntry).where(QueueEntry.status == "aguardando").order_by(
        QueueEntry.prioridade.desc(),
        QueueEntry.created_at.asc(),
    )
    return list(db.scalars(q).all())