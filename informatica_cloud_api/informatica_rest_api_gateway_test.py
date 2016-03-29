import unittest
import informatica_rest_api_gateway


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


class GetJobRunStatusStrategyMock(informatica_rest_api_gateway.GetJobRunStatusStrategy):
    def _do_http_request(self, payload):
        pass


informatica_rest_api_gateway.LoginStrategy = LoginStrategyMock
informatica_rest_api_gateway.LogoutStrategy = LogoutStrategyMock
informatica_rest_api_gateway.StartJobStrategy = StartJobStrategyMock
informatica_rest_api_gateway.StopJobStrategy = StopJobStrategyMock
informatica_rest_api_gateway.GetJobStatusStrategy = GetJobRunStatusStrategyMock


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
        self.assertEquals(status.current_state, informatica_rest_api_gateway.InformaticaJobStates.Running)
