Example service from https://github.com/grpc/grpc/tree/master/examples.

The server is implemented using `grpcapi`; the client is typical gRPC.

```
$ python server.py
```

```
$ python client.py
GetFeature: {"name": "feature"}
ListFeatures: {"name": "feature1"} {"name": "feature2"}
RecordRoute: {"pointCount": 3}
RouteChat: {"message": "msg1"} {"message": "msg2"} {"message": "msg3"}
```
