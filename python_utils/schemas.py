
from pydantic import BaseModel


class RequestBase64(BaseModel):
    base_64: str


class ResponseSpoofing(BaseModel):
    is_spoofed: bool
    trust: float
