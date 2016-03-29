import unittest
import informatica_rest_api_gateway
import requests
from module_resources import GeneralConstants


class InformaticaRestAccessStrategyMethodTests(unittest.TestCase):

    def test_login_formulate_payload(self):
        mock = informatica_rest_api_gateway.LoginStrategy({'username': 'someuser@expedia.com', 'password': 'aPassword', 'login_endpoint': 'anEndpoint'})
        payload = mock._formulate_payload()
        self.assertIsInstance(payload, informatica_rest_api_gateway.Payload)
        expected_payload_body = {'username': 'someuser@expedia.com', 'password': 'aPassword', '@type': 'login'}
        expected_payload_headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        self.assertEquals(payload.headers, expected_payload_headers)
        self.assertEquals(payload.payload_body, expected_payload_body)

    def test_logout_formulate_payload(self):
        mock = informatica_rest_api_gateway.LogoutStrategy({'username': 'someuser@expedia.com', 'password': 'aPassword', 'login_endpoint': 'anEndpoint'})
        payload = mock._formulate_payload()
        self.assertIsInstance(payload, informatica_rest_api_gateway.Payload)
        expected_payload_body = {'username': 'someuser@expedia.com', 'password': 'aPassword', '@type': 'logout'}
        expected_payload_headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        self.assertEquals(payload.headers, expected_payload_headers)
        self.assertEquals(payload.payload_body, expected_payload_body)

    def test_start_job_formulate_payload(self):
        mock = informatica_rest_api_gateway.StartJobStrategy({'icSessionId': '7890', 'taskId': '1234'})
        payload = mock._formulate_payload()
        self.assertIsInstance(payload, informatica_rest_api_gateway.Payload)
        expected_payload_body = {'taskId': '1234', 'taskType': 'Workflow'}
        expected_payload_headers = {'Accept': 'application/json', 'icSessionId': '7890'}
        self.assertEquals(payload.headers, expected_payload_headers)
        self.assertEquals(payload.payload_body, expected_payload_body)

    def test_stop_job_formulate_payload(self):
        mock = informatica_rest_api_gateway.StopJobStrategy({'icSessionId': '7890', 'taskId': '1234'})
        payload = mock._formulate_payload()
        self.assertIsInstance(payload, informatica_rest_api_gateway.Payload)
        expected_payload_body = {'taskId': '1234', 'taskType': 'Workflow'}
        expected_payload_headers = {'Accept': 'application/json', 'icSessionId': '7890'}
        self.assertEquals(payload.headers, expected_payload_headers)
        self.assertEquals(payload.payload_body, expected_payload_body)

    def test_get_job_status_formulate_payload(self):
        mock = informatica_rest_api_gateway.GetJobRunStatusStrategy({'icSessionId': '7890', 'taskId': '1234'})
        payload = mock._formulate_payload()
        self.assertIsInstance(payload, informatica_rest_api_gateway.Payload)
        expected_payload_body = {}
        expected_payload_headers = {'Accept': 'application/json', 'icSessionId': '7890'}
        self.assertEquals(payload.headers, expected_payload_headers)
        self.assertEquals(payload.payload_body, expected_payload_body)

    def test_login_process_response(self):
        mock = informatica_rest_api_gateway.LoginStrategy({})
        expected_response = informatica_rest_api_gateway.LoginResponse()
        expected_response.response_ok = True
        expected_response.login_data.login_session_id = u'zxcv1234'
        expected_response.login_data.login_server_url = u'https://app.informaticaondemand.com/saas'
        json_test_data = {u'name': u'user@fun.com', u'firstName': u'Sven', u'icSessionId': u'zxcv1234', u'lastName': u'Zoltan', u'forceChangePassword': False, u'serverUrl': u'https://app.informaticaondemand.com/saas'}
        actual_response = mock._process_response_json(json_test_data)
        self.assertEquals(expected_response.response_ok, actual_response.response_ok)
        self.assertEquals(expected_response.login_data.login_server_url, actual_response.login_data.login_server_url)
        self.assertEquals(expected_response.login_data.login_session_id, actual_response.login_data.login_session_id)

    def test_get_job_status_process_response_found_task_id(self):
        mock = informatica_rest_api_gateway.GetJobRunStatusStrategy({'taskId': '1234'})
        expected_response = informatica_rest_api_gateway.JobRunStatusResponse()
        expected_response.response_ok = True
        expected_response.job_status.job_id = '1234'
        expected_response.job_status.current_state = informatica_rest_api_gateway.InformaticaJobStates.Running

        json_test_data = [{u'scheduleName': u'Every Hour during Business Hours', u'startTime': u'2016-02-25T12:00:00.000Z', u'objectName': u'', u'executionState': u'RUNNING', u'successTargetRows': 0, u'id': u'0007LF0E00000001TIPR', u'runContextType': u'SCHEDULER', u'runId': 4557, u'taskId': u'1234', u'entries': [], u'successSourceRows': 0, u'taskName': u'Test Task', u'failedSourceRows': 0, u'type': u'WORKFLOW', u'@type': u'activityMonitoryEntry', u'failedTargetRows': 0}]

        actual_response = mock._process_response_json(json_test_data)
        self.assertEquals(expected_response.response_ok, actual_response.response_ok)
        self.assertEquals(expected_response.job_status.job_id, actual_response.job_status.job_id)
        self.assertEquals(expected_response.job_status.current_state, actual_response.job_status.current_state)

    def test_get_job_status_process_response_not_found_task_id(self):
        mock = informatica_rest_api_gateway.GetJobRunStatusStrategy({'taskId': '1234'})
        expected_response = informatica_rest_api_gateway.JobRunStatusResponse()
        expected_response.response_ok = True
        expected_response.job_status.job_id = '1234'
        expected_response.job_status.current_state = informatica_rest_api_gateway.InformaticaJobStates.Stopped

        json_test_data = []

        actual_response = mock._process_response_json(json_test_data)
        self.assertEquals(expected_response.response_ok, actual_response.response_ok)
        self.assertEquals(expected_response.job_status.job_id, actual_response.job_status.job_id)
        self.assertEquals(expected_response.job_status.current_state, actual_response.job_status.current_state)

    def test_login_get_url_path(self):
        mock = informatica_rest_api_gateway.LoginStrategy({'login_endpoint': 'https://app.informaticaondemand.com/ma'})
        constructed_url = mock._get_fully_constructed_url()
        self.assertEquals('https://app.informaticaondemand.com/ma/api/v2/user/login', constructed_url)

    def test_logout_get_url_path(self):
        mock = informatica_rest_api_gateway.LogoutStrategy({'login_endpoint': 'https://app.informaticaondemand.com/ma'})
        constructed_url = mock._get_fully_constructed_url()
        self.assertEquals('https://app.informaticaondemand.com/ma/api/v2/user/logoutall', constructed_url)

    def test_start_job_get_url_path(self):
        mock = informatica_rest_api_gateway.StartJobStrategy({'server_url': 'https://app.informaticaondemand.com/ma'})
        constructed_url = mock._get_fully_constructed_url()
        self.assertEquals('https://app.informaticaondemand.com/ma/api/v2/job', constructed_url)

    def test_stop_job_get_url_path(self):
        mock = informatica_rest_api_gateway.StopJobStrategy({'server_url': 'https://app.informaticaondemand.com/ma'})
        constructed_url = mock._get_fully_constructed_url()
        self.assertEquals('https://app.informaticaondemand.com/ma/api/v2/job/stop', constructed_url)

    def test_get_job_status_get_url_path(self):
        mock = informatica_rest_api_gateway.GetJobRunStatusStrategy({'server_url': 'https://app.informaticaondemand.com/ma'})
        constructed_url = mock._get_fully_constructed_url()
        self.assertEquals('https://app.informaticaondemand.com/ma/api/v2/activity/activityMonitor', constructed_url)

    def test_base_process_requests_response(self):
        mock = informatica_rest_api_gateway.StopJobStrategy({})
        requests_response = requests.Response()
        requests_response.status_code = GeneralConstants.HttpStatusOK
        response = mock._process_requests_response(requests_response)
        self.assertTrue(response.response_ok)
        requests_response = requests.Response()
        requests_response.status_code = GeneralConstants.HttpStatusNotFound
        response = mock._process_requests_response(requests_response)
        self.assertFalse(response.response_ok)