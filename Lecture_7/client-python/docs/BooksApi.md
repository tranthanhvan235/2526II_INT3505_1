# openapi_client.BooksApi

All URIs are relative to *http://localhost:8080/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_book**](BooksApi.md#create_book) | **POST** /books | Create a new book
[**delete_book**](BooksApi.md#delete_book) | **DELETE** /books/{id} | Delete a book
[**get_book_by_id**](BooksApi.md#get_book_by_id) | **GET** /books/{id} | Get book details
[**get_books**](BooksApi.md#get_books) | **GET** /books | Get all books
[**update_book**](BooksApi.md#update_book) | **PUT** /books/{id} | Update a book


# **create_book**
> Book create_book(book_request)

Create a new book

Add a new book to the catalog (Admin privileges required).

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import openapi_client
from openapi_client.models.book import Book
from openapi_client.models.book_request import BookRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8080/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): bearerAuth
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.BooksApi(api_client)
    book_request = openapi_client.BookRequest() # BookRequest | 

    try:
        # Create a new book
        api_response = api_instance.create_book(book_request)
        print("The response of BooksApi->create_book:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BooksApi->create_book: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **book_request** | [**BookRequest**](BookRequest.md)|  | 

### Return type

[**Book**](Book.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully created |  -  |
**400** | Invalid input data (Validation Error) |  -  |
**401** | Missing or invalid Authentication Token |  -  |
**403** | Access denied (e.g., standard user attempting to access admin endpoints) |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_book**
> delete_book(id)

Delete a book

Remove a book from the system completely (Admin privileges required).

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8080/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): bearerAuth
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.BooksApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Unique identifier (UUID) of the resource

    try:
        # Delete a book
        api_instance.delete_book(id)
    except Exception as e:
        print("Exception when calling BooksApi->delete_book: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**| Unique identifier (UUID) of the resource | 

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted (No content returned) |  -  |
**401** | Missing or invalid Authentication Token |  -  |
**403** | Access denied (e.g., standard user attempting to access admin endpoints) |  -  |
**404** | The requested resource was not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_book_by_id**
> Book get_book_by_id(id)

Get book details

Retrieve detailed information of a specific book by its ID.

### Example


```python
import openapi_client
from openapi_client.models.book import Book
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8080/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080/api/v1"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.BooksApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Unique identifier (UUID) of the resource

    try:
        # Get book details
        api_response = api_instance.get_book_by_id(id)
        print("The response of BooksApi->get_book_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BooksApi->get_book_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**| Unique identifier (UUID) of the resource | 

### Return type

[**Book**](Book.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved book details |  -  |
**404** | The requested resource was not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_books**
> BookListResponse get_books(page=page, limit=limit, search=search, category_id=category_id)

Get all books

Retrieve a paginated list of books with search and filter capabilities.

### Example


```python
import openapi_client
from openapi_client.models.book_list_response import BookListResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8080/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080/api/v1"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.BooksApi(api_client)
    page = 1 # int | The page number to retrieve (optional) (default to 1)
    limit = 10 # int | Number of items per page (optional) (default to 10)
    search = 'search_example' # str | Search by book title or ISBN (optional)
    category_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Filter books by Category ID (optional)

    try:
        # Get all books
        api_response = api_instance.get_books(page=page, limit=limit, search=search, category_id=category_id)
        print("The response of BooksApi->get_books:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BooksApi->get_books: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| The page number to retrieve | [optional] [default to 1]
 **limit** | **int**| Number of items per page | [optional] [default to 10]
 **search** | **str**| Search by book title or ISBN | [optional] 
 **category_id** | **UUID**| Filter books by Category ID | [optional] 

### Return type

[**BookListResponse**](BookListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the list of books |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_book**
> Book update_book(id, book_request)

Update a book

Update information of an existing book by its ID (Admin privileges required).

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import openapi_client
from openapi_client.models.book import Book
from openapi_client.models.book_request import BookRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8080/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): bearerAuth
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.BooksApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Unique identifier (UUID) of the resource
    book_request = openapi_client.BookRequest() # BookRequest | 

    try:
        # Update a book
        api_response = api_instance.update_book(id, book_request)
        print("The response of BooksApi->update_book:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BooksApi->update_book: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**| Unique identifier (UUID) of the resource | 
 **book_request** | [**BookRequest**](BookRequest.md)|  | 

### Return type

[**Book**](Book.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully updated |  -  |
**400** | Invalid input data (Validation Error) |  -  |
**401** | Missing or invalid Authentication Token |  -  |
**403** | Access denied (e.g., standard user attempting to access admin endpoints) |  -  |
**404** | The requested resource was not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

