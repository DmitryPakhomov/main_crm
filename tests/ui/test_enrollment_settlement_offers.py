import testit
import pytest
from typing import Any
from dotenv import load_dotenv
from autotests.pages.data.enrollments_data import enrollments_pages
from autotests.pages.data.main_data import roles
from autotests.pages.data.enrollments_data import enrollments_settlement_offer_statuses
from autotests.pages.queries import Customer as customer_queries


load_dotenv()


class TestEnrollmentsSettlementOffers:
    title = 'Checking creation offer [{role}]'
    @testit.displayName(title)
    @testit.externalId('settlement offer test 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, role, page',
        [
            ('1', roles.admin, enrollments_pages.enrollments_creditors)
        ]
    )
    def test_settlement_offer_create(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            enrollment_creditors_page
    ) -> Any:
        """ Checking creation offer - """
        enrollment_id = customer_queries.get_random_active_deal_id()
        login_page.login_with_cookies(page=page, client_id=enrollment_id)
        enrollment_creditors_page.click_btn_create_new_creditor()
        enrollment_creditors_page.fill_all_creditor_data()
        enrollment_creditors_page.select_creditors()
        enrollment_creditors_page.create_settlement_offer()
        enrollment_creditors_page.click_on_offer_again()
        enrollment_creditors_page.add_document_with_type_settlement_letter_to_offer()
        enrollment_creditors_page.check_settlement_offer()

    title = 'Checking offer statuses [{role}]'
    @testit.displayName(title)
    @testit.externalId('settlement offer test 2 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, role, page',
        [
            ('1', roles.admin, enrollments_pages.enrollments_creditors)
        ]
    )
    def test_creditor_offer_statuses(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            enrollment_creditors_page
    ) -> Any:
        """ Checking changing offer statuses - """
        enrollment_id = customer_queries.get_random_active_deal_id()
        login_page.login_with_cookies(page=page, client_id=enrollment_id)
        enrollment_creditors_page.click_btn_create_new_creditor()
        enrollment_creditors_page.fill_all_creditor_data()
        enrollment_creditors_page.select_creditors()
        enrollment_creditors_page.create_settlement_offer()
        enrollment_creditors_page.click_on_offer_again()
        enrollment_creditors_page.add_document_with_type_settlement_letter_to_offer()
        enrollment_creditors_page.change_status_offer(
            enrollments_settlement_offer_statuses.cancelled)
        enrollment_creditors_page.check_cancelled_offer()
        enrollment_creditors_page.change_status_offer(
            enrollments_settlement_offer_statuses.need_sif_letter)
        enrollment_creditors_page.check_status_need_sif_letter_offer()
        enrollment_creditors_page.change_status_offer(
            enrollments_settlement_offer_statuses.need_client_auth)
        enrollment_creditors_page.check_status_need_cl_auth_offer()
        enrollment_creditors_page.change_status_offer(
            enrollments_settlement_offer_statuses.need_acceptance)
        enrollment_creditors_page.check_need_acceptance_state()
        enrollment_creditors_page.click_on_offer_again()
        enrollment_creditors_page.accepting_settlement_offer()
        enrollment_creditors_page.check_status_accepted_offer()
        enrollment_creditors_page.click_on_offer_again()
        enrollment_creditors_page.turn_off_acceptance_state()

    title = 'Checking offer delete [{role}]'
    @testit.displayName(title)
    @testit.externalId('settlement offer test 3 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, role, page',
        [
            ('1', roles.admin, enrollments_pages.enrollments_creditors)
        ]
    )
    def test_settlement_offer_delete(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            enrollment_creditors_page,
            enrollment_payments_page
    ) -> Any:
        """ Checking deleting offer status - """
        enrollment_id = customer_queries.get_random_active_deal_id()
        login_page.login_with_cookies(page=page, client_id=enrollment_id)
        enrollment_creditors_page.click_btn_create_new_creditor()
        creditor = enrollment_creditors_page.fill_all_creditor_data().current_creditor_data
        creditor_account = creditor.current_account
        enrollment_creditors_page.select_creditors()
        enrollment_creditors_page.create_settlement_offer()
        enrollment_creditors_page.click_on_offer_again()
        enrollment_creditors_page.add_document_with_type_settlement_letter_to_offer()
        enrollment_creditors_page.click_on_offer_again()
        enrollment_creditors_page.accepting_settlement_offer()
        enrollment_creditors_page.delete_settlement_offer()
        enrollment_creditors_page.check_offer_in_deleted_status()
        enrollment_creditors_page.open_page(
            page=enrollments_pages.enrollments_drafts, client_id=enrollment_id)
        enrollment_payments_page.check_voided_creditors_payments(creditor_account=creditor_account)


    # title = 'Checking settlement letter due date in accepted offer [{role}]'
    # @testit.displayName(title)
    # @testit.externalId('settlement offer test 5 case {ex_id}')
    # @testit.title(title)
    # @pytest.mark.parametrize(
    #     'ex_id, role, page',
    #     [
    #         ('1', roles.admin, enrollments_pages.enrollments_creditors)
    #     ]
    # )
    # def test_settlement_offer_settlement_letter_due_in_status_accepted_old(
    #         self,
    #         ex_id: str,
    #         role: str,
    #         page: str,
    #         login_page,
    #         enrollment_creditors_page
    # ) -> Any:
    #     """ Checking settlement letter due in accepted offer - """  # TODO check valid case
    #     enrollment_id = customer_queries.get_random_active_deal_id()
    #     settlement_due = TestData.get_date(+14)
    #     login_page.login_with_cookies(page=page, client_id=enrollment_id)
    #     enrollment_creditors_page.click_btn_create_new_creditor()
    #     enrollment_creditors_page.fill_all_creditor_data()
    #     enrollment_creditors_page.select_creditors()
    #     enrollment_creditors_page.create_settlement_offer()
    #     enrollment_creditors_page.click_tab_settlement_offers_creditor()
    #     enrollment_creditors_page.click_on_offer_again()
    #     enrollment_creditors_page.add_document_with_type_settlement_letter_to_offer()
    #     # Checking that upload document change settlement letter due date + 14 days:
    #     enrollment_creditors_page.click_on_offer_again()
    #     enrollment_creditors_page.check_settlement_letter_due_in_offer(settlement_due)


    title = 'Checking no possibility to create settlement offer if ' \
            'previous offer is currently active [{role}]'
    @testit.displayName(title)
    @testit.externalId('settlement offer test 7 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, role, page',
        [
            ('1', roles.admin, enrollments_pages.enrollments_creditors)
        ]
    )
    def test_settlement_offer_no_possibility_create_second_offer(
            self,
            ex_id: str,
            role: str,
            page: str,
            login_page,
            enrollment_creditors_page
    ) -> Any:
        """ Checking no possibility create second offer - """
        enrollment_id = customer_queries.get_random_active_deal_id()
        login_page.login_with_cookies(page=page, client_id=enrollment_id)
        enrollment_creditors_page.click_btn_create_new_creditor()
        enrollment_creditors_page.fill_all_creditor_data()
        enrollment_creditors_page.select_creditors()
        enrollment_creditors_page.create_settlement_offer()
        enrollment_creditors_page.checking_offer_create_error_if_previous_offer_active()
