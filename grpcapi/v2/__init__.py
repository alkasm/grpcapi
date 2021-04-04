import collections
import importlib
import typing
from google.protobuf import message
import grpc

__all__ = ["App"]


class HandlerExtractor:
    def __init__(self, method_name: str):
        self.method_name: str = method_name
        self.service_name: typing.Optional[str] = None
        self.handler: typing.Optional[grpc.RpcMethodHandler] = None
        self.route: typing.Optional[str] = None

    def __getattr__(self, attr):
        """Accessing an unknown attr produces None instead of AttributeError"""
        return None

    def add_generic_rpc_handlers(self, handlers):
        generic_handler = handlers[0]
        self.service_name = generic_handler.service_name()
        self.route = f"/{self.service_name}/{self.method_name}"
        details = grpc.HandlerCallDetails()
        details.method = self.route
        self.handler = generic_handler.service(details)


Message = typing.TypeVar("Message", bound=message.Message)
UnaryOrStream = typing.Union[Message, typing.Iterable[Message]]
InputRpcMethod = typing.Callable[
    [typing.Any, UnaryOrStream, grpc.ServicerContext], UnaryOrStream
]
RpcMethod = typing.Callable[[UnaryOrStream, grpc.ServicerContext], UnaryOrStream]

T = typing.TypeVar("T")
Identity = typing.Callable[[T], T]


class App:
    def __init__(self):
        self.handlers = collections.defaultdict(dict)

    def rpc(self, method: InputRpcMethod) -> Identity[RpcMethod]:
        servicer_name, method_name = method.__qualname__.split(".", 1)
        mod = importlib.import_module(method.__module__)
        adder = getattr(mod, f"add_{servicer_name}_to_server")
        # Create a pseudo servicer/server and intercept the values gRPC adds.
        extractor = HandlerExtractor(method_name)
        adder(extractor, extractor)
        assert extractor.handler is not None
        handler = extractor.handler
        impl_attr = {
            (False, False): "unary_unary",
            (False, True): "unary_stream",
            (True, False): "stream_unary",
            (True, True): "stream_stream",
        }[handler.request_streaming, handler.response_streaming]

        def decorator(impl: RpcMethod) -> RpcMethod:
            impl_handler = handler._replace(**{impl_attr: impl})
            self.handlers[extractor.service_name][extractor.method_name] = impl_handler
            return impl

        return decorator

    def add_handlers(self, server: grpc.Server) -> None:
        generic_handlers = [
            grpc.method_handlers_generic_handler(service, handlers)
            for service, handlers in self.handlers.items()
        ]
        server.add_generic_rpc_handlers(generic_handlers)
