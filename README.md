SmartNIC Offload Simulation (Two-VM Network Pipeline)

A virtual SmartNIC / DPU simulation built using Python, Linux networking, and multiple virtual machines.
The SmartNIC VM receives packets, classifies them, drops unwanted packets, and forwards accepted packets to a backend service.

This project demonstrates core SmartNIC concepts used in:

NVIDIA BlueField

Intel IPU

AWS Nitro

Pensando SmartNICs

Features

SmartNIC-style packet pipeline (RX → Classify → Drop/Forward → TX)

Content-based filtering (simple match–action)

Forwarding accepted packets to a backend server

Real UDP packet flow between two VMs

Separation of RX and TX sockets

Packet stats (accepted, dropped, total)

Architecture
Host VM
    |
    | UDP 12345
    v
SmartNIC VM
+------------------------+
| RX Socket (UDP:12345)  |
| Classification Engine  |
| Drop / Accept          |
| TX Socket → 127.0.0.1  |
| UDP 9999               |
+------------------------+
    |
    v
Backend Server

Project Structure
listener/
├── udp_listener.py       # SmartNIC classifier + forwarder
├── backend_server.py     # Backend application
└── README.md             # Documentation

Setup Instructions
1. Requirements

Two Ubuntu Linux VMs

VirtualBox with Bridged Networking

Python 3 installed

Netcat installed on Host VM

Install netcat:

sudo apt install netcat

2. Run Backend (SmartNIC VM)
python3 backend_server.py

3. Run SmartNIC Listener (SmartNIC VM)
python3 udp_listener.py

4. Send Packets (Host VM)

Allowed:

echo "Normal request" | nc -u <SMARTNIC-IP> 12345


Blocked:

echo "This should be BLOCK" | nc -u <SMARTNIC-IP> 12345

Expected Output (SmartNIC)
[ACCEPT] msg='Normal request' -> forwarding to backend
[DROP] msg='This should be BLOCK'

Expected Output (Backend)
[BACKEND] msg='Normal request'

How It Relates to Real SmartNICs

RX/TX sockets simulate NIC hardware queues

Content matching simulates TCAM rule lookup

Forwarding simulates on-NIC offload engines

Two VMs simulate host vs. SmartNIC separation

Future Improvements

Add ACL/TCAM rule table

Add DPDK version

Add eBPF/XDP fast path

Add rule compiler

Add latency measurement