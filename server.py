from socket import *
from os.path import *


serverName = '127.0.0.1'
serverPort = 12345  # 임의의 port

serverSocket = socket(AF_INET, SOCK_STREAM)  # create TCP socket
serverSocket.bind((serverName, serverPort))  # ip address, port 할당하여 socket 정의
serverSocket.listen(1)  # server begins listening for incoming TCP requests
print('***** The server is ready to receive *****')

while True:  # loop forever
    # server waits on accept() for incoming requests, new socket created on return
    connectionSocket, addr = serverSocket.accept()
    print(str(addr), " connect")  # connect 완료했다고 알림

    sentence = connectionSocket.recv(1024).decode()  # read bytes from socket
    print('***** check request message *****\n' +
          sentence + '\n')  # check request message

    request_method = sentence.split()[0]  # request method
    request_file = sentence.split()[2]  # request file name
    request_file_type = splitext(request_file)[1]  # request file type

    # GET-응답 200, GET-응답 404, HEAD-응답 200, HEAD-404, POST-응답 201
    if request_method == 'GET':
        if exists(request_file):  # GET-응답 200
            with open(request_file, 'r', encoding="UTF-8") as f:  # read file for GET
                capitalizedSentence = ''
                for line in f:
                    capitalizedSentence += line

            start = capitalizedSentence.index('<p>') + 3  # <body> 시작 위치
            end = capitalizedSentence.index('</p>')  # <body> 끝 위치
            request_file_byte = len(
                capitalizedSentence[slice(start, end)])  # body length

            connectionSocket.send("HTTP/1.0 200 OK {}\r\nHost: 127.0.0.1\r\nContent-Type: {}; charset=UTF-8\r\nContent-Length: {}Bytes\r\n".format(
                request_file, request_file_type, request_file_byte).encode())  # send data
            connectionSocket.send(
                capitalizedSentence.encode())  # send file data
            connectionSocket.close()  # socket close
        else:  # GET-응답 404
            print('No File! :(\n')
            connectionSocket.send(
                "HTTP/1.0 404 NOT FOUND {}\r\nHost: 127.0.0.1\r\n".format(request_file).encode())  # send data
            connectionSocket.close()  # socket close

    elif request_method == 'HEAD':
        if exists(request_file):  # HEAD-응답 200
            with open(request_file, 'r', encoding="UTF-8") as f:  # read file for HEAD
                capitalizedSentence = ''
                for line in f:
                    capitalizedSentence += line

            start = capitalizedSentence.index('<p>') + 3  # <body> 시작 위치
            end = capitalizedSentence.index('</p>')  # <body> 끝 위치
            request_file_byte = len(
                capitalizedSentence[slice(start, end)])  # body length

            connectionSocket.send("HTTP/1.0 200 OK {}\r\nHost: 127.0.0.1\r\nContent-Type: {}; charset=UTF-8\r\nContent-Length: {}Bytes\r\n\r\n".format(
                request_file, request_file_type, request_file_byte).encode())  # send data
            connectionSocket.close()  # socket close
        else:  # HEAD-응답 404
            print('No File! :(\n')
            connectionSocket.send(
                "HTTP/1.0 404 NOT FOUND {}\r\nHost: 127.0.0.1\r\n\r\n".format(request_file).encode())  # send data
            connectionSocket.close()  # socket close

    elif request_method == 'POST':  # POST-응답 201
        data = sentence.split('\r\n')[2]  # POST message
        request_file_byte = len(data)  # POST file byte length

        f = open(request_file, 'w', encoding='UTF-8')  # create file for POST
        # write file using POST message
        f.write(
            "<!DOCTYPE html>\n<html>\n<head>\n<meta charset=\"utf-8\">\n<title>POST page</title>\n</head>\n<body>\n<p>{}</p>\n</body>\n</html>".format(data))
        f.close()  # file close

        connectionSocket.send("HTTP/1.0 201 OK {}\r\nHost: 127.0.0.1\r\nContent-Type: {}\r\nContent-Length: {}Bytes\r\n".format(
            request_file, request_file_type, request_file_byte).encode())  # send data

        # check POST file
        if exists(request_file):
            with open(request_file, 'r', encoding="UTF-8") as f:  # read file for POST
                capitalizedSentence = ''
                for line in f:
                    capitalizedSentence += line
        connectionSocket.send(capitalizedSentence.encode())  # send file data
        connectionSocket.close()  # socket close
