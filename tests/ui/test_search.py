import testit
import pytest
from typing import Any
from dotenv import load_dotenv
from autotests.pages.data.leads_data import leads_pages, leads_tabs
from autotests.pages.data.main_data import customer_types


load_dotenv()


class TestCommonPage:
    title = 'Checking main search by {case} for {user_type}[{role}]'
    @testit.displayName(title)
    @testit.externalId('search test 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, role, user_type, case, ui_data',
        [
            ('1', 'admin', customer_types.lead, 'id', ['common_page_search', customer_types.lead]),
            ('2', 'admin', customer_types.lead, 'name', ['common_page_search', customer_types.lead]),
            ('3', 'admin', customer_types.lead, 'phone', ['common_page_search', customer_types.lead]),
            ('4', 'admin', customer_types.lead, 'email', ['common_page_search', customer_types.lead]),
            ('5', 'admin', customer_types.deal, 'id', ['common_page_search', customer_types.deal]),
            ('6', 'admin', customer_types.deal, 'name', ['common_page_search', customer_types.deal]),
            ('7', 'admin', customer_types.deal, 'phone', ['common_page_search', customer_types.deal]),
            ('8', 'admin', customer_types.deal, 'email', ['common_page_search', customer_types.deal]),
            ('9', 'admin', customer_types.loan, 'id', ['common_page_search', customer_types.loan]),
            ('10', 'admin', customer_types.loan, 'name', ['common_page_search', customer_types.loan]),
            ('11', 'admin', customer_types.loan, 'phone', ['common_page_search', customer_types.loan]),
            ('12', 'admin', customer_types.loan, 'email', ['common_page_search', customer_types.loan]),
            ('13', 'admin', customer_types.loan_pro, 'id', ['common_page_search', customer_types.loan_pro]),
            ('14', 'admin', customer_types.loan_pro, 'name', ['common_page_search', customer_types.loan_pro]),
            ('15', 'admin', customer_types.loan_pro, 'phone', ['common_page_search', customer_types.loan_pro]),
            ('16', 'admin', customer_types.loan_pro, 'email', ['common_page_search', customer_types.loan_pro])
        ], indirect=['ui_data']
    )
    def test_common_page_search(
            self,
            ex_id: str,
            role: str,
            user_type: str,
            case: str,
            ui_data,
            login_page,
            lead_profile_page,
            loan_profile_page
    ) -> Any:
        """ Checking main search - """
        login_page.login_with_cookies(page=leads_pages.leads)
        customer = ui_data.data
        c_id = customer['id']
        c_type = customer['type']
        c_name = customer['name']
        c_phone = customer['phone']
        c_email = customer['email']
        expected_result = f"{c_name} - {c_type} (id: {c_id}) {c_phone}"
        if case == 'id':
            actual_result_by_id = lead_profile_page.search_applicant(search_text=c_id)
            lead_profile_page.check_search_result(
                actual_result=actual_result_by_id, expected_result=expected_result
            )
            lead_profile_page.check_customer_id_and_name(customer_id=c_id, name=c_name)
            lead_profile_page.check_valid_link(customer_id=c_id)

        if case == 'name':
            actual_result_by_name = lead_profile_page.search_applicant(
                search_text=c_name, many=True)
            lead_profile_page.check_search_result(
                actual_result=actual_result_by_name,
                expected_result=expected_result
            )

        if case == 'phone':
            phone = c_phone[2:]
            expected_phone = f"({phone[0:3]}) {phone[3:6]}-{phone[6:]}"  # "(757) 671-4140"
            lead_profile_page.search_applicant(search_text=expected_phone, many=True)
            lead_profile_page.click_by_found_user()
            lead_profile_page.choose_leads_tabs(tab=leads_tabs.profile)
            if user_type in customer_types.loan:
                actual_phone = loan_profile_page.get_phone_mobile_applicant()
            else:
                actual_phone = lead_profile_page.get_phone_mobile_applicant()
            assert actual_phone == expected_phone, AssertionError(
                lead_profile_page.error_handler(
                    action='Checking the compliance of the search data with the data in the profile',
                    error='Excepted search result data not equal profile data.',
                    as_is=actual_phone,
                    to_be=expected_phone
                )
            )

        if case == 'email':
            lead_profile_page.search_applicant(search_text=c_email, many=True)
            lead_profile_page.click_by_found_user()
            lead_profile_page.choose_leads_tabs(tab=leads_tabs.profile)
            if user_type == customer_types.loan:
                actual_email = loan_profile_page.get_email_applicant()
            else:
                actual_email = lead_profile_page.get_email_applicant()
            assert actual_email == c_email, AssertionError(
                lead_profile_page.error_handler(
                    action='Checking the compliance of the search data with the data in the profile',
                    error='Excepted search result data not equal profile data.',
                    as_is=actual_email,
                    to_be=c_email
                )
            )
