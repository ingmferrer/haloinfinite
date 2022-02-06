from functools import wraps

from haloinfinite.exceptions import (
    ClearanceTokenRequiredError,
    SpartanTokenRequiredError,
    UserTokenRequiredError,
    XboxUserTokenRequiredError,
    XstsHaloTokenRequiredError,
    XstsXboxTokenRequiredError,
)


def clearance_token_required(func):
    @wraps(func)
    def helper(*args, **kwargs):
        module = args[0]
        try:
            token = module._client._clearance_token
        except AttributeError:
            token = module._clearance_token
        if not token:
            raise ClearanceTokenRequiredError("You must set the Clearance Token.")
        return func(*args, **kwargs)

    return helper


def spartan_token_required(func):
    @wraps(func)
    def helper(*args, **kwargs):
        module = args[0]
        try:
            token = module._client._spartan_token
        except AttributeError:
            token = module._spartan_token
        if not token:
            raise SpartanTokenRequiredError("You must set the Spartan Token.")
        return func(*args, **kwargs)

    return helper


def user_token_required(func):
    @wraps(func)
    def helper(*args, **kwargs):
        module = args[0]
        try:
            token = module._client._user_token
        except AttributeError:
            token = module._user_token
        if not token:
            raise UserTokenRequiredError("You must set the User Token.")
        return func(*args, **kwargs)

    return helper


def xbox_user_token_required(func):
    @wraps(func)
    def helper(*args, **kwargs):
        module = args[0]
        try:
            token = module._client._xbox_user_token
        except AttributeError:
            token = module._xbox_user_token
        if not token:
            raise XboxUserTokenRequiredError("You must set the Xbox User Token.")
        return func(*args, **kwargs)

    return helper


def xsts_halo_token_required(func):
    @wraps(func)
    def helper(*args, **kwargs):
        module = args[0]
        try:
            token = module._client._xsts_halo_token
        except AttributeError:
            token = module._xsts_halo_token
        if not token:
            raise XstsHaloTokenRequiredError("You must set the Xsts Halo Token.")
        return func(*args, **kwargs)

    return helper


def xsts_xbox_token_required(func):
    @wraps(func)
    def helper(*args, **kwargs):
        module = args[0]
        try:
            token = module._client._xsts_xbox_token
        except AttributeError:
            token = module._xsts_xbox_token
        if not token:
            raise XstsXboxTokenRequiredError("You must set the Xsts Xbox Token.")
        return func(*args, **kwargs)

    return helper
