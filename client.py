import socket


def send(name, done):
    host = "192.168.24.72"
    port = 9876
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    s.send(f"{name},{done}".encode())
    res = s.recv(1024)
    #print(f"Got response {res}")
    s.close()
    return res.decode()


if __name__ == '__main__':
    send("Kristjan", 0)
