import threading
import socket
import ssl
import pickle

class ProcessData:
    process_id = 0
    project_id = 0
    task_id = 0
    start_time = 0
    end_time = 0
    user_id = 0
    weekend_id = 0
    message = ""

# SSL Context
# context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
# context.load_cert_chain(certfile="server.csr", keyfile="server.key")

HOST = '0.0.0.0'  # Bind to all available network interfaces
PORT = 50008

filename = r"C:\Users\varsh\Desktop\SEM-4\Computer Networks\video.mp4"


def handle_client(conn, addr):
    try:
        print('Connected by', addr)
        
        # Receive data from client
        data = conn.recv(4096)
        data_variable = pickle.loads(data)
        print("Message from client:", data_variable.message)
        print("Data received from client:", data_variable)

        # Send image file to client
        with open(filename, "rb") as file:
            while True:
                chunk = file.read(3 * 1024 * 1024)  # Read 3MB at a time
                if not chunk:
                    break
                conn.sendall(chunk)
            print("Video sent to client")
    finally:
        conn.close()

# Accept the number of clients dynamically from the user
num_clients = int(input("Enter the number of clients: "))

# Create a socket connection.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

threads = []

try:
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        threads.append(thread)
        
        # Remove finished threads
        threads = [t for t in threads if t.is_alive()]
finally:
    for thread in threads:
        thread.join()
    s.close()
