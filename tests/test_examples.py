import datetime

import requests_cache

import natstat


def test_basic_request():
    api = natstat.NatStatAPIv3()
    req = natstat.GamesReq(service="mbb", date=datetime.datetime(2025, 11, 23))
    resp = api.games(req)
    assert not isinstance(resp, natstat.NatStatError)
    assert len(resp.data["games"]) == 42


def test_cached_request():
    # cache HTTP requests locally on the filesystem
    session = requests_cache.CachedSession("natstat", backend="filesystem")
    api = natstat.NatStatAPIv3(session=session)
    req = natstat.GamesReq(service="mbb", date=datetime.datetime(2025, 11, 23))
    resp = api.games(req)
    assert not isinstance(resp, natstat.NatStatError)
    assert len(resp.data["games"]) == 42
    # request will used cached data instead of hitting the API
    cached = api.games(req)
    assert not isinstance(cached, natstat.NatStatError)
    assert resp.data == cached.data
    assert resp.user() == cached.user()
    assert resp.meta() == cached.meta()
