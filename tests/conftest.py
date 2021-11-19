import pytest

from retryable_requests import RetryableSession


@pytest.fixture
def session():
    return RetryableSession()
