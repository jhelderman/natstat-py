import datetime
from dataclasses import dataclass
from typing import Any

import pandas as pd
from pydantic import BaseModel, Field


class User(BaseModel):
    account: str
    levels: str
    apiplus: str
    ratelimit: int
    ratelimit_remaining: int = Field(alias="ratelimit-remaining")
    ratelimit_timeframe: str = Field(alias="ratelimit-timeframe")
    ratelimit_reset: datetime.datetime = Field(alias="ratelimit-reset")


class Meta(BaseModel):
    processing_time: str = Field(alias="processing-time")
    processed_at: datetime.datetime = Field(alias="processed-at")
    timezone: str
    ip: str
    ip_last24: str = Field(alias="ip-last24")
    queryid: str
    results_max: int = Field(alias="results-max")
    results_total: int = Field(alias="results-total")
    page: int
    pages_total: int = Field(alias="pages-total")
    stat_glossary: str = Field(alias="stat-glossary")
    codes_teams: str = Field(alias="codes-teams")
    codes_leagues: str = Field(alias="codes-leagues")
    api: str
    version: str
    documentation: str
    support: str
    report_errors: str
    note: str


class Error(BaseModel):
    message: str


@dataclass
class NatStatResp:
    data: dict[str, Any]
    key: str | None = None

    def set_key(self, key: str) -> NatStatResp:
        self.key = key
        return self

    def to_dataframe(self) -> pd.DataFrame | None:
        if self.key is None or self.key not in self.data:
            return None
        return pd.DataFrame(self.data[self.key].values())

    def success(self) -> bool:
        return "success" in self.data and self.data["success"] == "1"

    def user(self) -> User | None:
        try:
            return User.model_validate(self.data["user"])
        except:
            return None

    def meta(self) -> Meta | None:
        try:
            return Meta.model_validate(self.data["meta"])
        except:
            return None

    def error(self) -> Error | None:
        try:
            return Error.model_validate(self.data["error"])
        except:
            return None
