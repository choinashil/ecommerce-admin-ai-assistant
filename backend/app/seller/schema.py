from pydantic import BaseModel


class SellerResponse(BaseModel):
    token: str
    nickname: str
