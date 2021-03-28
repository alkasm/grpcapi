# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    FileDescriptor as google___protobuf___descriptor___FileDescriptor,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    Optional as typing___Optional,
    Text as typing___Text,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int


DESCRIPTOR: google___protobuf___descriptor___FileDescriptor = ...

class Point(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    latitude: builtin___int = ...
    longitude: builtin___int = ...

    def __init__(self,
        *,
        latitude : typing___Optional[builtin___int] = None,
        longitude : typing___Optional[builtin___int] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"latitude",b"latitude",u"longitude",b"longitude"]) -> None: ...
type___Point = Point

class Rectangle(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def lo(self) -> type___Point: ...

    @property
    def hi(self) -> type___Point: ...

    def __init__(self,
        *,
        lo : typing___Optional[type___Point] = None,
        hi : typing___Optional[type___Point] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"hi",b"hi",u"lo",b"lo"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"hi",b"hi",u"lo",b"lo"]) -> None: ...
type___Rectangle = Rectangle

class Feature(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    name: typing___Text = ...

    @property
    def location(self) -> type___Point: ...

    def __init__(self,
        *,
        name : typing___Optional[typing___Text] = None,
        location : typing___Optional[type___Point] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"location",b"location"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"location",b"location",u"name",b"name"]) -> None: ...
type___Feature = Feature

class RouteNote(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    message: typing___Text = ...

    @property
    def location(self) -> type___Point: ...

    def __init__(self,
        *,
        location : typing___Optional[type___Point] = None,
        message : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"location",b"location"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"location",b"location",u"message",b"message"]) -> None: ...
type___RouteNote = RouteNote

class RouteSummary(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    point_count: builtin___int = ...
    feature_count: builtin___int = ...
    distance: builtin___int = ...
    elapsed_time: builtin___int = ...

    def __init__(self,
        *,
        point_count : typing___Optional[builtin___int] = None,
        feature_count : typing___Optional[builtin___int] = None,
        distance : typing___Optional[builtin___int] = None,
        elapsed_time : typing___Optional[builtin___int] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"distance",b"distance",u"elapsed_time",b"elapsed_time",u"feature_count",b"feature_count",u"point_count",b"point_count"]) -> None: ...
type___RouteSummary = RouteSummary
