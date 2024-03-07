import grpc
import file_transfer_pb2
import file_transfer_pb2_grpc
from concurrent import futures

class FileTransferServicer(file_transfer_pb2_grpc.FileTransferServicer):
    def DownloadFile(self, request, context):
        file_path = request.file_path
        try:
            with open(file_path, 'rb') as file:
                content = file.read()
            return file_transfer_pb2.FileResponse(content=content)
        except FileNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"File not found: {file_path}")
            return file_transfer_pb2.FileResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_transfer_pb2_grpc.add_FileTransferServicer_to_server(FileTransferServicer(), server)
    server.add_insecure_port('[::]:8000')
    print("Serving on port 8000...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()