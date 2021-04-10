import grpcapi.v2
from route_guide_pb2 import (
    Point,
    Feature,
    Rectangle,
    RouteNote,
    RouteSummary,
)
from route_guide_pb2_grpc import RouteGuideServicer
import grpc
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable
import logging

logging.basicConfig(level=logging.DEBUG)

app = grpcapi.v2.App()


@app.rpc(RouteGuideServicer.GetFeature)
def get_feature(request, context):
    return Feature(name="feature")


@app.rpc(RouteGuideServicer.ListFeatures)
def list_features(request, context):
    yield Feature(name="feature1")
    yield Feature(name="feature2")


@app.rpc(RouteGuideServicer.RecordRoute)
def record_route(requests, context):
    count = len(list(requests))
    return RouteSummary(point_count=count)


@app.rpc(RouteGuideServicer.RouteChat)
def route_chat(requests, context):
    for note in requests:
        yield note


server = grpc.server(ThreadPoolExecutor())
app.add_handlers(server)
server.add_insecure_port("[::]:50051")
server.start()
server.wait_for_termination()
