from pydantic import BaseModel


class NatStatBasketballStats(BaseModel):
    min: int
    pts: int
    fgm: int
    fga: int
    threefm: int
    threefa: int
    ftm: int
    fta: int
    reb: int
    ast: int
    stl: int
    blk: int
    oreb: int
    to: int
    f: int
    teampts: int


class NatStatEmptyStats(BaseModel):
    teampts: int
