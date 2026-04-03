import unittest

from flask import json

from openapi_server.models.book import Book  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_books_book_id_delete(self):
        """Test case for books_book_id_delete

        Remove a book from the library
        """
        headers = { 
        }
        response = self.client.open(
            '/books/{book_id}'.format(book_id='book_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_book_id_get(self):
        """Test case for books_book_id_get

        Get book details by ID
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/books/{book_id}'.format(book_id='book_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_book_id_put(self):
        """Test case for books_book_id_put

        Update an existing book
        """
        book = {"author":"J.J. Geewax","id":"BK-2302","publishedYear":2021,"title":"API Design Patterns"}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/books/{book_id}'.format(book_id='book_id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(book),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_get(self):
        """Test case for books_get

        List all books
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/books',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_post(self):
        """Test case for books_post

        Create a new book
        """
        book = {"author":"J.J. Geewax","id":"BK-2302","publishedYear":2021,"title":"API Design Patterns"}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/books',
            method='POST',
            headers=headers,
            data=json.dumps(book),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
