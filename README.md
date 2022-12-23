# loyalty

part of https://github.com/cmrd-a/graduate_work

todo:
- [ ] alembic
- [ ] docker
- [ ] queries

1. `export PROTO_DIR=src/protos`
2. `python -m grpc_tools.protoc -I $PROTO_DIR --python_out=$PROTO_DIR --grpc_python_out=$PROTO_DIR --pyi_out=$PROTO_DIR $PROTO_DIR/*.proto`