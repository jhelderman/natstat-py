import datetime

from pydantic import BaseModel, Field

from natstat.models.game_type import NatStatGameType
from natstat.models.natstat_req import NatStatReq
from natstat.models.team import NatStatTeam
from natstat.models.venues import NatStatVenue


class GamesReq(NatStatReq):
    dataformat: str | None = None
    season: int | None = None
    date: datetime.datetime | None = None
    daterange: tuple[datetime.datetime, datetime.datetime] | None = None
    teamcode: str | None = None
    leaguecode: str | None = None
    playercode: str | None = None
    gamecode: str | None = None
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
            self.gamecode,
            self.search,
        ]


class NatStatGame(BaseModel):
    id: int
    visitor: str
    visitor_code: str = Field(alias="visitor-code")
    score_vis: int = Field(alias="score-vis")
    home: str
    home_code: str = Field(alias="home-code")
    score_home: int = Field(alias="score-home")
    gamestatus: str
    overtime: str
    winner_code: str = Field(alias="winner-code")
    loser_code: str = Field(alias="loser-code")
    gameday: datetime.datetime
    gameno: int
    venue: str
    venue_code: int = Field(alias="venue-code")


class NatStatGameSummary(BaseModel):
    id: int
    gameday: datetime.datetime
    description: str
    visitor: str
    visitor_code: str = Field(alias="visitor-code")
    home: str
    home_code: str = Field(alias="home-code")
    location: str
    winorloss: str
    venue: NatStatVenue
    team: NatStatTeam | None = None
    opponent: NatStatTeam | None = None
    gametype: NatStatGameType | None = None
    overtime: str | None = None
