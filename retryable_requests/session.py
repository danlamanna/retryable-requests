from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests_toolbelt.sessions import BaseUrlSession


class RetryableSession(BaseUrlSession):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            'retry_strategy',
            Retry(
                total=5,
                status_forcelist=[429, 500, 502, 503, 504],
                backoff_factor=0.1,
            ),
        )

        adapter = HTTPAdapter(max_retries=kwargs['retry_strategy'])
        kwargs.pop('retry_strategy')
        super().__init__(*args, **kwargs)

        self.mount('http://', adapter)
        self.mount('https://', adapter)

    def request(self, *args, **kwargs):
        kwargs.setdefault('timeout', (5, 5))
        return super().request(*args, **kwargs)