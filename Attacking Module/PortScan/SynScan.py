from scapy.all import IP, TCP, send
import time
from datetime import datetime

target_ip = "192.168.1.78"
start_port = 1
end_port = 5000
delay = 0.01
log_file = "attack_log.txt"

print("Starting SYN port scan... Ctrl+C to stop")

start_time = datetime.now()
sent_packets = 0


try:
    for port in range(start_port, end_port):
        ip = IP(dst=target_ip)
        tcp = TCP(dport=port, flags="S")

        send(ip/tcp, verbose=False)
        sent_packets += 1

        time.sleep(delay)

except KeyboardInterrupt:
    print("\nScan interrupted by user.")

finally:
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    rate = sent_packets / duration if duration > 0 else 0

    print("\nScan completed.")
    print(f"Total packets sent: {sent_packets}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Send rate: {rate:.2f} pps")
