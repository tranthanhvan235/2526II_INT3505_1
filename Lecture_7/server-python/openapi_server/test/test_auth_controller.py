import unittest

from flask import json

from openapi_server.models.auth_response import AuthResponse  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.login_request import LoginRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestAuthController(BaseTestCase):
    """AuthController integration test stubs"""

    def test_login(self):
        """Test case for login

        User Login
        """
        login_request = {"password":"secret123","email":"admin@example.com"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/auth/login',
            method='POST',
            headers=headers,
            data=json.dumps(login_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
