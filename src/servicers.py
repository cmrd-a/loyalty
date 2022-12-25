import datetime

import pytz
from google.protobuf.empty_pb2 import Empty  # noqa
from google.protobuf.timestamp_pb2 import Timestamp  # noqa
from grpc import StatusCode
from grpc.aio import ServicerContext
from utils import send_email
from config import config
from database.models import CodeStatus, CodeOperation
from database.service import db_svc
from protos import loyalty_pb2
from protos import loyalty_pb2_grpc


class PromoCode(loyalty_pb2_grpc.PromoCodeServicer):
    async def CreateV1(
        self, request: loyalty_pb2.CreatePromoCodeRequestV1, context: ServicerContext
    ) -> loyalty_pb2.CreatePromoCodeResponseV1:
        promo_code = await db_svc.create_promo_code(
            request.code,
            request.discount_percents,
            request.expired_at.ToDatetime(),
            list(request.users_ids),
        )

        if request.send_email and promo_code.users_ids:
            await send_email(promo_code.users_ids, promo_code.code, promo_code.discount_percents)

        expired_at_ts = Timestamp()
        expired_at_ts.FromDatetime(promo_code.expired_at)

        return loyalty_pb2.CreatePromoCodeResponseV1(
            id=str(promo_code.id),
            code=promo_code.code,
            discount_percents=promo_code.discount_percents,
            expired_at=expired_at_ts,
            users_ids=promo_code.users_ids,
        )

    async def ReserveV1(
        self, request: loyalty_pb2.CommonPromoCodeRequestV1, context: ServicerContext
    ) -> loyalty_pb2.CommonResponseV1:
        existed_promo_codes = await db_svc.get_promo_codes_by_code(request.code)
        if not existed_promo_codes:
            await context.abort(StatusCode.INVALID_ARGUMENT, "Неверный промокод")

        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        unexpired_promo_codes = [pc for pc in existed_promo_codes if pc.expired_at > now]
        if not unexpired_promo_codes:
            await context.abort(StatusCode.INVALID_ARGUMENT, "Время действия промокода истекло")

        user_promo_codes = [pc for pc in unexpired_promo_codes if request.user_id in pc.users_ids or not pc.users_ids]
        if not user_promo_codes:
            await context.abort(StatusCode.INVALID_ARGUMENT, "Промокод недоступен пользователю")

        all_statuses = await db_svc.get_promo_code_statuses(user_promo_codes, request.user_id)
        timeout = datetime.timedelta(seconds=config.reserve_timeout_seconds)
        timeouted_reserves = {
            status
            for status in all_statuses
            if now - status.created_at > timeout and status.status == CodeStatus.reserved
        }
        blocked_statuses = set(all_statuses) - timeouted_reserves
        status_codes_ids = [status.code_id for status in blocked_statuses]
        free_codes = [pc for pc in user_promo_codes if pc.id not in status_codes_ids]
        if not free_codes:
            await context.abort(StatusCode.INVALID_ARGUMENT, "Промокод зарезервирован или использован")

        promo_code_status = await db_svc.reserve_promo_code(free_codes[0], request.user_id)
        await db_svc.create_promo_code_status_log(free_codes[0].code, CodeOperation.reserve, request.user_id)
        return loyalty_pb2.CommonResponseV1(id=str(promo_code_status.id))

    async def FreeV1(self, request: loyalty_pb2.ReserveIdRequestV1, context: ServicerContext) -> Empty:
        status = await db_svc.get_promo_code_status(request.reserve_id)
        code = await db_svc.get_promo_code_by_id(status.code_id)

        await db_svc.free_promo_code(request.reserve_id)

        await db_svc.create_promo_code_status_log(code.code, CodeOperation.free, status.user_id)
        return Empty()

    async def ApplyV1(self, request: loyalty_pb2.ReserveIdRequestV1, context: ServicerContext) -> Empty:
        await db_svc.apply_promo_code(request.reserve_id)

        status = await db_svc.get_promo_code_status(request.reserve_id)
        code = await db_svc.get_promo_code_by_id(status.code_id)
        await db_svc.create_promo_code_status_log(code.code, CodeOperation.apply, status.user_id)
        return Empty()


class Discount(loyalty_pb2_grpc.DiscountServicer):
    async def CreateV1(
        self, request: loyalty_pb2.CreateDiscountRequestV1, context: ServicerContext
    ) -> loyalty_pb2.CommonResponseV1:
        user_discount = await db_svc.create_user_dicount(
            request.user_id, request.discount_percents, request.expired_at.ToDatetime()
        )
        return loyalty_pb2.CommonResponseV1(id=str(user_discount.id))

    async def ApplyV1(
        self, request: loyalty_pb2.ApplyDiscountRequestV1, context: ServicerContext
    ) -> loyalty_pb2.ApplyDiscountResponseV1:
        user_discount = await db_svc.get_user_discount(user_id=request.user_id)
        if user_discount:
            await db_svc.delete_user_discount(user_discount.id)
            if user_discount.expired_at > datetime.datetime.utcnow().replace(tzinfo=pytz.utc):
                return loyalty_pb2.ApplyDiscountResponseV1(discount_percents=user_discount.discount_percents)
        return loyalty_pb2.ApplyDiscountResponseV1(discount_percents=0)
