import unittest

from flask import json

from openapi_server.models.author import Author  # noqa: E501
from openapi_server.models.author_list_response import AuthorListResponse  # noqa: E501
from openapi_server.models.author_request import AuthorRequest  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.test import BaseTestCase


class TestAuthorsController(BaseTestCase):
    """AuthorsController integration test stubs"""

    def test_create_author(self):
        """Test case for create_author

        Create a new author
        """
        author_request = {"name":"name","biography":"biography","birthDate":"2000-01-23"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/authors',
            method='POST',
            headers=headers,
            data=json.dumps(author_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_authors(self):
        """Test case for get_authors

        Get all authors
        """
        query_string = [('page', 1),
                        ('limit', 10)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/authors',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
