from google.protobuf import json_format, descriptor_pool, message_factory
import grpc

_pool = descriptor_pool.Default()
_factory = message_factory.MessageFactory(_pool)


def method_descriptor(route):
    _, qualified_service, method = route.split("/")
    descriptor = _pool.FindMethodByName(f"{qualified_service}.{method}")
    return descriptor


class ProtoTransformer:
    def transform_request(self, client_call_details, request):
        return request

    def transform_response(self, client_call_details, response):
        return response


class UnaryUnaryTransformerInterceptor(
    ProtoTransformer, grpc.UnaryUnaryClientInterceptor
):
    def intercept_unary_unary(self, continuation, client_call_details, request):
        req = self.transform_request(client_call_details, request)
        resp = continuation(client_call_details, req)
        return self.transform_response(client_call_details, resp)


class UnaryStreamTransformerInterceptor(
    ProtoTransformer, grpc.UnaryStreamClientInterceptor
):
    def intercept_unary_stream(self, continuation, client_call_details, request):
        req = self.transform_request(client_call_details, request)
        resp = continuation(client_call_details, req)
        yield from (self.transform_response(client_call_details, r) for r in resp)


class StreamUnaryTransformerInterceptor(
    ProtoTransformer, grpc.StreamUnaryClientInterceptor
):
    def intercept_stream_unary(
        self, continuation, client_call_details, request_iterator
    ):
        reqs = (
            self.transform_request(client_call_details, r) for r in request_iterator
        )
        resp = continuation(client_call_details, reqs)
        return self.transform_response(resp)


class StreamStreamTransformerInterceptor(
    ProtoTransformer, grpc.StreamStreamClientInterceptor
):
    def intercept_stream_stream(
        self, continuation, client_call_details, request_iterator
    ):
        reqs = (
            self.transform_request(client_call_details, r) for r in request_iterator
        )
        resp = continuation(client_call_details, reqs)
        yield from (self.transform_response(client_call_details, r) for r in resp)


class DictRequestTransformer(ProtoTransformer):
    def transform_request(self, client_call_details, request):
        method_desc = method_descriptor(client_call_details.method)
        cls = _factory.GetPrototype(method_desc.input_type)
        msg = json_format.ParseDict(request, cls())
        return msg


class DictResponseTransformer(ProtoTransformer):
    def transform_response(self, client_call_details, response):
        return json_format.MessageToDict(
            response,
            including_default_value_fields=True,
            preserving_proto_field_name=True,
        )


class DictTransformer(DictRequestTransformer, DictResponseTransformer):
    pass
