import grpc
from concurrent import futures
import time

from generated import request_service_pb2_grpc, request_service_pb2


class BudgetServiceServicer(request_service_pb2_grpc.BudgetServiceServicer):
    def __init__(self):
        self.entries = {}

    def CreateBudgetEntry(self, request, context):
        entry = request.entry
        self.entries[entry.entry_id] = entry
        return request_service_pb2.BudgetEntryResponse(entry=entry, status='CREATED')

    def GetBudgetEntry(self, request, context):
        entry = self.entries.get(request.entry_id)
        if entry is None:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Entry not found')
        return request_service_pb2.BudgetEntryResponse(entry=entry, status='OK')

    def ListBudgetEntries(self, request, context):
        entries = [entry for entry in self.entries.values() if entry.budget_id == request.budget_id]
        return request_service_pb2.ListBudgetEntriesResponse(entries=entries)

    def ActivateBudgetEntry(self, request, context):
        entry = self.entries.get(request.entry_id)
        if entry is None:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Entry not found')
        entry.status = 'ACTIVE'
        return request_service_pb2.BudgetEntryResponse(entry=entry, status='ACTIVATED')

    def StreamActiveBudgetEntries(self, request, context):
        for entry in self.entries.values():
            if entry.budget_id == request.budget_id and entry.status == 'ACTIVE':
                yield request_service_pb2.BudgetEntryResponse(entry=entry, status='ACTIVE')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    request_service_pb2_grpc.add_BudgetServiceServicer_to_server(BudgetServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
