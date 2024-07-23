from fastapi import HTTPException
from http import HTTPStatus
from pydantic import BaseModel


class CustomHTTPExceptionModel(BaseModel):
    msg: str
    devMsg: str


class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int = 400,
                 detail: str = None,
                 msg: str = None,
                 devMsg: str = None) -> None:
        if detail is None:
            detail = HTTPStatus(status_code).phrase
            if not detail:
                detail = "Error: Custom"
        self.status_code = status_code
        self.detail = detail
        if msg is None:
            msg = self.detail
        self.msg = msg
        if devMsg is None:
            devMsg = self.msg
        self.dev_msg = devMsg

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r}," \
               f" msg={self.msg!r}, dev_msg={self.dev_msg!r})"
