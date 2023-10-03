import time
import testit
import pytest
from typing import Any
from autotests.pages.data.test_data import TestData
from autotests.pages.data.leads_data import leads_pages, leads_tabs, leads_debt_type
from autotests.pages.data.main_data import send_docs, main_tabs


class TestBrokersPage:
    title = 'Checking the console logs of the Leads page for errors with role [{role}]'
    @testit.displayName(title)
    @testit.externalId('brokers test 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role', [('1', 'broker_test')])
    def test_brokers_leads_pages_console_log(
            self,
            ex_id: str,
            role: str,
            config,
            brokers_login_page
    ) -> Any:
        """ Checking the console logs of the Leads page for errors - """
        brokers_login_page.login_by_password(role=role)
        pages = [
            leads_pages.leads,
            leads_pages.leads_history,
            leads_pages.leads_profile,
            leads_pages.leads_creditors,
            leads_pages.leads_income,
            leads_pages.leads_budget,
            leads_pages.leads_calculator,
            leads_pages.leads_ach,
            leads_pages.leads_document
        ]
        client_id = config.ui_data['leads_brokers']['client']
        brokers_login_page.check_page_console_log_errors(
            pages=pages, client_id=client_id
        )

    title = 'Checking the creation of leads in CRM [{broker_role}][{case}]'
    @testit.displayName(title)
    @testit.externalId('brokers test 2 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, broker_role, zip_code, address',
        [
            ('1', 'with_required_fields', 'broker_test', '15126', ''),
            ('2', 'with_all_fields', 'broker_test', '28715', '440 Dogwood Rd'),
            ('3', 'without_email', 'broker_test', '90746', '')
        ]
    )
    def test_brokers_lead_create_page_create_lead(
            self,
            ex_id: str,
            case: str,
            broker_role: str,
            zip_code: str,
            address: str,
            brokers_login_page,
            brokers_lead_create_page
    ) -> Any:
        """ Checking the creation of leads in CRM via the "Create new" button  - """
        brokers_login_page.login_by_password(role=broker_role)
        match case:
            case 'with_required_fields':
                brokers_lead_create_page.creating(zip_code=zip_code)
            case 'with_all_fields':
                brokers_lead_create_page.creating(zip_code=zip_code, address=address)
            case 'without_email':
                brokers_lead_create_page.creating(zip_code=zip_code, no_email=True)

    title = 'Checking send Agreement Only [{state}]'
    @testit.displayName(title)
    @testit.externalId('brokers test 3 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, state, broker_role',
        [
            ('1', 'CA', 'broker_test'),
            ('2', 'NC', 'broker_test')
        ]
    )
    def test_brokers_leads_send_agreement_only(
            self,
            ex_id: str,
            state: str,
            broker_role: str,
            brokers_login_page,
            brokers_lead_create_page,
            lead_profile_page,
            lead_income_page,
            lead_budget_page,
            lead_calculator_page,
            lead_ach_page,
            lead_creditors_page
    ) -> Any:
        """ Checking send Agreement Only - """
        brokers_login_page.login_by_password(role=broker_role)
        credit_data = TestData.credit_report_data(state=state)
        brokers_lead_create_page.creating(
            first_name=credit_data.first_name,
            last_name=credit_data.last_name,
            zip_code=credit_data.zip_code,
            address=credit_data.address,
            email=TestData.email()
        )
        lead_profile_page.choose_leads_tabs(tab=leads_tabs.profile)
        lead_profile_page.get_broker_credit_report(
            address=credit_data.address,
            ssn=credit_data.ssn,
            status='3 - Application Taken-Building File'
        )
        lead_profile_page.choose_leads_tabs(tab=leads_tabs.income)
        lead_income_page.remove_all_income()
        count = lead_income_page.get_income_count()
        lead_income_page.add_new_income(count=count)
        lead_budget_page.choose_leads_tabs(tab=leads_tabs.budget)
        lead_budget_page.fill_all_budget_data()
        lead_calculator_page.choose_leads_tabs(tab=leads_tabs.calculator)
        lead_calculator_page.calculator(number_of_months=20)
        lead_calculator_page.choose_leads_tabs(tab=leads_tabs.creditors)
        if state == 'NC':
            lead_creditors_page.add_new_creditor(balance='10000',
                                                 debt_type=leads_debt_type.charge_account)
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.ach)
        lead_ach_page.fill_ach_fields()
        lead_ach_page.sending_docs(sending_type=send_docs.agreement_only)

    title = 'Checking send financial profile [{broker_role}]'
    @testit.displayName(title)
    @testit.externalId('brokers test 4 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, broker_role', [('1', 'broker_test')])
    def test_brokers_lead_history_page_send_financial_profile(
            self,
            ex_id: str,
            broker_role: str,
            brokers_login_page,
            brokers_lead_create_page,
            lead_history_page,
            lead_profile_page
    ) -> Any:
        """ Checking send financial profile - """
        brokers_login_page.login_by_password(role=broker_role)
        credit_data = TestData.credit_report_data()
        first_name = credit_data.first_name
        last_name = credit_data.last_name
        brokers_lead_create_page.creating(
            first_name=first_name,
            last_name=last_name,
            zip_code=credit_data.zip_code,
            address=credit_data.address,
            email=TestData.email()
        )
        lead_profile_page.choose_leads_tabs(tab=leads_tabs.profile)
        lead_profile_page.get_broker_credit_report(
            address=credit_data.address,
            ssn=credit_data.ssn,
            status='5 - Proposal Completed'
        )
        lead_profile_page.change_status('Ready to Pitch')
        lead_profile_page.choose_leads_tabs(tab=leads_tabs.history)
        lead_history_page.change_tab_note_mail('Pre-made Email')
        lead_history_page.click_btn_financial_profile()
        time.sleep(2)
        lead_history_page.send_financial_profile()
        lead_history_page.check_after_send_fp(first_name, last_name)

    title = 'Checking adding note [{broker_role}]'
    @testit.displayName(title)
    @testit.externalId('brokers test 5 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, broker_role', [('1', 'broker_test')])
    def test_brokers_leads_pages_add_note(
            self,
            ex_id: str,
            broker_role: str,
            brokers_login_page,
            brokers_leads_page,
            brokers_lead_history_page,
            brokers_lead_create_page
    ) -> Any:
        """ Checking adding note - """
        brokers_login_page.login_by_password(role=broker_role)
        credit_data = TestData.credit_report_data()
        first_name = credit_data.first_name
        last_name = credit_data.last_name
        brokers_lead_create_page.creating(
            first_name=first_name,
            last_name=last_name,
            zip_code=credit_data.zip_code,
            address=credit_data.address,
            email=TestData.email()
        )
        note_text = TestData.words()
        brokers_leads_page.creating_new_note(note_text=note_text)
        brokers_lead_history_page.check_history_event_create_note(note_text=note_text)

    title ='Checking KPI report [{broker_role}]'
    @testit.displayName(title)
    @testit.externalId('brokers test 6 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, broker_role', [('1', 'broker_test')])
    def test_brokers_report_page_kpi_report(
            self, ex_id: str, broker_role: str, brokers_login_page, brokers_reports_page
    ) -> Any:
        """ Checking KPI report - """
        brokers_login_page.login_by_password(role=broker_role)
        brokers_login_page.click_main_tabs(tab=main_tabs.reports)
        brokers_reports_page.click_report('KPI Report')

    title = 'Checking rejecting of lead [{broker_role}]'
    @testit.displayName(title)
    @testit.externalId('brokers test 7 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, broker_role', [('1', 'broker_test')])
    def test_brokers_leads_page_reject_lead(
            self, ex_id: str, broker_role: str, brokers_login_page, brokers_lead_create_page
    ) -> Any:
        """ Checking rejecting of lead - """
        brokers_login_page.login_by_password(role=broker_role)
        credit_data = TestData.credit_report_data(state='CA')
        first_name = credit_data.first_name
        last_name = credit_data.last_name
        brokers_lead_create_page.creating(
            first_name=first_name,
            last_name=last_name,
            zip_code=credit_data.zip_code,
            address=credit_data.address,
            email=TestData.email()
        )
        brokers_lead_create_page.reject_lead(reason='Do Not Call/Mail')
        brokers_lead_create_page.check_reject_status(excepted_reason='Do Not Call/Mail')

    title = 'Checking reassign lead [{broker_role}]'
    @testit.displayName(title)
    @testit.externalId('brokers test 8 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, broker_role', [('1', 'broker_test')])
    def test_brokers_lead_history_page_reassign(
            self,
            ex_id: str,
            broker_role: str,
            brokers_login_page,
            brokers_lead_create_page,
            lead_history_page
    ) -> Any:
        """ Checking reassign lead - """
        brokers_login_page.login_by_password(role=broker_role)
        credit_data = TestData.credit_report_data(state='CA')
        first_name = credit_data.first_name
        last_name = credit_data.last_name
        brokers_lead_create_page.creating(
            first_name=first_name,
            last_name=last_name,
            zip_code=credit_data.zip_code,
            address=credit_data.address,
            email=TestData.email()
        )
        brokers_lead_create_page.reassign_lead(sales_rep='user qa')
        lead_history_page.check_sales_rep_quick_stats(sales_rep='user qa')
