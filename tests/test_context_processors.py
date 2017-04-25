from unittest.mock import Mock
import pytest

from directory_header_footer.sso import context_processors


@pytest.fixture
def sso_user():
    return Mock(
        id=1,
        email='jim@example.com'
    )


@pytest.fixture
def request_logged_in(rf, sso_user):
    request = rf.get('/')
    request.sso_user = sso_user
    return request


@pytest.fixture
def request_logged_out(rf):
    request = rf.get('/')
    request.sso_user = None
    return request


def test_sso_logged_in(request_logged_in):
    context = context_processors.sso_user_processor(request_logged_in)
    assert context['sso_is_logged_in'] is True


def test_sso_profile_url(request_logged_in, settings):
    settings.SSO_PROFILE_URL = expected = 'http://www.example.com/profile/'
    context = context_processors.sso_user_processor(request_logged_in)
    assert context['sso_profile_url'] == expected


def test_sso_register_url_url(request_logged_in, settings):
    settings.SSO_SIGNUP_URL = expected = 'http://www.example.com/signup/'
    context = context_processors.sso_user_processor(request_logged_in)
    assert context['sso_register_url'] == expected


def test_sso_logged_out(request_logged_out):
    context = context_processors.sso_user_processor(request_logged_out)
    assert context['sso_is_logged_in'] is False


def test_sso_login_url(request_logged_in, settings):
    settings.SSO_LOGIN_URL = 'http://www.example.com/login/'
    expected = 'http://www.example.com/login/?next=http://testserver/'
    context = context_processors.sso_user_processor(request_logged_in)
    assert context['sso_login_url'] == expected


def test_sso_logout_url(request_logged_in, settings):
    settings.SSO_LOGOUT_URL = expected = 'http://www.example.com/logout/'
    context = context_processors.sso_user_processor(request_logged_in)
    assert context['sso_logout_url'] == expected
