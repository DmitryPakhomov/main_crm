import pytest
import testit
from autotests.pages.api.api_utils import API
from autotests.pages.api.settings import leads_creating_request_body, ENDPOINTS_MAPPING
from autotests.pages.data.leads_data import leads_statuses
from autotests.pages.data.test_data import TestData


class TestApiLeads:
    title = 'Checking post: /rest/v1/lead/lender-leads [{case}]'
    @testit.displayName(title)
    @testit.externalId('leads api test 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case',
        [
            ('1', 'with_all_fields'),
            ('2', 'with_credit_report'),
            ('3', 'without_email')
        ]
    )
    def test_api_post_lender_leads(
            self, ex_id: str, case: str, urls, get_token_leads: str
    ) -> None:
        """ Checking post: /rest/v1/lead/lender-leads - """
        api = API()
        method = 'post_lender_leads'
        url = urls.url_api + ENDPOINTS_MAPPING[method]
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        body = leads_creating_request_body()
        params = ''
        match case:
            case 'with_credit_report':
                credit_data = TestData.credit_report_data_from_csv(state='CA')
                credit_data['isValidityCheckRequired'] = True
                body = leads_creating_request_body(**credit_data)
                params = {'need_creditor_list': True}
            case 'without_email':
                body = leads_creating_request_body(email='')
        res = api.make_request(
            method_type='POST', url=url, method=method, body=body, headers=headers, params=params)
        with testit.step('Checking additional logic.'):
            res_body = res.json()
            match case:
                case 'with_credit_report':
                    assert res_body['creditors'] != [], {'as_is': res_body['creditors'], 'to_be': 'list of creditors'}
                case 'without_email':
                    assert res_body['noEmail'], {'as_is': res_body['noEmail'], 'to_be': False}
                    assert res_body['creditors'] == [], {'as_is': res_body['creditors'], 'to_be': []}


    title = 'Checking put: /rest/v1/lead/lender-leads/lead_id [{case}]'
    @testit.displayName(title)
    @testit.externalId('leads api test 2 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, api_data',
        [
            ('1', 'with_all_fields', ['put_lender_leads', 'with_all_fields']),
            ('2', 'with_credit_report', ['put_lender_leads', 'with_credit_report']),
            ('3', 'without_email', ['put_lender_leads', 'without_email'])
        ], indirect=['api_data']
    )
    def test_api_put_lender_leads(
            self, ex_id: str, case: str, api_data, urls, get_token_leads: str
    ) -> None:
        """ Checking put: /rest/v1/lead/lender-leads/lead_id - """
        api = API()
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method] + api_data.data
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        body = leads_creating_request_body()
        params = {'need_creditor_list': False}
        match case:
            case 'with_credit_report':
                credit_data = TestData.credit_report_data_from_csv(state='CA')
                credit_data['isValidityCheckRequired'] = True
                body = leads_creating_request_body(**credit_data)
                params = {'need_creditor_list': True}
            case 'without_email':
                body = leads_creating_request_body(email='')
        res = api.make_request(
            method_type='PUT',
            url=url,
            method=api_data.method,
            body=body,
            headers=headers,
            params=params
        )
        with testit.step('Checking additional logic.'):
            res_body = res.json()
            match case:
                case 'with_all_fields':
                    assert not res_body['noEmail'], {'as_is': res_body['noEmail'], 'to_be': False}
                    assert res_body['creditors'] == [], {'as_is': res_body['creditors'], 'to_be': []}
                case 'with_credit_report':
                    assert res_body['creditors'] != [], {'as_is': res_body['creditors'], 'to_be': 'list of creditors'}
                case 'without_email':
                    assert res_body['noEmail'], {'as_is': res_body['noEmail'], 'to_be': False}
                    assert res_body['creditors'] == [], {'as_is': res_body['creditors'], 'to_be': []}

            assert body['firstName'] == res_body['firstName'], {'as_is': res_body['firstName'], 'to_be': body['firstName']}

    title = 'Checking get: /rest/v1/lead/lender-leads/lead_id [{case}]'
    @testit.displayName(title)
    @testit.externalId('leads api test 3 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, api_data',
        [
            ('1', 'need_creditor_list', ['get_lender_leads', 'unassigned']),
            ('2', 'rejected', ['get_lender_leads', 'rejected']),
            ('3', 'active', ['get_lender_leads', 'active']),
            ('4', 'unassigned', ['get_lender_leads', 'unassigned']),
            ('5', 'trickle', ['get_lender_leads', 'trickle'])
        ], indirect=['api_data']
    )
    def test_api_get_lender_leads(
            self,
            ex_id: str,
            case: str,
            urls,
            api_data,
            get_token_leads: str
    ) -> None:
        """ Checking get: /rest/v1/lead/lender-leads/lead_id - """
        api = API()
        api.timeout = 2
        params = ''
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method] + api_data.data
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        match case:
            case 'need_creditor_list':
                params = {'need_creditor_list': True}
        res = api.make_request(
            method_type='GET', url=url, method=api_data.method, headers=headers, params=params)
        with testit.step('Checking additional logic.'):
            res_body = res.json()
            match case:
                case 'need_creditor_list':
                    if res_body['fico']:
                        assert res_body['creditors'], {'as_is': res_body['creditors'], 'to_be': 'list of creditors'}
                    else:
                        assert res_body['creditors'] == [], {'as_is': res_body['creditors'], 'to_be': []}
                case _:
                    assert res_body['quality'] == case, {'as_is': res_body['quality'], 'to_be': case}
                    assert res_body['creditors'] == [], {'as_is': res_body['creditors'], 'to_be': []}

    title = 'Checking get: /rest/v1/lead/lender-leads/check-duplicates [{case}]'
    @testit.displayName(title)
    @testit.externalId('leads api test 4 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, api_data',
        [
            ('1', 'duplicate_phone_email', ['lender_leads_check_duplicates', 'duplicate_phone_email']),
            ('2', 'duplicate_phone', ['lender_leads_check_duplicates', 'duplicate_phone']),
            ('3', 'duplicate_email', ['lender_leads_check_duplicates', 'duplicate_email'])
        ], indirect=['api_data']
    )
    def test_api_lender_leads_check_duplicates(
            self, ex_id: str, case: str, api_data, urls, get_token_leads: str
    ) -> None:
        """ Checking get: /rest/v1/lead/lender-leads/check-duplicates - """
        api = API()
        api.timeout = 1
        params = {'phone': api_data.data['phone'], 'email': api_data.data['email']}
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method]
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        res = api.make_request(
            method_type='GET', url=url, method=api_data.method, headers=headers, params=params)

        with testit.step('Checking additional logic.'):
            res_body = res.json()
            match case:
                case 'duplicate_phone':
                    assert res_body['rejectReason'] == 4, {'as_is': res_body['rejectReason'], 'to_be': 4}
                    assert res_body['rejectReasonText'] == 'Duplicate Lead', {'as_is': res_body['rejectReasonText'], 'to_be': 'Duplicate Lead'}
                case 'no_duplicate':
                    assert not res_body['rejectReason'], {'as_is': res_body['rejectReason'], 'to_be': None}
                    assert not res_body['rejectReasonText'], {'as_is': res_body['rejectReasonText'], 'to_be': None}

    title = 'Checking put: /rest/v1/lead/sales-rep/lead_id [{case}]'
    @testit.displayName(title)
    @testit.externalId('leads api test 5 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, api_data',
        [
            ('1', 'without_sales_rep', ['sales_rep', 'without_sales_rep'])
        ], indirect=['api_data']
    )
    def test_api_sales_rep(
            self, ex_id: str, case: str, api_data, urls, get_token_leads: str
    ) -> None:
        """ Checking put: /rest/v1/lead/sales-rep/lead_id - """
        api = API()
        api.timeout = 1
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method] + api_data.data
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        body = {'salesRepEmail': 'egor.zotov@americor.com'}
        api.make_request(
            method_type='PUT',
            url=url,
            method=api_data.method,
            body=body,
            headers=headers,
            response_validator=False
        )

    title = 'Checking post: /rest/v1/lead/purchase [{case}]'
    @testit.displayName(title)
    @testit.externalId('leads api test 6 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, api_data',
        [
            ('1', 'debt_consolidation', ['purchase', 'debt_consolidation'])
        ], indirect=['api_data']
    )
    def test_api_purchase(
            self, ex_id: str, case: str, api_data, urls, get_token_leads: str
    ) -> None:
        """ Checking post: /rest/v1/lead/purchase - """
        api = API()
        api.timeout = 2
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method]
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        body = {
            "openerEmail": "egor.zotov@americor.com",
            "purchaserId": api_data.data['purchaser_id'],
            "customerId": api_data.data['lead_id']
        }
        api.make_request(
            method_type='POST',
            url=url,
            method=api_data.method,
            body=body,
            headers=headers,
            response_validator=False
        )

    title = 'Checking post: /rest/v1/lead/purchase_denial [{case}]'
    @testit.displayName(title)
    @testit.externalId('leads api test 7 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, reason_code, api_data',
        [
            ('1', 'not interested in a sell', 15, ['purchase_denial', 'lead_id'])
        ], indirect=['api_data']
    )
    def test_api_purchase_denial(
            self,
            ex_id: str,
            case: str,
            reason_code: int,
            api_data,
            urls,
            get_token_leads: str
    ) -> None:
        """ Checking post: /rest/v1/lead/purchase_denial - """
        api = API()
        api.timeout = 1
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method]
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        body = {
            "openerEmail": "egor.zotov@americor.com",
            "customerId": api_data.data,
            "rejectReason": reason_code
        }
        api.make_request(
            method_type='POST',
            url=url,
            method=api_data.method,
            body=body,
            headers=headers,
            response_validator=False
        )

    title = 'Checking get: /rest/v1/lead/lead_id/creditors [{case}]'
    @testit.displayName(title)
    @testit.externalId('leads api test 8 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, api_data',
        [
            ('1', 'with_creditors', ['creditors', 'with_creditors']),
            ('2', 'without_creditors', ['creditors', 'without_creditors'])
        ], indirect=['api_data']
    )
    def test_api_creditors(
            self, ex_id: str, case: str, api_data, urls, get_token_leads: str
    ) -> None:
        """ Checking get: /rest/v1/lead/lead_id/creditors - """
        api = API()
        api.timeout = 2
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method].format(lead_id=api_data.data)
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        res = api.make_request(method_type='GET', url=url, method=api_data.method, headers=headers)
        with testit.step('Checking additional logic.'):
            res_body = res.json()
            match case:
                case 'with_creditors':
                    assert res_body, {'as_is': res_body, 'to_be': 'list with creditors data'}
                case 'without_creditors':
                    assert res_body == [], {'as_is': res_body, 'to_be': []}

    title = 'Checking get: /rest/v1/lead/lead_id/deposits [{case}]'
    @testit.displayName(title)
    @testit.externalId('leads api test 9 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, api_data',
        [
            # ('1', 'with_docs', '21789883'), # TODO: добавить после фикса бага
            ('2', 'without_docs', ['deposits', 'without_docs'])
        ], indirect=['api_data']
    )
    def test_api_deposits(
            self, ex_id: str, case: str, api_data, urls, get_token_leads: str
    ) -> None:
        """ Checking get: /rest/v1/lead/lead_id/deposits - """
        api = API()
        api.timeout = 2
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method].format(lead_id=api_data.data)
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        res = api.make_request(method_type='GET', url=url, method=api_data.method, headers=headers)
        with testit.step('Checking additional logic.'):
            res_body = res.json()
            for deposit in res_body:
                match case:
                    case 'without_docs':
                        assert not deposit['id'], {'as_is': deposit['id'], 'to_be': None}
                        assert not deposit['date'], {'as_is': deposit['date'], 'to_be': None}
                        assert not deposit['description'], {'as_is': deposit['description'], 'to_be': None}
                        assert not deposit['statusDate'], {'as_is': deposit['statusDate'], 'to_be': None}
                        assert not deposit['status'], {'as_is': deposit['status'], 'to_be': None}
                        assert not deposit['statusText'], {'as_is': deposit['statusText'], 'to_be': None}
                        assert deposit['amount'], {'as_is': deposit['id'], 'to_be': 'amount of deposit'}
                        assert not deposit['memo'], {'as_is': deposit['memo'], 'to_be': None}

    title = 'Checking get: /rest/v1/lead/lead_id/summary [{case}]'
    @testit.displayName(title)
    @testit.externalId('leads api test 10 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, api_data',
        [
            ('1', 'no_advantage_law', ['summary', 'no_advantage_law']),
            ('2', 'is_advantage_law', ['summary', 'is_advantage_law'])
        ], indirect=['api_data']
    )
    def test_api_summary(
            self, ex_id: str, case: str, api_data, urls, get_token_leads: str
    ) -> None:
        """ Checking get: /rest/v1/lead/lead_id/summary - """
        api = API()
        api.timeout = 7
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method].format(lead_id=api_data.data)
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        res = api.make_request(method_type='GET', url=url, method=api_data.method, headers=headers)
        with testit.step('Checking additional logic.'):
            res_body = res.json()
            assert res_body['type'] == 'lead', {'as_is': res_body['type'], 'to_be': 'lead'}
            match case:
                case 'no_advantage_law':
                    assert not res_body['isAdvantageLaw'], {'as_is': res_body['isAdvantageLaw'], 'to_be': False}
                case 'is_advantage_law':
                    assert res_body['isAdvantageLaw'], {'as_is': res_body['isAdvantageLaw'], 'to_be': True}

    title = 'Checking get: /rest/v1/lead/lead_id/profile [{case}]'
    @testit.displayName(title)
    @testit.externalId('leads api test 11 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, api_data',
        [
            ('1', 'is_third_party_speaker', ['profile', 'is_third_party_speaker']),
            ('2', 'no_third_party_speaker', ['profile', 'no_third_party_speaker'])
        ], indirect=['api_data']
    )
    def test_api_profile(
            self, ex_id: str, case: str, api_data, urls, get_token_leads: str
    ) -> None:
        """ Checking get: /rest/v1/lead/lead_id/profile - """
        api = API()
        api.timeout = 1
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method].format(lead_id=api_data.data)
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        api.make_request(method_type='GET', url=url, method=api_data.method, headers=headers)

    # TODO: добавить кейсов по всем статусам
    title = 'Checking get: /rest/v1/lead/lead_id [{case}]'
    @testit.displayName(title)
    @testit.externalId('leads api test 12 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, api_data',
        [
            ('1', leads_statuses.new, ['lead', leads_statuses.new]),
            ('2', leads_statuses.docs_sent, ['lead', leads_statuses.docs_sent])
        ], indirect=['api_data']
    )
    def test_api_get_lead(
            self, ex_id: str, case: str, api_data, urls, get_token_leads: str
    ) -> None:
        """ Checking get: /rest/v1/lead/lead_id - """
        api = API()
        api.timeout = 1
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method] + str(api_data.data)
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        res = api.make_request(method_type='GET', url=url, method=api_data.method, headers=headers)
        with testit.step('Checking additional logic.'):
            res_body = res.json()
            match case:
                case 'new':
                    assert res_body['status'] == 0, {'as_is': res_body['status'], 'to_be': 0}
                case 'docs_sent':
                    assert res_body['status'] == 13, {'as_is': res_body['status'], 'to_be': 13}