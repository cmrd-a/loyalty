import asyncio

from grpc.aio import server as grpc_aio_server
from grpc_reflection.v1alpha import reflection

from core.config import config
from core.logging import log, LogInterceptor
from database.service import db_svc
from protos import loyalty_pb2
from protos import loyalty_pb2_grpc
from servicers import PromoCode, Discount

_cleanup_coroutines = []


async def serve() -> None:
    server = grpc_aio_server(interceptors=[LogInterceptor()])
    loyalty_pb2_grpc.add_PromoCodeServicer_to_server(PromoCode(), server)
    loyalty_pb2_grpc.add_DiscountServicer_to_server(Discount(), server)

    service_names = (
        loyalty_pb2.DESCRIPTOR.services_by_name["PromoCode"].full_name,
        loyalty_pb2.DESCRIPTOR.services_by_name["Discount"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    listen_addr = f"[::]:{config.app_listen_port}"
    server.add_insecure_port(listen_addr)
    await log.ainfo("Starting server on %s", listen_addr)
    await server.start()

    async def server_graceful_shutdown():
        await log.ainfo("Starting graceful shutdown...")
        await db_svc.engine.dispose()
        await server.stop(5)

    _cleanup_coroutines.append(server_graceful_shutdown())
    await server.wait_for_termination()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(serve())
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()
