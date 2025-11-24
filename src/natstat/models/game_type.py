from pydantic import BaseModel


class NatStatGameType(BaseModel):
    series: str
    seriesname: str
    seriesgameno: int
    seriesstatus: str
