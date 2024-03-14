import socket
import threading

def handle_client(connection, address):
    print(f"Connected to {address}")
    while True:
        data = connection.recv(1024)
        if not data:
            break
        if data.decode() == "close":
            connection.close()
            print("close")
            break
        print(f"Received: {data.decode()}")
        connection.sendall(data)
    connection.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 7384))
    server.listen()
    print("Socket Server listening on localhost:7384")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()