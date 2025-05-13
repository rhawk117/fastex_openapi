from ._registry import _Registry
from pydantic import BaseModel
from typing import Any, Dict, Optional, Type, TypedDict


class ResponseSpec(TypedDict, total=False):
    '''schema for a single HTTP response in OpenAPI.'''
    description: str
    model: Type[BaseModel]
    headers: Dict[str, Any]



def _make_response(
    status_code: int,
    description: str,
    model: Type[BaseModel],
    headers: Optional[Dict[str, Any]] = None,
) -> Dict[int, ResponseSpec]:
    spec: ResponseSpec = {"description": description, "model": model}
    if headers:
        spec["headers"] = headers
    return {status_code: spec}


def set_openapi_responses(
    *,
    default_error_model: Type[BaseModel],
    validation_error_model: Optional[Type[BaseModel]] = None,
) -> None:
    """Call once at startup to set up your global error schemas."""
    _Registry.configure(
        default_error_model=default_error_model,
        validation_error_model=validation_error_model,
    )



def error_response(
    status_code: int,
    *,
    description: str,
    model: Type[BaseModel] | None = None,
    headers: Optional[Dict[str, Any]] = None,
) -> Dict[int, ResponseSpec]:
    """
    Generate an error response spec. If `model` is omitted,
    uses the globally configured default_error_model.
    """
    if model is None:
        model = _Registry.get_error_model()
    return _make_response(
        status_code=status_code,
        description=description,
        model=model,
        headers=headers,
    )


def api_response(
    status_code: int,
    *,
    description: str,
    model: Type[BaseModel],
    headers: Optional[Dict[str, Any]] = None,
) -> Dict[int, ResponseSpec]:
    """Generate a normal (non-error) response spec."""
    return _make_response(
        status_code=status_code,
        description=description,
        model=model,
        headers=headers,
    )


def response_list(
    *response_dicts: Dict[int, ResponseSpec]
) -> Dict[int, ResponseSpec]:
    '''a tuple of api_response() or error_response() dicts
    merged into a single dict.

    Raises:
        ValueError: _if duplicate status codes appear_

    Returns:
        Dict[int, ResponseSpec]: _the response definition_
    '''
    merged: Dict[int, ResponseSpec] = {}
    for resp in response_dicts:
        for code, spec in resp.items():
            if code in merged:
                raise ValueError(f"Duplicate response for status {code}")
            merged[code] = spec
    return merged
