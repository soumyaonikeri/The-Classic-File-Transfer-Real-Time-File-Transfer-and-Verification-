# TCP File Transfer with Checksum and Sequence Numbers

This program implements a reliable TCP file transfer mechanism that ensures no data loss or corruption during the transfer process. The client sends a file to the server using TCP sockets, with sequence numbers for chunk ordering and SHA-256 checksum verification for data integrity. If any issues occur during the transfer, an error message is displayed, and the file is not processed.

## 🚀 Features:
- **Fully Reliable**: No packet loss or corruption.
- **TCP Sockets**: Ensures error-free transmission.
- **Sequence Numbers**: Ensures chunks are received in the correct order.
- **Checksum Verification**: Uses SHA-256 to verify the integrity of the transferred file.
- **Error Detection**: Displays an error message if missing or corrupted data is detected.

## 📋 Requirements:
- Python 3.x
- `tqdm` for progress bar (can be installed via `pip install tqdm`)

## 📂 File Structure:
- `client.py`: The client-side script that sends the file.
- `server.py`: The server-side script that receives the file.

## 🛠 How to Run:

### Step 1: Start the Server
Open a terminal window and run the following command to start the server:
### step 2:start the client
```bash
python server.py

python client.py
