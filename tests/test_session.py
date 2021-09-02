import pytest
from requests.exceptions import ConnectionError
from urllib3.connectionpool import HTTPConnectionPool
from werkzeug.wrappers import Response

from retryable_requests.session import DEFAULT_RETRY_STRATEGY


def fails_first_time(request):
    if fails_first_time.responded:
        return Response({}, 200)
    else:
        fails_first_time.responded = True
        return Response({}, 500)


fails_first_time.responded = False  # type: ignore


def test_base_url_session_retries_bad_status_codes(httpserver, base_url_session):
    httpserver.expect_request('/', method='GET').respond_with_handler(fails_first_time)
    r = base_url_session.get('/')
    assert r.ok, r.text


def test_session_retries_bad_status_codes(httpserver, base_url, session):
    httpserver.expect_request('/', method='GET').respond_with_handler(fails_first_time)
    r = session.get(f'{base_url}/')
    assert r.ok, r.text


def test_session_retries_connection_errors(session, mocker):
    spy = mocker.spy(HTTPConnectionPool, 'urlopen')
    with pytest.raises(ConnectionError):
        session.get('http://some-bad-connection.dev')

    # the initial request + the number of total retries
    assert spy.call_count == 1 + DEFAULT_RETRY_STRATEGY.total
