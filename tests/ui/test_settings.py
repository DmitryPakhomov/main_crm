import random
import testit
import pytest
from typing import Any
from autotests.pages.data.test_data import TestData


class TestSettingsPage:
    title = 'Checking the creation of broker [{role}]'
    @testit.displayName(title)
    @testit.externalId('settings test 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role', [('1', 'admin')])
    def test_settings_brokers_create_page_create_broker(
            self, ex_id: str, role: str, login_page, settings_brokers_create_page
    ) -> Any:
        """ Checking the creation of broker - """
        login_page.login_with_cookies(page='Brokers')
        settings_brokers_create_page.creating_broker()

    title = 'Checking the creation of brokers user [{role}][{case}]'
    @testit.displayName(title)
    @testit.externalId('settings test 2 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, role, password, broker_role',
        [
            ('1', 'with_required_fields', 'admin', 'Qwerty123!', 'Administrator'),
            ('2', 'with_all_fields', 'admin', 'Qwerty123!', 'Administrator'),
            ('3', 'with_required_fields', 'admin', 'Qwerty123!', 'User')
        ]
    )
    def test_settings_brokers_users_create_page_create_broker_user(
            self,
            ex_id: str,
            case: str,
            role: str,
            password: str,
            broker_role: str,
            login_page,
            settings_brokers_users_create_page
    ) -> Any:
        """ Checking creating broker user - """
        login_page.login_with_cookies(page='BrokersUsers')
        match case:
            case 'with_required_fields':
                settings_brokers_users_create_page.creating_broker_user(
                    full_name=f'{TestData.first_name()} {TestData.last_name()}',
                    username=TestData.first_name(),
                    email=TestData.email(),
                    password=password,
                    role=broker_role,
                )
            case 'with_all_fields':
                settings_brokers_users_create_page.creating_broker_user(
                    full_name=f'{TestData.first_name()} {TestData.last_name()}',
                    username=TestData.first_name(),
                    email=TestData.email(),
                    password=password,
                    role=broker_role,
                    legal_name=TestData.first_name(),
                    title=TestData.words(),
                    phone=TestData.phone(),
                    extension=random.randint(1000, 9999)
                )