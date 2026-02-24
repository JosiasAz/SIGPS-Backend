from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.models import EntradaFila


def obter_fila_ordenada(db: Session) -> list[EntradaFila]:
    # Maior prioridade primeiro, depois mais antigo
    q = select(EntradaFila).where(EntradaFila.status == "aguardando").order_by(
        EntradaFila.prioridade.desc(),
        EntradaFila.criado_em.asc(),
    )
    return list(db.scalars(q).all())