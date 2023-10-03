import pytest
import testit
from typing import Any
from dotenv import load_dotenv
from autotests.pages.data.enrollments_data import enrollments_pages
from autotests.pages.data.test_data import TestData
from autotests.pages.data.main_data import roles
from autotests.pages.queries import Customer as customer_queries


load_dotenv()


class TestEnrollmentHistoryPage:
    title = 'Checking history Email event of the Enrollments page with role [{role}]'
    @testit.displayName(title)
    @testit.externalId('enrollment communication test 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page',
                             [('1', roles.admin, enrollments_pages.enrollments_main)])
    def test_enrollment_check_send_email(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            enrollment_main_page
    ) -> Any:
        """ Checking history email saving - """
        email_text = TestData.words()
        email_subject = TestData.words()
        file_name = 'file_example.jpg'
        enrollment_id = customer_queries.get_random_active_deal_id()
        login_page.login_with_cookies(page=page, client_id=enrollment_id)
        enrollment_main_page.creating_new_email(
            email_text=email_text,
            subject_text=email_subject,
            attachments=False
        )
        enrollment_main_page.check_history_event_create_email(
            email_text=email_text,
            subject_text=email_subject,
            attachments=None
        )
        enrollment_main_page.refresh_page()
        enrollment_main_page.creating_new_email(
            email_text=email_text,
            subject_text=email_subject,
            attachments=True
        )
        enrollment_main_page.check_history_event_create_email(
            email_text=email_text,
            subject_text=email_subject,
            attachments=file_name
        )


    title = 'Check send e-docs fpr LOC'
    @testit.displayName(title)
    @testit.externalId('enrollment communication test 2 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, state, role, email_text, page',
        [
            ('1', 'CA', 'admin', 'signature request', enrollments_pages.enrollments_main)
        ]
    )
    def test_enrollment_send_e_docs(
            self,
            ex_id: str,
            state: str,
            role: str,
            page: str,
            email_text: str,
            login,
            login_page,
            enrollment_main_page
    ) -> Any:
        """ Checking send docs Pre-Enrollment - """
        user_data = customer_queries.get_data_random_deal_not_crb_not_loan_pro()
        client_id = str(user_data[0])
        email_subject = (f"document signature request for {user_data[1]} {user_data[2]}").lower()
        login_page.login_with_cookies(page=page, client_id=client_id)
        enrollment_main_page.click_send_documents()
        enrollment_main_page.refresh_page()
        enrollment_main_page.check_history_event_create_email(
             email_text=email_text,
             subject_text=email_subject,
             attachments=None,
        )
