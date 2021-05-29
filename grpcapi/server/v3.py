import collections
from google.protobuf.descriptor import MethodDescriptor
from google.protobuf.descriptor_pb2 import MethodDescriptorProto
from google.protobuf.message_factory import MessageFactory
import grpc
from .v2 import Identity, RpcMethod

__all__ = ["App"]


class App:
    def __init__(self, factory=None):
        self.handlers = collections.defaultdict(dict)
        self.factory = factory or MessageFactory()

    def rpc(self, desc: MethodDescriptor) -> Identity[RpcMethod]:
        proto = MethodDescriptorProto()
        desc.CopyToProto(proto)  # type: ignore[attr-defined]
        handler_factory = {
            (False, False): grpc.unary_unary_rpc_method_handler,
            (False, True): grpc.unary_stream_rpc_method_handler,
            (True, False): grpc.stream_unary_rpc_method_handler,
            (True, True): grpc.stream_stream_rpc_method_handler,
        }[proto.client_streaming, proto.server_streaming]

        input_type = self.factory.GetPrototype(desc.input_type)
        output_type = self.factory.GetPrototype(desc.output_type)

        def wrapper(f):
            handler = handler_factory(
                f,
                request_deserializer=input_type.FromString,
                response_serializer=output_type.SerializeToString,
            )
            self.handlers[desc.containing_service.full_name][desc.name] = handler

        return wrapper

    def add_handlers(self, server: grpc.Server) -> None:
        generic_handlers = [
            grpc.method_handlers_generic_handler(service, handlers)
            for service, handlers in self.handlers.items()
        ]
        server.add_generic_rpc_handlers(generic_handlers)
