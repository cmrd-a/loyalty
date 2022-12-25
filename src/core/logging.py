from typing import Callable, Any

import grpc
import structlog
from google.protobuf.json_format import MessageToDict
from google.protobuf.message import Message
from grpc_interceptor.server import AsyncServerInterceptor

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S"),
        structlog.dev.ConsoleRenderer(sort_keys=False),
    ]
)

log = structlog.getLogger()


class LogInterceptor(AsyncServerInterceptor):
    async def intercept(
        self, method: Callable, request: Any, context: grpc.aio.ServicerContext, method_name: str
    ) -> Any:
        response = None
        log_params = {"method": method_name}
        if isinstance(request, Message):
            log_params["request_message"] = MessageToDict(request)
        try:
            response_or_iterator = method(request, context)
            if hasattr(response_or_iterator, "__aiter__"):
                response = response_or_iterator
            else:
                response = await response_or_iterator
        finally:
            if isinstance(response, Message):
                log_params["response_message"] = MessageToDict(response)

            await log.ainfo("request logged", **log_params)

        return response
