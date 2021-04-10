from google.protobuf import descriptor_pool, json_format, message_factory
import grpc

_pool = descriptor_pool.Default()
_factory = message_factory.MessageFactory(_pool)


def method_descriptor(route):
    _, qualified_service, method = route.split("/")
    descriptor = _pool.FindMethodByName(f"{qualified_service}.{method}")
    return descriptor


class ProtoTransformer:
    def transform_request(self, method, request):
        return request

    def transform_response(self, method, response):
        return response


class ChannelInterceptor(grpc.Channel):
    def __init__(self, channel):
        self.channel = channel

    def close(self, *args, **kwargs):
        return self.channel.close(*args, **kwargs)

    def subscribe(self, *args, **kwargs):
        return self.channel.subscribe(*args, **kwargs)

    def unsubscribe(self, *args, **kwargs):
        return self.channel.unsubscribe(*args, **kwargs)

    def __getattr__(self, attr):
        return getattr(self.channel, attr)


class UnaryUnaryTransformerInterceptor(ProtoTransformer, ChannelInterceptor):
    def unary_unary(self, method, request_serializer=None, response_deserializer=None):
        return self.channel.unary_unary(
            method,
            lambda request: request_serializer(self.transform_request(method, request)),
            lambda response: self.transform_response(
                method, response_deserializer(response)
            ),
        )


class UnaryStreamTransformerInterceptor(ProtoTransformer, ChannelInterceptor):
    def unary_stream(self, method, request_serializer=None, response_deserializer=None):
        return self.channel.unary_stream(
            method,
            lambda request: request_serializer(self.transform_request(method, request)),
            lambda response: self.transform_response(
                method, response_deserializer(response)
            ),
        )


class StreamUnaryTransformerInterceptor(ProtoTransformer, ChannelInterceptor):
    def stream_unary(self, method, request_serializer=None, response_deserializer=None):
        return self.channel.stream_unary(
            method,
            lambda request: request_serializer(self.transform_request(method, request)),
            lambda response: self.transform_response(
                method, response_deserializer(response)
            ),
        )


class StreamStreamTransformerInterceptor(ProtoTransformer, ChannelInterceptor):
    def stream_stream(
        self, method, request_serializer=None, response_deserializer=None
    ):
        return self.channel.stream_stream(
            method,
            lambda request: request_serializer(self.transform_request(method, request)),
            lambda response: self.transform_response(
                method, response_deserializer(response)
            ),
        )


class DictRequestTransformer(ProtoTransformer):
    def transform_request(self, method, request):
        method_desc = method_descriptor(method)
        cls = _factory.GetPrototype(method_desc.input_type)
        msg = json_format.ParseDict(request, cls())
        return msg


class DictResponseTransformer(ProtoTransformer):
    def transform_response(self, method, response):
        return json_format.MessageToDict(
            response,
            including_default_value_fields=True,
            preserving_proto_field_name=True,
        )


class DictTransformer(DictRequestTransformer, DictResponseTransformer):
    pass
