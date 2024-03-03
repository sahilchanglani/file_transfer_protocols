import http.client

def main():
    connection = http.client.HTTPConnection('localhost', 8000)
    connection.request('GET', '/')
    response = connection.getresponse()
    print(response.status, response.reason)
    data = response.read()
    print(data.decode())

if __name__ == "__main__":
    main()
