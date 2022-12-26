from datetime import datetime, timedelta

import grpc
import pytz
from google.protobuf.timestamp_pb2 import Timestamp  # noqa

from protos import loyalty_pb2
from protos import loyalty_pb2_grpc
from tests.config import SERVICE_URL


def test_promo_code_apply():
    users_ids = [345, 456, 333]
    discount_percents = 10
    expired_at_ts = Timestamp()
    expired_at_ts.FromDatetime(datetime.utcnow().replace(tzinfo=pytz.utc) + timedelta(days=1))
    with grpc.insecure_channel(SERVICE_URL) as channel:
        stub = loyalty_pb2_grpc.PromoCodeStub(channel)
        create_response = stub.CreateV1(
            loyalty_pb2.CreatePromoCodeRequestV1(
                users_ids=users_ids, discount_percents=discount_percents, expired_at=expired_at_ts
            )
        )
        reserve_response = stub.ReserveV1(
            loyalty_pb2.CommonPromoCodeRequestV1(code=create_response.code, user_id=users_ids[0])
        )
        _, call = stub.ApplyV1.with_call(loyalty_pb2.ReserveIdRequestV1(reserve_id=reserve_response.reserve_id))
        assert call.code() == grpc.StatusCode.OK
