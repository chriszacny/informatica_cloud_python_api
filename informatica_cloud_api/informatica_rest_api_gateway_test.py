import unittest
import informatica_rest_api_gateway
import requests


class LoginStrategyMock(informatica_rest_api_gateway.LoginStrategy):
    def _do_http_request(self, payload):
        pass


class LogoutStrategyMock(informatica_rest_api_gateway.LogoutStrategy):
    def _do_http_request(self, payload):
        pass


class StartJobStrategyMock(informatica_rest_api_gateway.StartJobStrategy):
    def _do_http_request(self, payload):
        pass


class StopJobStrategyMock(informatica_rest_api_gateway.StopJobStrategy):
    def _do_http_request(self, payload):
        pass


class GetJobStatusStrategyMock(informatica_rest_api_gateway.GetJobStatusStrategy):
    def _do_http_request(self, payload):
        pass


"""
class InformaticaRestApiGatewayMock(informatica_rest_api_gateway.InformaticaRestApiGateway):

    def __init__(self, username, password, endpoint):
        super(InformaticaRestApiGatewayMock, self).__init__(username, password, endpoint)


    def _send_connect_request_to_informatica(self):
        response = informatica_rest_api_gateway.Response()
        response.response_ok = True
        return response

    def _send_close_request_to_informatica(self):
        response = informatica_rest_api_gateway.Response()
        response.response_ok = True
        return response

    def _send_start_request_to_informatica(self, job_id):
        response = informatica_rest_api_gateway.Response()
        response.response_ok = True
        return response

    def _send_stop_request_to_informatica(self, job_id):
        response = informatica_rest_api_gateway.Response()
        response.response_ok = True
        return response

    def _send_get_job_status_request_to_informatica(self, job_id):
        response = informatica_rest_api_gateway.JobStatusResponse()
        response.response_ok = True
        response.job_status = informatica_rest_api_gateway.JobStatus('1234', informatica_rest_api_gateway.InformaticaJobRunStates.Success, informatica_rest_api_gateway.InformaticaJobStates.Running)
        return response
"""


class InformaticaRestAccessTest(unittest.TestCase):
    def setUp(self):
        informatica_rest_api_gateway.LoginStrategy = LoginStrategyMock
        informatica_rest_api_gateway.LogoutStrategy = LogoutStrategyMock
        informatica_rest_api_gateway.StartJobStrategy = StartJobStrategyMock
        informatica_rest_api_gateway.StopJobStrategy = StopJobStrategyMock
        informatica_rest_api_gateway.GetJobStatusStrategy = GetJobStatusStrategyMock

    def test_informatica_basic_connection(self):
        access = informatica_rest_api_gateway.InformaticaRestApiGateway('someuser@expedia.com', 'aPassword', 'anEndpoint')
        self.assertEquals(access.is_connected, False)
        access.connect()
        self.assertEquals(access.is_connected, True)
        access.close_connection()
        self.assertEquals(access.is_connected, False)

    def test_informatica_start_job(self):
        access = informatica_rest_api_gateway.InformaticaRestApiGateway('someuser@expedia.com', 'aPassword', 'anEndpoint')
        self.assertRaises(StandardError, access.start_job, access, '1234')
        access.connect()
        started = access.start_job('1234')
        self.assertEquals(True, started)

    def test_informatica_stop_job(self):
        access = informatica_rest_api_gateway.InformaticaRestApiGateway('someuser@expedia.com', 'aPassword', 'anEndpoint')
        self.assertRaises(StandardError, access.stop_job, access, '1234')
        access.connect()
        access.start_job('1234')
        stopped = access.stop_job('1234')
        self.assertEquals(True, stopped)

    def test_informatica_get_job_status(self):
        access = informatica_rest_api_gateway.InformaticaRestApiGateway('someuser@expedia.com', 'aPassword', 'anEndpoint')
        self.assertRaises(StandardError, access.stop_job, access, '1234')
        access.connect()
        access.start_job('1234')
        status = access.get_job_status('1234')
        self.assertEquals(status.job_id, '1234')
        self.assertEquals(status.last_result, informatica_rest_api_gateway.InformaticaJobRunStates.Success)
        self.assertEquals(status.current_state, informatica_rest_api_gateway.InformaticaJobStates.Running)

    def test_login_formulate_payload(self):
        mock = LoginStrategyMock()
        payload = mock._formulate_payload({'username': 'someuser@expedia.com', 'password': 'aPassword', 'endpoint': 'anEndpoint'})
        self.assertIsInstance(payload, informatica_rest_api_gateway.Payload)
        expected_payload_body = {'username': 'someuser@expedia.com', 'password': 'aPassword', '@type': 'login'}
        expected_payload_headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        self.assertEquals(payload.headers, expected_payload_headers)
        self.assertEquals(payload.payload_body, expected_payload_body)

    def test_logout_formulate_payload(self):
        mock = LogoutStrategyMock()
        payload = mock._formulate_payload({'username': 'someuser@expedia.com', 'password': 'aPassword', 'endpoint': 'anEndpoint'})
        self.assertIsInstance(payload, informatica_rest_api_gateway.Payload)
        expected_payload_body = {'username': 'someuser@expedia.com', 'password': 'aPassword', '@type': 'logout'}
        expected_payload_headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        self.assertEquals(payload.headers, expected_payload_headers)
        self.assertEquals(payload.payload_body, expected_payload_body)

    def test_start_job_formulate_payload(self):
        #Can't implement till I can see the way a start job req should be sent
        raise NotImplementedError

    def test_stop_job_formulate_payload(self):
        #Can't implement till I can see the way a stop job req should be sent
        raise NotImplementedError

    def test_get_job_status_formulate_payload(self):
        #Can't implement till I can see the way a job should be queried
        raise NotImplementedError

    def test_login_process_response(self):
        #Can't implement till I can see an actual response
        raise NotImplementedError

    def test_logout_process_response(self):
        #Can't implement till I can see an actual response
        raise NotImplementedError

    def test_start_job_process_response(self):
        #Can't implement till I can see an actual response
        raise NotImplementedError

    def test_stop_job_process_response(self):
        #Can't implement till I can see an actual response
        raise NotImplementedError

    def test_get_job_status_process_response(self):
        #Can't implement till I can see an actual response
        raise NotImplementedError