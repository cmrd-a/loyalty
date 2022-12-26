# Система лояльности
Часть [основного проекта](https://github.com/cmrd-a/graduate_work)

Позволяет создавать и применять промокоды и персональные скидки.

Все ручки кроме создания должен вызывать предполагаемый сервис биллинга.

Пример алгоритма использования:
1. Создание промокода (Менеджер -> PromoCode.Create)
2. Резервирование промокода в момент начала оплаты (Биллинг -> PromoCode.Create)
   - Применение при завершении оплаты (Биллинг -> PromoCode.Apply)
   - Или отмена резерва при отмене оплаты (Биллинг -> PromoCode.Free)

### Генерация кода из протников
1. `export PROTO_DIR=src/protos`
2. `python -m grpc_tools.protoc -I $PROTO_DIR --python_out=$PROTO_DIR --grpc_python_out=$PROTO_DIR --pyi_out=$PROTO_DIR $PROTO_DIR/*.proto`

### Создание и применение миграций
1. `alembic revision --autogenerate -m "some changes"`
2. `alembic upgrade head`
