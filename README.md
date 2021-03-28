An experiment with FastAPI/Flask-like syntax for implementing gRPC methods.

```python3
from grpcapi import App

app = App()

@app.unary_stream("/pkg.Service/Method")
def method(
    request: pkg.service_pb2.RequestType, context: grpc.ServicerContext
) -> Iterable[pkg.service_pb2.ResponseType]:
    yield pkg.service_pb2.ResponseType()
    yield pkg.service_pb2.ResponseType()
```
