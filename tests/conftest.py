import pytest

from retryable_requests import RetryableSession

LISTEN_PORT = 6749


@pytest.fixture(scope='session')
def httpserver_listen_address():
    return 'localhost', LISTEN_PORT


@pytest.fixture
def session():
    return RetryableSession()
