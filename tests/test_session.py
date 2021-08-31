import responses

from retryable_requests.session import RetryableSession


@responses.activate
def test_session_retries():
    responses.add(responses.GET, 'http://foo.dev', status=500)
    responses.add(responses.GET, 'http://foo.dev', json={'success': True})

    session = RetryableSession(base_url='http://foo.dev')
    r = session.get('')
    assert r.ok, r.data
