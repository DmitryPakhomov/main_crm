import pytest
import testit
from autotests.pages.api.api_utils import API
from autotests.pages.api.settings import ENDPOINTS_MAPPING


class TestApiEnrollments:
    title = 'Checking get: /rest/v1/enrollment/UUID [{case}]'

    @testit.displayName(title)
    @testit.externalId('deals api test 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, api_data',
        [
            ('1', 'get_enrollment_valid', ['get_enrollment', 'get_enrollment_valid'])
        ], indirect=['api_data']
    )
    def test_api_get_enrollment(
            self, ex_id: str, case: str, api_data, urls, get_token_leads: str
    ) -> None:
        """ Checking get: /rest/v1/enrollment/ enrollmentUuid - """
        api = API()
        api.timeout = 2
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method] + api_data.data
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        res = api.make_request(method_type='GET', url=url, method=api_data.method, headers=headers)
        with testit.step('Checking get logic.'):
            res_body = res.json()
            match case:
                case 'get_enrollment_valid':
                    assert not res_body['uuid'] == '', {
                        'as_is': res_body['uuid'], 'to_be': 'uuid must not be empty '
                    }
                    assert not res_body['firstName'] == '', {
                        'as_is': res_body['firstName'], 'to_be': 'firstName must not be empty'
                    }
                    assert not res_body['lastName'] == '', {
                        'as_is': res_body['lastName'], 'to_be': 'lastName must not be empty'
                    }
                    assert res_body['status'] >= 0, {
                        'as_is': res_body['status'], 'to_be': 'status must be >= 0'
                    }

    title = 'Checking get: /rest/v1/enrollment/ [{case}]'

    @testit.displayName(title)
    @testit.externalId('deals api test 1 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, api_data',
        [
            ('1', 'get_enrollments',
             ['get_enrollments', 'valid_enrollments_list']
             ),
        ], indirect=['api_data']
    )
    def test_api_get_enrollments(
            self, ex_id: str, api_data, case: str, urls, get_token_leads: str
    ) -> None:
        """ Checking get: /rest/v1/enrollments/ date from date to- """
        api = API()
        api.timeout = 2
        params = {'dateFrom': api_data.data['date_from'],
                  'dateTo': api_data.data['date_to']}
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method]
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        res = api.make_request(method_type='GET', url=url, method=api_data.method, headers=headers,
                               params=params)
        with testit.step('Checking get logic.'):
            res_body = res.json()
            match case:
                case 'get_enrollments':
                    assert res_body['items'][0]['id'] >= 0, {
                        'as_is': res_body['items'][0]['id'], 'to_be': 'id must not be zero'
                    }
                    assert not res_body['items'][0]['type'] == '', {
                        'as_is': res_body['items'][0]['type'], 'to_be': 'type must not be empty'
                    }
                    assert not res_body['items'][0]['clientTypeChangeDate'] == '', {
                        'as_is': res_body['items'][0]['clientTypeChangeDate'],
                        'to_be': 'clientTypeChangeDate must not be empty'
                    }
                    assert not res_body['items'][0]['firstName'] == '', {
                        'as_is': res_body['items'][0]['firstName'],
                        'to_be': 'firstName must not be zero'
                    }
                    assert not res_body['items'][0]['lastName'] == '', {
                        'as_is': res_body['items'][0]['lastName'],
                        'to_be': 'lastName must not be zero'
                    }
                    assert not res_body['items'][0]['cellNumber'] == '', {
                        'as_is': res_body['items'][0]['cellNumber'],
                        'to_be': 'cellNumber must not be zero'
                    }
                    assert not res_body['items'][0]['homeNumber'] == '', {
                        'as_is': res_body['items'][0]['homeNumber'],
                        'to_be': 'homeNumber must not be zero'
                    }
                    assert not res_body['_links']['self']['href'] == '', {
                        'as_is': res_body['_links']['self']['href'],
                        'to_be': 'self link must not be empty'
                    }
                    assert not res_body['_links']['first']['href'] == '', {
                        'as_is': res_body['_links']['first']['href'],
                        'to_be': 'first link must not be empty'
                    }
                    assert not res_body['_links']['last']['href'] == '', {
                        'as_is': res_body['_links']['last']['href'],
                        'to_be': 'last link must not be empty'
                    }
                    assert res_body['_meta']['totalCount'] > 0, {
                        'as_is': res_body['_meta']['totalCount'],
                        'to_be': 'total count must be > 0'
                    }
                    assert res_body['_meta']['pageCount'] > 0, {
                        'as_is': res_body['_meta']['pageCount'],
                        'to_be': 'total count must be > 0'
                    }
                    assert res_body['_meta']['currentPage'] > 0, {
                        'as_is': res_body['_meta']['currentPage'],
                        'to_be': 'current page count must be > 0'
                    }
                    assert res_body['_meta']['perPage'] > 0, {
                        'as_is': res_body['_meta']['perPage'],
                        'to_be': 'per page must be > 0'
                    }
    title = 'Checking post: /rest/v1/enrollment/pinned_note [{case}]'

    @testit.displayName(title)
    @testit.externalId('deals api test 2 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, api_data',
        [
            ('1', 'get_enrollment_with_pinned_note',
             ['get_enrollment_pinned_note', 'enrollment_uuid_with_pinned']
             )
        ], indirect=['api_data']
    )
    def test_api_get_enrollment_pinned_note(
            self, ex_id: str, case: str, api_data, urls, get_token_leads: str
    ) -> None:
        """ Checking get: /rest/v1/enrollment/pinned-note enrollmentUuid - """
        api = API()
        api.timeout = 2
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method].format(
            enrollment_uuid_with_pinned=api_data.data)
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        res = api.make_request(method_type='GET', url=url, method=api_data.method, headers=headers)
        with testit.step('Checking get logic.'):
            res_body = res.json()
            match case:
                case 'get_enrollment_with_pinned_note':
                    assert res_body['id'] > 0, \
                        {
                        'as_is': res_body['id'], 'to_be': 'id must be > 0'
                        }
                    assert not res_body['datetime'] == '', \
                        {
                        'as_is': res_body['datetime'], 'to_be': 'datetime must not be empty'
                        }
                    assert not res_body['text'] == '', \
                        {
                        'as_is': res_body['text'], 'to_be': 'text must not be empty'
                        }
                    assert not res_body['uuid'] == '', \
                        {
                        'as_is': res_body['uuid'], 'to_be': 'uuid must not be empty'
                        }

    title = 'Checking get: /rest/v1/enrollment/partner-commission?enrollmentUuid [{case}]'

    @testit.displayName(title)
    @testit.externalId('deals api test 3 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, api_data',
        [
            ('1', 'get_enrollment_partner_commission',
             ['get_enrollment_partner_commission', 'enrollment_uuid_partner_commission']
             )
        ], indirect=['api_data']
    )
    def test_api_get_partner_commission(
            self, ex_id: str, case: str, api_data, urls, get_token_leads: str
    ) -> None:
        """ Checking get: /rest/v1/enrollment/partner-commission enrollmentUuid - """
        api = API()
        api.timeout = 2
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method] + api_data.data
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        res = api.make_request(method_type='GET', url=url, method=api_data.method, headers=headers)
        with testit.step('Checking get logic partner commission.'):
            res_body = res.json()[0]
            match case:
                case 'get_enrollment_partner_commission':
                    assert not res_body['enrollmentUuid'] == '', {
                        'as_is': res_body['enrollmentUuid'],
                        'to_be': 'enrollmentUuid must not be empty'
                    }
                    assert not res_body['commissionStatus'] == '', {
                        'as_is': res_body['commissionStatus'],
                        'to_be': 'commissionStatus must not be empty'
                    }
                    assert not res_body['commissionDate'] == '', {
                        'as_is': res_body['commissionDate'],
                        'to_be': 'commissionDate must not be empty'
                    }
                    assert res_body['debtChange'] == 0, {
                        'as_is': res_body['debtChange'], 'to_be': 'debtChange must not be empty'
                    }

    title = 'Checking get: /rest/v1/enrollment/payoff-quotes [{case}]'

    @testit.displayName(title)
    @testit.externalId('deals api test 4 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, api_data',
        [
            ('1', 'get_enrollment_payoff_quotes',
             ['get_enrollment_payoff_quotes', 'get_enrollment_valid'])
        ], indirect=['api_data']
    )
    def test_api_get_enrollment_payoff_quotes(
            self, ex_id: str, case: str, api_data, urls, get_token_leads: str
    ) -> None:
        """ Checking get: /rest/v1/enrollment/payoff-quotes - """
        api = API()
        api.timeout = 2
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method] + api_data.data
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        res = api.make_request(method_type='GET', url=url, method=api_data.method, headers=headers)
        with testit.step('Checking get logic partner commission.'):
            res_body = res.json()
            match case:
                case 'get_enrollment_payoff_quotes':
                    assert res_body['payoffQuoteValue'] >= 0, {
                        'as_is': res_body['payoffQuoteValue'], 'to_be': 'payoffQuoteValue must >= 0'
                    }
                    assert not res_body['quoteGoodUntilDraftCreditorPayment'] == '', \
                        {
                            'as_is': res_body['quoteGoodUntilDraftCreditorPayment'],
                            'to_be': 'quoteGoodUntilDraftCreditorPayment must not be empty'
                        }
                    assert res_body['haveAllDebtsBeenNegotiated'] == 'true' or 'false', \
                        {
                            'as_is': res_body['haveAllDebtsBeenNegotiated'],
                            'to_be': 'haveAllDebtsBeenNegotiated must be True or False'
                        }
                    assert res_body['lastRamMonthlyFee'] >= 0, \
                        {
                            'as_is': res_body['lastRamMonthlyFee'],
                            'to_be': 'lastRamMonthlyFee must be >= 0'
                        }
                    assert res_body['balanceDueAttorneyFees'] >= 0, \
                        {
                            'as_is': res_body['balanceDueAttorneyFees'],
                            'to_be': 'balanceDueAttorneyFees must be >= 0'
                        }
                    assert res_body['totalRamGcsCheckFeesDue'] >= 0, \
                        {
                            'as_is': res_body['totalRamGcsCheckFeesDue'],
                            'to_be': 'totalRamGcsCheckFeesDue must be >= 0'
                        }
                    assert res_body['currentRamBalance'] >= 0, \
                        {
                            'as_is': res_body['currentRamBalance'],
                            'to_be': 'currentRamBalance must be >= 0'
                        }

    title = 'Checking get: /rest/v1/deal/ach [{case}]'

    @testit.displayName(title)
    @testit.externalId('deals api test 5 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, api_data',
        [
            ('1', 'get_enrollment_ach', ['get_enrollment_ach', 'enrollment_id_ach'])
        ], indirect=['api_data']
    )
    def test_api_get_enrollment_ach(
            self, ex_id: str, case: str, api_data, urls, get_token_leads: str
    ) -> None:
        """ Checking get: /rest/v1/enrollment/ach - """
        api = API()
        api.timeout = 2
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method] + api_data.data
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        res = api.make_request(method_type='GET', url=url, method=api_data.method, headers=headers)
        with testit.step('Checking get logic deal ach.'):
            res_body = res.json()
            match case:
                case 'get_enrollment_ach':
                    assert not res_body['nameOnAccount'] == '', \
                        {
                            'as_is': res_body['nameOnAccount'],
                            'to_be': 'nameOnAccount must not be empty'
                        }
                    assert int(res_body['routingNumber']) >= 0, \
                        {
                            'as_is': res_body['routingNumber'],
                            'to_be': 'routingNumber  must be >= 0'
                        }
                    assert int(res_body['bankAccountNumber']) >= 0, \
                        {
                            'as_is': res_body['bankAccountNumber'],
                            'to_be': 'bankAccountNumber  must be >= 0'
                        }
                    assert not res_body['accountType'] == '', \
                        {
                            'as_is': res_body['accountType'],
                            'to_be': 'accountType must not be empty'
                        }

    title = 'Checking get: /rest/v1/deal/underwriting [{case}]'

    @testit.displayName(title)
    @testit.externalId('deals api test 7 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, api_data',
        [
            ('1', 'get_enrollment_with_underwriting',
             ['get_enrollment_underwriting', 'enrollment_id_with_underwriting']
             ),
            ('2', 'get_enrollment_without_underwriting',
             ['get_enrollment_underwriting', 'enrollment_id_without_underwriting']
             )
        ], indirect=['api_data']
    )
    def test_api_get_enrollment_underwriting(
            self, ex_id: str, case: str, api_data, urls, get_token_leads: str
    ) -> None:
        """ Checking get: /rest/v1/enrollment/underwriting - """
        api = API()
        api.timeout = 2
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method] + api_data.data
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        res = api.make_request(method_type='GET', url=url, method=api_data.method, headers=headers)
        with testit.step('Checking get logic deal underwriting.'):
            res_body = res.json()
            match case:
                case 'get_enrollment_with_underwriting':
                    assert res_body['underwritingStatus'] != '', \
                        {
                        'as_is': res_body['underwritingStatus'],
                        'to_be': 'underwritingStatus must not be equal None'
                        }
                    assert res_body['underwriter'] != [], \
                        {
                        'as_is': res_body['underwriter'],
                        'to_be': 'underwriter must be list'
                        }
                    assert res_body['loanParams'] != [], \
                        {
                        'as_is': res_body['loanParams'],
                        'to_be': 'loanParams must be list'
                        }
                    assert res_body['locProcessor'] != [], \
                        {
                        'as_is': res_body['locProcessor'],
                        'to_be': 'locProcessor must be list'
                        }
                case 'get_enrollment_without_underwriting':
                    assert res_body['underwritingStatus'] != '', \
                        {
                        'as_is': res_body['underwritingStatus'],
                        'to_be': 'underwritingStatus without must be None'
                        }
                    assert not res_body['underwriter'] == [], \
                        {
                        'as_is': res_body['underwriter'],
                        'to_be': 'underwriter must be None'
                        }
                    assert res_body['loanParams'] != [], \
                        {
                        'as_is': res_body['loanParams'],
                        'to_be': 'loanParams must be list'
                        }
                    assert not res_body['locProcessor'] == '', \
                        {
                        'as_is': res_body['locProcessor'],
                        'to_be': 'locProcessor must be None'
                        }

    title = 'Checking get: /rest/v1/deal/settlements [{case}]'

    @testit.displayName(title)
    @testit.externalId('deals api test 8 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, api_data',
        [
            ('1', 'valid_creditor_id', ['get_enrollment_settlement', 'valid_creditor_id'])
        ], indirect=['api_data']
    )
    def test_api_get_enrollment_settlements(
            self, ex_id: str, case: str, api_data, urls, get_token_leads: str
    ) -> None:
        """ Checking get: /rest/v1/enrollment/settlements - """
        api = API()
        api.timeout = 2
        params = {'customerId': api_data.data['customerId'],
                  'creditorId': api_data.data['creditorId']}
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method]
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        res = api.make_request(method_type='GET', url=url, method=api_data.method, headers=headers,
                               params=params)
        with testit.step('Checking get logic deal underwriting.'):
            res_body = res.json()[0]
            match case:
                case 'valid_creditor_id':
                    assert res_body['id'] > 0, {
                        'as_is': res_body['id'],
                        'to_be': 'ID original Creditor must not be empty'
                    }
                    assert res_body['originalCreditor'] != '', \
                        {
                        'as_is': res_body['originalCreditor'],
                        'to_be': 'Name original Creditor must not be empty'
                        }
                    assert res_body['originalCreditorGroupId'] > 0, \
                        {
                        'as_is': res_body['originalCreditorGroupId'],
                        'to_be': 'original Creditor GroupId must be >= 0'
                        }
                    assert res_body['originalCreditorGroupName'] != '', \
                        {
                        'as_is': res_body['originalCreditorGroupName'],
                        'to_be': 'original Creditor must not be empty'
                        }
                    assert res_body['currentCreditor'] != '', \
                        {
                         'as_is': res_body['currentCreditor'],
                         'to_be': 'current Creditor must not be empty'
                        }
                    assert res_body['currentBalance'] > 0, {
                        'as_is': res_body['currentBalance'],
                        'to_be': 'current Balance must be >= 0'
                        }
                    assert res_body['currentCreditorGroupId'] > 0, \
                        {
                        'as_is': res_body['currentCreditorGroupId'],
                        'to_be': 'current Creditor GroupId must be >= 0'
                        }
                    assert res_body['offerAmount'] > 0, {
                        'as_is': res_body['offerAmount'],
                        'to_be': 'offerAmount must be >= 0'
                        }
                    assert res_body['offerPercent'] > 0, \
                        {
                        'as_is': res_body['offerPercent'],
                        'to_be': 'offerPercent must be >= 0'
                        }
                    assert res_body['offerPercentCurrent'] > 0, \
                        {
                        'as_is': res_body['offerPercentCurrent'],
                        'to_be': 'offerPercentCurrent must be >= 0'
                        }
                    assert res_body['savings'] > 0, \
                        {
                        'as_is': res_body['savings'],
                        'to_be': 'savings must be >= 0'
                        }
                    assert res_body['creditorId'] > 0, \
                        {
                        'as_is': res_body['creditorId'],
                        'to_be': 'creditorId must be >= 0'
                        }
                    assert res_body['status'] != '', \
                        {
                        'as_is': res_body['status'],
                         'to_be': 'status must not be empty'
                        }
                    assert res_body['updatedDate'] != '', \
                        {
                        'as_is': res_body['updatedDate'],
                        'to_be': 'updatedDate must not be empty'
                        }
                    assert res_body['offerStatus'] > 0, \
                        {
                        'as_is': res_body['offerStatus'],
                        'to_be': 'offerStatus must be >= 0'
                        }
                    assert res_body['numberOfTerms'] > 0, {
                        'as_is': res_body['numberOfTerms'],
                        'to_be': 'numberOfTerms must be >= 0'
                    }
                    assert res_body['firstPaymentDate'] != '', \
                        {
                        'as_is': res_body['firstPaymentDate'],
                        'to_be': 'firstPaymentDate must not be empty'
                        }
                    assert res_body['last4DigitsOfAccountNumber'] != '', \
                        {
                        'as_is': res_body['last4DigitsOfAccountNumber'],
                        'to_be': 'last4DigitsOfAccountNumber must not be empty'
                        }
                    assert res_body['clientApproval'] >= 0, {
                        'as_is': res_body['clientApproval'],
                        'to_be': 'firstPaymentDate must be >= 0'
                    }

    title = 'Checking get: /rest/v1/enrollment/find [{case}]'

    @testit.displayName(title)
    @testit.externalId('deals api test 9 case {ex_id}')
    @testit.title(title)
    @pytest.mark.parametrize(
        'ex_id, case, api_data',
        [
            ('1', 'enrollment_find', ['get_enrollment_find', 'enrollment_find_valid'])
        ], indirect=['api_data']
    )
    def test_api_get_enrollment_find(
            self, ex_id: str, case: str, api_data, urls, get_token_leads: str
    ) -> None:
        """ Checking get: /rest/v1/enrollment/find - """
        api = API()
        api.timeout = 2
        params = {'email': api_data.data['enrollment_email_valid'],
                  'ssnLast4': api_data.data['find_valid_last4_ssn']}
        url = urls.url_api + ENDPOINTS_MAPPING[api_data.method]
        headers = {'Authorization': f'Bearer {get_token_leads}'}
        res = api.make_request(method_type='GET', url=url, method=api_data.method, headers=headers,
                               params=params)
        with testit.step('Checking find deal logic.'):
            res_body = res.json()
            match case:
                case 'enrollment_find':
                    assert res_body['id'] > 0, \
                        {
                        'as_is': res_body['id'],
                        'to_be': 'ID original Creditor must be > 0'
                        }
                    assert res_body['status'] > 0, \
                        {
                        'as_is': res_body['originalCreditor'],
                        'to_be': 'status must be > 0'
                        }
                    assert not res_body['statusDate'] == '', \
                        {
                        'as_is': res_body['statusDate'],
                         'to_be': 'statusDate must not be empty'
                        }
                    assert res_body['name'] != '', \
                        {
                        'as_is': res_body['name'],
                        'to_be': 'name must not be empty'
                        }
                    assert res_body['type'] != '', \
                        {
                        'as_is': res_body['type'],
                        'to_be': 'type must not be empty'
                        }
                    assert res_body['firstName'] != '', \
                        {
                        'as_is': res_body['firstName'],
                        'to_be': 'firstName must not be empty'
                        }
                    assert res_body['lastName'] != '', \
                        {
                        'as_is': res_body['lastName'],
                        'to_be': 'lastName must not be empty'
                        }
                    assert not res_body['email'] == '', \
                        {
                        'as_is': res_body['email'],
                        'to_be': 'email must not be empty'
                        }
                    assert not res_body['phoneMobile'] == '', \
                        {
                        'as_is': res_body['phoneMobile'],
                        'to_be': 'phoneMobile must not be empty'
                        }
                    assert res_body['ssnLast4'] == api_data.data['find_valid_last4_ssn'], \
                        {
                        'as_is': res_body['ssnLast4'], 'to_be': 'ssnLast4'
                        }
                    assert not res_body['dateOfBirth'] == '', \
                        {
                        'as_is': res_body['dateOfBirth'],
                        'to_be': 'dateOfBirth must not be empty'
                        }
                    assert not res_body['city'] == '', \
                        {
                        'as_is': res_body['city'],
                        'to_be': 'city must not be empty'
                        }
                    assert not res_body['state'] == '', \
                        {
                        'as_is': res_body['state'],
                        'to_be': 'state must not be empty'
                        }
                    assert not res_body['street'] == '', \
                        {
                        'as_is': res_body['street'],
                        'to_be': 'street must not be empty'
                        }
                    assert not res_body['zipcode'] == '', \
                        {
                        'as_is': res_body['zipcode'],
                        'to_be': 'zipcode must not be empty'
                        }
                    assert not res_body['creditReportId'] == '', \
                        {
                        'as_is': res_body['creditReportId'],
                        'to_be': 'creditReportId must not be empty'
                        }
                    assert not res_body['salesId'] == '', \
                        {
                        'as_is': res_body['salesId'],
                        'to_be': 'salesId must not be empty'
                        }
                    assert not res_body['salesIp'] == '', \
                        {
                        'as_is': res_body['salesIp'],
                        'to_be': 'salesIp must not be empty'
                        }
                    assert not res_body['salesName'] == '', \
                        {
                        'as_is': res_body['salesName'],
                         'to_be': 'salesName must not be empty'
                        }
                    assert not res_body['lang'] == '', \
                        {
                        'as_is': res_body['lang'],
                        'to_be': 'lang must not be empty'
                        }
                    assert res_body['fileStatus'] >= 0, \
                        {
                        'as_is': res_body['fileStatus'],
                        'to_be': 'fileStatus must be > 0'
                        }
                    assert res_body['paperStatementsEnabled'] > 0, \
                        {
                        'as_is': res_body['paperStatementsEnabled'],
                        'to_be': 'paperStatementsEnabled must be > 0'
                        }
                    assert not res_body['processingPaymentsService'] == '', \
                        {
                        'as_is': res_body['processingPaymentsService'],
                        'to_be': 'processingPaymentsService must not be empty'
                        }
