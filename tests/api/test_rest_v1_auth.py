import pytest
import testit
from autotests.pages.api.api_utils import API
from autotests.pages.api.settings import ENDPOINTS_MAPPING, API_USERS_TOKEN_MAPPING
from autotests.pages.data.api_data import api_users


class TestApiAuth:
    title = 'Checking post: /rest/v1/authentication/token [{username}]'
    @testit.displayName(title)
    @testit.externalId('leads api test 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, username',
        [
            ('1', api_users.leads)
        ]
    )
    def test_api_authentication_token(self, ex_id: str, username: str, urls) -> None:
        """ Checking post: /rest/v1/authentication/token - """
        api = API()
        method = 'authentication'
        url = urls.url_api + ENDPOINTS_MAPPING[method]
        body = {'username': username, 'publicKey': API_USERS_TOKEN_MAPPING[username]}
        api.make_request(method_type='POST', url=url, method=method, body=body)