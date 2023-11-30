import traceback

from django.conf import settings
from fastapi.responses import UJSONResponse


class AuthException(Exception):
    pass


class UserNotLoggedIn(Exception):
    pass


EXC_HTTP_CODES = {
    "UserInputException": 400,
    "ObjectDoesNotExist": 404,
    "DoesNotExist": 404,
    "ModuleNotFoundError": 404,
    "AuthException": 401,
    "UserNotLoggedIn": 403,
}


async def unhandled_exception_handler(request, exc):
    code = EXC_HTTP_CODES.get(exc.__class__.__name__, 500)
    content = {
        "status": "exception",
        "exception": exc.__class__.__name__,
        "detail": str(exc),
        "code": code,
    }
    if settings.DEBUG and exc.__class__.__name__ not in EXC_HTTP_CODES.keys():
        import logging

        logger = logging.getLogger()
        logger.error("".join(traceback.format_exception(exc)))
        logger.error(str(exc))

        content["traceback"] = []
        for n, line in enumerate(
            "".join(traceback.format_exception(exc)).replace('"', "'").split("\n")
        ):
            content["traceback"].append(line)
    return UJSONResponse(status_code=code, content=content)
