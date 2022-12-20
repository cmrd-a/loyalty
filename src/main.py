import asyncio
import logging

import grpc
from grpc_reflection.v1alpha import reflection

import loyalty_pb2
import loyalty_pb2_grpc


class PromoCode(loyalty_pb2_grpc.PromoCodeServicer):
    async def CreateV1(
        self, request: loyalty_pb2.CreatePromoCodeRequestV1, context: grpc.aio.ServicerContext
    ) -> loyalty_pb2.CommonResponse:
        return loyalty_pb2.CommonResponse(id="1")

    async def ReserveV1(
        self, request: loyalty_pb2.CommonPromoCodeRequestV1, context: grpc.aio.ServicerContext
    ) -> loyalty_pb2.CommonResponse:
        return loyalty_pb2.CommonResponse(id="1")

    async def FreeV1(
        self, request: loyalty_pb2.CommonPromoCodeRequestV1, context: grpc.aio.ServicerContext
    ) -> loyalty_pb2.CommonResponse:
        return loyalty_pb2.CommonResponse(id="1")

    async def ApplyV1(
        self, request: loyalty_pb2.CommonPromoCodeRequestV1, context: grpc.aio.ServicerContext
    ) -> loyalty_pb2.CommonResponse:
        return loyalty_pb2.CommonResponse(id="1")


class Discount(loyalty_pb2_grpc.DiscountServicer):
    async def CreateV1(
        self, request: loyalty_pb2.CreateDiscountRequestV1, context: grpc.aio.ServicerContext
    ) -> loyalty_pb2.CommonResponse:
        return loyalty_pb2.CommonResponse(id="1")

    async def GetV1(
        self, request: loyalty_pb2.GetDiscountRequestV1, context: grpc.aio.ServicerContext
    ) -> loyalty_pb2.GetDiscountResponseV1:
        return loyalty_pb2.GetDiscountResponseV1(discount_percents=1)


async def serve() -> None:
    server = grpc.aio.server()
    loyalty_pb2_grpc.add_PromoCodeServicer_to_server(PromoCode(), server)
    loyalty_pb2_grpc.add_DiscountServicer_to_server(Discount(), server)

    service_names = (
        loyalty_pb2.DESCRIPTOR.services_by_name["PromoCode"].full_name,
        loyalty_pb2.DESCRIPTOR.services_by_name["Discount"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
