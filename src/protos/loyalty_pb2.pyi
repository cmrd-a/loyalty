from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CommonPromoCodeRequestV1(_message.Message):
    __slots__ = ["code", "user_id"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    code: str
    user_id: int
    def __init__(self, code: _Optional[str] = ..., user_id: _Optional[int] = ...) -> None: ...

class CommonResponseV1(_message.Message):
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
    __slots__ = ["activation_quantity", "code", "discount_percents", "expired_at", "send_email", "users_ids"]
    ACTIVATION_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DISCOUNT_PERCENTS_FIELD_NUMBER: _ClassVar[int]
    EXPIRED_AT_FIELD_NUMBER: _ClassVar[int]
    SEND_EMAIL_FIELD_NUMBER: _ClassVar[int]
    USERS_IDS_FIELD_NUMBER: _ClassVar[int]
    activation_quantity: int
    code: str
    discount_percents: int
    expired_at: _timestamp_pb2.Timestamp
    send_email: bool
    users_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, code: _Optional[str] = ..., discount_percents: _Optional[int] = ..., activation_quantity: _Optional[int] = ..., expired_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., users_ids: _Optional[_Iterable[int]] = ..., send_email: bool = ...) -> None: ...

class CreatePromoCodeResponseV1(_message.Message):
    __slots__ = ["activation_quantity", "code", "discount_percents", "expired_at", "id", "users_ids"]
    ACTIVATION_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DISCOUNT_PERCENTS_FIELD_NUMBER: _ClassVar[int]
    EXPIRED_AT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    USERS_IDS_FIELD_NUMBER: _ClassVar[int]
    activation_quantity: int
    code: str
    discount_percents: int
    expired_at: _timestamp_pb2.Timestamp
    id: str
    users_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, id: _Optional[str] = ..., code: _Optional[str] = ..., discount_percents: _Optional[int] = ..., activation_quantity: _Optional[int] = ..., expired_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., users_ids: _Optional[_Iterable[int]] = ...) -> None: ...

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
