# AuthorRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**biography** | **str** |  | [optional] 
**birth_date** | **date** |  | [optional] 

## Example

```python
from openapi_client.models.author_request import AuthorRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AuthorRequest from a JSON string
author_request_instance = AuthorRequest.from_json(json)
# print the JSON string representation of the object
print(AuthorRequest.to_json())

# convert the object into a dict
author_request_dict = author_request_instance.to_dict()
# create an instance of AuthorRequest from a dict
author_request_from_dict = AuthorRequest.from_dict(author_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


