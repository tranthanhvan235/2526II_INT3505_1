import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.author import Author  # noqa: E501
from openapi_server.models.author_list_response import AuthorListResponse  # noqa: E501
from openapi_server.models.author_request import AuthorRequest  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server import util


def create_author(body):  # noqa: E501
    """Create a new author

    Add a new author to the system (Admin privileges required). # noqa: E501

    :param author_request: 
    :type author_request: dict | bytes

    :rtype: Union[Author, Tuple[Author, int], Tuple[Author, int, Dict[str, str]]
    """
    author_request = body
    if connexion.request.is_json:
        author_request = AuthorRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_authors(page=None, limit=None):  # noqa: E501
    """Get all authors

    Retrieve a paginated list of authors. # noqa: E501

    :param page: The page number to retrieve
    :type page: int
    :param limit: Number of items per page
    :type limit: int

    :rtype: Union[AuthorListResponse, Tuple[AuthorListResponse, int], Tuple[AuthorListResponse, int, Dict[str, str]]
    """
    return 'do some magic!'
