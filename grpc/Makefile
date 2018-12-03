stubs:
	python -m grpc.tools.protoc -I/usr/local/include -I. --python_out=./ --grpc_python_out=./ service.proto

#client:
#	python client.py 

server:
	python server.py

gen_key:
	openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.crt
