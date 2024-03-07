import grpc
import file_transfer_pb2
import file_transfer_pb2_grpc
import os
import time
from statistics import mean, stdev

SERVER_ADDRESS = 'localhost:8000'
FILE_PATHS = ['Data/A_10kB', 'Data/B_10kB', 'Data/A_100kB', 'Data/B_100kB', 'Data/A_1MB', 'Data/B_1MB', 'Data/A_10MB', 'Data/B_10MB']

def download_file(stub, file_path):
    request = file_transfer_pb2.FileRequest(file_path=file_path)
    response = stub.DownloadFile(request)
    return response.content

def main():
    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        stub = file_transfer_pb2_grpc.FileTransferStub(channel)

        download_times = []
        file_sizes = []
        total_data_transferred = []

        for file_path in FILE_PATHS:
            start_time = time.time()

            content = download_file(stub, file_path)

            end_time = time.time()
            download_time = end_time - start_time

            with open(file_path.replace('/', '_'), 'wb') as file:
                file.write(content)

            file_size = len(content)
            file_sizes.append(file_size)
            total_data_transferred.append(file_size)

            print(f"File '{file_path}' downloaded successfully in {download_time:.6f} seconds.")

        throughputs = [(file_size * 8 / 1024) / download_time for file_size, download_time in zip(file_sizes, download_times)]
        avg_throughput = mean(throughputs)
        std_dev_throughput = stdev(throughputs)
        avg_ratio = mean([data / size for data, size in zip(total_data_transferred, file_sizes)])

        print(f"Average throughput: {avg_throughput:.2f} kbps")
        print(f"Standard deviation of throughput: {std_dev_throughput:.2f} kbps")
        print(f"Average ratio of total data transferred to file size: {avg_ratio:.6f}")

if __name__ == "__main__":
    main()
