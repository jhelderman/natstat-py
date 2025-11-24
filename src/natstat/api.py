import json
from typing import Any

import requests
from ratelimit import limits, sleep_and_retry

from natstat.config import CONFIG
from natstat.log import get_logger
from natstat.models.games import GamesReq
from natstat.models.leaguecodes import LeagueCodesReq
from natstat.models.moneyline import MoneylineReq
from natstat.models.natstat_req import NatStatReq
from natstat.models.natstat_resp import NatStatResp
from natstat.models.overunder import OverunderReq
from natstat.models.playbyplay import PlayByPlayReq
from natstat.models.playerperfs import PlayerPerfsReq
from natstat.models.players import PlayersReq
from natstat.models.pointspread import PointSpreadReq
from natstat.models.seasons import SeasonsReq
from natstat.models.teamcodes import TeamCodesReq
from natstat.models.teamperfs import TeamPerfsReq
from natstat.models.teams import TeamsReq
from natstat.models.venues import VenuesReq
from natstat.util import format_range_offset_param

HOUR = 60 * 60


class NatStatError(Exception):
    def __init__(self, *args: object, resp: Any = None) -> None:
        super().__init__(*args)
        self.resp = resp


class EmptyResponseError(NatStatError):
    def __init__(self, *args: object, resp: Any = None) -> None:
        super().__init__(*args, resp=resp)


class InvalidResponseError(NatStatError):
    def __init__(self, *args: object, resp: Any = None) -> None:
        super().__init__(*args, resp=resp)


class NoDataError(NatStatError):
    def __init__(self, *args: object, resp: Any = None) -> None:
        super().__init__(*args, resp=resp)


class NoAPIKeyError(NatStatError):
    def __init__(self, *args: object, resp: Any = None) -> None:
        super().__init__(*args, resp=resp)


class NatStatAPIv3:
    def __init__(
        self,
        api_key: str = CONFIG.natstat_api_key,
        base_url: str = "https://api3.natst.at",
        session: requests.Session | None = None,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.log = get_logger()
        if session is None:
            self.session = requests.Session()
        else:
            self.session = session

    @sleep_and_retry
    @limits(CONFIG.natstat_req_per_hour, HOUR)
    def get(self, path: str) -> NatStatResp | NatStatError:
        if self.api_key == "":
            return NoAPIKeyError(
                "No API key was configured. This can be set via the NATSTAT_API_KEY "
                "environmental variable or passed directly to the NatStatAPIv3 object."
            )
        url = f"{self.base_url}/{self.api_key}/{path}"
        self.log.info(f"GET {path}")
        data = self.session.get(url).text
        if data is None or data == "":
            return EmptyResponseError(
                f"Bad url or empty response for {path}", resp=data
            )
        try:
            out = json.loads(data)
        except:
            return InvalidResponseError("Failed to parse JSON", resp=data)
        if not isinstance(out, dict):
            return InvalidResponseError("Invalid response format", resp=out)
        resp = NatStatResp(data=out)
        if not resp.success():
            err = resp.error()
            if err is not None and err.message == "NO_DATA":
                return NoDataError(f"No data for path: {path}", resp=out)
            return NatStatError(f"NatStat returned an error: {out['error']}", resp=out)
        return resp

    def endpoint(self, endpoint: str, req: NatStatReq) -> NatStatResp | NatStatError:
        path = f"{endpoint}/{req.service}"
        path += format_range_offset_param(req.to_range_options(), req.offset)
        resp = self.get(path)
        if isinstance(resp, NatStatError):
            return resp
        return resp

    def leaguecodes(self, req: LeagueCodesReq) -> NatStatResp | NatStatError:
        resp = self.endpoint("leaguecodes", req)
        if isinstance(resp, NatStatError):
            return resp
        return resp.set_key("leaguecodes")

    def teamcodes(self, req: TeamCodesReq) -> NatStatResp | NatStatError:
        resp = self.endpoint("teamcodes", req)
        if isinstance(resp, NatStatError):
            return resp
        return resp.set_key("teamcodes")

    def seasons(self, req: SeasonsReq) -> NatStatResp | NatStatError:
        resp = self.endpoint("seasons", req)
        if isinstance(resp, NatStatError):
            return resp
        return resp.set_key("seasons")

    def teams(self, req: TeamsReq) -> NatStatResp | NatStatError:
        resp = self.endpoint("teams", req)
        if isinstance(resp, NatStatError):
            return resp
        return resp.set_key("teams")

    def players(self, req: PlayersReq) -> NatStatResp | NatStatError:
        resp = self.endpoint("players", req)
        if isinstance(resp, NatStatError):
            return resp
        return resp.set_key("players")

    def games(self, req: GamesReq) -> NatStatResp | NatStatError:
        resp = self.endpoint("games", req)
        if isinstance(resp, NatStatError):
            return resp
        return resp.set_key("games")

    def teamperfs(self, req: TeamPerfsReq) -> NatStatResp | NatStatError:
        resp = self.endpoint("teamperfs", req)
        if isinstance(resp, NatStatError):
            return resp
        return resp.set_key("performances")

    def playerperfs(self, req: PlayerPerfsReq) -> NatStatResp | NatStatError:
        resp = self.endpoint("playerperfs", req)
        if isinstance(resp, NatStatError):
            return resp
        return resp.set_key("performances")

    def playbyplay(self, req: PlayByPlayReq) -> NatStatResp | NatStatError:
        resp = self.endpoint("playbyplay", req)
        if isinstance(resp, NatStatError):
            return resp
        return resp.set_key("playbyplay")

    def venues(self, req: VenuesReq) -> NatStatResp | NatStatError:
        resp = self.endpoint("venues", req)
        if isinstance(resp, NatStatError):
            return resp
        return resp.set_key("venues")

    def moneyline(self, req: MoneylineReq) -> NatStatResp | NatStatError:
        resp = self.endpoint("moneyline", req)
        if isinstance(resp, NatStatError):
            return resp
        return resp.set_key("moneylines")

    def pointspread(self, req: PointSpreadReq) -> NatStatResp | NatStatError:
        resp = self.endpoint("pointspread", req)
        if isinstance(resp, NatStatError):
            return resp
        return resp.set_key("spreads")

    def overunder(self, req: OverunderReq) -> NatStatResp | NatStatError:
        resp = self.endpoint("overunder", req)
        if isinstance(resp, NatStatError):
            return resp
        return resp.set_key("overunders")
