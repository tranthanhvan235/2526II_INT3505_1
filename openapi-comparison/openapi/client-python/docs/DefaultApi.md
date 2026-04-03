# openapi_client.DefaultApi

All URIs are relative to *http://localhost:8080*

Method | HTTP request | Description
------------- | ------------- | -------------
[**books_book_id_delete**](DefaultApi.md#books_book_id_delete) | **DELETE** /books/{book_id} | Remove a book from the library
[**books_book_id_get**](DefaultApi.md#books_book_id_get) | **GET** /books/{book_id} | Get book details by ID
[**books_book_id_put**](DefaultApi.md#books_book_id_put) | **PUT** /books/{book_id} | Update an existing book
[**books_get**](DefaultApi.md#books_get) | **GET** /books | List all books
[**books_post**](DefaultApi.md#books_post) | **POST** /books | Create a new book


# **books_book_id_delete**
> books_book_id_delete(book_id)

Remove a book from the library

### Example


```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8080
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    book_id = 'book_id_example' # str | 

    try:
        # Remove a book from the library
        api_instance.books_book_id_delete(book_id)
    except Exception as e:
        print("Exception when calling DefaultApi->books_book_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **book_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Book deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **books_book_id_get**
> Book books_book_id_get(book_id)

Get book details by ID

### Example


```python
import openapi_client
from openapi_client.models.book import Book
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8080
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    book_id = 'book_id_example' # str | 

    try:
        # Get book details by ID
        api_response = api_instance.books_book_id_get(book_id)
        print("The response of DefaultApi->books_book_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->books_book_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **book_id** | **str**|  | 

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
**200** | Book found |  -  |
**404** | Book not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **books_book_id_put**
> books_book_id_put(book_id, book=book)

Update an existing book

### Example


```python
import openapi_client
from openapi_client.models.book import Book
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8080
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    book_id = 'book_id_example' # str | 
    book = openapi_client.Book() # Book |  (optional)

    try:
        # Update an existing book
        api_instance.books_book_id_put(book_id, book=book)
    except Exception as e:
        print("Exception when calling DefaultApi->books_book_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **book_id** | **str**|  | 
 **book** | [**Book**](Book.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Book updated |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **books_get**
> List[Book] books_get()

List all books

### Example


```python
import openapi_client
from openapi_client.models.book import Book
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8080
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)

    try:
        # List all books
        api_response = api_instance.books_get()
        print("The response of DefaultApi->books_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->books_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[Book]**](Book.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of books |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **books_post**
> books_post(book)

Create a new book

### Example


```python
import openapi_client
from openapi_client.models.book import Book
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8080
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    book = openapi_client.Book() # Book | 

    try:
        # Create a new book
        api_instance.books_post(book)
    except Exception as e:
        print("Exception when calling DefaultApi->books_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **book** | [**Book**](Book.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Book created successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

