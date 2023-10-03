import pytest
import testit
import random
from typing import Any
from dotenv import load_dotenv
from autotests.pages.data.leads_data import leads_pages, leads_tabs, leads_account_type
from autotests.pages.data.test_data import TestData
from autotests.pages.data.main_data import roles, send_docs


load_dotenv()


class TestLeadHistoryPage:
    title = 'Checking sending SMS Consent [{company}][{lang}][{role}]'
    @testit.displayName(title)
    @testit.externalId('communication test 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, role, company, lang',
        [
            ('1', 'admin', 'credit9', 'eng'),
            ('2', 'admin', 'credit9', 'esp'),
            ('3', 'admin', 'americor', 'eng'),
            ('4', 'admin', 'americor', 'esp')
        ]
    )
    def test_sms_consent(
            self,
            ex_id: str,
            role: str,
            company: str,
            lang: str,
            login_page,
            lead_create_page,
            lead_history_page,
            lead_profile_page,
            get_token_leads
    ) -> Any:
        """ Sending and checking SMS - """
        mob_phone = TestData.phone_for_sms_consent()
        lead_id = lead_create_page.create_lead_via_api(
            get_token_leads, company=company, phoneMobile=mob_phone)
        login_page.login_with_cookies(page=leads_pages.leads_history, client_id=lead_id)
        lead_profile_page.check_rejected_lead()
        if lang == 'esp':
            lead_profile_page.choose_leads_tabs(tab=leads_tabs.profile)
            lead_profile_page.click_change_spanish_speaker()
            lead_profile_page.choose_leads_tabs(tab=leads_tabs.history)
        lead_history_page.click_sms_consent()
        lead_history_page.confirmation()
        lead_history_page.success_or_error_check()
        lead_history_page.refresh_page()
        lead_history_page.check_sms_text(mob_phone=mob_phone, lang=lang, company=company)

    title = 'Checking history Email event of the Leads page with role [{role}]'
    @testit.displayName(title)
    @testit.externalId('communication test 2 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page', [('1', roles.admin, leads_pages.leads_history)])
    def test_lead_check_send_email(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            lead_create_page,
            lead_history_page,
            lead_profile_page,
            loan_history_page,
            get_token_leads
    ) -> Any:
        """ Checking history email saving - """
        email_text = TestData.words()
        email_subject = TestData.words()
        file_name = 'file_example.jpg'
        mob_phone = TestData.phone_for_sms_consent()
        phone_home = TestData.phone_for_sms_consent()
        lead_id = lead_create_page.create_lead_via_api(
            get_token_leads, mob_phone=mob_phone, phone_home=phone_home)
        login_page.login_with_cookies(page=page, client_id=lead_id)
        lead_profile_page.check_rejected_lead()
        lead_history_page.creating_new_email(
            email_text=email_text,
            subject_text=email_subject,
            attachments=False
        )
        lead_history_page.check_history_event_create_email(
            email_text=email_text,
            subject_text=email_subject,
            attachments=None
        )
        lead_history_page.refresh_page()
        lead_history_page.creating_new_email(
            email_text=email_text,
            subject_text=email_subject,
            attachments=True
        )
        lead_history_page.check_history_event_create_email(
            email_text=email_text,
            subject_text=email_subject,
            attachments=file_name
        )

    title = 'Check send choice offer via Email'
    @testit.displayName(title)
    @testit.externalId('communication test 3 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page', [('1', 'admin', leads_pages.leads_history)])
    def test_lead_choice_offer_via_email(
            self,
            ex_id: str,
            role: str,
            page: str,
            login,
            lead_history_page,
            lead_create_page,
            login_page,
            lead_income_page,
            lead_profile_page,
            get_token_leads
    ) -> Any:
        """ Send choice offer via Email - """
        email_text = 'please click on the link below to see all ' \
                     'available offers you pre-qualify for.'
        email_subject = 'consolidation offers'
        state = 'CA'
        credit_data: dict = TestData.credit_report_data_for_api(state=state)
        credit_data['mob_phone'] = TestData.phone()
        credit_data['phone_home'] = TestData.phone()
        lead_id = lead_create_page.create_lead_via_api(get_token_leads, **credit_data)
        login_page.login_with_cookies(page=page, client_id=lead_id)
        lead_profile_page.check_rejected_lead()
        lead_income_page.choose_leads_tabs(tab=leads_tabs.income)
        lead_income_page.remove_all_income()
        count = lead_income_page.get_income_count()
        lead_income_page.add_new_income(count=count)
        lead_history_page.creating_new_send_choice_via_email()
        lead_income_page.choose_leads_tabs(tab=leads_tabs.history)
        lead_history_page.check_history_event_create_email(
            email_text=email_text,
            subject_text=email_subject,
            attachments=None,
            body_text=True
        )

    title = 'Check send financial profile'
    @testit.displayName(title)
    @testit.externalId('communication test 4 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page', [('1', 'admin', leads_pages.leads_history)])
    def test_lead_send_financial_profile(
            self,
            ex_id: str,
            role: str,
            page: str,
            login,
            lead_history_page,
            lead_create_page,
            login_page,
            get_token_leads
    ) -> Any:
        """ Send financial profile via Email - """
        email_text = 'hello paul burnia,\n\nwelcome to americor! below you will find a link that will provide ' \
                     'pertinent information specific to you. first, you will be able to ' \
                     'review your current financial situation in order to get a better ' \
                     'understanding of where you stand. after that, you will be able to ' \
                     'review your options and make an educated decision on what is best for ' \
                     'your financial future.\n\nlet’s get started!\n\nclick here'
        email_subject = 'financial profile'
        state = 'CA'
        credit_data: dict = TestData.credit_report_data_for_api(state=state)
        credit_data['mob_phone'] = TestData.phone()
        credit_data['phone_home'] = TestData.phone()
        credit_data['isValidityCheckRequired'] = True
        lead_id = lead_create_page.create_lead_via_api(get_token_leads, **credit_data)
        login_page.login_with_cookies(page=page, client_id=lead_id)
        lead_history_page.choose_leads_tabs(tab=leads_tabs.profile)
        lead_history_page.set_callback_date()
        lead_history_page.change_lead_status('Ready to Pitch')
        lead_history_page.refresh_page()
        lead_history_page.choose_leads_tabs(tab=leads_tabs.history)
        lead_history_page.get_popup_email_financial_profile()
        lead_history_page.send_financial_profile_email()
        lead_history_page.refresh_page()

        lead_history_page.check_history_event_create_email(
            email_text=email_text,
            subject_text=email_subject,
            attachments=None,
            body_text=True
        )

    title = 'Check send pre-enrollment, agreement only email and agreement to sign and save on files'
    @testit.displayName(title)
    @testit.externalId('communication test 5 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, state, role, case, email_subject, email_text, page',
        [
            ('1', 'CA', 'admin', 'agreement_only', 'document signature request for paul burnia',
             'signature request', leads_pages.leads_history),
            # ('2', 'CA', 'admin', 'pre-enrollment', 'pre-enrollment', 'hi paul',
            #  leads_pages.leads_history),
            # ('3', 'CA', 'admin', 'agreement_to_sign_and_save_on_files',
            #  'document signature request for paul burnia', 'signature request',
            #  leads_pages.leads_history)
        ]
    )
    def test_lead_send_pre_enrollment_agreement(
            self,
            ex_id: str,
            state: str,
            role: str,
            case: str,
            page: str,
            email_subject: str,
            email_text: str,
            login,
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
        """ Checking send docs Pre-Enrollment - """
        sales_rep = TestData.sales_rep(all_sales_rep=True)[1]
        state = 'CA'
        credit_data: dict = TestData.credit_report_data_for_api(state=state)
        credit_data['mob_phone'] = TestData.phone()
        credit_data['phone_home'] = TestData.phone()
        credit_data['isValidityCheckRequired'] = True
        lead_id = lead_create_page.create_lead_via_api(get_token_leads, **credit_data)
        login_page.login_with_cookies(page=page, client_id=lead_id)
        lead_history_page.reassigning(sales_rep=sales_rep)
        lead_history_page.check_sales_rep_quick_stats(sales_rep=sales_rep)
        lead_history_page.choose_leads_tabs(tab=leads_tabs.profile)
        lead_income_page.choose_leads_tabs(tab=leads_tabs.income)
        lead_income_page.remove_all_income()
        count = lead_income_page.get_income_count()
        lead_income_page.add_new_income(count=count)
        lead_budget_page.choose_leads_tabs(tab=leads_tabs.budget)
        lead_budget_page.fill_all_budget_data()
        lead_calculator_page.choose_leads_tabs(tab=leads_tabs.calculator)
        lead_calculator_page.calculator(number_of_months=20)
        lead_ach_page.choose_leads_tabs(tab=leads_tabs.ach)
        lead_ach_page.fill_ach_fields(
            routing_number=TestData.routing_number(),
            account_number=random.randint(10000000, 1000000000),
            account_type=leads_account_type.checking,
            ssn='666-39-0401',
            dob='01/26/1961',
            mother_name=TestData.last_name(gender='female')
        )
        sending_type = ''
        match case:
            case 'agreement_only':
                sending_type = send_docs.agreement_only
            case 'pre-enrollment':
                sending_type = send_docs.pre_enrollment
            case 'agreement_to_sign_and_save_on_files':
                sending_type = send_docs.agreement_to_sign_and_save_file
        lead_history_page.sending_docs(sending_type=sending_type)
        lead_history_page.refresh_page()
        lead_calculator_page.choose_leads_tabs(tab=leads_tabs.history)
        lead_history_page.check_history_event_create_email(
            email_text=email_text,
            subject_text=email_subject,
            attachments=None,
        )
