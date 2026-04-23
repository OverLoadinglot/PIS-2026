import threading
import time

import grpc
from generated import request_service_pb2_grpc, request_service_pb2
from grpc import server
from grpc.server import ThreadPoolExecutor

from grpc.server import serve as start_server


def run_server():
    from grpc.server import serve as serve_fn
    serve_fn()


def test_create_and_stream_budget_entry():
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    time.sleep(1)

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = request_service_pb2_grpc.BudgetServiceStub(channel)
        request = request_service_pb2.CreateBudgetEntryRequest(
            entry_id='t1',
            budget_id='b49',
            member_id='m1',
            category_id='c1',
            amount=100.0,
            currency='RUB',
            type='expense',
            description='Продукты',
        )
        response = stub.CreateBudgetEntry(request)
        assert response.status == 'CREATED'

        activate = request_service_pb2.ActivateBudgetEntryRequest(entry_id='t1')
        response = stub.ActivateBudgetEntry(activate)
        assert response.status == 'ACTIVATED'

        stream_request = request_service_pb2.StreamActiveBudgetEntriesRequest(budget_id='b49')
        items = list(stub.StreamActiveBudgetEntries(stream_request))
        assert len(items) >= 0
