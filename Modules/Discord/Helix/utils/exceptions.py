from discord.ext.commands import CheckFailure


class HelixGuildCheckFailure(CheckFailure):
    def __init__(self):
        super().__init__(message="Can only be used in Tortoise guild.")


class HelixBotDeveloperCheckFailure(CheckFailure):
    def __init__(self):
        super().__init__(message="Can only be used by Tortoise developers.")


class EndpointResponse(Exception):
    def __init__(self, code: int, message: str):
        self.response = {"status": {"code": code, "message": message}}


class EndpointSuccess(EndpointResponse):
    def __init__(self):
        super().__init__(200, "Success")


class EndpointError(EndpointResponse):
    def __init__(self, code: int, message: str, endpoint_key=""):
        super().__init__(code, f"{message}, endpoint:{endpoint_key}")


class EndpointNotFound(EndpointError):
    def __init__(self):
        super().__init__(400, "Endpoint not found.")


class EndpointBadArguments(EndpointError):
    def __init__(self):
        super().__init__(400, "Endpoint bad arguments.")


class DiscordIDNotFound(EndpointError):
    def __init__(self):
        super().__init__(404, "Discord ID not found.")


class InternalServerError(EndpointError):
    def __init__(self):
        super().__init__(500, "Internal server error.")