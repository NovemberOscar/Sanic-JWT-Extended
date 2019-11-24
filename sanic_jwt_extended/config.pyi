# Stubs for config (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from datetime import timedelta
from typing import Any, Optional, Tuple, Union

class Config:
    read_only: bool = ...
    secret_key: Optional[str] = ...
    public_key: Optional[str] = ...
    private_key: Optional[str] = ...
    default_iss: Optional[str] = ...
    default_aud: Optional[str] = ...
    json_encoder: Any = ...
    token_location: Tuple[str] = ...
    access_token_expires: Union[timedelta, bool] = ...
    refresh_token_expires: Union[timedelta, bool] = ...
    algorithm: str = ...
    public_claim_namespace: Optional[str] = ...
    private_claim_prefix: Optional[str] = ...
    jwt_header_key: str = ...
    jwt_header_prefix: str = ...
    jwt_query_param_name: str = ...
    use_acl: bool = ...
    acl_claim: str = ...
    use_blacklist: bool = ...
    def __setattr__(self, key: Any, value: Any) -> None: ...
    def __init__(
        self,
        read_only: Any = ...,
        secret_key: Any = ...,
        public_key: Any = ...,
        private_key: Any = ...,
        default_iss: Any = ...,
        default_aud: Any = ...,
        json_encoder: Any = ...,
        token_location: Any = ...,
        access_token_expires: Any = ...,
        refresh_token_expires: Any = ...,
        algorithm: Any = ...,
        public_claim_namespace: Any = ...,
        private_claim_prefix: Any = ...,
        jwt_header_key: Any = ...,
        jwt_header_prefix: Any = ...,
        use_acl: Any = ...,
        acl_claim: Any = ...,
        use_blacklist: Any = ...,
    ) -> None: ...
