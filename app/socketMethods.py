import socket
import threading

#### SOCKET
def handle_client(connection, address, stop_event):
    print(f"Connected to {address}")
    while not stop_event.is_set():
        data = connection.recv(1024)
        if not data:
            break
        connection.sendall(data)
        character = data.decode()  # Decodifica il singolo byte in un carattere
        print(f"Received: {character}.")
        if character == "c": 
            connection.sendall("Closing connection".encode())
            connection.close()
            print("Connection closed")
            break
        else:
            # Invia indietro il carattere ricevuto
            connection.sendall(data)
    connection.close()


def start_server(stop_event: threading.Event):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 7384))
    server.listen()
    print("Socket Server listening on localhost:7384")
    
    while not stop_event.is_set():
        # Accetta connessioni se disponibili, altrimenti controlla lo stop_event
        server.settimeout(1)  # Imposta un timeout per permettere controlli frequenti dello stop_event
        try:
            conn, addr = server.accept()
        except socket.timeout:
            continue  # Nessuna connessione, riprova

        thread = threading.Thread(target=handle_client, args=(conn, addr, stop_event))
        thread.start()

    server.close()
    print("Server shutdown")

stop_event = threading.Event()