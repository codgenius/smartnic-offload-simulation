import socket

BACKEND_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", BACKEND_PORT))

print(f"Backend server listening on UDP port {BACKEND_PORT}...")

while True:
    data, addr = sock.recvfrom(1024)
    msg = data.decode(errors="replace")
    print(f"[BACKEND] msg='{msg.strip()}' from {addr}")
