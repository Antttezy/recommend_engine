#!/bin/sh

GRPC_IN=api/grpc
GRPC_OUT=api/grpc/vector_processor

python -m grpc_tools.protoc \
-I$GRPC_IN --python_out=$GRPC_OUT --pyi_out=$GRPC_OUT --grpc_python_out=$GRPC_OUT \
vector_processor.proto

sed -i "s/^import \(.*_pb2\)/from . import \1/" api/grpc/vector_processor/vector_processor_pb2_grpc.py
