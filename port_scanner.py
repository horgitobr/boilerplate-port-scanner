import socket
import re
from common_ports import ports_and_services


def is_ip_format(target):
    pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    return re.match(pattern, target) is not None


def is_valid_ip(target):
    parts = target.split('.')
    return all(0 <= int(part) <= 255 for part in parts)


def get_open_ports(target, port_range, verbose=False):
    hostname = None
    ip = None

    if is_ip_format(target):
        if not is_valid_ip(target):
            return "Error: Invalid IP address"
        ip = target
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            hostname = None
    else:
        try:
            ip = socket.gethostbyname(target)
            hostname = target
        except socket.gaierror:
            return "Error: Invalid hostname"

    open_ports = []
    for port in range(port_range[0], port_range[1] + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
        finally:
            sock.close()

    if not verbose:
        return open_ports

    if hostname:
        output = f"Open ports for {hostname} ({ip})\n"
    else:
        output = f"Open ports for {ip}\n"

    output += f"{'PORT':<9}{'SERVICE'}\n"
    for port in open_ports:
        service = ports_and_services.get(port, "unknown")
        output += f"{port:<9}{service}\n"

    return output.rstrip("\n")