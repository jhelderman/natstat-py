from abc import ABC, abstractmethod

from pydantic import BaseModel


class NatStatReq(BaseModel, ABC):
    service: str = "mbb"
    offset: int | None = None

    @abstractmethod
    def to_range_options(self) -> list[str | None]:
        pass
