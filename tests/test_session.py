from itertools import chain, repeat

import pytest
from requests.exceptions import ConnectionError
from urllib3.connectionpool import HTTPConnectionPool
from werkzeug.wrappers import Response

from retryable_requests.session import DEFAULT_RETRY_STRATEGY, RetryableSession


@pytest.fixture
def fails_first_time(mocker):
    return mocker.Mock(
        side_effect=chain(
            [Response({}, 500)],
            repeat(Response({}, 200)),
        )
    )


def test_session_retries_bad_status_codes(httpserver, session, fails_first_time):
    httpserver.expect_request('/').respond_with_handler(fails_first_time)
    r = session.get(httpserver.url_for('/'))
    assert r.ok, r.text


def test_session_base_url_retries_bad_status_codes(httpserver, fails_first_time):
    httpserver.expect_request('/base/stem').respond_with_handler(fails_first_time)
    session = RetryableSession(base_url=httpserver.url_for('/base/'))

    r = session.get('stem')

    assert r.ok, r.text


@pytest.mark.parametrize('protocol', ['http', 'https'])
def test_session_retries_connection_errors(session, mocker, protocol):
    spy = mocker.spy(HTTPConnectionPool, 'urlopen')
    with pytest.raises(ConnectionError):
        session.get(f'{protocol}://some-bad-connection.invalid')

    # the initial request + the number of total retries
    assert spy.call_count == 1 + DEFAULT_RETRY_STRATEGY.total
