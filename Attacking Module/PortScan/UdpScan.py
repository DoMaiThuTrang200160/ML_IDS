from scapy.all import IP, UDP, send
import time
from datetime import datetime

target_ip = "192.168.1.78"
start_port = 1
end_port = 50000
delay = 0.002
log_file = "attack_log.txt"

print("Starting UDP port scan... Ctrl+C to stop")

start_time = datetime.now()
sent_packets = 0

# Log START
with open(log_file, "a") as f:
    f.write(f"UDP_SCAN,START,{start_time},{target_ip},{start_port}-{end_port},{delay}\n")

try:
    for port in range(start_port, end_port):
        ip = IP(dst=target_ip)
        udp = UDP(dport=port)

        send(ip/udp, verbose=False)
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

    # Log END
    with open(log_file, "a") as f:
        f.write(f"UDP_SCAN,END,{end_time},{duration:.2f},{sent_packets},{rate:.2f}\n")