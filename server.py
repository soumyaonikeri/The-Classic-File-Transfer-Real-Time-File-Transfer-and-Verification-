import socket
import os

BUFFER_SIZE = 1024  # 1KB per chunk
SERVER_ADDRESS = ('127.0.0.1', 12345)

def handle_client(client_socket):
    """Handle a client connection, receive a file, split into chunks, and send back."""
    try:
        # Receive file metadata (filename and size)
        metadata = client_socket.recv(1024).decode()
        if not metadata:
            print("Error: No metadata received.")
            return

        filename, file_size = metadata.split('|')
        file_size = int(file_size)
        print(f"Received file metadata: {filename}, Size: {file_size} bytes")

        # Receive the entire file
        received_data = b""
        while len(received_data) < file_size:
            chunk = client_socket.recv(BUFFER_SIZE)
            if not chunk:
                break
            received_data += chunk

        # Save received file
        with open(filename, 'wb') as f:
            f.write(received_data)

        print(f"Received file {filename} successfully. Now splitting into chunks.")

        # Split file into chunks and send back with sequence numbers
        with open(filename, 'rb') as f:
            seq_num = 0
            while chunk := f.read(BUFFER_SIZE):
                # Properly format each chunk: "seq_num|data"
                data_to_send = f"{seq_num}|".encode() + chunk
                client_socket.sendall(data_to_send)

                # Wait for acknowledgment from the client before sending the next chunk
                ack = client_socket.recv(10).decode()
                if ack != f"ACK{seq_num}":
                    print(f"Error: ACK{seq_num} not received. Retrying...")
                    client_socket.sendall(data_to_send)

                print(f"Sent chunk {seq_num} back to client.")
                seq_num += 1

        # Indicate end of transmission
        client_socket.sendall(b'END')  # Send the 'END' marker separately
        print("File transfer complete. Sent all chunks back to client.")

    except Exception as e:
        print(f"Error handling client: {e}")

    finally:
        client_socket.close()

def start_server():
    """Start the server, listen for connections, and handle clients."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(5)
    print(f"Server is listening on {SERVER_ADDRESS}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()
