from fastapi import HTTPException, status
from typing import Any, Optional, Dict

class BaseAPIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class NotFoundException(BaseAPIException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class BadRequestException(BaseAPIException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UnauthorizedException(BaseAPIException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

class ForbiddenException(BaseAPIException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class ConflictException(BaseAPIException):
    def __init__(self, detail: str = "Conflict"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class ValidationException(BaseAPIException):
    def __init__(self, detail: str = "Validation error"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

class DatabaseException(BaseAPIException):
    def __init__(self, detail: str = "Database error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class InternalServerError(BaseAPIException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)