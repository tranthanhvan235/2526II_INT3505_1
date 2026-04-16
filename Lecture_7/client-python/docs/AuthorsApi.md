# openapi_client.AuthorsApi

All URIs are relative to *http://localhost:8080/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_author**](AuthorsApi.md#create_author) | **POST** /authors | Create a new author
[**get_authors**](AuthorsApi.md#get_authors) | **GET** /authors | Get all authors


# **create_author**
> Author create_author(author_request)

Create a new author

Add a new author to the system (Admin privileges required).

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import openapi_client
from openapi_client.models.author import Author
from openapi_client.models.author_request import AuthorRequest
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
    api_instance = openapi_client.AuthorsApi(api_client)
    author_request = openapi_client.AuthorRequest() # AuthorRequest | 

    try:
        # Create a new author
        api_response = api_instance.create_author(author_request)
        print("The response of AuthorsApi->create_author:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthorsApi->create_author: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **author_request** | [**AuthorRequest**](AuthorRequest.md)|  | 

### Return type

[**Author**](Author.md)

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

# **get_authors**
> AuthorListResponse get_authors(page=page, limit=limit)

Get all authors

Retrieve a paginated list of authors.

### Example


```python
import openapi_client
from openapi_client.models.author_list_response import AuthorListResponse
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
    api_instance = openapi_client.AuthorsApi(api_client)
    page = 1 # int | The page number to retrieve (optional) (default to 1)
    limit = 10 # int | Number of items per page (optional) (default to 10)

    try:
        # Get all authors
        api_response = api_instance.get_authors(page=page, limit=limit)
        print("The response of AuthorsApi->get_authors:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthorsApi->get_authors: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| The page number to retrieve | [optional] [default to 1]
 **limit** | **int**| Number of items per page | [optional] [default to 10]

### Return type

[**AuthorListResponse**](AuthorListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the list of authors |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

