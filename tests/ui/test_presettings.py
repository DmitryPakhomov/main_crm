import json
import random
import pytest
from typing import Any
from dotenv import load_dotenv
from autotests.pages.data.leads_data import leads_statuses
from autotests.pages.queries import Customer
from autotests.pages.settings import Settings
from autotests.pages.data.main_data import roles, customer_types
from selenium.webdriver.chrome.webdriver import WebDriver


load_dotenv()


class TestPresettings:
    @pytest.mark.parametrize(
        'role',
        [
            roles.admin,
            roles.admin2,
            roles.sales,
            roles.sales_upfront_loan_processor,
            roles.sales_debt_consultant,
            roles.sales_debt_consultant_sp,
            roles.negotiations,
            roles.opener,
            roles.accounting,
            roles.enrollments,
            roles.customer_service,
            roles.customer_service_team_leads,
            roles.retention,
            roles.underwriting_manager,
            roles.loc_customer_service,
            roles.loan_consultant
        ]
    )
    def test_update_auth_cookies(
            self,
            role: str,
            browser: WebDriver,
            environ: str,
            login_page
    ) -> Any:
        """ Update auth cookies in config - """
        cookies = login_page.login_with_cookies_hmac(role=role)
        cfg = f'{Settings.CONFIGS_PATH}/{environ}_cfg/{environ}_auth_cfg.json'

        with open(cfg) as config_file:
            config_data = config_file.read()

        temp_data = json.loads(config_data)
        temp_data[role]['cookies'] = cookies

        with open(cfg, 'w') as f:
            json.dump(temp_data, f, indent=4, ensure_ascii=False)

    @pytest.mark.parametrize(
        'test',
        [
            'leads_pages_console_log',
            'common_page_search'
        ]
    )
    def test_update_ui_data(self, environ: str, test: str, config) -> Any:
        """ Update data in config for UI tests - """
        temp_data = config.ui_data

        if test == 'leads_pages_console_log':
            data = Customer.get_random_leads_with_all_status_types()
            temp_data[test] = {
                leads_statuses.new: str(random.choice(data[leads_statuses.new])[0]),
                leads_statuses.docs_sent: str(random.choice(data[leads_statuses.docs_sent])[0]),
                leads_statuses.nurtured: str(random.choice(data[leads_statuses.nurtured])[0]),
                leads_statuses.ready_to_pitch: str(
                    random.choice(data[leads_statuses.ready_to_pitch])[0]),
                leads_statuses.hot: str(random.choice(data[leads_statuses.hot])[0]),
                leads_statuses.automation: str(random.choice(data[leads_statuses.automation])[0]),
                leads_statuses.mail_fax_docs: str(
                    random.choice(data[leads_statuses.mail_fax_docs])[0]),
                leads_statuses.pre_enrollment_sent: str(
                    random.choice(data[leads_statuses.pre_enrollment_sent])[0]),
                leads_statuses.pre_enrollment_completed: str(
                    random.choice(data[leads_statuses.pre_enrollment_completed])[0]),
            }
        if test == 'common_page_search':
            leads = Customer.get_random_any_data_of_one_applicant(user_type=customer_types.lead)
            lead = random.choice(leads[customer_types.lead])
            lead_data = {
                'id': str(lead[0]),
                'type': lead[1],
                'name': f"{lead[2]} {lead[3]}".lower(),
                'phone': lead[4],
                'email': lead[5]
            }

            deals = Customer.get_random_any_data_of_one_applicant(user_type=customer_types.deal)
            deal = random.choice(deals[customer_types.deal])
            deal_data = {
                'id': str(deal[0]),
                'type': 'enrollment',
                'name': f"{deal[2]} {deal[3]}".lower(),
                'phone': deal[4],
                'email': deal[5]
            }
            loans = Customer.get_random_any_data_of_one_applicant(user_type=customer_types.loan)
            loan = random.choice(loans[customer_types.loan])
            loan_data = {
                'id': str(loan[0]),
                'type': loan[1],
                'name': f"{loan[2]} {loan[3]}".lower(),
                'phone': loan[4],
                'email': loan[5]
            }
            loans_pro = Customer.get_random_any_data_of_one_applicant(user_type=customer_types.loan_pro)
            loan_pro = random.choice(loans_pro[customer_types.loan_pro])
            loan_pro_data = {
                'id': str(loan_pro[0]),
                'type': 'loan pro',
                'name': f"{loan_pro[2]} {loan_pro[3]}".lower(),
                'phone': loan_pro[4],
                'email': loan_pro[5]
            }
            temp_data[test] = {
                customer_types.lead: lead_data,
                customer_types.deal: deal_data,
                customer_types.loan: loan_data,
                customer_types.loan_pro: loan_pro_data
            }

        cfg = f'{Settings.CONFIGS_PATH}/{environ}_cfg/{environ}_ui_data_cfg.json'
        with open(cfg, 'w') as f:
            json.dump(temp_data, f, indent=4, ensure_ascii=False)
