Example service from https://github.com/grpc/grpc/tree/master/examples.

```
$ python v1server.py  # or v2server.py
```

```
$ python client.py
GetFeature: {"name": "feature"}
ListFeatures: {"name": "feature1"} {"name": "feature2"}
RecordRoute: {"pointCount": 3}
RouteChat: {"message": "msg1"} {"message": "msg2"} {"message": "msg3"}
```

Codegen
```
$ python -m grpc_tools.protoc -I./ --python_out=./ --mypy_out=./ --grpc_python_out=./ route_guide.proto 
```
