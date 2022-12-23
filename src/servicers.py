import grpc

import db
import loyalty_pb2
import loyalty_pb2_grpc


class PromoCode(loyalty_pb2_grpc.PromoCodeServicer):
    async def CreateV1(
        self, request: loyalty_pb2.CreatePromoCodeRequestV1, context: grpc.aio.ServicerContext
    ) -> loyalty_pb2.CommonResponse:
        await db.pg_service.make_q()
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
