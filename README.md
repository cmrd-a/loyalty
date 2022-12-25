# loyalty

Часть [основного проекта](https://github.com/cmrd-a/graduate_work)

### Генерация кода из протников
1. `export PROTO_DIR=src/protos`
2. `python -m grpc_tools.protoc -I $PROTO_DIR --python_out=$PROTO_DIR --grpc_python_out=$PROTO_DIR --pyi_out=$PROTO_DIR $PROTO_DIR/*.proto`

### Создание и применение миграций
1. `alembic revision --autogenerate -m "Added initial tables"`
2. `alembic upgrade head`
