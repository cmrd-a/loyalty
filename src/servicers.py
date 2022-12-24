import datetime

import pytz
from google.protobuf.timestamp_pb2 import Timestamp  # noqa
from google.protobuf.empty_pb2 import Empty  # noqa
from grpc import StatusCode
from grpc.aio import ServicerContext

from config import config
from database.models import CodeStatus
from database.pg_service import pg_service
from protos import loyalty_pb2
from protos import loyalty_pb2_grpc


class PromoCode(loyalty_pb2_grpc.PromoCodeServicer):
    async def CreateV1(
        self, request: loyalty_pb2.CreatePromoCodeRequestV1, context: ServicerContext
    ) -> loyalty_pb2.CreatePromoCodeResponseV1:  # TODO: add validation
        promo_code = await pg_service.create_promo_code(
            request.code,
            request.discount_percents,
            request.activation_quantity,
            request.expired_at.ToDatetime(),
            list(request.users_ids),
        )

        if request.send_email:
            pass

        expired_at_ts = Timestamp()
        expired_at_ts.FromDatetime(promo_code.expired_at)

        return loyalty_pb2.CreatePromoCodeResponseV1(
            id=str(promo_code.id),
            code=promo_code.code,
            discount_percents=promo_code.discount_percents,
            activation_quantity=promo_code.activation_quantity,
            expired_at=expired_at_ts,
            users_ids=promo_code.users_ids,
        )

    async def ReserveV1(
        self, request: loyalty_pb2.CommonPromoCodeRequestV1, context: ServicerContext
    ) -> loyalty_pb2.CommonResponseV1:
        existed_promo_codes = await pg_service.get_promo_codes(request.code)
        if not existed_promo_codes:
            await context.abort(StatusCode.INVALID_ARGUMENT, "Неверный промокод")

        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        unexpired_promo_codes = [pc for pc in existed_promo_codes if pc.expired_at > now]
        if not unexpired_promo_codes:
            await context.abort(StatusCode.INVALID_ARGUMENT, "Время действия промокода истекло")

        user_promo_codes = [pc for pc in unexpired_promo_codes if request.user_id in pc.users_ids or not pc.users_ids]
        if not user_promo_codes:
            await context.abort(StatusCode.INVALID_ARGUMENT, "Промокод недоступен пользователю")

        all_statuses = await pg_service.get_promo_code_statuses(user_promo_codes, request.user_id)
        timeout = datetime.timedelta(seconds=config.reserve_timeout_seconds)
        timeouted_reserves = [
            s for s in all_statuses if now - s.created_at > timeout and s.status == CodeStatus.reserved
        ]
        blocked_statuses = set(all_statuses) - set(timeouted_reserves)
        status_codes_ids = {s.code_id for s in blocked_statuses}
        user_codes_ids = {pc.id for pc in user_promo_codes}
        free_codes_ids = list((user_codes_ids - status_codes_ids))
        if not free_codes_ids:
            await context.abort(StatusCode.INVALID_ARGUMENT, "Промокод зарезервирован или использован")

        promo_code_status = await pg_service.reserve_promo_code(free_codes_ids[0], request.user_id)
        return loyalty_pb2.CommonResponseV1(id=str(promo_code_status.id))

    async def FreeV1(self, request: loyalty_pb2.ReserveIdRequestV1, context: ServicerContext) -> Empty:
        await pg_service.free_promo_code(request.reserve_id)
        return Empty()

    async def ApplyV1(self, request: loyalty_pb2.ReserveIdRequestV1, context: ServicerContext) -> Empty:
        await pg_service.apply_promo_code(request.reserve_id)
        return Empty()


class Discount(loyalty_pb2_grpc.DiscountServicer):
    async def CreateV1(
        self, request: loyalty_pb2.CreateDiscountRequestV1, context: ServicerContext
    ) -> loyalty_pb2.CommonResponseV1:
        return loyalty_pb2.CommonResponseV1(id="1")

    async def GetV1(
        self, request: loyalty_pb2.GetDiscountRequestV1, context: ServicerContext
    ) -> loyalty_pb2.GetDiscountResponseV1:
        return loyalty_pb2.GetDiscountResponseV1(discount_percents=1)
