from socket import *
import time

webServerName = input("Enter URL: ")
# webServerName= 'www.google.com'


# create a new socket using the given address family(IPV4), socket type
socket = socket(AF_INET, SOCK_STREAM)

startTime = time.time()

# this is the http request that will be sent later
headReq = 'HEAD / HTTP/1.0\r\nHost:' + webServerName + '\r\n\r\n'


try:
    # now we connect to the desired web server on port '80' (http)
    socket.connect((webServerName, 80))

    # send the http head request and encode them in bytes
    socket.send(bytes(headReq, 'utf-8'))

    while True:

        # receive http response in 1024 bytes buffer size
        responseData = socket.recv(1024)
        if len(responseData) < 1:
            break

        # print format for http head response
        print(str(responseData).replace(r"\r\n", '\n').strip("b\'"))

    timeElapsed = time.time() - startTime
    socket.close()
    print("**************Sent/Received Elapsed Time**************", timeElapsed, "ms")

except OSError:

    print("Error:Please check entered URL and try again")
