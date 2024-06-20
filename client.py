import socket
import pickle

class ProcessData:
    message = ""

# Get the server's IP address from the user
HOST = input("Enter the server's IP address: ")
PORT = 50007

# Create a socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Authenticate with server
username = input("Enter username: ")
password = input("Enter password: ")
s.send(f"{username}:{password}".encode())

# Receive authentication result from the server
auth_result = s.recv(1024).decode()
if auth_result == "ERROR":
    print("Authentication failed. Please check your username and password.")
    s.close()
    exit()

# Accept input message and file type from the user
message_to_server = input("Enter message for server: ")
file_type = input("Enter file type to request (image/video/text): ")

# Create an instance of ProcessData() to send to the server
variable = ProcessData()
# Set the message attribute from user input
variable.message = message_to_server
# Pickle the object and send it to the server
data_string = pickle.dumps(variable)
s.send(data_string)

# Send file type request to the server
s.send(file_type.encode())

# Receive and save the file from the server
received_data = b""
while True:
    data = s.recv(1024)
    if not data:
        break
    received_data += data

# Determine the file extension based on the file type requested
if file_type == "image":
    file_extension = "jpg"
elif file_type == "video":
    file_extension = "mp4"
else:
    file_extension = "txt"

# Save the received file with the correct file extension
file_name = f"received_{file_type}.{file_extension}"
with open(file_name, "wb") as file:
    file.write(received_data)
    print(f'{file_type.capitalize()} file received from server and saved as {file_name}')

s.close()