import logging
import informatica_rest_api_gateway_test
import requests
import abc
import standard_python_app


class Payload(object):
    def __init__(self):
        self.payload_body = {}
        self.headers = {}


class InformaticaJobStates(object):
    Stopped = 1
    Running = 2


class InformaticaJobRunStates(object):
    Success = 1
    CompleteWithErrors = 2
    Fail = 3


class JobStatus(object):
    def __init__(self, job_id, last_result, current_state):
        self.job_id = job_id
        self.last_result = last_result
        self.current_state = current_state


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


class GetJobStatusesError(StandardError):
    pass


class JobStatusResponse(Response):
    def __init__(self):
        super(JobStatusResponse, self).__init__()
        self.job_status = None


class BaseStrategy(object):
    def request_template_algorithm(self, data):
        payload = self._formulate_payload(data)
        requests_response = self._do_http_request(payload)
        return self._process_response(requests_response)

    @abc.abstractmethod
    def _formulate_payload(self, data):
        pass

    @abc.abstractmethod
    def _do_http_request(self, payload):
        pass

    @abc.abstractmethod
    def _process_response(self, requests_response):
        pass


class LoginStrategy(BaseStrategy):
    def _formulate_payload(self, data):
        payload = Payload()
        payload.payload_body = {'username': data['username'], 'password': data['password'], '@type': 'login'}
        payload.headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        return payload

    def _do_http_request(self, payload):
        raise NotImplementedError

    def _process_response(self, requests_response):
        raise NotImplementedError


class LogoutStrategy(BaseStrategy):
    def _formulate_payload(self, data):
        payload = Payload()
        payload.payload_body = {'username': data['username'], 'password': data['password'], '@type': 'logout'}
        payload.headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        return payload

    def _do_http_request(self, payload):
        raise NotImplementedError

    def _process_response(self, requests_response):
        raise NotImplementedError


class StartJobStrategy(BaseStrategy):
    def _formulate_payload(self, data):
        raise NotImplementedError

    def _do_http_request(self, payload):
        raise NotImplementedError

    def _process_response(self, requests_response):
        raise NotImplementedError


class StopJobStrategy(BaseStrategy):
    def _formulate_payload(self, data):
        raise NotImplementedError

    def _do_http_request(self, payload):
        raise NotImplementedError

    def _process_response(self, requests_response):
        raise NotImplementedError


class GetJobStatusStrategy(BaseStrategy):
    def _formulate_payload(self, data):
        raise NotImplementedError

    def _do_http_request(self, payload):
        raise NotImplementedError

    def _process_response(self, requests_response):
        raise NotImplementedError


class InformaticaRestApiGateway(object):
    def __init__(self, username, password, endpoint):
        self.username = username
        self.password = password
        self.endpoint = endpoint
        self.login_session_id = None
        self.login_server_url = None
        self.is_connected = False

    def _verify_connected(self):
        if not self.is_connected:
            raise LoginRequiredError()

    def _send_informatica_request(self, data, strategy):
        return strategy.request_template_algorithm(data)

    def connect(self):
        response = self._send_informatica_request({'username': self.username, 'password': self.password, 'endpoint': self.endpoint}, LoginStrategy())
        if response.response_ok is True:
            self.is_connected = True
            self.login_session_id = response.login_data.login_session_id
            self.login_server_url = response.login_data.login_server_url
        else:
            raise LoginError()

    def close_connection(self):
        self._verify_connected()
        response = self._send_informatica_request({'username': self.username, 'password': self.password, 'endpoint': self.endpoint}, LogoutStrategy())
        if response.response_ok is True:
            self.is_connected = False
            self.login_session_id = None
            self.login_server_url = None
        else:
            raise LogoutError()

    def start_job(self, job_id):
        self._verify_connected()
        response = self._send_informatica_request({'session_id': self.login_session_id, 'server_url': self.login_server_url, 'job_id': job_id}, StartJobStrategy())
        if response.response_ok is True:
            return True
        else:
            raise StartJobError()

    def stop_job(self, job_id):
        self._verify_connected()
        response = self._send_informatica_request({'session_id': self.login_session_id, 'server_url': self.login_server_url, 'job_id': job_id}, StopJobStrategy())
        if response.response_ok is True:
            return True
        else:
            raise StopJobError()

    def get_job_status(self, job_id):
        self._verify_connected()
        response = self._send_informatica_request({'session_id': self.login_session_id, 'server_url': self.login_server_url, 'job_id': job_id}, GetJobStatusStrategy())
        if response.response_ok is True:
            return response.job_status
        else:
            raise GetJobStatusesError()


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

    def get_test_case_class(self):
        return informatica_rest_api_gateway_test.InformaticaRestAccessTest


if __name__ == '__main__':
    program = InformaticaRestApiGatewayTesterProgram()
    program.bootstrapper()
