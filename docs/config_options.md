---
layout: default
title: Configuration Options
nav_order: 3
---

# Configuration Option

You can change many options for how this extension works via

```python
with JWT.initialize(app) as manager:
    manager.handler.<OPTION> = <VALUE>
```

You can not change option after close initialize context manger!
{: .text-red-100 .code-example }

## Secrets

| key           | description                           | type   | default |
|:--------------|:--------------------------------------|:-------|:--------|
| `secret_key`  | encode/decode key for `HS*` algorithm | string | `None`  |
| `public_key`  | decode key for `RS*` algorithm        | string | `None`  |
| `private_key` | encode key for `RS*` algorithm        | string | `None`  |

## Default values for reserved claims

| key           | description      | type          | default |
|:--------------|:-----------------|:--------------|:--------|
| `default_iss` | default issuer   | string or URI | `None`  |
| `default_aud` | default audience | string or URI | `None`  |

## General configs

| key                     | description                                                                                                                                                                                                    | TYPE                          | default                 |
|:------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------|:------------------------|
| `json_encoder`          | json encoder                                                                                                                                                                                                   | Any                           | `JSONEncoder`           |
| `token_location`        | Where to look for a JWT when processing a request. The options are `headers`, `cookies` or `query_string`. You can pass in a sequence or a set to check more then one location, such as: `(headers, cookies)`. | Tuple[string]                 | `("header",)`           |
| `access_token_expires`  | How long an access token should live before it expires.                                                                                                                                                        | datetime.timedelta or `False` | `timedelta(minutes=15`) |
| `refresh_token_expires` | How long an refresh token should live before it expires.                                                                                                                                                       | datetime.timedelta or `False` | `timedelta(days=30) `   |
| `algorithm`             | Which algorithm to sign the JWT with. [See here](https://pyjwt.readthedocs.io/en/latest/algorithms.html) for the options.                                                                                      | string                        | `"HS256" `              |


## Additional claim configs

| key                      | description                 | type          | default |
|:-------------------------|:----------------------------|:--------------|:--------|
| `public_claim_namespace` | namespace for public claims | string or URI | `""`    |
| `private_claim_prefix`   | prefix for pricate claims   | string or URI | `""`    |

## Header configs

| key                         | description                                           | type   | default             |
|:----------------------------|:------------------------------------------------------|:-------|:--------------------|
| `jwt_header_key`            | What header to look for the access JWT in a request.  | string | `"Authorization"`   |
| `refresh_jwt_header_key`    | What header to look for the refresh JWT in a request. | string | `"X-Refresh-Token"` |
| `jwt_header_prefix`         | What type of header the JWT is in.                    | string | `"Bearer"`          |
| `refresh_jwt_header_prefix` | What type of header the JWT is in.                    | string | `"Bearer"`          |

## Cookie configs

| key                  | description                                         | type   | default                  |
|:---------------------|:----------------------------------------------------|:-------|:-------------------------|
| `jwt_cookie`         | The name of the cookie that holds the access token. | string | `"access_token_cookie"`  |
| `refresh_jwt_cookie` | The name of the cookie that holds the access token. | string | `"refresh_token_cookie"` |
| `csrf_protect`       | Enable/disable CSRF protection when using cookies.  | bool   | `True`                   |

## CSRF configs

| key                       | description                                                                            | type          | default                              |
|:--------------------------|:---------------------------------------------------------------------------------------|:--------------|:-------------------------------------|
| `csrf_request_methods`    | The request types that will use CSRF protection.                                       | Tuple[string] | `('POST', 'PUT', 'PATCH', 'DELETE')` |
| `jwt_csrf_header`         | Name of the header that should contain the CSRF double submit value for access tokens. | string        | `"X-CSRF-Token"`                     |
| `refresh_jwt_csrf_header` | Name of the header that should contain the CSRF double submit value for access tokens. | string        | `"X-CSRF-Token"`                     |


## Query parameter options

| key                    | description                                               | type   | default |
|:-----------------------|:----------------------------------------------------------|:-------|:--------|
| `jwt_query_param_name` | What query paramater name to look for a JWT in a request. | string | `"jwt"` |

## Access control configs

| key         | description                    | type   | default |
|:------------|:-------------------------------|:-------|:--------|
| `use_acl`   | Enable/disable access control  | bool   | `False` |
| `acl_claim` | Which claim to store role info | string | `role`  |

## Blacklist configs

| key                     | description                                     | type                     | default             |
|:------------------------|:------------------------------------------------|:-------------------------|:--------------------|
| `use_blacklist`         | Enable/disable token revoking.                  | bool                     | `False`             |
| `blacklist_class`       | Blacklist class to use                          | Type[BlacklistABC]       | `InMemoryBlacklist` |
| `blacklist_init_kwargs` | keyword arguments dictionary for blacklist init | Optional[Dict[str, Any]] | `None`              |
