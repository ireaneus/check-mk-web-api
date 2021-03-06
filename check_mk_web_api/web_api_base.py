import ast
import json
import logging
import os.path
import re

from six.moves import urllib

from check_mk_web_api.activate_mode import ActivateMode
from check_mk_web_api.exception import CheckMkWebApiResponseException, CheckMkWebApiException, \
    CheckMkWebApiAuthenticationException
from check_mk_web_api.no_none_value_dict import NoNoneValueDict


class WebApiBase:

    """
    Abstraction for Check_Mk Web API

    # Arguments
    check_mk_url (str): URL to Check_Mk web application, multiple formats are supported
    username (str): Name of user to connect as. Make sure this is an automation user.
    secret (str): Secret for automation user. This is different from the password!

    # Examples
    ```python
    WebApi('http://checkmk.company.com/monitor/check_mk/webapi.py', 'automation', 'secret')
    ```
    ```python
    WebApi('http://checkmk.company.com/monitor/check_mk', 'automation', 'secret')
    ```
    ```python
    WebApi('http://checkmk.company.com/monitor', 'automation', 'secret')
    ```
    """

    __DISCOVERY_REGEX = {
        'added': re.compile(r'.*Added (\d+),.*'),
        'removed': re.compile(r'.*Removed (\d+),.*'),
        'kept': re.compile(r'.*Kept (\d+),.*'),
        'new_count': re.compile(r'.*New Count (\d+)$')
    }

    def __init__(self, check_mk_url, username, secret):
        check_mk_url = check_mk_url.rstrip('/')

        if check_mk_url.endswith('.py'):  # ends with /webapi.py
            self.web_api_base = check_mk_url
        elif check_mk_url.endswith('check_mk'):  # ends with /$SITE_NAME/check_mk
            self.web_api_base = os.path.join(check_mk_url, 'webapi.py')
        else:  # ends with /$SITE_NAME
            self.web_api_base = os.path.join(check_mk_url, 'check_mk', 'webapi.py')

        self.web_view_base = self.web_api_base.replace('webapi', 'view')

        self.username = username
        self.secret = secret

    @staticmethod
    def __build_request_data(data, request_format):
        if not data:
            return None

        if request_format == 'json':
            request_string = 'request=' + json.dumps(data)
        elif request_format == 'python':
            request_string = 'request=' + str(data)
        else:
            return CheckMkWebApiResponseException(data)

        return request_string.encode()

    def __build_request_path(self, query_params=None):

        path = self.web_api_base + '?'

        query_params = self.__check_query_params(query_params)

        query_params.update({
            '_username': self.username,
            '_secret': self.secret
        })

        query_string = urllib.parse.urlencode(query_params)

        path += query_string

        return path

    def __build_view_request_path(self, query_params):
        path = self.web_view_base + '?'

        query_params = self.__check_query_params(query_params)
        query_params['output_format'] = query_params.get('output_format', 'json')

        query_params.update({
            '_username': self.username,
            '_secret': self.secret,
        })

        query_string = urllib.parse.urlencode(query_params)

        path += query_string

        return path

    def __check_query_params(self, query_params):
        if not query_params:
            return {}

        return dict(query_params)

    def __parse_response_body(self, body, query_params):
        if 'output_format' in query_params:
            if query_params['output_format'] == 'python':
                return ast.literal_eval(body)

            if query_params['output_format'] == 'json':
                try:
                    return json.loads(body)
                except json.decoder.JSONDecodeError as error:
                    return body

        return body

    def __decode_response(self, response, query_params={'output_format': 'json'}):
        if response.code != 200:
            raise CheckMkWebApiResponseException(response)

        body = response.read().decode()

        if body.startswith('Authentication error:'):
            raise CheckMkWebApiAuthenticationException(body)

        body_dict = self.__parse_response_body(body, query_params)

        # Views return json lists and not dicts of information.
        # Validate the result is a list, return result

        if isinstance(body_dict, list):
            return body_dict

        result = body_dict['result']

        if body_dict['result_code'] == 0:
            return result

        raise CheckMkWebApiException(result)

    def __make_call(self, query, data):
        """
        Wrapper for all calls to CheckMK service

        # Arguments
        query: unstructured query from internal calls

        # Raises
        CheckMkWebApiResponseException: Raised when the HTTP status code != 200
        CheckMkWebApiException: Raised when the action's result_code != 0
        """

        query_params = self.__check_query_params(query)

        request_format = query_params.get('request_format', 'json')
        query_params['output_format'] = query_params.get('output_format', 'json')

        built_request = [
            self.__build_request_path(query_params),
            WebApiBase.__build_request_data(data, request_format)
        ]

        logging.debug('Request built url and arguments', built_request)

        response = urllib.request.urlopen(
            *built_request
        )

        return self.__decode_response(response, query_params)

    def make_view_request(self, query, data=None):
        """
        Make calls to services that require view.py url's

        # Arguments
        query: block of query params to append to url
        data: data to post to form in a dict format

        # Raises
        CheckMkWebApiResponseException: Raised when the HTTP status code != 200
        CheckMkWebApiException: Raised when the action's result_code != 0
        """
        query_params = self.__check_query_params(query)

        query_params['output_format'] = query_params.get('output_format', 'json')
        request_format = query_params.get('request_format', 'json')

        built_request = [
            self.__build_view_request_path(query_params),  # call to correct endpoint
            WebApiBase.__build_request_data(data, request_format)
        ]

        print('Request built url and arguments')
        print(built_request)

        response = urllib.request.urlopen(
            *built_request
        )

        return self.__decode_response(response)

    def make_view_name_request(self, view_name, query=None, data=None):
        """
        Make calls to get View

        # Arguments
        viewName: name of view to get e.g. downtimes

        # Raises
        CheckMkWebApiResponseException: Raised when the HTTP status code != 200
        CheckMkWebApiException: Raised when the action's result_code != 0
        """

        built_request = [
            self.__build_view_request_path({'view_name': view_name}),  # call to correct endpoint
            None
        ]

        logging.debug('Request built url and arguments', built_request)

        response = urllib.request.urlopen(
            *built_request
        )

        # TODO: investigate query parameters req for code response

        return self.__decode_response(response)

    def make_request(self, action, query_params=None, data=None):
        """
        Make arbitrary request to Check_Mk Web API

        # Arguments
        action (str): Action request, e.g. add_host
        query_params (dict): dict of path parameters
        data (dict): dict that will be sent as request body

        # Raises
        CheckMkWebApiResponseException: Raised when the HTTP status code != 200
        CheckMkWebApiException: Raised when the action's result_code != 0
        """
        query_params = self.__check_query_params(query_params)

        query_params.update({'action': action})

        return self.__make_call(query_params, data)

    def activate_changes(self, mode=ActivateMode.DIRTY,
                         sites=None, allow_foreign_changes=False):
        """
        Activates all changes previously done

        # Arguments
        mode (ActivateMode): see #WebApi.ActivateMode
        sites (list): List of sites to activates changes on
        allow_foreign_changes (bool): If True changes of other users will be applied as well
        """
        data = NoNoneValueDict({
            'sites': sites
        })

        query_params = {
            'mode': mode.value,
            'allow_foreign_changes': 1 if allow_foreign_changes else 0
        }

        return self.make_request('activate_changes', query_params=query_params, data=data)
