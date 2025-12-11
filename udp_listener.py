import socket

LISTEN_PORT = 12345
BACKEND_IP = "127.0.0.1"
BACKEND_PORT = 9999

BLOCKED_KEYWORDS = ["BLOCK", "DROP", "BAN"]

rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rx_sock.bind(("", LISTEN_PORT))

tx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"SmartNIC listener on UDP port {LISTEN_PORT}...")

total_packets = 0
dropped_packets = 0

while True:
    data, addr = rx_sock.recvfrom(1024)
    msg = data.decode(errors="replace").strip()
    total_packets += 1

    if any(word in msg for word in BLOCKED_KEYWORDS):
        dropped_packets += 1
        print(f"[DROP] from {addr}, msg='{msg}'")
        print(f"Stats: total={total_packets}, dropped={dropped_packets}")
        continue

    print(f"[ACCEPT] from {addr}, msg='{msg}' -> forwarding to backend")
    tx_sock.sendto(data, (BACKEND_IP, BACKEND_PORT))
    print(f"Stats: total={total_packets}, dropped={dropped_packets}")
