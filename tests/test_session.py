import pytest
from werkzeug.wrappers import Response

from retryable_requests.session import RetryableSession

LISTEN_PORT = 6749


@pytest.fixture(scope='session')
def httpserver_listen_address():
    return 'localhost', LISTEN_PORT


@pytest.fixture
def base_url(httpserver_listen_address):
    return f'http://{httpserver_listen_address[0]}:{httpserver_listen_address[1]}'


def fails_first_time(request):
    if fails_first_time.responded:
        return Response({}, 200)
    else:
        fails_first_time.responded = True
        return Response({}, 500)


fails_first_time.responded = False  # type: ignore


def test_session_retries_bad_status_codes(httpserver, base_url):
    httpserver.expect_request('/', method='GET').respond_with_handler(fails_first_time)
    session = RetryableSession(base_url)
    r = session.get('/')
    assert r.ok, r.text
