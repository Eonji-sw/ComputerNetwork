from socket import *


serverName = '127.0.0.1'
serverPort = 12345  # 임의의 port

# GET-응답 200, GET-응답 404, HEAD-응답 200, HEAD-404, POST-응답 201
request_method, request_file = input(str()).split()

# create TCP socket for server
clientSocket = socket(AF_INET, SOCK_STREAM)
# connect server and socket
clientSocket.connect((serverName, serverPort))


if request_method == 'GET':
    if request_file == './test.html':  # GET-응답 200
        clientSocket.send(
            b"GET 200 ./test.html HTTP/1.0\r\nHost: 127.0.0.1\r\n")  # send request message
        modifiedSentence = clientSocket.recv(1024)  # receive data
        print('From Server:', modifiedSentence.decode())
        modifiedSentence = clientSocket.recv(1024)  # receive data
        print('From Server:', modifiedSentence.decode())
    else:  # GET-응답 404
        clientSocket.send(
            b"GET 404 ./test3.html HTTP/1.0\r\nHost: 127.0.0.1\r\n")  # send request message
        modifiedSentence = clientSocket.recv(1024)  # receive data
        print('From Server:', modifiedSentence.decode())

elif request_method == 'HEAD':
    if request_file == './test.html':  # HEAD-응답 200
        clientSocket.send(
            b"HEAD 200 ./test.html HTTP/1.0\r\nHost: 127.0.0.1\r\n")  # send request message
        modifiedSentence = clientSocket.recv(1024)  # receive data
        print('From Server:', modifiedSentence.decode())
    else:  # HEAD-응답 404
        clientSocket.send(
            b"HEAD 404 ./test3.html HTTP/1.0\r\nHost: 127.0.0.1\r\n")  # send request message
        modifiedSentence = clientSocket.recv(1024)  # receive data
        print('From Server:', modifiedSentence.decode())

elif request_method == 'POST':  # POST-응답 201
    # send request message
    clientSocket.send(b"POST 201 ./test2.html HTTP/1.0\r\nHost: 127.0.0.1\r\n")
    clientSocket.send(b"This is test file for POST")  # send POST message
    modifiedSentence = clientSocket.recv(1024)  # receive data
    print('From Server:', modifiedSentence.decode())
    modifiedSentence = clientSocket.recv(1024)  # receive data
    print('From Server:', modifiedSentence.decode())


clientSocket.close()  # socket close
