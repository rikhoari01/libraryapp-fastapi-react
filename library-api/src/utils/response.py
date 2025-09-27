from typing import Any, Optional
from fastapi import status
from fastapi.responses import JSONResponse

def response_success(message: str, data: Optional[Any] = None, code: int = status.HTTP_200_OK) -> JSONResponse:
    return JSONResponse({"success": True, "code": code, "message": message, "data": data})

def response_error(message: str, code: int = status.HTTP_400_BAD_REQUEST) -> JSONResponse:
    return JSONResponse({"success": False, "code": code, "message": message})
