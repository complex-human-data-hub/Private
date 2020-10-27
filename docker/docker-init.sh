#!/bin/sh

#Load private data
python Private/private_data.py

#Start private server
python grpc/server.py

