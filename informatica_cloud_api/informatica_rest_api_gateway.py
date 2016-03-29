import logging
import requests
import abc
import standard_python_app
import json
from module_resources import DataFieldnameStrings
from module_resources import GeneralConstants


API_URL_PART = '/api/v2'


class Payload(object):
    def __init__(self):
        self.payload_body = {}
        self.headers = {}


class InformaticaJobExecutionStates(object):
    Stopped = 'STOPPED'
    Running = 'RUNNING'
    Initialized = 'INITIALIZED'
    Stopping = 'STOPPING'


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
        raise NotImplementedError

    def _process_requests_response(self, requests_response):
        if requests_response.status_code == GeneralConstants.HttpStatusOK:
            return self._process_response_json(requests_response.json())
        else:
            to_return = LoginResponse()
            to_return.response_ok = False
            return to_return

    def _process_response_json(self, requests_response_jsonified):
        to_return = LoginResponse()
        to_return.response_ok = True
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
        raise NotImplementedError


class StartJobStrategy(BaseStrategy):
    def __init__(self, data):
        super(StartJobStrategy, self).__init__(data)
        self.uri = '/job'

    def _formulate_payload(self):
        payload = Payload()
        taskType = GeneralConstants.DefaultTaskType
        if DataFieldnameStrings.TaskType in self.data:
            taskType = self.data[DataFieldnameStrings.TaskType]
        payload.payload_body = {DataFieldnameStrings.TaskId: self.data[DataFieldnameStrings.TaskId], DataFieldnameStrings.TaskType: taskType}
        payload.headers = {'Accept': 'application/json', DataFieldnameStrings.ICSessionId: self.data[DataFieldnameStrings.ICSessionId]}
        return payload

    def _get_fully_constructed_url(self):
        return '{}{}{}'.format(self.data[DataFieldnameStrings.ServerUrl], API_URL_PART, self.uri)

    def _do_http_request(self, payload):
        raise NotImplementedError


class StopJobStrategy(BaseStrategy):
    def __init__(self, data):
        super(StopJobStrategy, self).__init__(data)
        self.uri = '/job/stop'

    def _formulate_payload(self):
        payload = Payload()
        taskType = GeneralConstants.DefaultTaskType
        if DataFieldnameStrings.TaskType in self.data:
            taskType = self.data[DataFieldnameStrings.TaskType]
        payload.payload_body = {DataFieldnameStrings.TaskId: self.data[DataFieldnameStrings.TaskId], DataFieldnameStrings.TaskType: taskType}
        payload.headers = {'Accept': 'application/json', DataFieldnameStrings.ICSessionId: self.data[DataFieldnameStrings.ICSessionId]}
        return payload

    def _get_fully_constructed_url(self):
        return '{}{}{}'.format(self.data[DataFieldnameStrings.ServerUrl], API_URL_PART, self.uri)

    def _do_http_request(self, payload):
        raise NotImplementedError


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
        raise NotImplementedError

    def _process_requests_response(self, requests_response):
        if requests_response.status_code == GeneralConstants.HttpStatusOK:
            return self._process_response_json(requests_response.json())
        else:
            to_return = JobRunStatusResponse()
            to_return.response_ok = False
            return to_return

    def _process_response_json(self, requests_response_jsonified):
        to_return = JobRunStatusResponse()
        to_return.response_ok = True
        task_id_to_find = self.data[DataFieldnameStrings.TaskId]
        to_return.job_status.job_id = task_id_to_find
        to_return.job_status.current_job_execution_state = InformaticaJobExecutionStates.Stopped
        for activity_monitor_entry in requests_response_jsonified:
            if activity_monitor_entry[DataFieldnameStrings.TaskId] == task_id_to_find:
                to_return.job_status.current_job_execution_state = activity_monitor_entry['executionState']
        return to_return


class InformaticaRestApiGateway(object):
    def __init__(self, username, password, login_endpoint):
        self.username = username
        self.password = password
        self.login_endpoint = login_endpoint
        self.login_session_id = None
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
            self.login_session_id = response.login_data.login_session_id
            self.login_server_url = response.login_data.login_server_url
        else:
            raise LoginError()

    def close_connection(self):
        self._verify_connected()
        response = self._send_informatica_request(LogoutStrategy({DataFieldnameStrings.UserName: self.username, DataFieldnameStrings.Password: self.password, DataFieldnameStrings.LoginEndpoint: self.login_endpoint}))
        if response.response_ok is True:
            self.is_connected = False
            self.login_session_id = None
            self.login_server_url = None
        else:
            raise LogoutError()

    def start_job(self, job_id):
        self._verify_connected()
        response = self._send_informatica_request(StartJobStrategy({DataFieldnameStrings.SessionId: self.login_session_id, DataFieldnameStrings.ServerUrl: self.login_server_url, DataFieldnameStrings.TaskId: job_id}))
        if response.response_ok is True:
            return True
        else:
            raise StartJobError()

    def stop_job(self, job_id):
        self._verify_connected()
        response = self._send_informatica_request(StopJobStrategy({DataFieldnameStrings.SessionId: self.login_session_id, DataFieldnameStrings.ServerUrl: self.login_server_url, DataFieldnameStrings.TaskId: job_id}))
        if response.response_ok is True:
            return True
        else:
            raise StopJobError()

    def get_job_run_status(self, job_id):
        self._verify_connected()
        response = self._send_informatica_request(GetJobRunStatusStrategy({DataFieldnameStrings.SessionId: self.login_session_id, DataFieldnameStrings.ServerUrl: self.login_server_url, DataFieldnameStrings.TaskId: job_id}))
        if response.response_ok is True:
            return response.job_status
        else:
            raise GetJobRunStatusesError()


class InformaticaRestApiGatewayTesterProgramCommandLineArgs(standard_python_app.CommandLineArgs):
    def __init__(self):
        super(InformaticaRestApiGatewayTesterProgramCommandLineArgs, self).__init__()

    def get_program_description(self):
        return 'Testing bootstrapper'

    def add_program_specific_arguments(self):
        pass

    def validate(self):
        pass

    def set_parsed_args_on_class(self):
        pass

    def has_required_command_line_arguments(self):
        return True


class InformaticaRestApiGatewayTesterProgram(standard_python_app.StandardPythonApp):

    def execute(self):
        pass

    def initialize_logger(self):
        logging.basicConfig(level=logging.INFO)

    def instantiate_command_line_args(self):
        return InformaticaRestApiGatewayTesterProgramCommandLineArgs()


if __name__ == '__main__':
    program = InformaticaRestApiGatewayTesterProgram()
    program.bootstrapper()
