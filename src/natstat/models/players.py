from natstat.models.natstat_req import NatStatReq


class PlayersReq(NatStatReq):
    dataformat: str | None = None
    season: int | None = None
    teamcode: str | None = None
    leaguecode: str | None = None
    playercode: str | None = None
    search: str | None = None

    def to_range_options(self) -> list[str | None]:
        return [
            self.dataformat,
            str(self.season) if self.season is not None else None,
            self.teamcode,
            self.leaguecode,
            self.playercode,
            self.search,
        ]
