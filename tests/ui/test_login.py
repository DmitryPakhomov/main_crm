import pytest
import testit
from typing import Any
from autotests.pages.data.settings_data import settings_pages


class TestLoginPage:
    title = 'Checking authorization via username and password [{role}]'
    @testit.displayName(title)
    @testit.externalId('login test 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role', [('1', 'admin')])
    def test_login_page_login_via_username_and_password(
            self, ex_id: str, role: str, login_page
    ) -> Any:
        """ Checking authorization via username and password - """
        login_page.login_by_password(role=role)

    title = 'Checking authorization via username and password [{case}][n]'
    @testit.displayName(title)
    @testit.externalId('login test 2 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, username, password',
        [
            ('1', 'empty_fields', '', ''),
            ('2', 'empty_username', '', 'test'),
            ('3', 'empty_password', 'test', ''),
            ('4', 'incorrect_password', 'parvin.ibrahimov', 'test'),
            ('5', 'script_username', '<script>alert(123)</script>', 'test'),
            ('6', 'html_tag_username', '<a>"Hello, World!"</a>', 'test'),
            ('7', 'symbols_username', '«♣☺♂»,«»‘~!@#$%^&*()?>,.<][/*<!—«»,«${code}»;—>', 'test'),
            ('8', 'spaces_username', '   ', 'test')
        ]
    )
    def test_login_page_negative_login_via_username_and_password(
            self, ex_id: str, case: str, username: str, password: str, login_page
    ) -> Any:
        """ Checking authorization via username and password with incorrect data - """
        login_page.open_page(page='Password')
        login_page.fill_username(username=username)
        login_page.fill_password(password=password)
        login_page.click_btn_login()
        login_page.login_field_validation_check_negative(case=case)

    title = "Checking authorization via settings under user with role [{role}]"
    @testit.displayName(title)
    @testit.externalId('login test 3 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, role',
        [
            ('1', 'sales'),
            ('2', 'negotiations'),
            ('3', 'opener'),
            ('4', 'accounting'),
            ('5', 'enrollments'),
            ('6', 'customer_service')
        ]
    )
    def test_login_page_login_as_user(
            self, ex_id: str, role: str, login_page, settings_users_page
    ) -> Any:
        """ Checking authorization via settings under users with different roles - """
        login_page.login_by_password(role='admin', main_tab=None)
        login_page.click_dl_avatar()
        login_page.click_btn_settings()
        settings_users_page.change_settings_page(page=settings_pages.users, internal_title=True)
        settings_users_page.login_as_user(role=role)
