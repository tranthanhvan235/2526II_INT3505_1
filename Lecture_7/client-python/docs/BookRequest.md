# BookRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**isbn** | **str** |  | 
**price** | **float** |  | 
**publish_date** | **date** |  | [optional] 
**author_id** | **UUID** |  | 
**category_id** | **UUID** |  | 

## Example

```python
from openapi_client.models.book_request import BookRequest

# TODO update the JSON string below
json = "{}"
# create an instance of BookRequest from a JSON string
book_request_instance = BookRequest.from_json(json)
# print the JSON string representation of the object
print(BookRequest.to_json())

# convert the object into a dict
book_request_dict = book_request_instance.to_dict()
# create an instance of BookRequest from a dict
book_request_from_dict = BookRequest.from_dict(book_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


