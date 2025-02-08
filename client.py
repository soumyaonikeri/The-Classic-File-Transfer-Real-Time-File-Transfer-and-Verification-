import socket
import os
import hashlib

SERVER_ADDRESS = ('127.0.0.1', 12345)
BUFFER_SIZE = 1024  # 1KB per chunk

def calculate_checksum(file_path):
    """Calculate SHA256 checksum of the file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(BUFFER_SIZE):
            sha256.update(chunk)
    return sha256.hexdigest()

def receive_file_chunks(client_socket, output_file_path):
    """Receive file chunks from the server, acknowledge them, and reassemble them in order."""
    received_data = {}

    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE + 10)  # Extra space for sequence number

            # If empty data received, connection may have closed
            if not data:
                print("Connection closed by the server.")
                break

            # Check if this is the END message
            if data.strip() == b'END':
                print("End of transmission received.")
                break

            # Ensure data is properly formatted before processing
            if b'|' not in data:
                print(f"Warning: Unexpected data format received: {data[:50]}...")  # Only show a snippet
                continue  # Skip invalid data

            seq_num, chunk_data = data.split(b'|', 1)
            seq_num = int(seq_num.decode())

            # Store received chunks in dictionary
            received_data[seq_num] = chunk_data
            print(f"Received chunk {seq_num}")

            # Send acknowledgment (ACK)
            ack_message = f"ACK{seq_num}".encode()
            client_socket.sendall(ack_message)

        except ValueError as e:
            print(f"Error while processing chunk: {e}")
            continue

    # Reassemble the file in correct order
    with open(output_file_path, 'wb') as f:
        for seq_num in sorted(received_data.keys()):  # Ensure chunks are written in order
            f.write(received_data[seq_num])

    print("File reassembled successfully.")
    return output_file_path

def upload_file(file_path, server_address):
    """Upload a file to the server and receive it back in chunks."""
    file_size = os.path.getsize(file_path)
    checksum = calculate_checksum(file_path)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    try:
        # Send file metadata (filename and size)
        metadata = f"{os.path.basename(file_path)}|{file_size}".encode()
        client_socket.sendall(metadata)
        print(f"File metadata sent: {file_path} | Size: {file_size} bytes")

        # Send entire file
        with open(file_path, 'rb') as f:
            client_socket.sendall(f.read())

        print(f"Sent {file_size} bytes of data.")

        # Receive file chunks and reassemble them
        output_file_path = f"received_{file_path}"
        receive_file_chunks(client_socket, output_file_path)

        # Verify checksum
        received_checksum = calculate_checksum(output_file_path)
        if received_checksum == checksum:
            print(f"File transfer successful. Checksum verified for {file_path}. ✅")
        else:
            print(f"File transfer failed. Checksum mismatch for {file_path}. ❌")

    finally:
        client_socket.close()

if __name__ == "__main__":
    upload_file("friends-final14.txt", SERVER_ADDRESS)
