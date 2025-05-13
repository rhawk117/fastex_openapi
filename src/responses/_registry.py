from pydantic import BaseModel

from typing import Optional, Self, Type


class OpenAPIConfig(TypedDict, total=False):
    '''stored in the registry for the default error model and validation error model.'''
    default_error_model: Type[BaseModel]
    validation_error_model: Type[BaseModel]

class _Registry:
    _instance: Self | None = None
    _config: OpenAPIConfig

    def __new__(cls) -> '_Registry':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = {}
        return cls._instance

    @classmethod
    def configure(
        cls,
        *,
        default_error_model: Type[BaseModel],
        validation_error_model: Optional[Type[BaseModel]] = None,
    ) -> None:
        inst = cls()
        inst._config["default_error_model"] = default_error_model
        if validation_error_model is not None:
            inst._config["validation_error_model"] = validation_error_model

    @classmethod
    def get_error_model(cls) -> Type[BaseModel]:
        inst = cls()
        model = inst._config.get("default_error_model")
        if model is None:
            raise RuntimeError(
                "FastexOpenAPIConfig not initialized. "
                "Call `configure()` before using `error_response`."
            )
        return model

    def __repr__(self) -> str:
        return f"OpenAPIConfig({self._config!r})"
