import unittest
import informatica_rest_api_gateway
import requests
from module_resources import GeneralConstants
from module_resources import DataFieldnameStrings


class LoginStrategyMock(informatica_rest_api_gateway.BaseStrategy):
    def _do_http_request(self, payload):
        to_return = requests.Response()
        to_return.status_code = GeneralConstants.HttpStatusOK
        return to_return

    def _process_requests_response(self, requests_response):
        to_return = informatica_rest_api_gateway.LoginResponse()
        to_return.login_data.login_session_id = 'zxcv1234'
        to_return.login_data.login_server_url = 'https://www.fun.com'
        to_return.response_ok = True
        return to_return


class LogoutStrategyMock(informatica_rest_api_gateway.BaseStrategy):
    def _do_http_request(self, payload):
        to_return = requests.Response()
        to_return.status_code = GeneralConstants.HttpStatusOK
        return to_return


class StartJobStrategyMock(informatica_rest_api_gateway.BaseStrategy):
    def _do_http_request(self, payload):
        to_return = requests.Response()
        to_return.status_code = GeneralConstants.HttpStatusOK
        return to_return


class StopJobStrategyMock(informatica_rest_api_gateway.BaseStrategy):
    def _do_http_request(self, payload):
        to_return = requests.Response()
        to_return.status_code = GeneralConstants.HttpStatusOK
        return to_return


class GetJobRunStatusStrategyMock(informatica_rest_api_gateway.BaseStrategy):
    def _do_http_request(self, payload):
        to_return = requests.Response()
        to_return.status_code = GeneralConstants.HttpStatusOK
        return to_return

    def _process_requests_response(self, requests_response):
        to_return = informatica_rest_api_gateway.JobRunStatusResponse()
        to_return.response_ok = True
        to_return.job_status.job_id = '1234'
        to_return.job_status.current_job_execution_state = informatica_rest_api_gateway.InformaticaJobExecutionStates.Running
        return to_return

informatica_rest_api_gateway.LoginStrategy = LoginStrategyMock
informatica_rest_api_gateway.LogoutStrategy = LogoutStrategyMock
informatica_rest_api_gateway.StartJobStrategy = StartJobStrategyMock
informatica_rest_api_gateway.StopJobStrategy = StopJobStrategyMock
informatica_rest_api_gateway.GetJobRunStatusStrategy = GetJobRunStatusStrategyMock


class InformaticaRestAccessTest(unittest.TestCase):
    def setUp(self):
        pass

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
        status = access.get_job_run_status('1234')
        self.assertEquals(status.job_id, '1234')
        self.assertEquals(status.current_job_execution_state, informatica_rest_api_gateway.InformaticaJobExecutionStates.Running)
