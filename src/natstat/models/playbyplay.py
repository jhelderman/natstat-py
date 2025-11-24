import datetime

from natstat.models.natstat_req import NatStatReq


class PlayByPlayReq(NatStatReq):
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
