from pydantic import BaseModel

from natstat.models.natstat_req import NatStatReq


class VenuesReq(NatStatReq):
    dataformat: str | None = None
    season: int | None = None
    venuecode: int | None = None
    search: str | None = None

    def to_range_options(self) -> list[str | None]:
        return [
            self.dataformat,
            str(self.season) if self.season is not None else None,
            str(self.venuecode) if self.venuecode is not None else None,
            self.search,
        ]


class NatStatVenue(BaseModel):
    code: int
    name: str
    location: str
    longitude: str
    latitude: str
