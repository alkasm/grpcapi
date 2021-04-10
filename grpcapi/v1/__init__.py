import collections
import inspect
import typing
import grpc
from google.protobuf import message

__all__ = ["App"]


Message = typing.TypeVar("Message", bound=message.Message)

UnaryUnaryHandler = typing.Callable[
    [Message, grpc.ServicerContext],
    Message,
]
UnaryStreamHandler = typing.Callable[
    [Message, grpc.ServicerContext],
    typing.Iterable[Message],
]
StreamUnaryHandler = typing.Callable[
    [typing.Iterable[Message], grpc.ServicerContext],
    Message,
]
StreamStreamHandler = typing.Callable[
    [typing.Iterable[Message], grpc.ServicerContext],
    typing.Iterable[Message],
]

T = typing.TypeVar("T")
Identity = typing.Callable[[T], T]


class App:
    def __init__(self):
        self.handlers = collections.defaultdict(dict)

    def unary_unary(self, route: str) -> Identity[UnaryUnaryHandler]:
        service_name, method_name = parse_route(route)

        def decorator(impl: UnaryUnaryHandler) -> UnaryUnaryHandler:
            sig = inspect.signature(impl)
            req_type = sig.parameters["request"].annotation
            resp_type = sig.return_annotation
            handler = grpc.unary_unary_rpc_method_handler(
                impl,
                request_deserializer=req_type.FromString,
                response_serializer=resp_type.SerializeToString,
            )
            self.handlers[service_name][method_name] = handler
            return impl

        return decorator

    def unary_stream(self, route: str) -> Identity[UnaryStreamHandler]:
        service_name, method_name = parse_route(route)

        def decorator(impl: UnaryStreamHandler) -> UnaryStreamHandler:
            sig = inspect.signature(impl)
            req_type = sig.parameters["request"].annotation
            resp_type = sig.return_annotation.__args__[0]
            handler = grpc.unary_stream_rpc_method_handler(
                impl,
                request_deserializer=req_type.FromString,
                response_serializer=resp_type.SerializeToString,
            )
            self.handlers[service_name][method_name] = handler
            return impl

        return decorator

    def stream_unary(self, route: str) -> Identity[StreamUnaryHandler]:
        service_name, method_name = parse_route(route)

        def decorator(impl: StreamUnaryHandler) -> StreamUnaryHandler:
            sig = inspect.signature(impl)
            req_type = sig.parameters["requests"].annotation.__args__[0]
            resp_type = sig.return_annotation
            handler = grpc.stream_unary_rpc_method_handler(
                impl,
                request_deserializer=req_type.FromString,
                response_serializer=resp_type.SerializeToString,
            )
            self.handlers[service_name][method_name] = handler
            return impl

        return decorator

    def stream_stream(self, route: str) -> Identity[StreamStreamHandler]:
        service_name, method_name = parse_route(route)

        def decorator(impl: StreamStreamHandler) -> StreamStreamHandler:
            sig = inspect.signature(impl)
            req_type = sig.parameters["requests"].annotation.__args__[0]
            resp_type = sig.return_annotation.__args__[0]
            handler = grpc.stream_stream_rpc_method_handler(
                impl,
                request_deserializer=req_type.FromString,
                response_serializer=resp_type.SerializeToString,
            )
            self.handlers[service_name][method_name] = handler
            return impl

        return decorator

    def add_handlers(self, server: grpc.Server):
        generic_handlers = [
            grpc.method_handlers_generic_handler(service, handlers)
            for service, handlers in self.handlers.items()
        ]
        server.add_generic_rpc_handlers(generic_handlers)


def parse_route(route: str) -> typing.Tuple[str, str]:
    *_, service, method = route.rsplit("/")
    return service, method
