# Classic File Transfer with Chunk Handling, Sequence Numbers and Verification

This project demonstrates a client-server file transfer system where:

-The client sends an entire file to the server.

-The server splits the file into smaller chunks, assigns each chunk a sequence number, and sends these chunks back to the client.

-The client reassembles the chunks in the correct order and verifies the integrity of the reassembled file using a checksum.

## Features:
- **Reliable file transfer** with acknowledgment (ACK) handling for each chunk(TCP sockets).
- **Checksum verification** to ensure file integrity during transfer(SHA-256).
- **Robust error handling** to manage unexpected data formats or connection issues.
- **Sequential reassembly** of file chunks to match original file order.
- **Error Detection**: Displays an error message if missing or corrupted data is detected.

## File Structure:
- `client.py`: The client-side script that sends the file.
- `server.py`: The server-side script that receives the file.

## Configuration
-`BUFFER_SIZE`: Size of each chunk sent by the server. Default is 1024 bytes (1KB).

-`SERVER_ADDRESS`: The IP and port where the server listens (127.0.0.1:12345).
## How to Run:

### Step 1: Start the Server
Open a terminal window and run the following command to start the server:
- The server listens on 127.0.0.1:12345 and waits for incoming client connections.
```bash
python server.py
```
### step 2:start the client
- The client uploads a specified file (dataset.txt), receives it back in chunks from the server, reassembles it, and checks the checksum.
- The size of the Transmitted file **dataset.txt is 15.04MB**
```bash
python client.py
