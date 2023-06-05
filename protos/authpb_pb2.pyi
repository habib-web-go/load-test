from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class IsValidAuthKeyRequest(_message.Message):
    __slots__ = ["authkey"]
    AUTHKEY_FIELD_NUMBER: _ClassVar[int]
    authkey: str
    def __init__(self, authkey: _Optional[str] = ...) -> None: ...

class IsValidAuthKeyResponse(_message.Message):
    __slots__ = ["isValid"]
    ISVALID_FIELD_NUMBER: _ClassVar[int]
    isValid: bool
    def __init__(self, isValid: bool = ...) -> None: ...

class ReqPQRequest(_message.Message):
    __slots__ = ["messageId", "nonce"]
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    messageId: int
    nonce: str
    def __init__(self, nonce: _Optional[str] = ..., messageId: _Optional[int] = ...) -> None: ...

class ReqPQResponse(_message.Message):
    __slots__ = ["g", "messageId", "nonce", "p", "serverNonce"]
    G_FIELD_NUMBER: _ClassVar[int]
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    P_FIELD_NUMBER: _ClassVar[int]
    SERVERNONCE_FIELD_NUMBER: _ClassVar[int]
    g: int
    messageId: int
    nonce: str
    p: str
    serverNonce: str
    def __init__(self, nonce: _Optional[str] = ..., serverNonce: _Optional[str] = ..., messageId: _Optional[int] = ..., p: _Optional[str] = ..., g: _Optional[int] = ...) -> None: ...

class reqDHParamsRequest(_message.Message):
    __slots__ = ["a", "messageId", "nonce", "serverNonce"]
    A_FIELD_NUMBER: _ClassVar[int]
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    SERVERNONCE_FIELD_NUMBER: _ClassVar[int]
    a: str
    messageId: int
    nonce: str
    serverNonce: str
    def __init__(self, nonce: _Optional[str] = ..., serverNonce: _Optional[str] = ..., messageId: _Optional[int] = ..., a: _Optional[str] = ...) -> None: ...

class reqDHParamsResponse(_message.Message):
    __slots__ = ["b", "messageId", "nonce", "serverNonce"]
    B_FIELD_NUMBER: _ClassVar[int]
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    SERVERNONCE_FIELD_NUMBER: _ClassVar[int]
    b: str
    messageId: int
    nonce: str
    serverNonce: str
    def __init__(self, nonce: _Optional[str] = ..., serverNonce: _Optional[str] = ..., messageId: _Optional[int] = ..., b: _Optional[str] = ...) -> None: ...
