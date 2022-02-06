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


class ClearanceTokenRequiredError(BaseError):
    pass

class TokenExpiredError(BaseError):
    pass


class UnknownError(BaseError):
    pass

class BadRequestError(BaseError):
    pass


class UnauthorizedError(BaseError):
    pass


class ForbiddenError(BaseError):
    pass


class NotFoundError(BaseError):
    pass


class MethodNotAllowedError(BaseError):
    pass


class NotAcceptableError(BaseError):
    pass


class ConflictError(BaseError):
    pass


class GoneError(BaseError):
    pass


class LengthRequiredError(BaseError):
    pass


class PreconditionFailedError(BaseError):
    pass


class RequestEntityTooLargeError(BaseError):
    pass


class UnsupportedMediaTypeError(BaseError):
    pass


class RequestedRangeNotSatisfiableError(BaseError):
    pass


class UnprocessableEntityError(BaseError):
    pass


class TooManyRequestsError(BaseError):
    pass


class InternalServerErrorError(BaseError):
    pass


class NotImplementedAPIError(BaseError):
    pass


class ServiceUnavailableError(BaseError):
    pass


class GatewayTimeoutError(BaseError):
    pass


class InsufficientStorageError(BaseError):
    pass


class BandwidthLimitExceededError(BaseError):
    pass
