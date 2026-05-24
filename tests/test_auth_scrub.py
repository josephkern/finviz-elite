"""Offline tests for auth-token scrubbing in HTTPError propagation.

Unlike the other test modules that patch _get_url, these patch
requests.get one level deeper so the actual scrub path runs end-to-end.
"""

import re

import pytest
import requests

import finviz_elite as fe


FAKE_TOKEN = "secret-7d975abc-1c60-4d38-a3de-4541350e5cf2"


def _make_fake_response(status: int, url: str, reason: str = "Bad Request"):
    resp = requests.Response()
    resp.status_code = status
    resp.url = url
    resp.reason = reason
    # Attach a PreparedRequest so response.request.url is populated --
    # matches what real requests.get produces.
    req = requests.PreparedRequest()
    req.url = url
    req.method = "GET"
    resp.request = req
    return resp


@pytest.fixture
def patch_requests_get(monkeypatch):
    monkeypatch.setenv("AUTH_TOKEN_FINVIZ", FAKE_TOKEN)

    def _install(response):
        monkeypatch.setattr("requests.get", lambda *a, **kw: response)

    return _install


def test_http_error_message_does_not_leak_token(patch_requests_get):
    leaky_url = f"https://elite.finviz.com/export?v=152&auth={FAKE_TOKEN}"
    patch_requests_get(_make_fake_response(400, leaky_url))

    with pytest.raises(requests.HTTPError) as exc:
        fe.screener()

    msg = str(exc.value)
    assert FAKE_TOKEN not in msg
    assert "auth=<redacted>" in msg


def test_http_error_response_url_is_scrubbed(patch_requests_get):
    leaky_url = f"https://elite.finviz.com/export?v=152&auth={FAKE_TOKEN}"
    patch_requests_get(_make_fake_response(500, leaky_url, reason="Server Error"))

    with pytest.raises(requests.HTTPError) as exc:
        fe.screener()

    # Callers can still introspect e.response, but its url + request.url
    # are scrubbed.
    assert FAKE_TOKEN not in exc.value.response.url
    assert "auth=<redacted>" in exc.value.response.url
    assert FAKE_TOKEN not in exc.value.response.request.url


def test_http_error_status_still_inspectable(patch_requests_get):
    leaky_url = f"https://elite.finviz.com/export?v=152&auth={FAKE_TOKEN}"
    patch_requests_get(_make_fake_response(404, leaky_url, reason="Not Found"))

    with pytest.raises(requests.HTTPError) as exc:
        fe.screener()

    # The scrub must preserve enough of the exception that callers can
    # tell what went wrong without parsing the message.
    assert exc.value.response.status_code == 404


def test_other_url_params_preserved_in_message(patch_requests_get):
    leaky_url = (
        f"https://elite.finviz.com/export?v=152&c=0,1,2"
        f"&f=sec_technology&auth={FAKE_TOKEN}"
    )
    patch_requests_get(_make_fake_response(400, leaky_url))

    with pytest.raises(requests.HTTPError) as exc:
        fe.screener()

    msg = str(exc.value)
    # Diagnostic information (other query params) must survive the scrub
    # so the error remains useful for debugging.
    assert "v=152" in msg
    assert "c=0,1,2" in msg
    assert "f=sec_technology" in msg


def test_rate_limit_error_does_not_carry_url(patch_requests_get):
    # The 429 path raises a RuntimeError with no URL embedded -- verify
    # the token isn't there either (regression guard for future edits).
    leaky_url = f"https://elite.finviz.com/export?v=152&auth={FAKE_TOKEN}"
    patch_requests_get(_make_fake_response(429, leaky_url, reason="Too Many Requests"))

    with pytest.raises(RuntimeError) as exc:
        fe.screener()

    assert FAKE_TOKEN not in str(exc.value)


def test_scrub_handles_auth_in_middle_or_end_of_query():
    # Direct unit test of the helper for both positions.
    from finviz_elite._core import _scrub_auth

    assert _scrub_auth("https://x/y?a=1&auth=xyz&b=2") == "https://x/y?a=1&auth=<redacted>&b=2"
    assert _scrub_auth("https://x/y?auth=xyz") == "https://x/y?auth=<redacted>"
    assert _scrub_auth("nothing to scrub here") == "nothing to scrub here"
