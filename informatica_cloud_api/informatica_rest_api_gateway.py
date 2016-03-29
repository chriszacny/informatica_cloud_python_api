import requests
import abc
import json
import logging
from module_resources import DataFieldnameStrings
from module_resources import GeneralConstants


API_URL_PART = '/api/v2'


class Payload(object):
    def __init__(self):
        self.payload_body = {}
        self.headers = {}


class InformaticaJobExecutionStates(object):
    Completed = 'COMPLETED'
    Running = 'RUNNING'
    Initialized = 'INITIALIZED'
    Stopping = 'STOPPING'
    Failed = 'FAILED'


class JobStatus(object):
    def __init__(self):
        self.job_id = None
        self.current_job_execution_state = None


class LoginData(object):
    def __init__(self):
        self.login_session_id = None
        self.login_server_url = None


class Response(object):
    def __init__(self):
        self.response_ok = None
        self.status_code = None
        self.text = None


class LoginRequiredError(StandardError):
    pass


class LoginError(StandardError):
    pass


class LogoutError(StandardError):
    pass


class StartJobError(StandardError):
    pass


class StopJobError(StandardError):
    pass


class GetJobRunStatusesError(StandardError):
    pass


class LoginResponse(Response):
    def __init__(self):
        super(LoginResponse, self).__init__()
        self.login_data = LoginData()


class JobRunStatusResponse(Response):
    def __init__(self):
        super(JobRunStatusResponse, self).__init__()
        self.job_status = JobStatus()


class BaseStrategy(object):
    def __init__(self, data):
        self.data = data

    def request_template_algorithm(self):
        payload = self._formulate_payload()
        requests_response = self._do_http_request(payload)
        return self._process_requests_response(requests_response)

    @abc.abstractmethod
    def _get_fully_constructed_url(self):
        pass

    @abc.abstractmethod
    def _formulate_payload(self):
        pass

    @abc.abstractmethod
    def _do_http_request(self, payload):
        pass

    def _process_requests_response(self, requests_response):
        to_return = Response()
        to_return.status_code = requests_response.status_code
        to_return.text = requests_response.text
        if requests_response.status_code == GeneralConstants.HttpStatusOK:
            to_return = Response()
            to_return.response_ok = True
            return to_return
        else:
            to_return = Response()
            to_return.response_ok = False
            return to_return


class LoginStrategy(BaseStrategy):
    def __init__(self, data):
        super(LoginStrategy, self).__init__(data)
        self.uri = '/user/login'

    def _formulate_payload(self):
        payload = Payload()
        payload.payload_body = {DataFieldnameStrings.UserName: self.data[DataFieldnameStrings.UserName], DataFieldnameStrings.Password: self.data[DataFieldnameStrings.Password], '@type': 'login'}
        payload.headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        return payload

    def _get_fully_constructed_url(self):
        return '{}{}{}'.format(self.data[DataFieldnameStrings.LoginEndpoint], API_URL_PART, self.uri)

    def _do_http_request(self, payload):
        return requests.post(url=self._get_fully_constructed_url(), data=json.dumps(payload.payload_body), headers=payload.headers)

    def _process_requests_response(self, requests_response):
        to_return = LoginResponse()
        to_return.status_code = requests_response.status_code
        to_return.text = requests_response.text
        if requests_response.status_code == GeneralConstants.HttpStatusOK:
            to_return.response_ok = True
            return self._process_response_json(requests_response.json(), to_return)
        else:
            to_return.response_ok = False
            return to_return

    def _process_response_json(self, requests_response_jsonified, to_return):
        to_return.login_data.login_server_url = requests_response_jsonified['serverUrl']
        to_return.login_data.login_session_id = requests_response_jsonified['icSessionId']
        return to_return


class LogoutStrategy(BaseStrategy):
    def __init__(self, data):
        super(LogoutStrategy, self).__init__(data)
        self.uri = '/user/logoutall'

    def _formulate_payload(self):
        payload = Payload()
        payload.payload_body = {DataFieldnameStrings.UserName: self.data[DataFieldnameStrings.UserName], DataFieldnameStrings.Password: self.data[DataFieldnameStrings.Password], '@type': 'logout'}
        payload.headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        return payload

    def _get_fully_constructed_url(self):
        return '{}{}{}'.format(self.data[DataFieldnameStrings.LoginEndpoint], API_URL_PART, self.uri)

    def _do_http_request(self, payload):
        return requests.post(url=self._get_fully_constructed_url(), headers=payload.headers, data=json.dumps(payload.payload_body))


class StartJobStrategy(BaseStrategy):
    def __init__(self, data):
        super(StartJobStrategy, self).__init__(data)
        self.uri = '/job'

    def _formulate_payload(self):
        payload = Payload()
        taskType = GeneralConstants.DefaultTaskType
        if DataFieldnameStrings.TaskType in self.data:
            taskType = self.data[DataFieldnameStrings.TaskType]
        payload.payload_body = {DataFieldnameStrings.TaskId: self.data[DataFieldnameStrings.TaskId], DataFieldnameStrings.TaskType: taskType, '@type': 'job'}
        payload.headers = {'content-type': 'application/json', 'Accept': 'application/json', DataFieldnameStrings.ICSessionId: self.data[DataFieldnameStrings.ICSessionId]}
        return payload

    def _get_fully_constructed_url(self):
        return '{}{}{}'.format(self.data[DataFieldnameStrings.ServerUrl], API_URL_PART, self.uri)

    def _do_http_request(self, payload):
        logging.info('Doing Start Job POST.')
        logging.info('URL is: ' + self._get_fully_constructed_url())
        logging.info('Payload is: ' + str(payload.payload_body))
        logging.info('Headers are: ' + str(payload.headers))
        return requests.post(url=self._get_fully_constructed_url(), headers=payload.headers, data=json.dumps(payload.payload_body))


class StopJobStrategy(BaseStrategy):
    def __init__(self, data):
        super(StopJobStrategy, self).__init__(data)
        self.uri = '/job/stop'

    def _formulate_payload(self):
        payload = Payload()
        taskType = GeneralConstants.DefaultTaskType
        if DataFieldnameStrings.TaskType in self.data:
            taskType = self.data[DataFieldnameStrings.TaskType]
        payload.payload_body = {DataFieldnameStrings.TaskId: self.data[DataFieldnameStrings.TaskId], DataFieldnameStrings.TaskType: taskType, '@type': 'job'}
        payload.headers = {'content-type': 'application/json', 'Accept': 'application/json', DataFieldnameStrings.ICSessionId: self.data[DataFieldnameStrings.ICSessionId]}
        return payload

    def _get_fully_constructed_url(self):
        return '{}{}{}'.format(self.data[DataFieldnameStrings.ServerUrl], API_URL_PART, self.uri)

    def _do_http_request(self, payload):
        return requests.post(url=self._get_fully_constructed_url(), headers=payload.headers, data=json.dumps(payload.payload_body))


class GetJobRunStatusStrategy(BaseStrategy):
    def __init__(self, data):
        super(GetJobRunStatusStrategy, self).__init__(data)
        self.uri = '/activity/activityMonitor'

    def _formulate_payload(self):
        payload = Payload()
        payload.payload_body = {}
        payload.headers = {'Accept': 'application/json', DataFieldnameStrings.ICSessionId: self.data[DataFieldnameStrings.ICSessionId]}
        return payload

    def _get_fully_constructed_url(self):
        return '{}{}{}'.format(self.data[DataFieldnameStrings.ServerUrl], API_URL_PART, self.uri)

    def _do_http_request(self, payload):
        return requests.get(self._get_fully_constructed_url(), headers=payload.headers)

    def _process_requests_response(self, requests_response):
        to_return = JobRunStatusResponse()
        to_return.status_code = requests_response.status_code
        to_return.text = requests_response.text
        if requests_response.status_code == GeneralConstants.HttpStatusOK:
            to_return.response_ok = True
            return self._process_response_json(requests_response.json(), to_return)
        else:
            to_return = JobRunStatusResponse()
            to_return.response_ok = False
            return to_return

    def _find_task_in_informatica_and_set_default_values(self, task_id_to_find, to_return):
        #TODO I am setting defaults without finding the task here - but instead of this, we should verify that the task id actually exists in Informatica, else, raise an Exception
        to_return.job_status.job_id = task_id_to_find
        to_return.job_status.current_job_execution_state = InformaticaJobExecutionStates.Completed
        return to_return

    def _process_response_json(self, requests_response_jsonified, to_return):
        task_id_to_find = self.data[DataFieldnameStrings.TaskId]
        to_return = self._find_task_in_informatica_and_set_default_values(task_id_to_find, to_return)
        for activity_monitor_entry in requests_response_jsonified:
            if activity_monitor_entry[DataFieldnameStrings.TaskId] == task_id_to_find:
                to_return.job_status.current_job_execution_state = activity_monitor_entry['executionState']
        return to_return


class InformaticaRestApiGateway(object):
    def __init__(self, username, password, login_endpoint):
        self.username = username
        self.password = password
        self.login_endpoint = login_endpoint
        self.ic_session_id = None
        self.login_server_url = None
        self.is_connected = False

    def _verify_connected(self):
        if not self.is_connected:
            raise LoginRequiredError()

    def _send_informatica_request(self, strategy):
        return strategy.request_template_algorithm()

    def connect(self):
        response = self._send_informatica_request(LoginStrategy({DataFieldnameStrings.UserName: self.username, DataFieldnameStrings.Password: self.password, DataFieldnameStrings.LoginEndpoint: self.login_endpoint}))
        if response.response_ok is True:
            self.is_connected = True
            self.ic_session_id = response.login_data.login_session_id
            self.login_server_url = response.login_data.login_server_url
        else:
            raise LoginError()

    def close_connection(self):
        response = self._send_informatica_request(LogoutStrategy({DataFieldnameStrings.UserName: self.username, DataFieldnameStrings.Password: self.password, DataFieldnameStrings.LoginEndpoint: self.login_endpoint}))
        if response.response_ok is True:
            self.is_connected = False
            self.ic_session_id = None
            self.login_server_url = None
        else:
            raise LogoutError()

    def start_job(self, job_id):
        self._verify_connected()
        response = self._send_informatica_request(StartJobStrategy({DataFieldnameStrings.ICSessionId: self.ic_session_id, DataFieldnameStrings.ServerUrl: self.login_server_url, DataFieldnameStrings.TaskId: job_id}))
        if response.response_ok is True:
            return True
        else:
            raise StartJobError()

    def stop_job(self, job_id):
        self._verify_connected()
        response = self._send_informatica_request(StopJobStrategy({DataFieldnameStrings.ICSessionId: self.ic_session_id, DataFieldnameStrings.ServerUrl: self.login_server_url, DataFieldnameStrings.TaskId: job_id}))
        if response.response_ok is True:
            return True
        else:
            raise StopJobError()

    def get_job_run_status(self, job_id):
        self._verify_connected()
        response = self._send_informatica_request(GetJobRunStatusStrategy({DataFieldnameStrings.ICSessionId: self.ic_session_id, DataFieldnameStrings.ServerUrl: self.login_server_url, DataFieldnameStrings.TaskId: job_id}))
        if response.response_ok is True:
            return response.job_status
        else:
            raise GetJobRunStatusesError()
