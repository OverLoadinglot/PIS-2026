# Лабораторная 9 — gRPC

## Запуск

1. Установите зависимости:

```bash
pip install -r requirements.txt
```

2. Сгенерируйте Python-модули из `.proto`:

```bash
python -m grpc_tools.protoc -I=proto --python_out=generated --grpc_python_out=generated proto/request_service.proto
```

3. Запустите сервер:

```bash
python grpc/server.py
```

4. Запустите клиента:

```bash
python grpc/client.py
```
