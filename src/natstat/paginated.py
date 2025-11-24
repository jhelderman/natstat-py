from typing import Callable

import pandas as pd
from pydantic import BaseModel

from natstat.api import NatStatError
from natstat.models.natstat_req import NatStatReq
from natstat.models.natstat_resp import NatStatResp


class PaginatedResp(BaseModel):
    pages: list[NatStatResp]

    def to_dataframe(self) -> pd.DataFrame | None:
        data = []
        for page in self.pages:
            df = page.to_dataframe()
            if df is None:
                return None
            data.append(df)
        return pd.concat(data, ignore_index=True)


def paginated_get_all(
    endpoint: Callable[[NatStatReq], NatStatResp | NatStatError], req: NatStatReq
) -> PaginatedResp | NatStatError:
    out = []
    page_req = req.model_copy()
    page_req.offset = None
    first = endpoint(page_req)
    if isinstance(first, NatStatError):
        return first
    out.append(first)
    meta = first.meta()
    if meta is None:
        return NatStatError(f"Could not parse meta for: {first}")
    pages_total = meta.pages_total
    results_max = meta.results_max
    for i in range(1, pages_total):
        page_req = req.model_copy()
        page_req.offset = i * results_max
        page = endpoint(page_req)
        if isinstance(page, NatStatError):
            return page
        out.append(page)
    return PaginatedResp(pages=out)
