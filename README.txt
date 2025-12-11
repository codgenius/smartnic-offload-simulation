🧠 SmartNIC Offload Simulation (Two-VM Network Pipeline)

A virtual SmartNIC / DPU simulation built using Python, Linux networking, and multiple virtual machines.
This project demonstrates how SmartNICs classify, filter, and forward packets, similar to hardware behavior in:

NVIDIA BlueField

Intel IPU

AWS Nitro

Pensando SmartNICs

It is designed as a learning project, portfolio piece, and interview-ready demo.

🚀 Features

SmartNIC-style packet pipeline (RX → Classify → Drop/Forward → TX)

Content-based packet filtering (simple firewall behavior)

Forwarding of accepted packets to a backend service

Real cross-machine packet flow using UDP

Clean separation of RX and TX sockets (like NIC queues)

Packet statistics (total, accepted, dropped)

Multi-VM networking using VirtualBox bridged adapters

🖥️ Architecture
                  +------------------------+
                  |        Host VM         |
                  |   Sends UDP Traffic    |
                  |    nc -u <IP> 12345    |
                  +-----------+------------+
                              |
                              | UDP 12345
                              v
         +----------------------------------------------+
         |                SmartNIC VM                   |
         |                                              |
         | +----------------+     +------------------+  |
         | |  RX Socket     | --> | Classification   |  |
         | | UDP:12345      |     | Rule Engine      |  |
         | +----------------+     +------------------+  |
         |         | ACCEPT                     | DROP |
         |         v                             v     |
         |   +-----------------+        +------------------+
         |   | TX Socket       |        |  Drop Counter    |
         |   | UDP → 9999      |        +------------------+
         |   +--------+--------+
         |            |
         +------------+------------------------------+
                      |
                      | UDP 9999
                      v
         +-------------------------------+
         |         Backend Server        |
         |         Receives Accepted     |
         |         Packets Only          |
         +-------------------------------+

📁 Project Structure
/listener
│
├── udp_listener.py        # SmartNIC classifier + forwarder
├── backend_server.py      # Backend application
└── README.md              # Documentation (this file)

⚙️ Setup Instructions
1️⃣ Requirements

Two Linux VMs (Ubuntu recommended)

VirtualBox with Bridged Adapter networking enabled

Python 3 installed

Netcat installed on Host VM:

sudo apt install netcat

2️⃣ Clone the Repository

On both VMs:

git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>/listener

3️⃣ Start the Backend Server (SmartNIC VM)
python3 backend_server.py


Expected output:

Backend server listening on UDP port 9999...

4️⃣ Start the SmartNIC Listener (SmartNIC VM)

Open a second terminal:

python3 udp_listener.py


Expected output:

SmartNIC listener on UDP port 12345...

5️⃣ Send Traffic from Host VM

Allowed traffic:

echo "Normal request" | nc -u <SMARTNIC-IP> 12345


Blocked traffic:

echo "This should be BLOCK" | nc -u <SMARTNIC-IP> 12345

6️⃣ Expected SmartNIC Output
[ACCEPT] from (...) msg='Normal request' -> forwarding to backend
Stats: total=1, dropped=0

[DROP] from (...) msg='This should be BLOCK'
Stats: total=2, dropped=1

7️⃣ Expected Backend Output
[BACKEND] msg='Normal request' from (...)


Blocked messages never reach the backend.

 Source Code
SmartNIC Listener (RX → Classify → TX)
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

Backend Server
import socket

BACKEND_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", BACKEND_PORT))

print(f"Backend server listening on UDP port {BACKEND_PORT}...")

while True:
    data, addr = sock.recvfrom(1024)
    msg = data.decode(errors="replace")
    print(f"[BACKEND] msg='{msg.strip()}' from {addr}")

 How This Relates to Real SmartNICs
This Project	Real SmartNIC Component
rx_sock.bind()	Hardware RX queue
Keyword-based filtering	TCAM rule tables (match/action)
Forwarding to backend	On-NIC processing engines
Python logic	Prototype of DPDK/XDP/P4 pipelines
Two VMs setup	Host ↔ SmartNIC architecture


 Future Improvements

Stateful firewall with per-flow tracking

TCAM-style wildcard rules

Latency measurements & performance stats

DPDK port for near line-rate performance

eBPF/XDP version that runs in the kernel

P4 programmable data plane implementation

Web Dashboard showing packet stats

 License

MIT License — free to use and modify.