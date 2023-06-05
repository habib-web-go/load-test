from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
Female: Sex
Man: Sex

class GetUsersRequest(_message.Message):
    __slots__ = ["authKey", "messageId", "userId"]
    AUTHKEY_FIELD_NUMBER: _ClassVar[int]
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    authKey: str
    messageId: int
    userId: int
    def __init__(self, userId: _Optional[int] = ..., authKey: _Optional[str] = ..., messageId: _Optional[int] = ...) -> None: ...

class GetUsersResponse(_message.Message):
    __slots__ = ["messageId", "users"]
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    messageId: int
    users: _containers.RepeatedCompositeFieldContainer[User]
    def __init__(self, users: _Optional[_Iterable[_Union[User, _Mapping]]] = ..., messageId: _Optional[int] = ...) -> None: ...

class GetUsersWithSqlInjectRequest(_message.Message):
    __slots__ = ["authKey", "messageId", "userId"]
    AUTHKEY_FIELD_NUMBER: _ClassVar[int]
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    authKey: str
    messageId: int
    userId: str
    def __init__(self, userId: _Optional[str] = ..., authKey: _Optional[str] = ..., messageId: _Optional[int] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ["age", "createdAt", "family", "id", "name", "sex"]
    AGE_FIELD_NUMBER: _ClassVar[int]
    CREATEDAT_FIELD_NUMBER: _ClassVar[int]
    FAMILY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SEX_FIELD_NUMBER: _ClassVar[int]
    age: int
    createdAt: str
    family: str
    id: int
    name: str
    sex: Sex
    def __init__(self, name: _Optional[str] = ..., family: _Optional[str] = ..., id: _Optional[int] = ..., age: _Optional[int] = ..., sex: _Optional[_Union[Sex, str]] = ..., createdAt: _Optional[str] = ...) -> None: ...

class Sex(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
