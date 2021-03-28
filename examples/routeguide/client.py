from google.protobuf import json_format
import grpc
from route_guide_pb2_grpc import RouteGuideStub
from route_guide_pb2 import Point, Rectangle, RouteNote

channel = grpc.insecure_channel("[::]:50051")
stub = RouteGuideStub(channel)


def jsonify(*responses):
    return " ".join([json_format.MessageToJson(r, indent=None) for r in responses])


resp = stub.GetFeature(Point())
print("GetFeature:", jsonify(resp))

resp = stub.ListFeatures(Rectangle())
print("ListFeatures:", jsonify(*resp))

resp = stub.RecordRoute(iter([Point(), Point(), Point()]))
print("RecordRoute:", jsonify(resp))

resp = stub.RouteChat(
    iter(
        [
            RouteNote(message="msg1"),
            RouteNote(message="msg2"),
            RouteNote(message="msg3"),
        ]
    )
)
print("RouteChat:", jsonify(*resp))
