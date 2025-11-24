import datetime

from pydantic import BaseModel, Field

from natstat.models.natstat_req import NatStatReq


class PlayerPerfsReq(NatStatReq):
    dataformat: str | None = None
    season: int | None = None
    date: datetime.datetime | None = None
    daterange: tuple[datetime.datetime, datetime.datetime] | None = None
    teamcode: str | None = None
    leaguecode: str | None = None
    playercode: str | None = None
    search: str | None = None

    def to_range_options(self) -> list[str | None]:
        return [
            self.dataformat,
            str(self.season) if self.season is not None else None,
            self.date.strftime("%Y-%m-%d") if self.date is not None else None,
            (
                f"{self.daterange[0].strftime('%Y-%m-%d')},"
                f"{self.daterange[1].strftime('%Y-%m-%d')}"
                if self.daterange is not None
                else None
            ),
            self.teamcode,
            self.leaguecode,
            self.playercode,
            self.search,
        ]


class NatStatBasketballPlayerPerf(BaseModel):
    id: int
    player: str
    player_code: str = Field(alias="player-code")
    player_number: int = Field(alias="player-number")
    position: str
    starter: str
    game: str
    team: str
    opponent: str
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
    pf: int
    fgpct: float | None
    twofgpct: float | None
    dreb: int | None
    usgpct: float | None
    eff: float | None
    perfscore: float | None
    perfscoreseasonavg: float | None
    presencerate: float | None
    adjpresencerate: float | None
    teamposs: float
    teamfga: float
    teamfta: float
    teamto: float
    statline: str
    ftpct: float | None
    perfscoreseasonavgdev: float | None
    threefgpct: float | None
