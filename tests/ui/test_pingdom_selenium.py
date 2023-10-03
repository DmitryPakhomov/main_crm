import os
import time
import pytest
from typing import NoReturn
from selenium.webdriver.chrome.webdriver import WebDriver
from autotests.pages.data.enrollments_data import enrollments_pages
from autotests.pages.data.leads_data import leads_pages
from autotests.pages.data.loans_data import loans_pages
from autotests.pages.data.main_data import roles
from autotests.pages.utils import slack_post_msg, get_list_avg_value


class TestPingdomSelenium:
    @pytest.mark.parametrize(
        'page, client_id',
        [
            (leads_pages.leads, ''),
            (leads_pages.leads_history, os.environ['LEAD_ID']),
            (leads_pages.leads_profile, os.environ['LEAD_ID']),
            (leads_pages.leads_income, os.environ['LEAD_ID']),
            (leads_pages.leads_creditors, os.environ['LEAD_ID']),
            (leads_pages.leads_budget, os.environ['LEAD_ID']),
            (leads_pages.leads_calculator, os.environ['LEAD_ID']),
            (leads_pages.leads_ach, os.environ['LEAD_ID']),
            (leads_pages.leads_document, os.environ['LEAD_ID']),
            (leads_pages.leads_duplicate, os.environ['LEAD_ID'])
        ]
    )
    def test_pingdom_selenium_leads(
            self,
            page: str,
            client_id: str,
            browser: WebDriver,
            login_page
    ) -> NoReturn:
        """ Checking page load time - """
        login_page.login_with_cookies_hmac(role=roles.admin2)
        login_page.open_page(page=page, client_id=client_id)
        browser.refresh()

        count = int(os.environ['REFRESH_COUNT'])  # число переоткрытий страниц
        load_times = []
        for j in range(count):
            browser.refresh()
            time.sleep(2)  # ждем 3 сек загрузку страницы, раскомментировать для Chrome!
            load_time = (browser.execute_script(
                "return ( window.performance.timing.loadEventEnd - "
                "window.performance.timing.navigationStart )")) / 1000
            load_times.append(round(load_time, 2))

        min_value = min(load_times)
        max_value = max(load_times)
        avg = get_list_avg_value(load_times)
        emoji = ':white_check_mark:' if avg <= int(os.environ["LOAD_TIME_LIMIT"]) else ':x:'

        text = f'*{page}:* {emoji} AVG: {avg} ( min: {min_value} | max: {max_value} | count: {count} )'

        blocks = [
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": text
                    }
                ]
            }
        ]

        if avg > int(os.environ["LOAD_TIME_LIMIT"]):
            slack_post_msg(
                token=os.environ['PERFORMANCE_BOT_TOKEN'],
                channel=os.environ['PERFORMANCE_CHANNEL'],
                blocks=str(blocks),
                icon_emoji=':smoking_stress:',
                username='Selenium'
            )

    creditor_id = '78231350'
    @pytest.mark.parametrize(
        'page, client_id',
        [
            (enrollments_pages.enrollments, ''),
            (enrollments_pages.enrollments_main, os.environ['ENROLLMENT_ID']),
            (enrollments_pages.enrollments_creditors, os.environ['ENROLLMENT_ID']),
            (enrollments_pages.enrollments_customer_creditors, creditor_id),
            (enrollments_pages.enrollments_customer_creditors_offers, creditor_id),
            (enrollments_pages.enrollments_customer_creditors_documents, creditor_id),
            (enrollments_pages.enrollments_customer_creditors_payments, creditor_id),
            (enrollments_pages.enrollments_drafts, os.environ['ENROLLMENT_ID']),
            (enrollments_pages.enrollments_plan, os.environ['ENROLLMENT_ID']),
            (enrollments_pages.enrollments_loan_plan, os.environ['ENROLLMENT_ID']),
            (enrollments_pages.enrollments_profile, os.environ['ENROLLMENT_ID']),
            (enrollments_pages.enrollments_income, os.environ['ENROLLMENT_ID']),
            (enrollments_pages.enrollments_budget, os.environ['ENROLLMENT_ID']),
            (enrollments_pages.enrollments_ach, os.environ['ENROLLMENT_ID']),
            (enrollments_pages.enrollments_document, os.environ['ENROLLMENT_ID']),
            (enrollments_pages.enrollments_duplicate, os.environ['ENROLLMENT_ID'])
        ]
    )
    def test_pingdom_selenium_enrollments(
            self,
            page: str,
            client_id: str,
            browser: WebDriver,
            login_page
    ) -> NoReturn:
        """ Checking page load time - """
        login_page.login_with_cookies_hmac(role=roles.admin2)
        login_page.open_page(page=page, client_id=client_id)
        browser.refresh()

        count = int(os.environ['REFRESH_COUNT'])  # число переоткрытий страниц
        load_times = []
        for j in range(count):
            browser.refresh()
            time.sleep(2)  # ждем 3 сек загрузку страницы, раскомментировать для Chrome!
            load_time = (browser.execute_script(
                "return ( window.performance.timing.loadEventEnd - "
                "window.performance.timing.navigationStart )")) / 1000
            load_times.append(round(load_time, 2))

        min_value = min(load_times)
        max_value = max(load_times)
        avg = get_list_avg_value(load_times)
        emoji = ':white_check_mark:' if avg <= int(os.environ["LOAD_TIME_LIMIT"]) else ':x:'

        text = f'*{page}:* {emoji} AVG: {avg} ( min: {min_value} | max: {max_value} | count: {count} )'

        blocks = [
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": text
                    }
                ]
            }
        ]

        if avg > int(os.environ["LOAD_TIME_LIMIT"]):
            slack_post_msg(
                token=os.environ['PERFORMANCE_BOT_TOKEN'],
                channel=os.environ['PERFORMANCE_CHANNEL'],
                blocks=str(blocks),
                icon_emoji=':smoking_stress:',
                username='Selenium'
            )

    @pytest.mark.parametrize(
        'page, client_id',
        [
            (loans_pages.loans, ''),
            (loans_pages.loans_history, os.environ['LOAN_ID']),
            (loans_pages.loans_drafts, os.environ['LOAN_ID']),
            (loans_pages.loans_profile, os.environ['LOAN_ID']),
            (loans_pages.loans_creditors, os.environ['LOAN_ID']),
            (loans_pages.loans_loan_plan, os.environ['LOAN_ID']),
            (loans_pages.loans_income, os.environ['LOAN_ID']),
            (loans_pages.loans_budget, os.environ['LOAN_ID']),
            (loans_pages.loans_ach, os.environ['LOAN_ID']),
            (loans_pages.loans_document, os.environ['LOAN_ID']),
            (loans_pages.loans_duplicate, os.environ['LOAN_ID'])
        ]
    )
    def test_pingdom_selenium_loans(
            self,
            page: str,
            client_id: str,
            browser: WebDriver,
            login_page
    ) -> NoReturn:
        """ Checking page load time - """
        login_page.login_with_cookies_hmac(role='admin2')
        login_page.open_page(page=page, client_id=client_id)
        browser.refresh()

        count = int(os.environ['REFRESH_COUNT'])  # число переоткрытий страниц
        load_times = []
        for j in range(count):
            browser.refresh()
            time.sleep(2)  # ждем 3 сек загрузку страницы, раскомментировать для Chrome!
            load_time = (browser.execute_script(
                "return ( window.performance.timing.loadEventEnd - "
                "window.performance.timing.navigationStart )")) / 1000
            load_times.append(round(load_time, 2))

        min_value = min(load_times)
        max_value = max(load_times)
        avg = get_list_avg_value(load_times)
        emoji = ':white_check_mark:' if avg <= int(os.environ["LOAD_TIME_LIMIT"]) else ':x:'

        text = f'*{page}:* {emoji} AVG: {avg} ( min: {min_value} | max: {max_value} | count: {count} )'

        blocks = [
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": text
                    }
                ]
            }
        ]

        if avg > int(os.environ["LOAD_TIME_LIMIT"]):
            slack_post_msg(
                token=os.environ['PERFORMANCE_BOT_TOKEN'],
                channel=os.environ['PERFORMANCE_CHANNEL'],
                blocks=str(blocks),
                icon_emoji=':smoking_stress:',
                username='Selenium'
            )