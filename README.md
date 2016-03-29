# informatica_cloud_python_api
Python client API for interacting with Informatica Cloud REST API

# Setup
This is a client API to be used to connect to the Informatica Cloud REST API using Python. To use it, import informatica_rest_api_gateway and create an instance of InformaticaRestApiGateway as such:

	access = informatica_rest_api_gateway.InformaticaRestApiGateway('someuser@expedia.com', 'aPassword', 'anEndpoint')
	
Install all requirements into your interpreter environment using: 

	pip install -r 'requirements.txr'
	
To run unit tests:

	python -m unittest -v informatica_rest_api_gateway_test
	python -m unittest -v strategy_method_tests
	
I have not yet tested this with Python 3, though I'd assume it works OK.
	
#API Method Support
As of now, the following functionality is supported:

* Login
* Logout
* Start Job
* Stop Job
* Get Job Execution Status
	
# Usage Examples
See informatica_rest_api_gateway_test.py for basic usage examples.