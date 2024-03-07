import http.client
import os
import time

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 8000
FILE_NAME = 'Data/A_10kB'

# Prepare the request
client = http.client.HTTPConnection(SERVER_ADDRESS, SERVER_PORT)
client.request('GET', f'/{FILE_NAME}')

start_time = time.time()  # Record the start time
# Get the response
response = client.getresponse()

# Check if the request was successful
if response.status == 200:
    file_content = response.read()

    with open(FILE_NAME, 'wb') as file:
        file.write(file_content)

    end_time = time.time()  # Record the end time
    download_time = end_time - start_time
    print(f"File '{FILE_NAME}' downloaded successfully in {download_time:.6f} seconds.")
else:
    print(f"Failed to download file '{FILE_NAME}'. Error code: {response.status}")

# Close the connection
client.close()