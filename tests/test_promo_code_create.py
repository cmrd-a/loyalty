from datetime import datetime, timedelta

import grpc
import pytz
from google.protobuf.timestamp_pb2 import Timestamp  # noqa

from protos import loyalty_pb2
from protos import loyalty_pb2_grpc


def test_promo_code_create():
    users_ids = [345, 456, 333]
    discount_percents = 10
    expired_at_ts = Timestamp()
    expired_at_ts.FromDatetime(datetime.utcnow().replace(tzinfo=pytz.utc) + timedelta(days=1))
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = loyalty_pb2_grpc.PromoCodeStub(channel)
        response = stub.CreateV1(
            loyalty_pb2.CreatePromoCodeRequestV1(
                users_ids=users_ids, discount_percents=discount_percents, expired_at=expired_at_ts
            )
        )
        assert response.users_ids == users_ids
