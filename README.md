# natstat-py

A python interface for the National Statistical API

## Installation

```bash
git clone https://github.com/jhelderman/natstat-py.git
cd natstat-py
pip install .
```

## Configuration

Usage of this API requires an API key for National Statistical, which can
be obtained via purchase on the National Statistical website. Configuration
can be done via environmental variable or by setting the API key directly
when initializing the API in python.

Environmental variable:

```bash
export NATSTAT_API_KEY=replace-me
```

```python
import natstat
api = natstat.NatStatAPIv3()
```

Python:

```python
import natstat
api = natstat.NatStatAPIv3(api_key="replace-me")
```

Additionally, the library has built-in rate limiting to comply with the
API policies. The rate limiting can be configured on an hourly basis through
the `NATSTAT_REQ_PER_HOUR` environmental variable. For example:

```bash
export NATSTAT_REQ_PER_HOUR=500
```

## Usage

### Basic request

The basic workflow for using the API is to initialize an API object,
select the method corresponding to the API endpoint, form the corresponding request
object, and invoke the method on the request. There is a method for each endpoint
in the API. See [the NatStat documentation](https://natstat.com/api-v3/endpoints)
for more information on the endpoints. The following example makes a request to the
`games` endpoint for the `mbb` service for 2025-11-23.

```python
api = natstat.NatStatAPIv3()
req = natstat.GamesReq(service="mbb", date=datetime.datetime(2025, 11, 23))
resp = api.games(req)
print(resp.to_dataframe())
```

Responses from the API can be converted to a pandas dataframe as is done in the
last line of the example. Each record in the response will become a row in the
dataframe.

### Cached request

Caching is not supported directly in this library but can be implemented easily
with the `requests-cache` library. To cache requests, make a cached session
with the desired configuration and pass it when the API object is created.

```python
# cache HTTP requests locally on the file system
# this library also has options to back the cache with Redis or a database
session = requests_cache.CachedSession("natstat", backend="filesystem")
api = natstat.NatStatAPIv3(session=session)
req = natstat.GamesReq(service="mbb", date=datetime.datetime(2025, 11, 23))
resp = api.games(req)
# request will used cached data instead of hitting the API
cached = api.games(req)
assert not isinstance(cached, natstat.NatStatError)
assert resp.data == cached.data
# user and meta objects have request-specific information
# if the response was successfully cached, these will be the same
assert resp.user() == cached.user()
assert resp.meta() == cached.meta()
```
