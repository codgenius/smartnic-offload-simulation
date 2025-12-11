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

Forwarding of accepted packets to a backend

Real UDP packet flow across two VMs

Separation of RX and TX sockets

Packet statistics (total, accepted, dropped)

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
|            UDP:9999    |
+------------------------+
    |
    | UDP 9999
    v
Backend Server

Project Structure
listener/
├── udp_listener.py       # SmartNIC packet classifier + forwarder
├── backend_server.py     # Backend application to receive accepted packets
└── README.md             # Documentation

Setup Instructions
1. Requirements

Two Ubuntu Linux VMs

VirtualBox with Bridged Networking

Python 3 installed

Netcat installed on the Host VM

Install netcat:

sudo apt install netcat

2. Run Backend Server (on SmartNIC VM)
python3 backend_server.py


Expected:

Backend server listening on UDP port 9999...

3. Run SmartNIC Listener (on SmartNIC VM)
python3 udp_listener.py

4. Send Packets from Host VM

Allowed:

echo "Normal request" | nc -u <SMARTNIC-IP> 12345


Blocked:

echo "This should be BLOCK" | nc -u <SMARTNIC-IP> 12345

Expected Output (SmartNIC)
[ACCEPT] msg='Normal request' -> forwarding to backend
[DROP] msg='This should be BLOCK'

Expected Output (Backend)
[BACKEND] msg='Normal request'

How This Relates to Real SmartNICs

RX/TX sockets simulate NIC queues

Keyword matching simulates TCAM rule filtering

Forwarding simulates offload engines

Separate VMs simulate host vs SmartNIC architecture

Future Improvements

Add connection tracking

Add TCAM-style wildcard rules

Add latency measurement

Implement DPDK version

Implement eBPF/XDP version