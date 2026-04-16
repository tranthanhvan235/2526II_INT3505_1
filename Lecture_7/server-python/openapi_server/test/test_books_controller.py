import unittest

from flask import json

from openapi_server.models.book import Book  # noqa: E501
from openapi_server.models.book_list_response import BookListResponse  # noqa: E501
from openapi_server.models.book_request import BookRequest  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.test import BaseTestCase


class TestBooksController(BaseTestCase):
    """BooksController integration test stubs"""

    def test_create_book(self):
        """Test case for create_book

        Create a new book
        """
        book_request = {"price":45.99,"isbn":"9780132350884","publishDate":"2008-08-01","title":"Clean Code","authorId":"550e8400-e29b-41d4-a716-446655440000","categoryId":"550e8400-e29b-41d4-a716-446655440001"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/books',
            method='POST',
            headers=headers,
            data=json.dumps(book_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_book(self):
        """Test case for delete_book

        Delete a book
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/books/{id}'.format(id=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_book_by_id(self):
        """Test case for get_book_by_id

        Get book details
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/books/{id}'.format(id=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_books(self):
        """Test case for get_books

        Get all books
        """
        query_string = [('page', 1),
                        ('limit', 10),
                        ('search', 'search_example'),
                        ('categoryId', UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d'))]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/books',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_book(self):
        """Test case for update_book

        Update a book
        """
        book_request = {"price":45.99,"isbn":"9780132350884","publishDate":"2008-08-01","title":"Clean Code","authorId":"550e8400-e29b-41d4-a716-446655440000","categoryId":"550e8400-e29b-41d4-a716-446655440001"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/books/{id}'.format(id=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
            method='PUT',
            headers=headers,
            data=json.dumps(book_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
