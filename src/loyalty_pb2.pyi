from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CommonPromoCodeRequestV1(_message.Message):
    __slots__ = ["promo_code", "user_id"]
    PROMO_CODE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    promo_code: str
    user_id: int
    def __init__(self, promo_code: _Optional[str] = ..., user_id: _Optional[int] = ...) -> None: ...

class CommonResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class CreateDiscountRequestV1(_message.Message):
    __slots__ = ["discount_percents", "user_id"]
    DISCOUNT_PERCENTS_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    discount_percents: int
    user_id: int
    def __init__(self, discount_percents: _Optional[int] = ..., user_id: _Optional[int] = ...) -> None: ...

class CreatePromoCodeRequestV1(_message.Message):
    __slots__ = ["discount_percents", "expired_at", "id", "send_email", "users_ids"]
    DISCOUNT_PERCENTS_FIELD_NUMBER: _ClassVar[int]
    EXPIRED_AT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SEND_EMAIL_FIELD_NUMBER: _ClassVar[int]
    USERS_IDS_FIELD_NUMBER: _ClassVar[int]
    discount_percents: int
    expired_at: _timestamp_pb2.Timestamp
    id: str
    send_email: bool
    users_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, id: _Optional[str] = ..., expired_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., users_ids: _Optional[_Iterable[int]] = ..., discount_percents: _Optional[int] = ..., send_email: bool = ...) -> None: ...

class GetDiscountRequestV1(_message.Message):
    __slots__ = ["user_id"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    def __init__(self, user_id: _Optional[int] = ...) -> None: ...

class GetDiscountResponseV1(_message.Message):
    __slots__ = ["discount_percents"]
    DISCOUNT_PERCENTS_FIELD_NUMBER: _ClassVar[int]
    discount_percents: int
    def __init__(self, discount_percents: _Optional[int] = ...) -> None: ...
