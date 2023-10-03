import os
import testit
import pytest
from typing import Any
from dotenv import load_dotenv
from autotests.pages import pages_details
from autotests.pages.data.leads_data import leads_pages, leads_tabs
from autotests.pages.data.test_data import TestData
from autotests.pages.data.main_data import roles
from autotests.pages.utils import slack_post_msg, convert_dict_to_string


load_dotenv()


def get_leads_text_blocks(
        title_text: str,
        message_text: str,
) -> str:
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": title_text
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": message_text
            }
        },
        {
            "type": "divider"
        }
    ]
    return str(blocks)


class TestLeadsPreparePage:
    title = 'Prepare lead for manual testing'

    @testit.displayName(title)
    @testit.externalId('leads prepare 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, state, role',
        [
            ('1', 'CA', roles.sales_debt_consultant),
            ('2', 'NJ', roles.sales_debt_consultant),
            ('3', '', roles.sales_debt_consultant)
        ]
    )
    def test_leads_prepare_lead(
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
            get_token_leads
    ) -> Any:
        """ Prepare lead """
        credit_data_first_applicant = TestData.credit_report_data_from_csv(state=state)
        credit_data_first_applicant['isValidityCheckRequired'] = True
        lead_id = lead_create_page.create_lead_via_api(
            get_token_leads, **credit_data_first_applicant)
        login_page.login_with_cookies(
            role=role,
            page=leads_pages.leads_history,
            client_id=lead_id
        )
        lead_history_page.check_rejected_lead()
        lead_history_page.reassigning(
            sales_rep=login_page.cfg.auth[roles.sales_debt_consultant]['username'])
        lead_income_page.choose_leads_tabs(tab=leads_tabs.income)
        lead_income_page.remove_all_income()
        count = lead_income_page.get_income_count()
        lead_income_page.add_new_income(count=count)
        lead_budget_page.choose_leads_tabs(tab=leads_tabs.budget)
        lead_budget_page.fill_all_budget_data()
        lead_calculator_page.choose_leads_tabs(tab=leads_tabs.calculator)
        lead_calculator_page.calculator()
        lead_calculator_page.fill_next_pay_date_field(TestData.get_date(+7))
        lead_calculator_page.fill_funding_depost(300)
        lead_calculator_page.fill_funding_deposit_date_field(TestData.get_date(+5))
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.ach)
        lead_ach_page.fill_ach_fields(ssn=credit_data_first_applicant['ssn'])
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.documents)
        lead_documents_page.add_document(document_type='W2')
        lead_documents_page.add_document(document_type='Bank Statements')
        lead_documents_page.add_document(document_type='Paycheck')
        title_text = f'    :star: *TEST LEAD: {state}* :star:'
        message_text = f'\n *CLIENT DATA*: ' \
                       f'```{convert_dict_to_string(credit_data_first_applicant)}\n```'\
                       f'\n :nyancat_big: <{lead_history_page.base_url+getattr(pages_details, leads_pages.leads_profile).ENDPOINT+lead_id}|*GO TO LEAD*> '
        slack_post_msg(
            token=os.environ['PERFORMANCE_BOT_TOKEN'],
            channel=os.environ['LEADS_PREPARATION_CHANNEL'],
            blocks=get_leads_text_blocks(title_text, message_text),
            icon_emoji=':smoking_stress:',
            username='Selenium'
        )

    title = 'Prepare lead with co-applicant for manual testing'

    @testit.displayName(title)
    @testit.externalId('leads prepare 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, state, role',
        [
            ('1', 'CA', roles.admin),
            ('2', 'NJ', roles.admin),
            ('3', '', roles.admin)
        ]
    )
    def test_leads_prepare_lead_co_applicant(
            self,
            ex_id: str,
            state: str,
            role: str,
            login,
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
            get_token_leads
    ) -> Any:
        """ Prepare lead """
        credit_data_first_applicant = TestData.credit_report_data_from_csv(state=state)
        credit_data_first_applicant['isValidityCheckRequired'] = True
        credit_data_co_applicant = TestData.credit_report_data_from_csv()
        lead_id = lead_create_page.create_lead_via_api(
            get_token_leads, **credit_data_first_applicant)
        login_page.login_with_cookies(
            role=role,
            page=leads_pages.leads_history,
            client_id=lead_id
        )
        lead_history_page.check_rejected_lead()
        lead_history_page.reassigning(
            sales_rep=login_page.cfg.auth[roles.sales_debt_consultant]['username'])
        lead_history_page.choose_leads_tabs(tab=leads_tabs.profile)
        lead_profile_page.added_co_applicant(
            first_name=credit_data_co_applicant['firstName'],
            last_name=credit_data_co_applicant['lastName'],
            zip_code=credit_data_co_applicant['zip'],
            address=credit_data_co_applicant['address'],
            city=credit_data_co_applicant['city'],
            dob=credit_data_co_applicant['dob'],
            ssn=credit_data_co_applicant['ssn']
        )
        lead_profile_page.get_credit_report_co_applicant(
            address=credit_data_co_applicant['address'], ssn=credit_data_co_applicant['ssn'])
        lead_income_page.choose_leads_tabs(tab=leads_tabs.income)
        lead_income_page.remove_all_income()
        count = lead_income_page.get_income_count()
        lead_income_page.add_new_income(count=count)
        lead_income_page.add_new_income_co_applicant(count=0)
        lead_budget_page.choose_leads_tabs(tab=leads_tabs.budget)
        lead_budget_page.fill_all_budget_data()
        lead_calculator_page.choose_leads_tabs(tab=leads_tabs.calculator)
        lead_calculator_page.calculator()
        lead_calculator_page.fill_next_pay_date_field(TestData.get_date(+7))
        lead_calculator_page.fill_funding_depost(300)
        lead_calculator_page.fill_funding_deposit_date_field(TestData.get_date(+5))
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.ach)
        lead_ach_page.fill_ach_fields(ssn=credit_data_co_applicant['ssn'])
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.documents)
        lead_documents_page.add_document(document_type='W2')
        lead_documents_page.add_document(document_type='Bank Statements')
        lead_documents_page.add_document(document_type='Paycheck')
        title_text = f'    :star: *TEST LEAD CO-APPLICANT: {state}* :star:'
        message_text = f'\n *CLIENT DATA*: ' \
                       f'```{convert_dict_to_string(credit_data_first_applicant)}\n```'\
                       f'\n\n *CO-APPLICANT DATA*: ' \
                       f'```{convert_dict_to_string(credit_data_co_applicant)}```' \
                       f'\n :nyancat_big: <{lead_history_page.base_url+getattr(pages_details, leads_pages.leads_profile).ENDPOINT+lead_id}|*GO TO LEAD*> '
        slack_post_msg(
            token=os.environ['PERFORMANCE_BOT_TOKEN'],
            channel=os.environ['LEADS_PREPARATION_CHANNEL'],
            blocks=get_leads_text_blocks(title_text, message_text),
            icon_emoji=':smoking_stress:',
            username='Selenium'
        )


class TestRamVerificationLeadsPreparePage:

    title = 'Prepare RAM lead for manual testing'

    @testit.displayName(title)
    @testit.externalId('leads prepare 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, state, role',
        [
            ('1', 'CA', roles.sales_debt_consultant),
            ('2', 'NJ', roles.sales_debt_consultant),
            ('3', '', roles.sales_debt_consultant),
        ]
    )
    def test_ram_leads_prepare_lead(
            self,
            ex_id: str,
            state: str,
            role: str,
            login,
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
            get_token_leads
    ) -> Any:
        """ Prepare lead """
        credit_data_first_applicant = TestData.credit_report_data_from_csv(state=state)
        credit_data_first_applicant['isValidityCheckRequired'] = True
        lead_id = lead_create_page.create_lead_via_api(
            get_token_leads, **credit_data_first_applicant)
        login_page.login_with_cookies(
            role=role,
            page=leads_pages.leads_history,
            client_id=lead_id
        )
        lead_history_page.check_rejected_lead()
        lead_history_page.reassigning(
            sales_rep=login_page.cfg.auth[roles.sales_debt_consultant]['username'])
        lead_income_page.choose_leads_tabs(tab=leads_tabs.income)
        lead_income_page.remove_all_income()
        count = lead_income_page.get_income_count()
        lead_income_page.add_new_income(count=count)
        lead_budget_page.choose_leads_tabs(tab=leads_tabs.budget)
        lead_budget_page.fill_all_budget_data()
        lead_calculator_page.choose_leads_tabs(tab=leads_tabs.calculator)
        lead_calculator_page.calculator()
        lead_calculator_page.fill_next_pay_date_field(TestData.get_date(+7))
        lead_calculator_page.fill_funding_depost(300)
        lead_calculator_page.fill_funding_deposit_date_field(TestData.get_date(+5))
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.ach)
        lead_ach_page.fill_ach_fields(ssn=TestData.ssn())
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.documents)
        lead_documents_page.add_document(document_type='W2')
        lead_documents_page.add_document(document_type='Bank Statements')
        lead_documents_page.add_document(document_type='Paycheck')
        lead_documents_page.add_document(document_type='SSN Verification Proof')
        lead_documents_page.add_document(document_type='Address Verification Proof')
        lead_documents_page.add_document(document_type='DOB Verification Proof')
        lead_documents_page.add_document(document_type='OFAC Verification Proof')
        title_text = f'    :star: *TEST RAM LEAD: {state}* :star:'
        message_text = f'\n *CLIENT DATA*: ' \
                       f'```{convert_dict_to_string(credit_data_first_applicant)}\n```'\
                       f'\n :nyancat_big: <{lead_history_page.base_url+getattr(pages_details, leads_pages.leads_profile).ENDPOINT+lead_id}|*GO TO LEAD*> '
        slack_post_msg(
            token=os.environ['PERFORMANCE_BOT_TOKEN'],
            channel=os.environ['LEADS_PREPARATION_CHANNEL'],
            blocks=get_leads_text_blocks(title_text, message_text),
            icon_emoji=':smoking_stress:',
            username='Selenium'
        )

    title = 'Prepare RAM lead with co-applicant for manual testing'

    @testit.displayName(title)
    @testit.externalId('leads prepare 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, state, role',
        [
            ('1', 'CA', roles.admin),
            ('2', 'NJ', roles.admin),
            ('3', '', roles.admin)
        ]
    )
    def test_ram_leads_prepare_lead_co_applicant(
            self,
            ex_id: str,
            state: str,
            role: str,
            login,
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
            get_token_leads
    ) -> Any:
        """ Prepare lead """
        credit_data_first_applicant = TestData.credit_report_data_from_csv(state=state)
        credit_data_first_applicant['isValidityCheckRequired'] = True
        credit_data_co_applicant = TestData.credit_report_data_from_csv()
        lead_id = lead_create_page.create_lead_via_api(
            get_token_leads, **credit_data_first_applicant)
        login_page.login_with_cookies(
            role=role,
            page=leads_pages.leads_history,
            client_id=lead_id
        )
        lead_history_page.check_rejected_lead()
        lead_history_page.reassigning(
            sales_rep=login_page.cfg.auth[roles.sales_debt_consultant]['username'])
        lead_history_page.choose_leads_tabs(tab=leads_tabs.profile)
        lead_profile_page.added_co_applicant(
            first_name=credit_data_co_applicant['firstName'],
            last_name=credit_data_co_applicant['lastName'],
            zip_code=credit_data_co_applicant['zip'],
            address=credit_data_co_applicant['address'],
            city=credit_data_co_applicant['city'],
            dob=credit_data_co_applicant['dob'],
            ssn=credit_data_co_applicant['ssn']
        )
        lead_profile_page.get_credit_report_co_applicant(
            address=credit_data_co_applicant['address'], ssn=credit_data_co_applicant['ssn'])
        lead_income_page.choose_leads_tabs(tab=leads_tabs.income)
        lead_income_page.remove_all_income()
        count = lead_income_page.get_income_count()
        lead_income_page.add_new_income(count=count)
        lead_income_page.add_new_income_co_applicant(count=0)
        lead_budget_page.choose_leads_tabs(tab=leads_tabs.budget)
        lead_budget_page.fill_all_budget_data()
        lead_calculator_page.choose_leads_tabs(tab=leads_tabs.calculator)
        lead_calculator_page.calculator()
        lead_calculator_page.fill_next_pay_date_field(TestData.get_date(+7))
        lead_calculator_page.fill_funding_depost(300)
        lead_calculator_page.fill_funding_deposit_date_field(TestData.get_date(+5))
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.ach)
        lead_ach_page.fill_ach_fields(ssn=TestData.ssn())
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.documents)
        lead_documents_page.add_document(document_type='W2')
        lead_documents_page.add_document(document_type='Bank Statements')
        lead_documents_page.add_document(document_type='Paycheck')
        lead_documents_page.add_document(document_type='SSN Verification Proof')
        lead_documents_page.add_document(document_type='Address Verification Proof')
        lead_documents_page.add_document(document_type='DOB Verification Proof')
        lead_documents_page.add_document(document_type='OFAC Verification Proof')
        lead_documents_page.add_document_co_applicant(
            document_type='SSN Verification Proof',
            applicant_name=credit_data_co_applicant["lastName"]
        )
        lead_documents_page.add_document_co_applicant(
            document_type='Address Verification Proof',
            applicant_name=credit_data_co_applicant["lastName"]
        )
        lead_documents_page.add_document_co_applicant(
            document_type='DOB Verification Proof',
            applicant_name=credit_data_co_applicant["lastName"]
        )
        title_text = f'    :star: *TEST RAM LEAD CO-APPLICANT: {state}* :star:'
        message_text = f'\n *CLIENT DATA*: ' \
                       f'```{convert_dict_to_string(credit_data_first_applicant)}\n```'\
                       f'\n\n *CO-APPLICANT DATA*: ' \
                       f'```{convert_dict_to_string(credit_data_co_applicant)}```' \
                       f'\n :nyancat_big: <{lead_history_page.base_url+getattr(pages_details, leads_pages.leads_profile).ENDPOINT+lead_id}|*GO TO LEAD*> '
        slack_post_msg(
            token=os.environ['PERFORMANCE_BOT_TOKEN'],
            channel=os.environ['LEADS_PREPARATION_CHANNEL'],
            blocks=get_leads_text_blocks(title_text, message_text),
            icon_emoji=':smoking_stress:',
            username='Selenium'
        )


class TestUpfrontLoanPreparePage:

    title = 'Prepare Upfront lead for manual testing'

    @testit.displayName(title)
    @testit.externalId('leads prepare 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, state, role',
        [
            ('1', 'CA', roles.loan_consultant),
            ('2', 'NJ', roles.loan_consultant),
            ('3', '', roles.loan_consultant),
        ]
    )
    def test_upfront_loan_prepare_lead(
            self,
            ex_id: str,
            state: str,
            role: str,
            login,
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
            get_token_leads
    ) -> Any:
        """ Prepare Upfront lead """
        credit_data_first_applicant = TestData.credit_report_data_from_csv(state=state)
        credit_data_first_applicant['isValidityCheckRequired'] = True
        lead_id = lead_create_page.create_lead_via_api(
            get_token_leads, **credit_data_first_applicant)
        login_page.login_with_cookies(
            role=roles.admin,
            page=leads_pages.leads_history,
            client_id=lead_id
        )
        lead_history_page.check_rejected_lead()
        login_page.login_with_cookies(
            role=role,
            page=leads_pages.leads_history,
            client_id=lead_id
        )
        lead_history_page.reassigning(
            sales_rep=login_page.cfg.auth[roles.sales_debt_consultant]['username'])
        lead_income_page.choose_leads_tabs(tab=leads_tabs.income)
        lead_budget_page.choose_leads_tabs(tab=leads_tabs.budget)
        lead_budget_page.fill_all_budget_data()
        lead_history_page.enabling_upfront()
        lead_income_page.choose_leads_tabs(tab=leads_tabs.income)
        lead_income_page.remove_all_income()
        count = lead_income_page.get_income_count()
        lead_income_page.add_upfront_new_income(count=count)
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.ach)
        lead_ach_page.fill_ach_fields(ssn=credit_data_first_applicant['ssn'])
        lead_history_page.underwriting_and_confirmation()
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.documents)
        lead_documents_page.add_document(document_type='W2')
        lead_documents_page.add_document(document_type='Bank Statements')
        lead_documents_page.add_document(document_type='Paycheck')
        assert lead_history_page.api_convert_lead_to_upfront_loan(
            token=get_token_leads,
            client_id=lead_id
        )
        title_text = f'    :star: *TEST UPFRONT LOAN: {state}* :star:'
        message_text = f'\n *CLIENT DATA*: ' \
                       f'```{convert_dict_to_string(credit_data_first_applicant)}\n```'\
                       f'\n :nyancat_big: <{lead_history_page.base_url+getattr(pages_details, leads_pages.leads_profile).ENDPOINT+lead_id}|*GO TO LEAD*> '
        slack_post_msg(
            token=os.environ['PERFORMANCE_BOT_TOKEN'],
            channel=os.environ['LEADS_PREPARATION_CHANNEL'],
            blocks=get_leads_text_blocks(title_text, message_text),
            icon_emoji=':smoking_stress:',
            username='Selenium'
        )

    title = 'Prepare Upfront lead with co-applicant for manual testing'

    @testit.displayName(title)
    @testit.externalId('leads prepare 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, state, role',
        [
            ('1', 'CA', roles.admin),
            ('2', 'NJ', roles.admin),
            ('3', '', roles.admin)
        ]
    )
    def test_upfront_loan_prepare_lead_co_applicant(
            self,
            ex_id: str,
            state: str,
            role: str,
            login,
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
            get_token_leads
    ) -> Any:
        """ Prepare Upfront lead co-applicant"""
        credit_data_first_applicant = TestData.credit_report_data_from_csv(state=state)
        credit_data_first_applicant['isValidityCheckRequired'] = True
        credit_data_co_applicant = TestData.credit_report_data_from_csv()
        lead_id = lead_create_page.create_lead_via_api(
            get_token_leads, **credit_data_first_applicant)
        login_page.login_with_cookies(
            role=roles.admin,
            page=leads_pages.leads_history,
            client_id=lead_id
        )
        lead_history_page.check_rejected_lead()
        login_page.login_with_cookies(
            role=role,
            page=leads_pages.leads_history,
            client_id=lead_id
        )
        lead_history_page.reassigning(
            sales_rep=login_page.cfg.auth[roles.sales_debt_consultant]['username'])
        lead_history_page.choose_leads_tabs(tab=leads_tabs.profile)
        lead_profile_page.added_co_applicant(
            first_name=credit_data_co_applicant['firstName'],
            last_name=credit_data_co_applicant['lastName'],
            zip_code=credit_data_co_applicant['zip'],
            address=credit_data_co_applicant['address'],
            city=credit_data_co_applicant['city'],
            dob=credit_data_co_applicant['dob'],
            ssn=credit_data_co_applicant['ssn'],
            state=credit_data_co_applicant['state']
        )
        lead_profile_page.get_credit_report_co_applicant(
            address=credit_data_co_applicant['address'], ssn=credit_data_co_applicant['ssn'])
        lead_budget_page.choose_leads_tabs(tab=leads_tabs.budget)
        lead_budget_page.fill_all_budget_data()
        lead_history_page.enabling_upfront()
        lead_income_page.choose_leads_tabs(tab=leads_tabs.income)
        lead_income_page.remove_all_income()
        count = lead_income_page.get_income_count()
        lead_income_page.add_upfront_new_income(count=count, case_co_applicant=True)
        lead_income_page.add_upfront_new_income_co_applicant(count=0)
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.ach)
        lead_ach_page.fill_ach_fields(ssn=credit_data_first_applicant['ssn'])
        lead_history_page.underwriting_and_confirmation()
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.documents)
        lead_documents_page.add_document(document_type='W2')
        lead_documents_page.add_document(document_type='Bank Statements')
        lead_documents_page.add_document(document_type='Paycheck')
        assert lead_history_page.api_convert_lead_to_upfront_loan(
            token=get_token_leads,
            client_id=lead_id
        )
        title_text = f'    :star: *TEST UPFRONT LOAN CO-APPLICANT: {state}* :star:'
        message_text = f'\n *CLIENT DATA*: ' \
                       f'```{convert_dict_to_string(credit_data_first_applicant)}\n```'\
                       f'\n\n *CO-APPLICANT DATA*: ' \
                       f'```{convert_dict_to_string(credit_data_co_applicant)}```' \
                       f'\n :nyancat_big: <{lead_history_page.base_url+getattr(pages_details, leads_pages.leads_profile).ENDPOINT+lead_id}|*GO TO LEAD*> '
        slack_post_msg(
            token=os.environ['PERFORMANCE_BOT_TOKEN'],
            channel=os.environ['LEADS_PREPARATION_CHANNEL'],
            blocks=get_leads_text_blocks(title_text, message_text),
            icon_emoji=':smoking_stress:',
            username='Selenium'
        )


class TestRamVerificationUpfrontLeadsPreparePage:

    title = 'Prepare RAM Upfront lead for manual testing'

    @testit.displayName(title)
    @testit.externalId('leads prepare 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, state, role',
        [
            ('1', 'CA', roles.sales_upfront_loan_processor),
            ('2', 'NJ', roles.sales_upfront_loan_processor),
            ('3', '', roles.sales_upfront_loan_processor),
        ]
    )
    def test_ram_upfront_leads_prepare_lead(
            self,
            ex_id: str,
            state: str,
            role: str,
            login,
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
            get_token_leads
    ) -> Any:
        """ Prepare Upfront lead """
        credit_data_first_applicant = TestData.credit_report_data_from_csv(state=state)
        credit_data_first_applicant['isValidityCheckRequired'] = True
        lead_id = lead_create_page.create_lead_via_api(
            get_token_leads, **credit_data_first_applicant)
        login_page.login_with_cookies(
            role=role,
            page=leads_pages.leads_history,
            client_id=lead_id
        )
        lead_history_page.check_rejected_lead()
        lead_history_page.reassigning(
            sales_rep=login_page.cfg.auth[roles.sales_debt_consultant]['username'])
        lead_income_page.choose_leads_tabs(tab=leads_tabs.income)
        lead_budget_page.choose_leads_tabs(tab=leads_tabs.budget)
        lead_budget_page.fill_all_budget_data()
        lead_history_page.enabling_upfront()
        lead_income_page.choose_leads_tabs(tab=leads_tabs.income)
        lead_income_page.remove_all_income()
        count = lead_income_page.get_income_count()
        lead_income_page.add_upfront_new_income(count=count)
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.ach)
        lead_ach_page.fill_ach_fields(ssn=TestData.ssn())
        lead_history_page.underwriting_and_confirmation()
        lead_underwriting_page.loc_processing_verification_kyc()
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.ach)
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.documents)
        lead_documents_page.add_document(document_type='W2')
        lead_documents_page.add_document(document_type='Bank Statements')
        lead_documents_page.add_document(document_type='Paycheck')
        title_text = f'    :star: *TEST RAM UPFRONT LOAN: {state}* :star:'
        message_text = f'\n *CLIENT DATA*: ' \
                       f'```{convert_dict_to_string(credit_data_first_applicant)}\n```'\
                       f'\n :nyancat_big: <{lead_history_page.base_url+getattr(pages_details, leads_pages.leads_profile).ENDPOINT+lead_id}|*GO TO LEAD*> '
        slack_post_msg(
            token=os.environ['PERFORMANCE_BOT_TOKEN'],
            channel=os.environ['LEADS_PREPARATION_CHANNEL'],
            blocks=get_leads_text_blocks(title_text, message_text),
            icon_emoji=':smoking_stress:',
            username='Selenium'
        )

    title = 'Prepare RAM Upfront lead with co-applicant for manual testing'

    @testit.displayName(title)
    @testit.externalId('leads prepare 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, state, role',
        [
            ('1', 'CA', roles.admin),
            ('2', 'NJ', roles.admin),
            ('3', '', roles.admin)
        ]
    )
    def test_ram_upfront_leads_prepare_lead_co_applicant(
            self,
            ex_id: str,
            state: str,
            role: str,
            login,
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
            get_token_leads
    ) -> Any:
        """ Prepare Upfront lead co-applicant"""
        credit_data_first_applicant = TestData.credit_report_data_from_csv(state=state)
        credit_data_first_applicant['isValidityCheckRequired'] = True
        credit_data_co_applicant = TestData.credit_report_data_from_csv()
        lead_id = lead_create_page.create_lead_via_api(
            get_token_leads, **credit_data_first_applicant)
        login_page.login_with_cookies(
            role=role,
            page=leads_pages.leads_history,
            client_id=lead_id
        )
        lead_history_page.check_rejected_lead()
        lead_history_page.reassigning(
            sales_rep=login_page.cfg.auth[roles.sales_debt_consultant]['username'])
        lead_history_page.choose_leads_tabs(tab=leads_tabs.profile)
        lead_profile_page.added_co_applicant(
            first_name=credit_data_co_applicant['firstName'],
            last_name=credit_data_co_applicant['lastName'],
            zip_code=credit_data_co_applicant['zip'],
            address=credit_data_co_applicant['address'],
            city=credit_data_co_applicant['city'],
            dob=credit_data_co_applicant['dob'],
            ssn=credit_data_co_applicant['ssn'],
            state=credit_data_co_applicant['state']
        )
        lead_profile_page.get_credit_report_co_applicant(
            address=credit_data_co_applicant['address'], ssn=credit_data_co_applicant['ssn'])
        lead_budget_page.choose_leads_tabs(tab=leads_tabs.budget)
        lead_budget_page.fill_all_budget_data()
        lead_history_page.enabling_upfront()
        lead_income_page.choose_leads_tabs(tab=leads_tabs.income)
        lead_income_page.remove_all_income()
        count = lead_income_page.get_income_count()
        lead_income_page.add_upfront_new_income(count=count, case_co_applicant=True)
        lead_income_page.add_upfront_new_income_co_applicant(count=0)
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.ach)
        lead_ach_page.fill_ach_fields(ssn=TestData.ssn())
        lead_history_page.underwriting_and_confirmation()
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.documents)
        lead_documents_page.add_document(document_type='W2')
        lead_documents_page.add_document(document_type='Bank Statements')
        lead_documents_page.add_document(document_type='Paycheck')
        lead_documents_page.add_document_co_applicant(
            document_type='SSN Verification Proof',
            applicant_name=credit_data_co_applicant["lastName"]
        )
        lead_documents_page.add_document_co_applicant(
            document_type='Address Verification Proof',
            applicant_name=credit_data_co_applicant["lastName"]
        )
        lead_documents_page.add_document_co_applicant(
            document_type='DOB Verification Proof',
            applicant_name=credit_data_co_applicant["lastName"]
        )
        lead_documents_page.add_document_co_applicant(
            document_type='Full Name Verification Proof',
            applicant_name=credit_data_co_applicant["lastName"]
        )
        lead_documents_page.add_document_co_applicant(
            document_type='OFAC Verification Proof',
            applicant_name=credit_data_co_applicant["lastName"]
        )
        lead_underwriting_page.loc_processing_verification_kyc()
        title_text = f'    :star: *TEST RAM UPFRONT LOAN CO-APPLICANT: {state}* :star:'
        message_text = f'\n *CLIENT DATA*: ' \
                       f'```{convert_dict_to_string(credit_data_first_applicant)}\n```'\
                       f'\n\n *CO-APPLICANT DATA*: ' \
                       f'```{convert_dict_to_string(credit_data_co_applicant)}```' \
                       f'\n :nyancat_big: <{lead_history_page.base_url+getattr(pages_details, leads_pages.leads_profile).ENDPOINT+lead_id}|*GO TO LEAD*> '
        slack_post_msg(
            token=os.environ['PERFORMANCE_BOT_TOKEN'],
            channel=os.environ['LEADS_PREPARATION_CHANNEL'],
            blocks=get_leads_text_blocks(title_text, message_text),
            icon_emoji=':smoking_stress:',
            username='Selenium'
        )
