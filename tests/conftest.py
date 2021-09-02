import pytest

from retryable_requests import RetryableBaseUrlSession, RetryableSession

LISTEN_PORT = 6749


@pytest.fixture(scope='session')
def httpserver_listen_address():
    return 'localhost', LISTEN_PORT


@pytest.fixture
def base_url(httpserver_listen_address):
    return f'http://{httpserver_listen_address[0]}:{httpserver_listen_address[1]}'


@pytest.fixture
def base_url_session(base_url):
    return RetryableBaseUrlSession(base_url)


@pytest.fixture
def session():
    return RetryableSession()
