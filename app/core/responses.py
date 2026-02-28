from typing import Any, Optional
from fastapi.responses import JSONResponse

def standard_response(success: bool, data: Any = None, message: Optional[str] = None, error_code: Optional[str] = None, status_code: int = 200):
    content = {"success": success}
    
    if success:
        if data is not None:
            content["data"] = data
        if message:
            content["message"] = message
    else:
        content["error"] = {
            "code": error_code or "INTERNAL_ERROR",
            "message": message or "Ocorreu um erro inesperado."
        }
    
    return JSONResponse(content=content, status_code=status_code)
