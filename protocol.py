import socket
import struct
import json


def recv_exact(sock, num_bytes):
    """Reads exactly num_bytes from the socket. Prevents stream fragmentation issues."""
    data = bytearray()
    while len(data) < num_bytes:
        packet = sock.recv(num_bytes - len(data))
        if not packet:
            return None  # Connection closed by client
        data.extend(packet)
    return bytes(data)


def recv_message(sock):
    """Unmarshals a length-prefixed JSON message from the socket."""
    # 1. Read the 4-byte header
    header = recv_exact(sock, 4)
    if not header:
        return None

    # 2. Unpack the Network Byte Order (Big-Endian) unsigned int
    payload_length = struct.unpack('!I', header)[0]

    # 3. Read the exact payload length
    payload_bytes = recv_exact(sock, payload_length)
    if not payload_bytes:
        return None

    # 4. Decode and deserialize
    return json.loads(payload_bytes.decode('utf-8'))


def send_message(sock, message_dict):
    """Marshals a dictionary into a length-prefixed JSON message and sends it."""
    payload_bytes = json.dumps(message_dict).encode('utf-8')
    payload_length = len(payload_bytes)

    # Pack the length into a 4-byte Big-Endian unsigned int (!I)
    header = struct.pack('!I', payload_length)

    # Send header and payload
    sock.sendall(header + payload_bytes)