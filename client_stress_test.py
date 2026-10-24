import socket
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from protocol import send_message, recv_message

HOST = '127.0.0.1'
PORT = 9090
NUM_WORKERS = 20


def worker_task(worker_id):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))

        # Test 1: KV Store PUT
        send_message(sock, {"action": "PUT", "key": f"key_{worker_id}", "value": worker_id})
        recv_message(sock)

        # Test 2: KV Store GET
        send_message(sock, {"action": "GET", "key": f"key_{worker_id}"})
        val = recv_message(sock)
        assert val["value"] == worker_id

        # Test 3: Task Queue ENQUEUE
        send_message(sock, {"action": "ENQUEUE", "task": f"task_{worker_id}"})
        recv_message(sock)

        sock.close()
        print(f"[Worker Thread {worker_id:02d}] Transaction verified successfully.")
    except Exception as e:
        print(f"[Worker Thread {worker_id:02d}] FAILED: {e}")


if __name__ == "__main__":
    print(f"[*] Launching {NUM_WORKERS} concurrent client worker threads...")
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        for i in range(NUM_WORKERS):
            executor.submit(worker_task, i)

    elapsed = time.time() - start_time
    print(f"[+] All {NUM_WORKERS} workers completed execution in {elapsed:.3f} seconds.")