from datetime import datetime, timedelta

import grpc
import pytz
from google.protobuf.descriptor_pool import DescriptorPool
from google.protobuf.message_factory import MessageFactory
from google.protobuf.timestamp_pb2 import Timestamp  # noqa
from grpc_reflection.v1alpha.proto_reflection_descriptor_database import ProtoReflectionDescriptorDatabase

from protos import loyalty_pb2
from protos import loyalty_pb2_grpc
from tests.config import SERVICE_URL


def test_promo_code_create():
    users_ids = [345, 456, 333]
    discount_percents = 10
    expired_at_ts = Timestamp()
    dt = datetime.utcnow().replace(tzinfo=pytz.utc) + timedelta(days=1)
    expired_at_ts.FromDatetime(dt)
    with grpc.insecure_channel(SERVICE_URL) as channel:
        reflection_db = ProtoReflectionDescriptorDatabase(channel)
        desc_pool = DescriptorPool(reflection_db)
        services = reflection_db.get_services()
        service_desc = desc_pool.FindServiceByName("loyalty.PromoCode")
        method_desc = service_desc.FindMethodByName("CreateV1")

        request_desc = desc_pool.FindMessageTypeByName("loyalty.CreatePromoCodeRequestV1")
        request = MessageFactory(desc_pool).GetPrototype(request_desc)(
            users_ids=users_ids, discount_percents=discount_percents, expired_at=expired_at_ts
        )

        stub = loyalty_pb2_grpc.PromoCodeStub(channel)
        req2 = loyalty_pb2.CreatePromoCodeRequestV1(
            users_ids=users_ids, discount_percents=discount_percents, expired_at=expired_at_ts
        )
        response = stub.CreateV1(req2)
        assert response.users_ids == users_ids
