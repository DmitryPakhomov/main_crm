import pytest
import testit
from typing import Any
from datetime import datetime
from dotenv import load_dotenv
from autotests.pages.data.main_data import roles
from autotests.pages.data.enrollments_data import enrollments_pages, enrollments_tabs
from autotests.pages.queries import Customer as customer_queries

load_dotenv()


class TestEnrollmentsPage:
    title = 'Checking the console logs of the Enrollments page for errors with role [{role}]'

    @testit.displayName(title)
    @testit.externalId('enrollments test 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role', [('1', 'admin')])
    def test_enrollments_pages_console_log(
            self,
            ex_id: str,
            role: str,
            config,
            login,
            login_page
    ) -> Any:
        """ Checking the console logs of the Enrollments page for errors - """
        pages = [
            enrollments_pages.enrollments,
            enrollments_pages.enrollments_main,
            enrollments_pages.enrollments_creditors,
            enrollments_pages.enrollments_drafts,
            enrollments_pages.enrollments_plan,
            enrollments_pages.enrollments_profile,
            enrollments_pages.enrollments_income,
            enrollments_pages.enrollments_budget,
            enrollments_pages.enrollments_strategy,
            enrollments_pages.enrollments_ach,
            enrollments_pages.enrollments_document,
            enrollments_pages.enrollments_tasks,
            enrollments_pages.enrollments_logs
        ]
        client_id = config.ui_data['enrollments']['client']
        login_page.check_page_console_log_errors(pages=pages, client_id=client_id)

    # title = 'EnrollmentsPage: Checking the transition Enrollment to Loan with role [{role}]'
    # @testit.displayName(title)
    # @testit.externalId('enrollment_budget_page_{ex_id}')
    # @testit.title(title)
    # @pytest.mark.parametrize('ex_id, role', [('1', 'admin')])
    # def test_enrollment_to_loan_old(
    #         self,
    #         ex_id: str,
    #         role: str
    # ) -> Any:
    #     """ Checking the transition Enrollment to Loan - """
    #     login_page = LoginPageBlocks(self.driver, self.cfg)
    #     enrollments_page = EnrollmentsCommonPageBlocks(self.driver, self.cfg)
    #     enrollments_page_income = EnrollmentIncomePageBlocks(self.driver, self.cfg)
    #     enrollments_page_main = EnrollmentMainPageCommonActions(self.driver, self.cfg)
    #
    #     login_page.login_by_password(role=role)
    #     deal_id = enrollments_page.read_id_and_check_history()
    #     sales_list = TestData.sales_rep(all_sales_rep=True)
    #     # enrollments_page.reassigning_enrollments(
    #     #     deal_id=deal_id, sales_rep=sales_list[1], underwriter=sales_list[1], loc=sales_list[1])
    #     enrollments_page.crb_and_loanpro_off()
    #     enrollments_page.check_exception_loan()
    #     enrollments_page.click_send_documents()
    #     enrollments_page.signing_docs()
    #     enrollments_page.click_override_qualify()
    #     enrollments_page_income.choose_leads_tabs(tab=enrollments_tabs.income)
    #     enrollments_page_income.remove_all_income()
    #     enrollments_page_income.add_new_income(
    #         status_income=enrollments_income_statuses.full_time_employed,
    #         occupation=enrollments_occupation.accountant,
    #         length_years=str(random.randint(1, 3)),
    #         length_months=str(random.randint(1, 11)),
    #         company_name=TestData.words(),
    #         phone_work=TestData.phone(mask='(###) ###-####'),
    #         net_monthly_income=str(random.randint(10000, 20000)),
    #         additional_phone_work=TestData.phone(mask='(###) ###-####'),
    #         gross_monthly_income=str(random.randint(10000, 20000)),
    #         w2income=str(random.randint(1000, 2000)),
    #         type_of_pay=enrollments_type_of_pays.monthly,
    #         how_to_calculate=enrollments_how_to_calculate.base,
    #         bank_statements_review=enrollments_bank_statements_review.a_borrower_has_direct_deposits
    #     )
    #     #enrollments_page_income.adding_income_from_deal(deal_id=deal_id)
    #     enrollments_page.click_underwriting()
    #     enrollments_page.change_status(deal_id)
    #     enrollments_page.upload_documents_kyc(deal_id)
    #     enrollments_page.click_approved(deal_id)
    #     enrollments_page.send_pre_load_docs(deal_id)
    #     enrollments_page.signing_docs()
    #     enrollments_page.click_ready_for_funding(deal_id)
    #     enrollments_page.send_final_load_docs(deal_id)
    #     enrollments_page.check_docusign_agreements_deal(lead_id=deal_id, url='https://mail.tm')

    title = 'Checking all budget data [{role}]'

    @testit.displayName(title)
    @testit.externalId('enrollments test 2 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role', [('1', roles.admin)])
    def test_enrollment_budget_page_data(
            self,
            ex_id: str,
            role: str,
            login_page,
            enrollment_budget_page
    ) -> Any:
        """ Check all budget data - """
        enrollment_id = customer_queries.get_random_active_deal_id()
        login_page.login_with_cookies(
            page=enrollments_pages.enrollments_budget,
            client_id=enrollment_id
        )
        all_expected_data = enrollment_budget_page.fill_all_budget_data()
        enrollment_budget_page.check_all_budget_data(all_expected_data=all_expected_data)

    title = 'Checking all creditors data [{role}]'

    @testit.displayName(title)
    @testit.externalId('enrollments test 3 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role', [('3', roles.admin)])
    def test_enrollment_creditors_page_data(
            self,
            ex_id: str,
            role: str,
            login_page,
            enrollment_creditors_page
    ) -> Any:
        """ Creating and deleting creditors - """
        enrollment_id = customer_queries.get_random_active_deal_id()
        login_page.login_with_cookies(
            page=enrollments_pages.enrollments_creditors,
            client_id=enrollment_id
        )
        enrollment_creditors_page.check_js_errors()
        enrollment_creditors_page.click_btn_create_new_creditor()
        all_expected_data = enrollment_creditors_page.fill_all_creditor_data()
        enrollment_creditors_page.select_creditors()
        enrollment_creditors_page.check_all_creditors_data(all_expected_data=all_expected_data)

    title = 'Checking create income for deals with role [{role}]'

    @testit.displayName(title)
    @testit.externalId('enrollments test 4 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role', [('1', 'admin')])
    def test_create_income_for_deals(
            self,
            ex_id: str,
            role: str,
            login_page,
            enrollment_income_page
    ) -> Any:
        """ Creating income from deals - """
        with testit.step('Test added income for deals'):
            enrollment_id = customer_queries.get_random_active_deal_id()
            login_page.login_with_cookies(
                page=enrollments_pages.enrollments_income,
                client_id=enrollment_id
            )
            count = enrollment_income_page.get_income_count()
            enrollment_income_page.check_unlock_status()
            enrollment_income_page.clean_income_fields(count)
            all_expected_data = enrollment_income_page.fill_all_income_data()
            enrollment_income_page.check_income(excepted_income_data=all_expected_data)

    title = 'Checking accept offer with role [{role}]'

    @testit.displayName(title)
    @testit.externalId('enrollments test 5 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role', [('1', 'admin')])
    def test_creditor_offer_statuses_old(
            self,
            ex_id: str,
            role: str,
            login_page,
            enrollment_creditors_page
    ) -> Any:
        """ Test creditor offer statuses - """
        with testit.step('Create and accept offer for deals'):
            enrollment_id = customer_queries.get_random_active_deal_id()
            login_page.login_with_cookies(page=enrollments_pages.enrollments_creditors, client_id=enrollment_id)
            enrollment_creditors_page.click_btn_create_new_creditor()
            enrollment_creditors_page.fill_all_creditor_data()
            enrollment_creditors_page.select_creditors()
            enrollment_creditors_page.add_document_with_type_settlement_letter()
            enrollment_creditors_page.create_settlement_offer()
            enrollment_creditors_page.check_settlement_offer()
            enrollment_creditors_page.check_canceled_state()
            enrollment_creditors_page.check_need_sf_letter_state()
            enrollment_creditors_page.check_need_cl_auth_state()
            enrollment_creditors_page.check_need_acceptance_state()
            enrollment_creditors_page.check_override_errors_acceptance_state()
            enrollment_creditors_page.turn_off_acceptance_state()

    title = 'Checking change ACH for enrollments with role [{role}]'

    @testit.displayName(title)
    @testit.externalId('enrollments test 6 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role', [('1', 'admin')])
    def test_change_enrollment_for_loans(
            self,
            ex_id: str,
            role: str,
            config,
            login_page,
            enrollment_ach_page
    ) -> Any:
        """ Creating ACH from deals - """
        with testit.step('Test change ach for loans'):
            loan_id = config.ui_data['enrollments']['client']
            login_page.login_with_cookies(
                page=enrollments_pages.enrollments_ach,
                client_id=loan_id
            )
            all_expected_data = enrollment_ach_page.fill_ach_fields()
            enrollment_ach_page.check_all_fields_ach(excepted_data=all_expected_data)
            enrollment_ach_page.sending_ach_docs('Email Only')

    title = 'Checking New plan for Different Schedule Type with role [{role}]'

    @testit.displayName(title)
    @testit.externalId('enrollments test 7 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize('ex_id, role, new_program_term, schedule_type',
                             [
                                  ('1', 'admin', '45', 'Monthly'),
                                  ('2', 'admin', '50', 'Semi-Monthly'),
                                  ('3', 'admin', '55', 'Be-Weekly')
                             ]
                             )
    def test_checking_new_plan_for_different_schedule_type(
            self,
            ex_id: str,
            role: str,
            new_program_term: int,
            schedule_type: str,
            login_page,
            enrollment_plan_page
    ) -> Any:
        """ Checking New Plan - """
        with testit.step('Test checking new plan term for different schedule type'):
            current_date = datetime.now()
            formatted_date = current_date.strftime("%m/%d/%Y")
            plan_history = 'current - ' + formatted_date + ' (Dmitry Paxomov)'
            enrollment_id = customer_queries.get_random_active_deal_id()
            login_page.login_with_cookies(
                page=enrollments_pages.enrollments_profile,
                client_id=enrollment_id
            )
            enrollment_plan_page.choose_leads_tabs(tab=enrollments_tabs.plan)
            enrollment_plan_page.click_btn_create_new_plan()
            enrollment_plan_page.fill_plan_and_press_simulate_schedule(
                schedule_type=schedule_type,
                new_program_term=new_program_term
            )
            enrollment_plan_page.check_plan_after_saving()
            enrollment_plan_page.press_commit_to_schedule()
            enrollment_plan_page.check_plan_after_commit(plan_history)


    # title = 'Checking Automatically added payments after accepting the settlement offer [{role}]'
    #
    # @testit.displayName(title)
    # @testit.externalId('enrollments test 8 case {ex_id}')
    # @testit.title(title)
    # @pytest.mark.parametrize('ex_id, role', [('1', 'admin')])
    # def test_automatically_added_payments_after_accepting_the_settlement_offer(
    #         self,
    #         ex_id: str,
    #         role: str,
    #         login_page,
    #         enrollment_payments_page
    # ) -> Any:
    #     """ Automatically added payments - """
    #     with testit.step(
    #             'Checking Automatically added payments after accepting the settlement offer'):
    #         enrollment_id = customer_queries.get_random_new_active_deal_id()
    #         expected_data = enrollment_payments_page.set_expected_payment_data()
    #         login_page.login_with_cookies(
    #             page=enrollments_pages.enrollments_drafts, client_id=enrollment_id)
    #         actual_data = enrollment_payments_page.get_payments_data(enrollment_payments_page)
    #         enrollment_payments_page.сompare_payment_data(expected_data, actual_data)
    #         enrollment_payments_page.choose_leads_tabs(
    #             tab=enrollments_pages.enrollments_creditors_tab)
    #         enrollment_payments_page.click_button_autosimulate_on()  # TODO Доделать тест когда починят кнопку
    #         #enrollment_payments_page.select_creditors()
    #         #enrollment_payments_page.add_document_with_type_settlement_letter()
