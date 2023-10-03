import pytest
import testit
from typing import Any
from dotenv import load_dotenv
from autotests.pages.data.loans_data import loans_pages


load_dotenv()


class TestLoansPage:
    title = 'Checking the console logs of the Loans page for errors with role [{role}]'
    @testit.displayName(title)
    @testit.externalId('loans test 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role', [('1', 'admin')])
    def test_loans_pages_console_log(
            self, ex_id: str, role: str, config, login, login_page
    ) -> Any:
        """ Checking the console logs of the Loans page for errors - """
        pages = [
            loans_pages.loans,
            loans_pages.loans_history,
            loans_pages.loans_drafts,
            loans_pages.loans_creditors,
            loans_pages.loans_loan_plan,
            loans_pages.loans_profile,
            loans_pages.loans_income,
            loans_pages.loans_budget,
            loans_pages.loans_ach,
            loans_pages.loans_document,
            loans_pages.loans_tasks,
            loans_pages.loans_logs
        ]
        client_id = config.ui_data['loans']['client']
        login_page.check_page_console_log_errors(pages=pages, client_id=client_id)

    title = 'Checking the adding creditor [{role}]'
    @testit.displayName(title)
    @testit.externalId('loans test 2 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role', [('2', 'admin')])
    def test_loan_add_creditor(
            self, ex_id: str, role: str, config, login, loan_creditors_page, login_page
    ) -> Any:
        """ Checking adding creditor - """
        loan_id = config.ui_data['loans']['client']
        login_page.login_with_cookies(page=loans_pages.loans_creditors, client_id=loan_id)
        loan_creditors_page.check_js_errors()
        loan_creditors_page.click_btn_create_new_creditor()
        all_expected_data = loan_creditors_page.fill_all_creditor_data()
        loan_creditors_page.select_creditors()
        loan_creditors_page.check_all_creditors_data(all_expected_data=all_expected_data)

    title = 'Checking create income for loans with role [{role}]'
    @testit.displayName(title)
    @testit.externalId('loans test 3 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role', [('3', 'admin')])
    def test_create_income_for_loans(
            self, ex_id: str, role: str, config, login_page, loan_income_page
    ) -> Any:
        """ Creating income from deals - """
        with testit.step('Test added income for deals'):
            loan_id = config.ui_data['loans']['client']
            login_page.login_with_cookies(page=loans_pages.loans_income, client_id=loan_id)
            count = loan_income_page.get_income_count()
            loan_income_page.check_unlock_status()
            loan_income_page.clean_income_fields(count)
            all_expected_data = loan_income_page.fill_all_income_data()
            loan_income_page.check_income(excepted_income_data=all_expected_data)

    title = 'Checking all budget data [{role}]'
    @testit.displayName(title)
    @testit.externalId('enrollments test 4 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role', [('4', 'admin')])
    def test_loan_budget_page_data(
            self, ex_id: str, role: str, login_page, loan_budget_page, config
    ) -> Any:
        """ Check all budget data - """
        loan_id = config.ui_data['loans']['client']
        login_page.login_with_cookies(page=loans_pages.loans_budget, client_id=loan_id)
        all_expected_data = loan_budget_page.fill_all_budget_data()
        loan_budget_page.check_all_budget_data(all_expected_data=all_expected_data)

    title = 'Checking change ACH for loans with role [{role}]'
    @testit.displayName(title)
    @testit.externalId('loans test 5 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role', [('5', 'admin')])
    def test_change_ach_for_loans(
            self, ex_id: str, role: str, config, login_page, loan_ach_page
    ) -> Any:
        """ Creating income from deals - """
        with testit.step('Test change ach for loans'):
            loan_id = config.ui_data['loan_for_ach']['client']
            login_page.login_with_cookies(page=loans_pages.loans_ach, client_id=loan_id)
            all_expected_data = loan_ach_page.fill_ach_fields()
            loan_ach_page.check_all_fields_ach(excepted_data=all_expected_data)
            loan_ach_page.sending_ach_docs('Email Only')
