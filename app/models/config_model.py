from pydantic import BaseModel


class CantorURL(BaseModel):
    url1: str
    url2: str
