from pydantic import BaseModel


class NatStatTeam(BaseModel):
    code: str
    name: str
