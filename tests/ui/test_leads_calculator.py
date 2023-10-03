import testit
import pytest
from dotenv import load_dotenv
from typing import Any
from autotests.pages.data.leads_data import leads_pages, leads_tabs, LeadsTypeOfPays, \
    leads_debt_type
from autotests.pages.data.main_data import roles
from autotests.pages.data.test_data import TestData


load_dotenv()


class TestLeadCalculatorPage:
    title = 'Checking lead calculator sales permission [{role}]'
    @testit.displayName(title)
    @testit.externalId('calculator test 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page', [('1', 'admin', leads_pages.leads_calculator)])
    def test_lead_calculator_sales_permission(
            self,
            ex_id: str,
            role: str,
            page: str,
            login,
            login_page,
            lead_create_page,
            lead_profile_page,
            lead_calculator_page,
            get_token_leads
    ) -> Any:
        state = 'CA'
        credit_data: dict = TestData.credit_report_data_for_api(state=state)
        lead_id = lead_create_page.create_lead_via_api(get_token_leads, **credit_data)
        login_page.login_with_cookies(page=page, client_id=lead_id)
        lead_calculator_page.fill_next_pay_date(10)
        lead_calculator_page.click_elem_by_text('label', 'Total Debt')
        number_of_months = lead_calculator_page.edit_number_of_months(19)
        lead_profile_page.refresh_page()
        lead_calculator_page.check_number_of_months(number_of_months)
        number_of_months = lead_calculator_page.edit_number_of_months(31)
        lead_profile_page.refresh_page()
        lead_calculator_page.check_number_of_months(number_of_months)
        type_deposits_frequency = lead_calculator_page.edit_deposits_frequency(
            LeadsTypeOfPays.semimonthly)
        lead_calculator_page.check_deposits_frequency(type_deposits_frequency)

    title = 'Checking default calculator value Number Of Months[{role}]'
    @testit.displayName(title)
    @testit.externalId('calculator test 2 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, role, balance, number_creditor',
        [
            ('1', 'admin', '30000', 1),
            ('2', 'admin', '20000', 1),
            ('3', 'admin', '12499', 2),
            ('4', 'admin', '8333', 3),
            ('5', 'admin', '6240', 4),
            ('6', 'admin', '3000', 5),
            ('7', 'admin', '8666', 3)
        ]
    )
    def test_lead_calculator_number_of_months_default_value(
            self,
            ex_id: str,
            role: str,
            balance: str,
            number_creditor: int,
            login,
            login_page,
            lead_create_page,
            lead_profile_page,
            lead_calculator_page,
            lead_creditors_page,
            get_token_leads
    ) -> Any:
        page = leads_pages.leads_profile
        lead_id = lead_create_page.create_lead_via_api(get_token_leads)
        login_page.login_with_cookies(page=page, client_id=lead_id)
        lead_profile_page.check_rejected_lead()
        lead_profile_page.choose_leads_tabs(tab=leads_tabs.creditors)
        i = 1
        while i <= number_creditor:
            lead_creditors_page.add_new_creditor(
                balance=balance,
                debt_type=leads_debt_type.credit_card
            )
            i += 1
        lead_profile_page.choose_leads_tabs(tab=leads_tabs.calculator)
        lead_profile_page.refresh_page()
        full_balance = int(balance) * number_creditor
        if full_balance > 25000 and number_creditor == 1:
            lead_calculator_page.check_number_of_months(48)
        if full_balance < 25000 and number_creditor == 1:
            lead_calculator_page.check_number_of_months(24)
        if full_balance < 25000 and number_creditor == 2:
            lead_calculator_page.check_number_of_months(24)
        if full_balance < 25000 and number_creditor == 3:
            lead_calculator_page.check_number_of_months(36)
        if full_balance < 25000 and number_creditor == 4:
            lead_calculator_page.check_number_of_months(48)
        if full_balance < 25000 and number_creditor == 5:
            lead_calculator_page.check_number_of_months(48)
        if full_balance > 25000 and number_creditor == 3:
            lead_calculator_page.check_number_of_months(48)

    title = 'Checking calculator top managers permission fields [{state}][{role}]'
    @testit.displayName(title)
    @testit.externalId('leads test 12 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, state, role, number_of_months',
        [
            ('1', 'CA', roles.admin, 6)
        ]
    )
    def test_lead_calculator_top_managers_permissions(
            self,
            ex_id: str,
            state: str,
            role: str,
            number_of_months: int,
            login_page,
            lead_create_page,
            lead_history_page,
            lead_profile_page,
            lead_calculator_page,
            get_token_leads
    ) -> Any:
        """ Checking calculator page - """
        credit_data: dict = TestData.credit_report_data_for_api(state=state)
        credit_data['mob_phone'] = TestData.phone()
        credit_data['phone_home'] = TestData.phone()
        credit_data['isValidityCheckRequired'] = True
        lead_id = lead_create_page.create_lead_via_api(get_token_leads, **credit_data)
        login_page.login_with_cookies(page=leads_pages.leads_calculator, client_id=lead_id)
        current_number_of_months = lead_calculator_page.get_number_of_months()
        lead_calculator_page.fill_funding_deposit_date_field(TestData.get_date(+5))
        lead_calculator_page.fill_next_pay_date_field(TestData.get_date(+7))
        lead_calculator_page.fill_funding_depost(100)
        lead_calculator_page.click_elem_by_text('label', 'Total Debt')
        lead_calculator_page.change_number_of_months(number_of_months, action='plus')
        lead_calculator_page.check_number_of_months(current_number_of_months+number_of_months)
        lead_profile_page.refresh_page()
        current_number_of_months = lead_calculator_page.get_number_of_months()
        lead_calculator_page.change_number_of_months(number_of_months, action='minus')
        lead_calculator_page.check_number_of_months(current_number_of_months-number_of_months)
        lead_profile_page.refresh_page()
        calculator_data_before = lead_calculator_page.get_calculator_data()
        lead_calculator_page.check_valid_deposit_schedule_lines()

        lead_calculator_page.edit_deposits_frequency(LeadsTypeOfPays.semimonthly)
        lead_calculator_page.check_calculator_data(calculator_data_before)
        lead_calculator_page.check_valid_deposit_schedule_lines()

        lead_calculator_page.edit_deposits_frequency(LeadsTypeOfPays.monthly)
        lead_calculator_page.check_calculator_data(calculator_data_before)
        lead_calculator_page.check_valid_deposit_schedule_lines()
