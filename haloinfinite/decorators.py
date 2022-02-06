from functools import wraps

from haloinfinite.exceptions import (
    ClearanceIdRequiredError,
    SpartanTokenRequiredError,
    UserTokenRequiredError,
    XboxUserTokenRequiredError,
    XstsHaloTokenRequiredError,
    XstsXboxTokenRequiredError,
)


def clearance_id_required(func):
    @wraps(func)
    def helper(*args, **kwargs):
        module = args[0]
        if not module._client._clearance_token:
            raise ClearanceIdRequiredError("You must set the Clearance Token.")
        return func(*args, **kwargs)

    return helper


def spartan_token_required(func):
    @wraps(func)
    def helper(*args, **kwargs):
        module = args[0]
        if not module._client._spartan_token:
            raise SpartanTokenRequiredError("You must set the Spartan Token.")
        return func(*args, **kwargs)

    return helper


def user_token_required(func):
    @wraps(func)
    def helper(*args, **kwargs):
        module = args[0]
        if not module._client._user_token:
            raise UserTokenRequiredError("You must set the User Token.")
        return func(*args, **kwargs)

    return helper

def xbox_user_token_required(func):
    @wraps(func)
    def helper(*args, **kwargs):
        module = args[0]
        if not module._client._xbox_user_token:
            raise XboxUserTokenRequiredError("You must set the Xbox User Token.")
        return func(*args, **kwargs)

    return helper

def xsts_halo_token_required(func):
    @wraps(func)
    def helper(*args, **kwargs):
        module = args[0]
        if not module._client._xsts_halo_token:
            raise XstsHaloTokenRequiredError("You must set the Xsts Halo Token.")
        return func(*args, **kwargs)

    return helper

def xsts_xbox_token_required(func):
    @wraps(func)
    def helper(*args, **kwargs):
        module = args[0]
        if not module._client._xsts_xbox_token:
            raise XstsXboxTokenRequiredError("You must set the Xsts Xbox Token.")
        return func(*args, **kwargs)

    return helper
