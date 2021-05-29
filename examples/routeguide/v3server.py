import grpcapi.server.v3
import route_guide_pb2
import grpc
from concurrent.futures import ThreadPoolExecutor
import logging


logging.basicConfig(level=logging.DEBUG)


def md(module, service, method):
    return module.DESCRIPTOR.services_by_name[service].methods_by_name[method]


app = grpcapi.server.v3.App()

get_feature_desc = md(route_guide_pb2, "RouteGuide", "GetFeature")
list_features_desc = md(route_guide_pb2, "RouteGuide", "ListFeatures")
record_route_desc = md(route_guide_pb2, "RouteGuide", "RecordRoute")
route_chat_desc = md(route_guide_pb2, "RouteGuide", "RouteChat")


@app.rpc(get_feature_desc)
def get_feature(request, context):
    return route_guide_pb2.Feature(name="feature")


@app.rpc(list_features_desc)
def list_features(request, context):
    yield route_guide_pb2.Feature(name="feature1")
    yield route_guide_pb2.Feature(name="feature2")


@app.rpc(record_route_desc)
def record_route(requests, context):
    count = len(list(requests))
    return route_guide_pb2.RouteSummary(point_count=count)


@app.rpc(route_chat_desc)
def route_chat(requests, context):
    for note in requests:
        yield note


server = grpc.server(ThreadPoolExecutor())
app.add_handlers(server)
server.add_insecure_port("[::]:50051")
server.start()
server.wait_for_termination()
