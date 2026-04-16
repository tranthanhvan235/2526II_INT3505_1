import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.auth_response import AuthResponse  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.login_request import LoginRequest  # noqa: E501
from openapi_server import util


def login(body):  # noqa: E501
    """User Login

    Authenticate using email and password to receive a JWT Access Token. # noqa: E501

    :param login_request: 
    :type login_request: dict | bytes

    :rtype: Union[AuthResponse, Tuple[AuthResponse, int], Tuple[AuthResponse, int, Dict[str, str]]
    """
    login_request = body
    if connexion.request.is_json:
        login_request = LoginRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
