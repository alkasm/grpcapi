from google.protobuf import json_format
import grpc
from route_guide_pb2_grpc import RouteGuideStub
from route_guide_pb2 import Point, Rectangle, RouteNote
from grpcapi.client_interceptor.v2 import *


class DictTransformerInterceptor(
    DictTransformer,
    UnaryUnaryTransformerInterceptor,
    UnaryStreamTransformerInterceptor,
    StreamUnaryTransformerInterceptor,
    StreamStreamTransformerInterceptor,
):
    pass


channel = grpc.intercept_channel(
    grpc.insecure_channel("[::]:50051"), DictTransformerInterceptor()
)
stub = RouteGuideStub(channel)

resp = stub.GetFeature({"latitude": 1234, "longitude": 1111})
print("GetFeature:", resp)

resp = stub.ListFeatures(
    {
        "lo": {"latitude": 1234, "longitude": 1111},
        "hi": {"latitude": 1234, "longitude": 3333},
    }
)
print("ListFeatures:", *resp)

resp = stub.RecordRoute(
    iter(
        [
            {"latitude": 1234, "longitude": 1111},
            {"latitude": 1234, "longitude": 2222},
            {"latitude": 1234, "longitude": 3333},
        ]
    )
)
print("RecordRoute:", resp)

resp = stub.RouteChat(
    iter(
        [
            {"message": "msg1"},
            {"message": "msg2"},
            {"message": "msg3"},
        ]
    )
)
print("RouteChat:", *resp)
