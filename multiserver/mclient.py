import socket

if __name__ == "__main__":

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect(("localhost", 9000))

    data = input("enter some data: ")

    sock.send(data.encode())

    result = sock.recv(1024).decode()

    print(result)

    sock.close()