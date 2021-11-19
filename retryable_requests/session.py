from typing import Optional

from requests import Response
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests_toolbelt.sessions import BaseUrlSession

DEFAULT_RETRY_STRATEGY = Retry(
    total=5,
    status_forcelist=[429, 500, 502, 503, 504],
    backoff_factor=0.1,
    # Let Requests be responsible for all redirection
    redirect=False,
    # Behave like normal usage of Requests and transparently return a failing response,
    # instead of raising a MaxRetryError. Otherwise, callers have to handle multiple failure
    # pathways, depending on whether a retry occurred prior to failure.
    raise_on_status=False,
)


class RetryableSession(BaseUrlSession):
    def __init__(self, base_url: Optional[str] = None, retry_strategy: Optional[Retry] = None):
        if retry_strategy is None:
            retry_strategy = DEFAULT_RETRY_STRATEGY

        super().__init__(base_url=base_url)

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.mount('http://', adapter)
        self.mount('https://', adapter)

    def request(self, *args, **kwargs) -> Response:
        # See https://docs.python-requests.org/en/master/user/advanced/#timeouts
        kwargs.setdefault('timeout', (3.05, 5))
        return super().request(*args, **kwargs)
