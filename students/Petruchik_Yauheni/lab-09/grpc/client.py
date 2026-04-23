import grpc
from generated import request_service_pb2_grpc, request_service_pb2


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = request_service_pb2_grpc.BudgetServiceStub(channel)
        request = request_service_pb2.CreateBudgetEntryRequest(
            entry_id='t1',
            budget_id='b49',
            member_id='m1',
            category_id='c1',
            amount=150.0,
            currency='RUB',
            type='expense',
            description='Продукты',
        )
        response = stub.CreateBudgetEntry(request)
        print('Create response:', response.status)

        stream_request = request_service_pb2.StreamActiveBudgetEntriesRequest(budget_id='b49')
        for item in stub.StreamActiveBudgetEntries(stream_request):
            print('Stream item:', item)


if __name__ == '__main__':
    run()
