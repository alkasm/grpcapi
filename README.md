An experiment with FastAPI/Flask-like syntax for implementing gRPC methods.

```python3
from grpcapi.v1 import App

app = App()

@app.unary_stream("/pkg.Service/Method")
def method(
    request: pkg.service_pb2.RequestType, context: grpc.ServicerContext
) -> Iterable[pkg.service_pb2.ResponseType]:
    yield pkg.service_pb2.ResponseType()
    yield pkg.service_pb2.ResponseType()
```

The `v2.App` can be used without type annotations, using only a little bit of magic.

```python3
from grpcapi.v2 import App
from pkg_pb2_grpc import MyServiceServicer

app = App()

@app.rpc(MyServiceServicer.Method)
def method(request, context):
    yield pkg.service_pb2.ResponseType()
    yield pkg.service_pb2.ResponseType()
```

See [examples/routeguide](examples/routeguide) for runnable examples with the gRPC example Route Guide service.
