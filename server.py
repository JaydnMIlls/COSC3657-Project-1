import socket
import logging
from concurrent.futures import ThreadPoolExecutor
from protocol import recv_message, send_message
from storage import ThreadSafeKVStore, ThreadSafeTaskQueue

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

HOST = '0.0.0.0'
PORT = 9090
#maximum number of concurrent threads in pool
MAX_WORKERS = 10

#instantiate thread-safe memory structures
kv_store = ThreadSafeKVStore()
task_queue = ThreadSafeTaskQueue()


def handle_client(client_sock, address):
    logging.info(f"[+] Client connected from {address}")
    try:
        # keep connection alive to process multiple sequential requests
        while True:
            #block until a full length prefix msg is received
            msg = recv_message(client_sock)
            if msg is None:
                break  # Client disconnected

            action = msg.get("action")
            response = {"status": "error", "message": "Unknown action"}

            if action == "PUT":
                kv_store.put(msg["key"], msg["value"])
                response = {"status": "ok"}

            elif action == "GET":
                val = kv_store.get(msg["key"])
                response = {"status": "ok", "value": val}

            elif action == "ENQUEUE":
                task_queue.enqueue(msg["task"])
                response = {"status": "ok"}

            elif action == "DEQUEUE":
                # This will block the specific worker thread if the queue is empty
                # until another client enqueues a task
                task = task_queue.dequeue()
                response = {"status": "ok", "task": task}

            # Serialize and send the response back to this specific client
            send_message(client_sock, response)

    except Exception as e:
        # Catch unexpected socket drops or malformed data to prevent thread crashes
        logging.error(f"[-] Error handling client {address}: {e}")
    finally:
        client_sock.close()
        logging.info(f"[-] Client disconnected from {address}")


def start_server():
    # IPv4 (AF_INET), TCP Stream (SOCK_STREAM)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow port reuse to prevent "Address already in use" errors during dev
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the network interface and port
    server_sock.bind((HOST, PORT))
    # Enable the server to accept connections, queuing up to 5 pending connections
    server_sock.listen(5)

    logging.info(f"[*] Server initialized on {HOST}:{PORT}")
    logging.info(f"[*] Thread Pool initialized with max_workers={MAX_WORKERS}...")

    # Create a bounded pool of worker threads to prevent resource exhaustion
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        try:
            while True:
                #waiting for a new client handshake
                client_sock, address = server_sock.accept()
                # Immediately hand off the active socket to a background worker thread.
                # This frees the main thread to instantly loop back and accept the next client.
                executor.submit(handle_client, client_sock, address)
        except KeyboardInterrupt:
            logging.info("\n[*] Server shutting down.")
        finally:
            server_sock.close()


if __name__ == "__main__":
    start_server()