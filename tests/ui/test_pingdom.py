import os
import time
import pytest
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from autotests.pages.elements import Element
from autotests.pages.utils import slack_post_msg


def get_emoji(load_time: str, limit: int = int(os.environ["LOAD_TIME_LIMIT"])) -> str:
    if 'No data' not in load_time:
        load_time_int = float(load_time.split('\u2008')[0])
        emoji = ':large_green_circle:' if load_time_int <= limit else ':red_circle:'
    else:
        emoji = ':large_yellow_circle:'
    return emoji


def get_pingdom_url(**filters):
    url = f'https://my.pingdom.com/3/visitor-insights/{os.environ["PINGDOM_ID"]}/' \
          f'experience?token={os.environ["PINGDOM_TOKEN"]}&period=1h'
    for filter_name, filter_value in filters.items():
        url += f'&{filter_name}={filter_value.replace("/", "%2F")}'
    return url


def get_text_block(text: str) -> str:
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
    return str(blocks)


class TestPingdom:
    @pytest.mark.parametrize(
        'page, country',
        [
            ('', ''),
            ('/lead', 'US'),
            ('/leads/main', 'US'),
            ('/lead/profile', 'US'),
            ('/lead/income', 'US'),
            ('/lead/creditors', 'US'),
            ('/lead/calculator', 'US'),
            ('/lead/ach', 'US'),
            ('/lead/document', 'US'),
            ('/lead/duplicate', 'US'),
            ('/lead/create', 'US'),
            ('/deals', 'US'),
            ('/deals/main', 'US'),
            ('/deals/creditors', 'US'),
            ('/deals/drafts', 'US'),
            ('/deal/plan', 'US'),
            ('/deal/loan-plan-calculator', 'US'),
            ('/deal/profile', 'US'),
            ('/deal/income', 'US'),
            ('/deal/budget', 'US'),
            ('/deal/strategy', 'US'),
            ('/deal/ach/index', 'US'),
            ('/deal/document', 'US'),
            ('/loan', 'US'),
            ('/loans/main', 'US'),
            ('/loan/loan-drafts', 'US'),
            ('/loans/creditors', 'US'),
            ('/loan/plan/override/index', 'US'),
            ('/loan/profile', 'US'),
            ('/loan/income', 'US'),
            ('/loan/budget', 'US'),
            ('/loan/ach/index', 'US'),
            ('/loan/document', 'US'),
            ('/loans/fees', 'US'),
            ('/loans/creditors-payments', 'US'),
            ('/loan/advances-and-recoups', 'US'),
            ('/loan/creditor/document/index', 'US')
        ]
    )
    def test_pingdom(self, browser: WebDriver, page: str, country: str):
        """ Checking page load time via pingdom - """
        active_sessions = 'No data'
        load_time = 'No data'
        avg_load_time = 'No data'
        emoji_avg_load_time = ''
        if page == '':
            text = '*************************** *START* ***************************'
        else:
            elem = Element(browser)

            url = get_pingdom_url(url=page, country=country)
            elem.get_page(url)
            time.sleep(6)
            active_session_loc = (By.XPATH, "//h6[contains(text(), 'Active Sessions (Now)')]//following-sibling::span")
            load_time_loc = (By.XPATH, "//h6[contains(text(), 'Load Time (Now)')]//following-sibling::span")
            avg_load_time_loc = (By.XPATH, "//div[contains(text(), 'Avg. load time')]//ancestor::thead//following-sibling::tbody//td[3]//div//div")

            if elem.element_is_present(active_session_loc):
                active_sessions = elem.get_text(active_session_loc)
            if elem.element_is_present(load_time_loc):
                load_time = elem.get_text(load_time_loc)
            if elem.element_is_present(avg_load_time_loc):
                avg_load_time = elem.get_text(avg_load_time_loc)

            emoji_load_time = get_emoji(load_time=load_time)
            emoji_avg_load_time = get_emoji(load_time=avg_load_time)

            text = f'*{page}({country}):* ' \
                   f'Sessions: {active_sessions} ' \
                   f'| {emoji_load_time} Load Time: {load_time} ' \
                   f'| {emoji_avg_load_time} AVG Page Load Time: {avg_load_time}'

        if page == '':
            slack_post_msg(
                token=os.environ['PERFORMANCE_BOT_TOKEN'],
                channel=os.environ['PERFORMANCE_CHANNEL'],
                blocks=get_text_block(text=text),
                icon_emoji=':smoking_stress:',
                username='Pingdom'
            )
        if avg_load_time != 'No data' and emoji_avg_load_time == ':red_circle:':
            slack_post_msg(
                token=os.environ['PERFORMANCE_BOT_TOKEN'],
                channel=os.environ['PERFORMANCE_CHANNEL'],
                blocks=get_text_block(text=text),
                icon_emoji=':smoking_stress:',
                username='Pingdom'
            )
