import http.client
import os

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 8000
FILE_NAME = 'Data/A_10kB'

# Prepare the request
client = http.client.HTTPConnection(SERVER_ADDRESS, SERVER_PORT)
client.request('GET', f'/{FILE_NAME}')

# Get the response
response = client.getresponse()

# Check if the request was successful
if response.status == 200:
    file_content = response.read()

    with open(FILE_NAME, 'wb') as file:
        file.write(file_content)

    print(f"File '{FILE_NAME}' downloaded successfully.")
else:
    print(f"Failed to download file '{FILE_NAME}'. Error code: {response.status}")

# Close the connection
client.close()