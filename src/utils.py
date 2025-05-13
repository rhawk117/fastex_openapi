import json

from fastapi import FastAPI
from fastapi.routing import APIRoute


def create_operation_id(route: APIRoute) -> str:
    '''Generates a unique id for the route to help normalize
    the API service names.
    https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function
    Returns:
        str -- the adjusted operation ID
    '''
    return f"{route.tags[0]}-{route.name}" # type: ignore


def normalize_route_path_names(openapi_schema: dict) -> dict:
    '''Normalizes service names from "userGetAllUsers" to "getAllUsers"

    Taken directly from 
        https://fastapi.tiangolo.com/advanced/generate-clients/#preprocess-the-openapi-specification-for-the-client-generator

    Arguments:
        openapi_schema {dict} -- the openapi schema of the app

    Returns:
        dict -- the normalized openapi schema
    '''
    path_schema: dict[str, dict] = openapi_schema['paths']

    for path_data in path_schema.values():
        for operation in path_data.values():
            tag = operation['tags'][0]
            operation_id = operation['operationId']
            to_remove = f'{tag}-'
            new_operation_id = operation_id[len(to_remove):]
            operation['operationId'] = new_operation_id

    return openapi_schema


def export_openapi_json(
    *,
    app: FastAPI,
    destination: str = 'openapi.json'
) -> None:
    '''Exports the openapi schema to a json file

    Arguments:
        app {FastAPI} -- the fastapi app instance
        destination {str} -- the destination file name
    '''
    openapi_schema = app.openapi()
    openapi_schema = normalize_path_names(openapi_schema)
    with open(destination, 'w') as f:
        json_str = json.dumps(openapi_schema, indent=2)
        f.write(json_str)


