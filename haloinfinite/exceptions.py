class BaseError(Exception):
    pass


class UserTokenRequiredError(BaseError):
    pass


class XboxUserTokenRequiredError(BaseError):
    pass


class XstsXboxTokenRequiredError(BaseError):
    pass


class XstsHaloTokenRequiredError(BaseError):
    pass


class SpartanTokenRequiredError(BaseError):
    pass


class ClearanceIdRequiredError(BaseError):
    pass
