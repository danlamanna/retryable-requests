# retryable-requests
[![PyPI](https://img.shields.io/pypi/v/retryable-requests)](https://pypi.org/project/retryable-requests/)

Easy to use retryable requests sessions.

## Quickstart

### Common case

``` python
from retryable_requests import RetryableSession

with RetryableSession() as session:
    session.get('https://httpbin.org/get')  # will be retried up to 5 times
```


### Only retry on 429 errors

``` python
from requests.packages.urllib3.util.retry import Retry
from retryable_requests import RetryableSession

retry_strategy = Retry(
    total=5,
    status_forcelist=[429],
    backoff_factor=0.1,
)

with RetryableSession(retry_strategy=retry_strategy) as session:
    session.get('https://httpbin.org/get')  # will be retried up to 5 times, only for 429 errors
```

### Automatically use a base URL for every request

``` python
from retryable_requests import RetryableSession

with RetryableSession('https://httpbin.org/') as session:
    session.get('get')  # 'https://httpbin.org/get' will be retried up to 5 times
    session.post('post')  # 'https://httpbin.org/post' won't be retried (POST request)
```

## Features

- Automatic backing off retries for failed requests that can be safely retried
- Quick timeouts for non-responsive requests

## See also

- [urllib3.util.Retry](https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#urllib3.util.Retry)
- [requests.Session](https://docs.python-requests.org/en/master/user/advanced/#session-objects)
- [requests_toolbelt.sessions.BaseUrlSession](https://toolbelt.readthedocs.io/en/latest/sessions.html#baseurlsession)
- [Timeouts in Requests](https://docs.python-requests.org/en/master/user/advanced/#timeouts)
