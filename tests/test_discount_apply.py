from datetime import datetime, timedelta
from random import randint

import grpc
import pytz
from google.protobuf.timestamp_pb2 import Timestamp  # noqa

from protos import loyalty_pb2
from protos import loyalty_pb2_grpc


def test_discount_apply():
    discount_percents = 10
    user_id = randint(10, 999999)
    expired_at_ts = Timestamp()
    expired_at_ts.FromDatetime(datetime.utcnow().replace(tzinfo=pytz.utc) + timedelta(days=1))
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = loyalty_pb2_grpc.DiscountStub(channel)
        stub.CreateV1(
            loyalty_pb2.CreateDiscountRequestV1(
                user_id=user_id, discount_percents=discount_percents, expired_at=expired_at_ts
            )
        )
        response = stub.ApplyV1(loyalty_pb2.ApplyDiscountRequestV1(user_id=user_id))
        assert response.discount_percents == discount_percents
