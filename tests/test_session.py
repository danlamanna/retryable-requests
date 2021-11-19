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


def test_session_retries_bad_status_codes(httpserver, fails_first_time):
    httpserver.expect_request('/').respond_with_handler(fails_first_time)

    with RetryableSession() as session:
        r = session.get(httpserver.url_for('/'))

    assert r.ok, r.text


def test_session_base_url_retries_bad_status_codes(httpserver, fails_first_time):
    httpserver.expect_request('/base/stem').respond_with_handler(fails_first_time)

    with RetryableSession(base_url=httpserver.url_for('/base/')) as session:
        r = session.get('stem')

    assert r.ok, r.text


@pytest.mark.parametrize('protocol', ['http', 'https'])
def test_session_retries_connection_errors(mocker, protocol):
    spy = mocker.spy(HTTPConnectionPool, 'urlopen')

    with pytest.raises(ConnectionError):
        with RetryableSession() as session:
            session.get(f'{protocol}://some-bad-connection.invalid')

    # the initial request + the number of total retries
    assert spy.call_count == 1 + DEFAULT_RETRY_STRATEGY.total


def test_session_failing_termination(httpserver):
    """Ensure that failing retries eventually terminate."""
    httpserver.expect_request('/').respond_with_data(status=500)

    with RetryableSession() as session:
        r = session.get(httpserver.url_for('/'))

    assert r.status_code == 500


@pytest.mark.parametrize('allow_redirects', [True, False])
def test_session_redirects(httpserver, allow_redirects):
    """Ensure that redirect handling with Requests is still respected."""
    httpserver.expect_request('/start').respond_with_data(
        status=303, headers={'Location': httpserver.url_for('/end')}
    )
    httpserver.expect_request('/end').respond_with_data()

    with RetryableSession() as session:
        r = session.get(httpserver.url_for('/start'), allow_redirects=allow_redirects)

    assert (r.status_code == 200) == allow_redirects
