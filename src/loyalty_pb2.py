# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: loyalty.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rloyalty.proto\x12\x07loyalty\x1a\x1fgoogle/protobuf/timestamp.proto\"\xa5\x01\n\x18\x43reatePromoCodeRequestV1\x12\x0f\n\x02id\x18\x01 \x01(\tH\x00\x88\x01\x01\x12.\n\nexpired_at\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x11\n\tusers_ids\x18\x03 \x03(\x03\x12\x19\n\x11\x64iscount_percents\x18\x04 \x01(\x05\x12\x13\n\x0bsend_emails\x18\x05 \x01(\x08\x42\x05\n\x03_id\"\x1c\n\x0e\x43ommonResponse\x12\n\n\x02id\x18\x01 \x01(\t\"?\n\x18\x43ommonPromoCodeRequestV1\x12\x12\n\npromo_code\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\x03\"E\n\x17\x43reateDiscountRequestV1\x12\x19\n\x11\x64iscount_percents\x18\x01 \x01(\x05\x12\x0f\n\x07user_id\x18\x02 \x01(\x03\"\'\n\x14GetDiscountRequestV1\x12\x0f\n\x07user_id\x18\x01 \x01(\x03\"2\n\x15GetDiscountResponseV1\x12\x19\n\x11\x64iscount_percents\x18\x01 \x01(\x05\x32\xb1\x02\n\tPromoCode\x12H\n\x08\x43reateV1\x12!.loyalty.CreatePromoCodeRequestV1\x1a\x17.loyalty.CommonResponse\"\x00\x12I\n\tReserveV1\x12!.loyalty.CommonPromoCodeRequestV1\x1a\x17.loyalty.CommonResponse\"\x00\x12\x46\n\x06\x46reeV1\x12!.loyalty.CommonPromoCodeRequestV1\x1a\x17.loyalty.CommonResponse\"\x00\x12G\n\x07\x41pplyV1\x12!.loyalty.CommonPromoCodeRequestV1\x1a\x17.loyalty.CommonResponse\"\x00\x32\x9d\x01\n\x08\x44iscount\x12G\n\x08\x43reateV1\x12 .loyalty.CreateDiscountRequestV1\x1a\x17.loyalty.CommonResponse\"\x00\x12H\n\x05GetV1\x12\x1d.loyalty.GetDiscountRequestV1\x1a\x1e.loyalty.GetDiscountResponseV1\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'loyalty_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CREATEPROMOCODEREQUESTV1._serialized_start=60
  _CREATEPROMOCODEREQUESTV1._serialized_end=225
  _COMMONRESPONSE._serialized_start=227
  _COMMONRESPONSE._serialized_end=255
  _COMMONPROMOCODEREQUESTV1._serialized_start=257
  _COMMONPROMOCODEREQUESTV1._serialized_end=320
  _CREATEDISCOUNTREQUESTV1._serialized_start=322
  _CREATEDISCOUNTREQUESTV1._serialized_end=391
  _GETDISCOUNTREQUESTV1._serialized_start=393
  _GETDISCOUNTREQUESTV1._serialized_end=432
  _GETDISCOUNTRESPONSEV1._serialized_start=434
  _GETDISCOUNTRESPONSEV1._serialized_end=484
  _PROMOCODE._serialized_start=487
  _PROMOCODE._serialized_end=792
  _DISCOUNT._serialized_start=795
  _DISCOUNT._serialized_end=952
# @@protoc_insertion_point(module_scope)
