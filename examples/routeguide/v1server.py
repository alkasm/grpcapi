import grpcapi.server.v1
from route_guide_pb2 import (
    Point,
    Feature,
    Rectangle,
    RouteNote,
    RouteSummary,
)
import grpc
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable
import logging

logging.basicConfig(level=logging.DEBUG)

app = grpcapi.server.v1.App()


@app.unary_unary("/routeguide.RouteGuide/GetFeature")
def get_feature(request: Point, context: grpc.ServicerContext) -> Feature:
    return Feature(name="feature")


@app.unary_stream("/routeguide.RouteGuide/ListFeatures")
def list_features(
    request: Rectangle, context: grpc.ServicerContext
) -> Iterable[Feature]:
    yield Feature(name="feature1")
    yield Feature(name="feature2")


@app.stream_unary("/routeguide.RouteGuide/RecordRoute")
def record_route(
    requests: Iterable[Point], context: grpc.ServicerContext
) -> RouteSummary:
    count = len(list(requests))
    return RouteSummary(point_count=count)


@app.stream_stream("/routeguide.RouteGuide/RouteChat")
def route_chat(
    requests: Iterable[RouteNote], context: grpc.ServicerContext
) -> Iterable[RouteNote]:
    for note in requests:
        yield note


server = grpc.server(ThreadPoolExecutor())
app.add_handlers(server)
server.add_insecure_port("[::]:50051")
server.start()
server.wait_for_termination()
