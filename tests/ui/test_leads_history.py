import pytest
import testit
from typing import Any
from dotenv import load_dotenv
from autotests.pages.data.test_data import TestData
from autotests.pages.data.leads_data import leads_pages
from autotests.pages.data.main_data import roles


load_dotenv()


class TestLeadHistoryPage:
    title = 'Checking the history Note event of the Leads page with role [{role}]'
    @testit.displayName(title)
    @testit.externalId('history test 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page', [('1', roles.admin, leads_pages.leads_history)])
    def test_lead_history_page_note(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            lead_create_page,
            lead_history_page,
            get_token_leads
    ) -> Any:
        """ Checking history note saving - """
        note_text = TestData.words()
        lead_id = lead_create_page.create_lead_via_api(get_token_leads)
        login_page.login_with_cookies(page=page, client_id=lead_id)
        lead_history_page.creating_new_note(note_text=note_text)
        lead_history_page.check_history_event_create_note(note_text=note_text)

    title = 'Checking history Note event of the Leads page with role [{role}]'
    @testit.displayName(title)
    @testit.externalId('history test 2 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page',[('1', roles.admin, leads_pages.leads_history)])
    def test_lead_history_page_email(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            lead_create_page,
            lead_history_page,
            get_token_leads
    ) -> Any:
        """ Checking history email saving - """
        email_text = TestData.words()
        email_subject = TestData.words()
        lead_id = lead_create_page.create_lead_via_api(get_token_leads)
        login_page.login_with_cookies(page=page, client_id=lead_id)
        lead_history_page.creating_new_email(
            email_text=email_text, subject_text=email_subject, attachments=False)
        lead_history_page.check_history_event_create_email(
            email_text=email_text,
            subject_text=email_subject,
            attachments=None
        )

    title = 'Checking history Task event of the Leads page with role [{role}]'
    @testit.displayName(title)
    @testit.externalId('history test 3 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page', [('1', roles.admin, leads_pages.leads_history)])
    def test_lead_history_page_task(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            lead_create_page,
            lead_history_page,
            lead_creditors_page,
            get_token_leads
    ) -> Any:
        """ Checking history task saving - """
        title_text = TestData.words()
        description_text = TestData.words()
        lead_id = lead_create_page.create_lead_via_api(get_token_leads)
        login_page.login_with_cookies(page=leads_pages.leads_creditors, client_id=lead_id)
        lead_creditors_page.add_new_creditor(
            creditor='American Express',
            balance='10000',
            account_holder='Applicant',
            account='12345678',
            debt_type='Credit Card',
        )
        login_page.open_page(page=page, client_id=lead_id)
        lead_history_page.creating_new_task(title_text=title_text, description_text=description_text)
        lead_history_page.check_history_event_create_task(title_text=title_text)

    title = 'Checking history Note by Tab event of the Leads page with role [{role}]'
    @testit.displayName(title)
    @testit.externalId('history test 4 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page', [('1', roles.admin, leads_pages.leads_history)])
    def test_lead_history_page_tab_form_note(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            lead_create_page,
            lead_history_page,
            get_token_leads
    ) -> Any:
        """ Checking history tab note saving - """
        note_text = TestData.words()
        lead_id = lead_create_page.create_lead_via_api(get_token_leads)
        login_page.login_with_cookies(page=page, client_id=lead_id)
        lead_history_page.creating_note_by_tab_form(note_text=note_text)
        lead_history_page.check_history_event_create_note(note_text=note_text)

    title = 'Checking history Email by Tab event of the Leads page with role [{role}]'
    @testit.displayName(title)
    @testit.externalId('history test 5 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page', [('1', roles.admin, leads_pages.leads_history)])
    def test_lead_history_page_tab_form_email(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            lead_create_page,
            lead_history_page,
            get_token_leads
    ) -> Any:
        """ Checking history tab email saving - """
        email_text = TestData.words()
        email_subject = TestData.words()
        lead_id = lead_create_page.create_lead_via_api(get_token_leads)
        login_page.login_with_cookies(page=page, client_id=lead_id)
        lead_history_page.creating_email_by_tab_form(
            email_text=email_text, subject_text=email_subject)
        lead_history_page.check_history_event_create_email(
            email_text=email_text,
            subject_text=email_subject,
            attachments=None
        )

    title = 'Checking history Reassign event of the Leads page with role [{role}]'
    @testit.displayName(title)
    @testit.externalId('history test 6 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page', [('1', roles.admin, leads_pages.leads_history)])
    def test_lead_history_page_reassign(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            lead_create_page,
            lead_history_page,
            get_token_leads
    ) -> Any:
        """ Checking history reassign - """
        sales_rep = TestData.sales_rep()
        lead_id = lead_create_page.create_lead_via_api(get_token_leads)
        login_page.login_with_cookies(page=page, client_id=lead_id)
        lead_history_page.reassign_lead(sales_rep=sales_rep)
        lead_history_page.check_history_event_reassigning(sales_rep=sales_rep)
