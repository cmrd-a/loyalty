import asyncio
import logging

import grpc
from grpc_reflection.v1alpha import reflection

import db
import helloworld_pb2
import helloworld_pb2_grpc

# Coroutines to be invoked when the event loop is shutting down.
_cleanup_coroutines = []


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    async def SayHello(
        self, request: helloworld_pb2.HelloRequest, context: grpc.aio.ServicerContext
    ) -> helloworld_pb2.HelloReply:
        await db.pg_service.make_q()
        return helloworld_pb2.HelloReply(message="Hello, %s!" % request.name)


async def serve() -> None:
    # db.pg_conn = await connect_to_pg()
    server = grpc.aio.server()
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

    service_names = (
        helloworld_pb2.DESCRIPTOR.services_by_name["Greeter"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()

    async def server_graceful_shutdown():
        logging.info("Starting graceful shutdown...")
        await db.engine.dispose()
        await server.stop(5)

    _cleanup_coroutines.append(server_graceful_shutdown())
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(serve())
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()
