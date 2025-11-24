from natstat.models.natstat_req import NatStatReq


class SeasonsReq(NatStatReq):
    dataformat: str | None = None
    season: int | None = None

    def to_range_options(self) -> list[str | None]:
        return [
            self.dataformat,
            str(self.season) if self.season is not None else None,
        ]
