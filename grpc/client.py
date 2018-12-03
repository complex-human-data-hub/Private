import grpc
import json
import service_pb2
import service_pb2_grpc
import sys

def main(cmd):
    host = 'localhost'
    port = 51134

    with open('server.crt', 'rb') as f:
        trusted_certs = f.read()

    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    channel = grpc.secure_channel('{}:{}'.format(host, port), credentials)

    stub = service_pb2_grpc.ServerStub(channel)
    stub.Foo(service_pb2.Empty())
    project_uid = '12345'
    req = {
        #'cmd': 'l = [0,1,1]'
        'cmd': cmd
    }
    response = stub.Private(service_pb2.PrivateParcel(json=json.dumps(req), project_uid=project_uid))
    print json.loads(response.json)

if __name__ == '__main__':
    main(sys.argv[1])
