import http.client
import os
import time
from statistics import mean, stdev

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 8000
FILE_NAMES = [('Data/A_10kB', 'Data/B_10kB'), 'Data/A_1MB', 'Data/A_10MB', 'Data/A_100kB']


for files in FILE_NAMES:
    download_times = []
    file_sizes = []
    for file_name in files:
        # Prepare the request
        client = http.client.HTTPConnection(SERVER_ADDRESS, SERVER_PORT)
        client.request('GET', f'/{file_name}')

        # Get the response
        start_time = time.time()  # Record the start time
        response = client.getresponse()

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

            print(f"File '{file_name}' downloaded successfully in {download_time:.6f} seconds.")
        else:
            print(f"Failed to download file '{file_name}'. Error code: {response.status}")
    
    
    # Calculate throughput (in kilobits per second)
    throughputs = [(file_size * 8 / 1024) / download_time for file_size, download_time in zip(file_sizes, download_times)]

    # Calculate average throughput and standard deviation
    avg_throughput = mean(throughputs)
    std_dev_throughput = stdev(throughputs)

    print(f"Average throughput for filesize {files[2:]}: {avg_throughput:.2f} kbps")
    print(f"Standard deviation of throughput for filesize {files[2:]}: {std_dev_throughput:.2f} kbps")

# Close the connection
client.close()
