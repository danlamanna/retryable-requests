from werkzeug.wrappers import Response


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
