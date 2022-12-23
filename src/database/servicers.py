from google.protobuf.timestamp_pb2 import Timestamp  # noqa
from grpc.aio import ServicerContext

from database.db import pg_service
from protos import loyalty_pb2
from protos import loyalty_pb2_grpc


class PromoCode(loyalty_pb2_grpc.PromoCodeServicer):
    async def CreateV1(
        self, request: loyalty_pb2.CreatePromoCodeRequestV1, context: ServicerContext
    ) -> loyalty_pb2.CreatePromoCodeResponseV1:  # TODO: add validation
        code = await pg_service.create_promo_code(
            request.code,
            request.discount_percents,
            request.activation_quantity,
            request.expired_at.ToDatetime(),
            list(request.users_ids),
        )
        if request.send_email:
            pass
        expired_at_ts = Timestamp()
        expired_at_ts.FromDatetime(code.expired_at)

        return loyalty_pb2.CreatePromoCodeResponseV1(
            id=str(code.id),
            code=code.code,
            discount_percents=code.discount_percents,
            activation_quantity=code.activation_quantity,
            expired_at=expired_at_ts,
            users_ids=code.for_users,
        )

    async def ReserveV1(
        self, request: loyalty_pb2.CommonPromoCodeRequestV1, context: ServicerContext
    ) -> loyalty_pb2.CommonResponseV1:
        return loyalty_pb2.CommonResponseV1(id="1")

    async def FreeV1(
        self, request: loyalty_pb2.CommonPromoCodeRequestV1, context: ServicerContext
    ) -> loyalty_pb2.CommonResponseV1:
        return loyalty_pb2.CommonResponseV1(id="1")

    async def ApplyV1(
        self, request: loyalty_pb2.CommonPromoCodeRequestV1, context: ServicerContext
    ) -> loyalty_pb2.CommonResponseV1:
        return loyalty_pb2.CommonResponseV1(id="1")


class Discount(loyalty_pb2_grpc.DiscountServicer):
    async def CreateV1(
        self, request: loyalty_pb2.CreateDiscountRequestV1, context: ServicerContext
    ) -> loyalty_pb2.CommonResponseV1:
        return loyalty_pb2.CommonResponseV1(id="1")

    async def GetV1(
        self, request: loyalty_pb2.GetDiscountRequestV1, context: ServicerContext
    ) -> loyalty_pb2.GetDiscountResponseV1:
        return loyalty_pb2.GetDiscountResponseV1(discount_percents=1)
