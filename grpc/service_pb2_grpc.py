# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import service_pb2 as service__pb2


class ServerStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Foo = channel.unary_unary(
        '/Server/Foo',
        request_serializer=service__pb2.Empty.SerializeToString,
        response_deserializer=service__pb2.Empty.FromString,
        )
    self.Private = channel.unary_unary(
        '/Server/Private',
        request_serializer=service__pb2.PrivateParcel.SerializeToString,
        response_deserializer=service__pb2.PrivateParcel.FromString,
        )


class ServerServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Foo(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Private(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ServerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Foo': grpc.unary_unary_rpc_method_handler(
          servicer.Foo,
          request_deserializer=service__pb2.Empty.FromString,
          response_serializer=service__pb2.Empty.SerializeToString,
      ),
      'Private': grpc.unary_unary_rpc_method_handler(
          servicer.Private,
          request_deserializer=service__pb2.PrivateParcel.FromString,
          response_serializer=service__pb2.PrivateParcel.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Server', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))