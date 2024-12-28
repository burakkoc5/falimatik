from typing import TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T] = None

    @classmethod
    def success(cls, message: str, data: T = None) -> 'ResponseModel[T]':
        return cls(
            code=200,
            message=message,
            data=data
        )

    @classmethod
    def error(cls, code: int, message: str) -> 'ResponseModel':
        return cls(
            code=code,
            message=message,
            data=None
        ) 