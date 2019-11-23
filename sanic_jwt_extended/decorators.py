from functools import wraps
from typing import Callable, List, Optional

from sanic.request import Request

from sanic_jwt_extended.exceptions import (
    AccessDeniedError,
    ConfigurationConflictError,
    FreshTokenRequiredError,
    InvalidHeaderError,
    NoAuthorizationError,
    WrongTokenError,
)
from sanic_jwt_extended.jwt_manager import JWT
from sanic_jwt_extended.tokens import Token


def _get_request(args) -> Request:
    if isinstance(args[0], Request):
        request = args[0]
    else:
        request = args[1]
    return request


def _get_raw_jwt_from_request(request: Request) -> str:
    functions: List[Callable[[Request], str]] = []

    for eligible_location in JWT.config.token_location:
        if eligible_location == "header":
            functions.append(_get_raw_jwt_from_headers)
        else:
            raise NotImplementedError("Currently only token in 'header' is supported")

    raw_jwt = None
    errors = []

    for f in functions:
        try:
            raw_jwt = f(request)
            break
        except NoAuthorizationError as e:
            errors.append(str(e))

    if not raw_jwt:
        raise NoAuthorizationError(', '.join(errors))

    return raw_jwt


def _get_raw_jwt_from_headers(request: Request) -> str:
    header_key = JWT.config.jwt_header_key
    header_prefix = JWT.config.jwt_header_prefix

    token_header: str = request.headers.get(header_key)

    if not token_header:
        raise NoAuthorizationError(f"Missing {header_key} header")

    parts: List[str] = token_header.split()

    if parts[0] != header_prefix or len(parts) != 2:
        raise InvalidHeaderError(
            f"Bad {header_key} header. Expected value '{header_prefix} <JWT>'"
        )

    encoded_token: str = parts[1]

    return encoded_token


def _get_raw_jwt_from_query_params(request: Request) -> str:
    pass


def _get_raw_jwt_from_cookies(request: Request) -> str:
    pass


def jwt_required(
    function: Callable = None,
    *,
    allow: List[str] = None,
    deny: List[str] = None,
    fresh_required: bool = False,
):
    def real(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            request = _get_request(*args)
            raw_jwt = _get_raw_jwt_from_request(request)

            token_obj = Token(raw_jwt)

            if token_obj.type != "access":
                raise WrongTokenError("Only access tokens are allowed")

            if fresh_required and not token_obj.fresh:
                raise FreshTokenRequiredError("Only fresh access tokens are allowed")

            if allow and token_obj.role not in allow:
                raise AccessDeniedError("You are not allowed to access here")

            if deny and token_obj.role in deny:
                raise AccessDeniedError("You are not allowed to access here")

            kwargs["token"] = token_obj

            return await fn(*args, **kwargs)

        return wrapper

    if function:
        return real(function)
    else:
        if allow and deny:
            raise ConfigurationConflictError(
                "Can not use 'deny' and 'allow' option together."
            )
        return real


def jwt_optional(function: Callable):
    @wraps(function)
    async def wrapper(*args, **kwargs):
        request = _get_request(*args)
        token_obj: Optional[Token] = None

        try:
            raw_jwt = _get_raw_jwt_from_request(request)

            token_obj = Token(raw_jwt)

            if token_obj.type != "access":
                raise WrongTokenError("Only access tokens are allowed")
        except NoAuthorizationError:
            pass

        kwargs["token"] = token_obj

        return await function(*args, **kwargs)

    return wrapper


def refresh_jwt_required(
    function: Callable = None, *, allow: List[str] = None, deny: List[str] = None
):
    def real(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            request = _get_request(*args)
            raw_jwt = _get_raw_jwt_from_request(request)

            token_obj = Token(raw_jwt)

            if token_obj.type != "refresh":
                raise WrongTokenError("Only access tokens are allowed")

            if allow and token_obj.role not in allow:
                raise AccessDeniedError("You are not allowed to refresh in here")

            if deny and token_obj.role in deny:
                raise AccessDeniedError("You are not allowed to refresh in here")

            kwargs["token"] = token_obj

            return await fn(*args, **kwargs)

        return wrapper

    if function:
        return real(function)
    else:
        if allow and deny:
            raise ConfigurationConflictError(
                "Can not use 'deny' and 'allow' option together."
            )
        return real
