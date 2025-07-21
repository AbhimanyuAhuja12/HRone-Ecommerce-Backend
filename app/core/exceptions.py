"""
Custom application exceptions
"""
from fastapi import HTTPException


class AppException(HTTPException):
    """Base application exception"""
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)
        self.status_code = status_code
        self.detail = detail


class ValidationError(AppException):
    """Validation error exception"""
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)


class NotFoundError(AppException):
    """Not found error exception"""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)


class DatabaseError(AppException):
    """Database error exception"""
    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(status_code=500, detail=detail)
