from fastapi import APIRouter

router = APIRouter(prefix="/saude", tags=["Saúde"])


@router.get("")
def verificar_saude():
    return {"status": "ok"}