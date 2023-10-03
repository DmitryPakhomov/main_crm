import time

import testit
import pytest
from typing import Any
from dotenv import load_dotenv
from autotests.pages.data.leads_data import leads_pages, leads_tabs, leads_statuses
from autotests.pages.data.main_data import send_docs, roles
from autotests.pages.data.settings_data import settings_pages
from autotests.pages.data.test_data import TestData


load_dotenv()


class TestLeadsPage:
    title = 'Checking the console logs of the Leads page for errors [{case}][{role}]'
    @testit.displayName(title)
    @testit.externalId('leads test 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, role, ui_data',
        [
            ('1', leads_statuses.new, 'admin', ['leads_pages_console_log', leads_statuses.new]),
            ('2', leads_statuses.docs_sent, 'admin', ['leads_pages_console_log', leads_statuses.docs_sent]),
            ('3', leads_statuses.nurtured, 'admin', ['leads_pages_console_log', leads_statuses.nurtured]),
            ('4', leads_statuses.ready_to_pitch, 'admin', ['leads_pages_console_log', leads_statuses.ready_to_pitch]),
            ('5', leads_statuses.hot, 'admin', ['leads_pages_console_log', leads_statuses.hot]),
            ('6', leads_statuses.automation, 'admin', ['leads_pages_console_log', leads_statuses.automation]),
            ('7', leads_statuses.mail_fax_docs, 'admin', ['leads_pages_console_log', leads_statuses.mail_fax_docs]),
            ('8', leads_statuses.pre_enrollment_sent, 'admin', ['leads_pages_console_log', leads_statuses.pre_enrollment_sent]),
            ('9', leads_statuses.pre_enrollment_completed, 'admin', ['leads_pages_console_log', leads_statuses.pre_enrollment_completed])
        ], indirect=['ui_data']
    )
    def test_leads_pages_console_log(
            self, ex_id: str, case: str, role: str, ui_data, login, login_page
    ) -> Any:
        """ Checking the console logs of the Leads page for errors - """
        pages = [
            leads_pages.leads,
            leads_pages.leads_history,
            leads_pages.leads_profile,
            leads_pages.leads_income,
            leads_pages.leads_creditors,
            leads_pages.leads_budget,
            leads_pages.leads_calculator,
            leads_pages.leads_loan_calculator,
            leads_pages.leads_ach,
            leads_pages.leads_document,
            leads_pages.leads_duplicate,
            leads_pages.leads_tasks,
            leads_pages.leads_logs
        ]
        login_page.check_page_console_log_errors(pages=pages, client_id=ui_data.data)

    title = 'Checking the creation of leads in CRM [{role}][{case}]'
    @testit.displayName(title)
    @testit.externalId('leads test 2 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, role, zip_code, address',
        [
            ('1', 'with_required_fields', roles.sales, '97209', ''),
            ('2', 'with_all_fields', roles.sales, '28715', '440 Dogwood Rd'),
            ('3', 'without_email', roles.admin, '90746', '')
        ]
    )
    def test_lead_create_page_create_lead(
            self,
            ex_id: str,
            case: str,
            role: str,
            zip_code: str,
            address: str,
            login_page,
            lead_create_page
    ) -> Any:
        """ Checking the creation of leads in CRM via the "Create new" button - """
        login_page.login_with_cookies(role=role)
        match case:
            case 'with_required_fields':
                lead_create_page.creating(zip_code=zip_code)
            case 'with_all_fields':
                lead_create_page.creating(zip_code=zip_code, address=address)
            case 'without_email':
                lead_create_page.creating(zip_code=zip_code, no_email=True)

    title = 'Checking applicant fields [{role}]'
    @testit.displayName(title)
    @testit.externalId('leads test 3 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role', [('1', 'admin')])
    def test_lead_profile_page_applicant_fields(
            self, ex_id: str, role: str, login, login_page, lead_create_page, lead_profile_page
    ) -> Any:
        """ Checking applicant fields - """
        login_page.login_with_cookies()
        credit_data = TestData.credit_report_data(state='CA')

        lead_data = lead_create_page.creating(
            first_name=credit_data.first_name,
            last_name=credit_data.last_name,
            zip_code=credit_data.zip_code,
            address=credit_data.address
        )
        lead_profile_page.choose_leads_tabs(tab=leads_tabs.profile)
        lead_data_part_two = lead_profile_page.fill_empty_applicants_field_after_lead_creating()
        lead_profile_page.saving()
        lead_profile_page.check_all_fields_applicant(
            lead_create_form_data=lead_data[1],
            lead_applicant_empty_fields_data=lead_data_part_two
        )

    title = 'Checking adding income [{role}]'
    @testit.displayName(title)
    @testit.externalId('leads test 4 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, role, page',
        [
            ('1', 'admin', leads_pages.leads_profile)
        ]
    )
    def test_lead_income_page_add_income(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            lead_create_page,
            lead_income_page,
            get_token_leads
    ) -> Any:
        """ Checking adding income - """
        state = 'CA'
        credit_data: dict = TestData.credit_report_data_for_api(state=state)
        credit_data['mob_phone'] = TestData.phone()
        credit_data['phone_home'] = TestData.phone()
        credit_data['isValidityCheckRequired'] = True
        lead_id = lead_create_page.create_lead_via_api(get_token_leads, **credit_data)
        login_page.login_with_cookies(page=page, client_id=lead_id)
        lead_income_page.choose_leads_tabs(tab=leads_tabs.income)
        lead_income_page.remove_all_income()
        count = lead_income_page.get_income_count()
        income_data = lead_income_page.add_new_income(count=count)
        lead_income_page.check_income(excepted_income_data=income_data, count=count)

    title = 'Checking adding creditor [{role}]'
    @testit.displayName(title)
    @testit.externalId('leads test 5 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page', [('1', 'admin', leads_pages.leads_profile)])
    def test_lead_creditors_page_add_creditor(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            lead_create_page,
            lead_creditors_page,
            get_token_leads
    ) -> Any:
        """ Checking adding creditor - """
        state = 'CA'
        credit_data: dict = TestData.credit_report_data_for_api(state=state)
        lead_id = lead_create_page.create_lead_via_api(get_token_leads, **credit_data)
        login_page.login_with_cookies(page=page, client_id=lead_id)
        lead_creditors_page.choose_leads_tabs(tab=leads_tabs.creditors)
        creditor_data = lead_creditors_page.add_new_creditor()
        lead_creditors_page.check_creditors(excepted_creditor_data=creditor_data)

    title = 'Checking creditors data [{role}]'
    @testit.displayName(title)
    @testit.externalId('leads test 6 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page', [('1', 'admin', leads_pages.leads_profile)])
    def test_lead_creditors_page_data(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            lead_create_page,
            lead_profile_page,
            lead_creditors_page,
            get_token_leads
    ) -> Any:
        """ Checking creditors data - """
        state = 'CA'
        credit_data: dict = TestData.credit_report_data_for_api(state=state)
        credit_data['mob_phone'] = TestData.phone()
        credit_data['phone_home'] = TestData.phone()
        credit_data['isValidityCheckRequired'] = True
        lead_id = lead_create_page.create_lead_via_api(get_token_leads, **credit_data)
        login_page.login_with_cookies(page=page, client_id=lead_id)
        lead_creditors_page.choose_leads_tabs(tab=leads_tabs.creditors)
        lead_creditors_page.check_creditors_total_data()
        lead_creditors_page.check_creditors_section()
        lead_creditors_page.check_total_unsecured_debt_section()

    title = 'Checking all budget data [{role}]'
    @testit.displayName(title)
    @testit.externalId('leads test 7 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page', [('1', 'admin', leads_pages.leads_profile)])
    def test_lead_budget_page_data(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            lead_create_page,
            lead_budget_page,
            get_token_leads
    ) -> Any:
        """ Check all budget data - """
        state = 'CA'
        credit_data: dict = TestData.credit_report_data_for_api(state=state)
        credit_data['mob_phone'] = TestData.phone()
        credit_data['phone_home'] = TestData.phone()
        credit_data['isValidityCheckRequired'] = True
        lead_id = lead_create_page.create_lead_via_api(get_token_leads, **credit_data)
        login_page.login_with_cookies(page=page, client_id=lead_id)
        lead_create_page.choose_leads_tabs(tab=leads_tabs.budget)
        all_expected_data = lead_budget_page.fill_all_budget_data()
        lead_budget_page.check_all_budget_data(all_expected_data=all_expected_data)

    title = 'Checking send docs Agreement Only state {state}'
    @testit.displayName(title)
    @testit.externalId('leads test 8 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, state, role, page',
        [
            ('1', 'CA', 'admin', leads_pages.leads_profile),
            # ('2', 'NC', 'admin', leads_pages.leads_profile),
        ]
    )
    def test_leads_pages_send_agreement_only(
            self,
            ex_id: str,
            state: str,
            role: str,
            page: str,
            login_page,
            lead_create_page,
            lead_history_page,
            lead_profile_page,
            lead_income_page,
            lead_budget_page,
            lead_calculator_page,
            lead_ach_page,
            get_token_leads
    ) -> Any:
        """ Checking send docs Agreement Only - """
        sales_rep = TestData.sales_rep(all_sales_rep=True)[1]
        credit_data: dict = TestData.credit_report_data_for_api(state=state)
        credit_data['mob_phone'] = TestData.phone()
        credit_data['phone_home'] = TestData.phone()
        credit_data['isValidityCheckRequired'] = True
        lead_id = lead_create_page.create_lead_via_api(get_token_leads, **credit_data)
        login_page.login_with_cookies(page=page, client_id=lead_id)
        lead_profile_page.check_rejected_lead()
        lead_history_page.reassigning(sales_rep=sales_rep)
        lead_income_page.choose_leads_tabs(tab=leads_tabs.income)
        lead_income_page.remove_all_income()
        count = lead_income_page.get_income_count()
        lead_income_page.add_new_income(count=count)
        lead_budget_page.choose_leads_tabs(tab=leads_tabs.budget)
        lead_budget_page.fill_all_budget_data()
        lead_calculator_page.choose_leads_tabs(tab=leads_tabs.calculator)
        lead_calculator_page.calculator(number_of_months=20)
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.ach)
        lead_ach_page.fill_ach_fields()
        lead_history_page.sending_docs(sending_type=send_docs.agreement_only)

    title = 'Checking reassign notifications [{role}]'
    @testit.displayName(title)
    @testit.externalId('leads test 9 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, role, page',
        [
            ('1', 'loan_consultant', leads_pages.leads_profile)
        ]
    )
    def test_lead_profile_page_reassign_notification(
            self,
            ex_id: str,
            role: str,
            page: str,
            config,
            login_page,
            lead_create_page,
            lead_profile_page,
            settings_users_page,
            get_token_leads
    ) -> Any:
        """ Check reassign notification - """
        state = 'CA'
        credit_data: dict = TestData.credit_report_data_for_api(state=state)
        credit_data['mob_phone'] = TestData.phone()
        credit_data['phone_home'] = TestData.phone()
        credit_data['isValidityCheckRequired'] = True
        lead_id = lead_create_page.create_lead_via_api(get_token_leads, **credit_data)
        login_page.login_with_cookies(page=page, client_id=lead_id)
        sales_rep = TestData.sales_rep(all_sales_rep=True)[1]
        lead_profile_page.reassigning(sales_rep=sales_rep)
        lead_profile_page.choose_leads_tabs(tab=leads_tabs.profile)
        lead_profile_page.click_tg_upfront_lending_candidate()
        lead_profile_page.reassigning(c9_loan_consultant=config.auth[role]['username'])
        lead_profile_page.click_dl_avatar()
        lead_profile_page.click_btn_settings()
        settings_users_page.change_settings_page(page=settings_pages.users, internal_title=True)
        login_page.login_with_cookies(role=role, page=page, client_id=lead_id)
        settings_users_page.check_notification(
            name=credit_data['firstName'], last_name=credit_data['lastName'], lead_id=lead_id)

    title = 'Checking send upfront final loan [{state}][{role}]'
    @testit.displayName(title)
    @testit.externalId('leads test 10 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, state, role, page',
        [
            ('1', 'CA', 'admin', leads_pages.leads_profile)
        ]
    )
    def test_leads_pages_send_upfront_final_loan(
            self,
            ex_id: str,
            state: str,
            role: str,
            page: str,
            login_page,
            lead_create_page,
            lead_history_page,
            lead_profile_page,
            lead_income_page,
            lead_budget_page,
            lead_calculator_page,
            lead_ach_page,
            lead_documents_page,
            lead_underwriting_page,
            get_token_leads
    ) -> Any:
        """ Checking send upfront final loan - """
        sales_rep = TestData.sales_rep(all_sales_rep=True)[1]
        state = 'CA'
        credit_data: dict = TestData.credit_report_data_for_api(state=state)
        credit_data['mob_phone'] = TestData.phone()
        credit_data['phone_home'] = TestData.phone()
        credit_data['isValidityCheckRequired'] = True
        lead_id = lead_create_page.create_lead_via_api(get_token_leads, **credit_data)
        login_page.login_with_cookies(page=page, client_id=lead_id)
        lead_history_page.reassigning(sales_rep=sales_rep)
        lead_income_page.choose_leads_tabs(tab=leads_tabs.history)
        lead_history_page.check_sales_rep_quick_stats(sales_rep=sales_rep)
        lead_income_page.choose_leads_tabs(tab=leads_tabs.income)
        lead_income_page.remove_all_income()
        count = lead_income_page.get_income_count()
        lead_income_page.add_new_income(count=count)
        lead_budget_page.choose_leads_tabs(tab=leads_tabs.budget)
        lead_budget_page.fill_all_budget_data()
        lead_calculator_page.choose_leads_tabs(tab=leads_tabs.calculator)
        lead_calculator_page.calculator()
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.ach)
        lead_ach_page.fill_ach_fields()
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.documents)
        lead_documents_page.add_document(document_type='W2')
        lead_documents_page.add_document(document_type='Bank Statements')
        lead_documents_page.add_document(document_type='Paycheck')
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.history)
        lead_history_page.enabling_upfront()
        lead_history_page.underwriting()
        lead_underwriting_page.loc_processing_verification_kyc()
        lead_history_page.underwriting()
        lead_income_page.choose_leads_tabs(tab=leads_tabs.income)
        lead_income_page.fill_other_income()
        lead_history_page.underwriting_and_confirmation()
        lead_history_page.turn_off_and_on_loan_pro()
        lead_history_page.sending_upfront_docs(sending_type=send_docs.upfront_final_loan)
        lead_history_page.choose_leads_tabs(tab=leads_tabs.history)
        lead_history_page.check_locked_status()
        lead_history_page.check_history_event(subject_text='underwriting status changed')

    title = 'Checking co-applicant fields [{state}][{role}]'
    @testit.displayName(title)
    @testit.externalId('leads test 11 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, state, role',
        [
            ('1', 'CA', roles.admin),
            ('2', 'NJ', roles.admin),
        ]
    )
    def test_lead_ach_page_check_fields_co_applicant(
            self,
            ex_id: str,
            state: str,
            role: str,
            lead_create_page,
            lead_history_page,
            lead_profile_page,
            lead_income_page,
            lead_budget_page,
            lead_calculator_page,
            lead_ach_page,
            lead_documents_page,
            lead_underwriting_page,
            login_page,
            get_token_leads,
            config
    ) -> Any:
        """ Checking co-applicant fields - """
        credit_data_first_applicant = TestData.credit_report_data_from_csv(state=state)
        credit_data_first_applicant['isValidityCheckRequired'] = True
        lead_id = lead_create_page.create_lead_via_api(
            get_token_leads, **credit_data_first_applicant)
        login_page.login_with_cookies(page=leads_pages.leads_history, client_id=lead_id)
        lead_history_page.check_rejected_lead()
        lead_history_page.reassigning(
            sales_rep=config.auth[roles.sales_debt_consultant]['username'])
        lead_history_page.choose_leads_tabs(tab=leads_tabs.profile)
        all_expected_data = lead_profile_page.added_co_applicant()
        lead_profile_page.check_all_fields_co_applicant(all_expected_data=all_expected_data)

    title = 'Checking ach fields [{state}][{role}]'
    @testit.displayName(title)
    @testit.externalId('leads test 12 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, state, role',
        [
            ('1', 'CA', roles.admin)
        ]
    )
    def test_lead_ach_page_check_fields(
            self,
            ex_id: str,
            state: str,
            role: str,
            login_page,
            lead_create_page,
            lead_history_page,
            lead_profile_page,
            lead_ach_page,
            get_token_leads
    ) -> Any:
        """ Checking ach page - """
        credit_data: dict = TestData.credit_report_data_for_api(state=state)
        credit_data['mob_phone'] = TestData.phone()
        credit_data['phone_home'] = TestData.phone()
        lead_id = lead_create_page.create_lead_via_api(get_token_leads, **credit_data)
        login_page.login_with_cookies(page=leads_pages.leads_ach, client_id=lead_id)
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.ach)
        all_expected_data = lead_ach_page.fill_full_ach_fields()
        lead_ach_page.check_full_all_fields_ach(excepted_data=all_expected_data)

    title = 'Checking creditors rules [{role}]'
    @testit.displayName(title)
    @testit.externalId('leads test 6 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page', [('1', 'admin', leads_pages.leads_profile)])
    def test_lead_creditors_rules(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            lead_create_page,
            lead_profile_page,
            lead_creditors_page,
            get_token_leads
    ) -> Any:
        """ Checking creditors rules - """
        state = 'CA'
        credit_data: dict = TestData.credit_report_data_for_api(state=state)
        credit_data['mob_phone'] = TestData.phone()
        credit_data['phone_home'] = TestData.phone()
        credit_data['isValidityCheckRequired'] = True
        lead_id = lead_create_page.create_lead_via_api(get_token_leads, **credit_data)
        login_page.login_with_cookies(page=page, client_id=lead_id)
        lead_creditors_page.choose_leads_tabs(tab=leads_tabs.creditors)
        lead_creditors_page.check_creditors_rules()
