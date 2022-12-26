from datetime import datetime, timedelta
from random import randint

import grpc
import pytz
from google.protobuf.timestamp_pb2 import Timestamp  # noqa

from protos import loyalty_pb2
from protos import loyalty_pb2_grpc
from tests.config import SERVICE_URL


def test_discount_create():
    user_id = randint(10, 999999)
    discount_percents = 10
    expired_at_ts = Timestamp()
    expired_at_ts.FromDatetime(datetime.utcnow().replace(tzinfo=pytz.utc) + timedelta(days=1))
    with grpc.insecure_channel(SERVICE_URL) as channel:
        stub = loyalty_pb2_grpc.DiscountStub(channel)
        response, call = stub.CreateV1.with_call(
            loyalty_pb2.CreateDiscountRequestV1(
                user_id=user_id, discount_percents=discount_percents, expired_at=expired_at_ts
            )
        )
        assert call.code() == grpc.StatusCode.OK
        assert response.id
