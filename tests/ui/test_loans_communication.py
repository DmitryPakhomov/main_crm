import pytest
import testit
from typing import Any
from dotenv import load_dotenv
from autotests.pages.data.loans_data import loans_pages
from autotests.pages.data.test_data import TestData
from autotests.pages.data.main_data import roles
from autotests.pages.queries import Customer as customer_queries


load_dotenv()


class TestLoansHistoryPage:
    title = 'Checking history Email event of the loans page with role [{role}]'
    @testit.displayName(title)
    @testit.externalId('loans communication test 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, page',
                             [('1', roles.admin, loans_pages.loans_history)])
    def test_loans_check_send_email(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            loan_history_page
    ) -> Any:
        """ Checking history email saving - """
        email_text = TestData.words()
        email_subject = TestData.words()
        file_name = 'file_example.jpg'
        user_data = customer_queries.get_random_any_data_of_one_applicant(user_type='loan')
        client_id = str(user_data[0])
        login_page.login_with_cookies(page=page, client_id=client_id)
        loan_history_page.creating_new_email(
            email_text=email_text,
            subject_text=email_subject,
            attachments=False
        )
        loan_history_page.check_history_event_create_email(
            email_text=email_text,
            subject_text=email_subject,
            attachments=None
        )
        loan_history_page.refresh_page()
        loan_history_page.creating_new_email(
            email_text=email_text,
            subject_text=email_subject,
            attachments=True
        )
        loan_history_page.check_history_event_create_email(
            email_text=email_text,
            subject_text=email_subject,
            attachments=file_name
        )



    title = 'Check send e-docs'
    @testit.displayName(title)
    @testit.externalId('enrollment communication test 2 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, role, doc_type, content, page',
        [
            ('1', 'admin', 'Amortization Schedule', 'amortization schedule', loans_pages.loans_history),
            ('2', 'admin', 'Payoff Statement PDF', 'payoff statement pdf',  loans_pages.loans_history)
        ]
    )
    def test_loan_send_e_docs(
            self,
            ex_id: str,
            role: str,
            page: str,
            doc_type: str,
            content: str,
            login,
            login_page,
            loan_history_page
    ) -> Any:
        """ Checking send docs - """
        user_data = customer_queries.get_random_any_data_of_one_applicant(user_type='loan',
                                                                          loan_pro=False)
        client_id = str(user_data[0])
        email_subject = ("Document uploaded").lower()
        login_page.login_with_cookies(page=page, client_id=client_id)
        loan_history_page.click_loan_send_documents(doc_type=doc_type)
        loan_history_page.refresh_page()
        loan_history_page.check_history_event_download_document(text=content,
                                                                subject_text=email_subject)
