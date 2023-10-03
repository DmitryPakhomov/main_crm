import random

import pytest
import testit
from typing import Any
from dotenv import load_dotenv
from autotests.pages.data.test_data import TestData
from autotests.pages.data.enrollments_data import enrollments_pages, enrollments_history_events
from autotests.pages.data.main_data import roles
from autotests.pages.queries import Customer as customer_queries


load_dotenv()


class TestEnrollmentHistoryPage:

    title = 'Checking change status event of the Enrollment page with role [{role}]'
    @testit.displayName(title)
    @testit.externalId('history test 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, role, page, history_event_type',
        [
            (
                    '1',
                    roles.admin,
                    enrollments_pages.enrollments_main,
                    enrollments_history_events.lead_to_enrollment_event,
            ),
            (
                    '2',
                    roles.admin,
                    enrollments_pages.enrollments_main,
                    enrollments_history_events.docs_signed_event,
            )
        ]
    )
    def test_enrollment_change_status(
            self,
            ex_id: str,
            role: str,
            page: str,
            history_event_type: str,
            login_page,
            enrollment_main_page,
            get_token_leads
    ) -> Any:
        """ Checking events text in history - """
        enrollment_id = str(random.choice(customer_queries.get_random_new_active_deal_id())[0])
        login_page.login_with_cookies(page=page, client_id=enrollment_id)
        enrollment_main_page.check_history_event_change_status(
            history_event_type=history_event_type,
            )

    title = 'Checking history Note event of the Enrollment page with role [{role}]'
    @testit.displayName(title)
    @testit.externalId('history test 2 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page', [('1', roles.admin, enrollments_pages.enrollments_main)])
    def test_enrollment_history_page_email(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            enrollment_main_page,
            get_token_leads
    ) -> Any:
        """ Checking history email saving - """
        email_text = TestData.words()
        email_subject = TestData.words()
        enrollment_id = str(random.choice(customer_queries.get_random_new_active_deal_id_old())[0])
        login_page.login_with_cookies(page=page, client_id=enrollment_id)
        enrollment_main_page.creating_new_email(
            email_text=email_text, subject_text=email_subject, attachments=False)
        enrollment_main_page.check_history_event_create_email(
            email_text=email_text,
            subject_text=email_subject,
            attachments=None
        )

    title = 'Checking history Task event of the Enrollment page with role [{role}]'
    @testit.displayName(title)
    @testit.externalId('history test 3 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page',
                             [('1', roles.admin, enrollments_pages.enrollments_main)])
    def test_enrollment_history_page_task(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            enrollment_main_page,
            lead_creditors_page,
            get_token_leads
    ) -> Any:
        """ Checking history task saving - """
        title_text = TestData.words()
        description_text = TestData.words()
        enrollment_id = str(random.choice(customer_queries.get_random_new_active_deal_id_old())[0])
        login_page.login_with_cookies(page=page, client_id=enrollment_id)
        enrollment_main_page.creating_new_task(title_text=title_text, description_text=description_text)
        enrollment_main_page.check_history_event_create_task(title_text=title_text)


    title = 'Checking history Email by Tab event of the Enrollment page with role [{role}]'
    @testit.displayName(title)
    @testit.externalId('history test 4 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page', [('1', roles.admin, enrollments_pages.enrollments_main)])
    def test_enrollment_history_page_tab_form_email(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            enrollment_main_page,
            get_token_leads
    ) -> Any:
        """ Checking history tab email saving - """
        email_text = TestData.words()
        email_subject = TestData.words()
        enrollment_id = str(random.choice(customer_queries.get_random_new_active_deal_id_old())[0])
        login_page.login_with_cookies(page=page, client_id=enrollment_id)
        enrollment_main_page.creating_email_by_tab_form(
            email_text=email_text, subject_text=email_subject)
        enrollment_main_page.check_history_event_create_email(
            email_text=email_text,
            subject_text=email_subject,
            attachments=None
        )

    title = 'Checking history Reassign event of the Enrollment page with role [{role}]'
    @testit.displayName(title)
    @testit.externalId('history test 5 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page', [('1', roles.admin, enrollments_pages.enrollments_main)])
    def test_enrollment_history_page_reassign(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            enrollment_main_page,
            lead_history_page,
            get_token_leads
    ) -> Any:
        """ Checking history reassign - """
        sales_rep = TestData.sales_rep()
        enrollment_id = str(random.choice(customer_queries.get_random_new_active_deal_id_old())[0])
        login_page.login_with_cookies(page=page, client_id=enrollment_id)
        enrollment_main_page.reassigning_enrollment(sales_rep=sales_rep)
        enrollment_main_page.check_history_event_reassigning(sales_rep=sales_rep)
