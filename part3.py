from socket import *
import socket
import csv

# the server will be serving on port 6500
serverPort = 6500

# create a TCP socket
serverSocket = socket.socket(AF_INET, SOCK_STREAM)

# associate the socket with the server address
serverSocket.bind(('', serverPort))

# become a server socket and queue up as many as 5 connect requests
serverSocket.listen(5)

# *****************check how to connect from different device

print("The Server Is Ready to Receive Request Serving On Port 6500")

while True:
    # accept connections
    (connectionSocket, address) = serverSocket.accept()

    # receive data
    data = connectionSocket.recv(1024).decode()

    # get the desired request from data response 'GET */REQUEST* ...etc'
    request = data.split(' ')[1]
    print("sent: ", request)

    if (request == '/') or (request.endswith(".html")) or request.endswith('index.html'):

        myFile = open('main.html')  # open the main.html file and read it

        # send response header then html #
        # HTTP 200 response status indicates that the request has succeeded
        connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())

        # specify that the type is text/html
        connectionSocket.send('Content-Type: text/html \r\n'.encode())

        # end of header
        connectionSocket.send('\r\n'.encode())

        # send html code
        connectionSocket.send((myFile.read()).encode())

    elif request.endswith('.css') or request.endswith('.css/') or request.endswith('css'):
        myFile = open('cssFile.css')

        connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())
        connectionSocket.send('Content-Type: text/css \r\n'.encode())
        connectionSocket.send('\r\n'.encode())

        # Send encoded css code .
        connectionSocket.send((myFile.read()).encode())
        connectionSocket.close()

    elif request.endswith('.jpg') or request.endswith('.jpg/'):

        # open image in read-binary mode
        image = open('lap.jpg', 'rb')

        connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())
        connectionSocket.send('Content-Type: image/jpeg \r\n'.encode())
        connectionSocket.send('\r\n'.encode())

        connectionSocket.send(image.read())
        image.close()

    elif request.endswith('.png') or request.endswith('.png/'):

        image = open('w202.png', 'rb')

        connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())
        connectionSocket.send('Content-Type: image/png \r\n'.encode())
        connectionSocket.send('\r\n'.encode())

        connectionSocket.send(image.read())
        image.close()

    elif request.endswith('SortByName') or request.endswith('SortByName/'):
        # read csv file
        items = csv.reader(open('itemsSheet.csv'), delimiter=',')

        # sort csv based on first column NAME file store the sorted in sortedList
        sortedList = sorted(items, key=lambda column: column[0])

        connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())

        # send as text/html
        connectionSocket.send('Content-Type: text/html \r\n'.encode())

        connectionSocket.send('\r\n'.encode())
        connectionSocket.send('SORTED BY NAME\n\n'.encode())

        # display each sorted item on one line
        for eachItem in sortedList:
            display = f"<h1>{eachItem}</h1>"

            connectionSocket.send(display.encode())

    elif request.endswith('SortByPrice') or request.endswith('SortByPrice/'):
        items = csv.reader(open('itemsSheet.csv'))

        sortedList = sorted(items, key=lambda column: int(column[1]), reverse=True)

        connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())
        connectionSocket.send('Content-Type: text/html \r\n'.encode())  # Set the type to HTML page.
        connectionSocket.send('\r\n'.encode())  # End of the header of the response.
        connectionSocket.send('SORTED BY PRICE\n\n'.encode())

        for eachItem in sortedList:
            display = f"<h1>{eachItem}</h1>"

            connectionSocket.send(display.encode())

    else:
        # if the request is not found we send
        # 404 error not found html and display client io
        # and port number

        notFoundPage = open('404page.html')
        notFoundError = notFoundPage.read()
        notFoundPage.close()

        # response status indicates that file is not found
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n'.encode())
        connectionSocket.send('Content-Type: text/html \r\n'.encode())
        connectionSocket.send('\r\n'.encode())

        connectionSocket.send(notFoundError.encode())

        # display the client IP and port number
        html = f"<h1>Client IP and Port No. {address} </h1>"
        connectionSocket.send(html.encode())

    connectionSocket.close()