import socket
import time
from datetime import datetime

target_ip = "192.168.1.78"
start_port = 1
end_port = 5000
delay = 0.01

print(f"Starting TCP connect scan on {target_ip}\n")

start_time = datetime.now()
open_ports = []
scanned_ports = 0

try:
    for port in range(start_port, end_port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)

        try:
            result = s.connect_ex((target_ip, port))
            scanned_ports += 1

            if result == 0:
                print(f"[OPEN]     Port {port}")
                open_ports.append(port)
            else:
                print(f"[CLOSED]   Port {port}")

        except socket.timeout:
            print(f"[FILTERED] Port {port} (timeout)")

        except Exception as e:
            print(f"[ERROR]    Port {port} -> {e}")

        finally:
            s.close()

        time.sleep(delay)

except KeyboardInterrupt:
    print("\nScan interrupted by user.")

finally:
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print("\nScan completed.")
    print(f"Total ports scanned: {scanned_ports}")
    print(f"Open ports found: {len(open_ports)}")
    print(f"Duration: {duration:.2f} seconds")
