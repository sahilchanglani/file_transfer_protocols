import os
import time
from statistics import mean, stdev
from hyper import HTTP20Connection

SERVER_ADDRESS = '192.168.1.40'
SERVER_PORT = 8000
FILE_NAMES = [('Data/A_10kB', 'Data/B_10kB'), ('Data/A_100kB', 'Data/B_100kB'), ('Data/A_1MB', 'Data/B_1MB'), ('Data/A_10MB', 'Data/B_10MB')]

for files in FILE_NAMES:
    download_times = []
    file_sizes = []
    total_data_transferred = []
    for file_name in files:
        # Prepare the request
        client = HTTP20Connection(SERVER_ADDRESS, SERVER_PORT)
        client.request('GET', f'/{file_name}')

        # Get the response
        start_time = time.time()  # Record the start time
        response = client.get_response()

        # Check if the request was successful
        if response.status == 200:
            # Read the file content
            file_content = response.read()

            # Save the file content to a file
            with open(file_name, 'wb') as file:
                file.write(file_content)

            end_time = time.time()  # Record the end time
            download_time = end_time - start_time
            download_times.append(download_time)

            # Get the file size
            file_size = len(file_content)
            file_sizes.append(file_size)
            total_data_transferred.append(file_size + len(response.headers))
            print(len(response.headers))
            print(file_size)
            print((file_size + len(response.headers)) / file_size)

            print(f"File '{file_name}' downloaded successfully in {download_time:.6f} seconds.")
        else:
            print(f"Failed to download file '{file_name}'. Error code: {response.status}")
    
    # Calculate throughput (in kilobits per second)
    throughputs = [(file_size * 8 / 1024) / download_time for file_size, download_time in zip(file_sizes, download_times)]

    # Calculate average throughput and standard deviation
    avg_throughput = mean(throughputs)
    std_dev_throughput = stdev(throughputs)
    # Calculate average ratio of total data transferred to file size
    avg_ratio = mean([data / size for data, size in zip(total_data_transferred, file_sizes)])

    print(f"Average throughput for filesize {files[2:]}: {avg_throughput:.2f} kbps")
    print(f"Standard deviation of throughput for filesize {files[2:]}: {std_dev_throughput:.2f} kbps")
    print(f"Average ratio of total data transferred to file size for filesize {files[2:]}: {avg_ratio:.6f}")

# Close the connection
client.close()
