import os
import subprocess
import json
import socket
import netifaces
import csv

def get_local_subnet():
    """Automatically detects the local subnet."""
    interface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    addr_info = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]
    subnet = f"{addr_info['addr']}/24"  # Assuming /24 subnet mask
    return subnet

def identify_device(mac: str) -> str:
    """Identifies device type based on MAC address prefix."""
    prefixes = {
        "PC": ["00:1A:4B", "00:1D:60", "3C:D9:2B"],
        "Mobile": ["D0:22:BE", "28:EF:01", "5C:0A:5B"],
        "Camera": ["00:0F:7C", "00:1B:C1", "58:BF:EA"],
        "Router": ["F4:EC:38", "C8:3A:35", "18:31:BF"]
    }
    
    for device, mac_prefixes in prefixes.items():
        if any(mac.startswith(prefix) for prefix in mac_prefixes):
            return device
    return "Unknown"

def scan_local_network():
    """Uses arp-scan and nmap to detect active devices on the LAN."""
    subnet = get_local_subnet()
    print(f"Scanning local network: {subnet}")
    
    command = "sudo arp-scan --localnet --interface=$(ip route | grep default | awk '{print $5}') -g -q -x"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    devices = []
    for line in result.stdout.splitlines():
        parts = line.strip().split()
        if len(parts) >= 2:
            ip, mac = parts[0], parts[1]
            manufacturer = " ".join(parts[2:]) if len(parts) > 2 else "Unknown"
            device_type = identify_device(mac)
            open_ports = scan_ports(ip)
            devices.append({"ip": ip, "mac": mac, "manufacturer": manufacturer, "device_type": device_type, "open_ports": open_ports})
    
    print("Scan complete. Detected devices:")
    for device in devices:
        print(f"IP: {device['ip']}, MAC: {device['mac']}, Manufacturer: {device['manufacturer']}, Device Type: {device['device_type']}, Open Ports: {device['open_ports']}")

def scan_ports(ip: str) -> list:
    """Scans open ports on a given IP using nmap."""
    command = f"sudo nmap -p 1-65535 --open {ip} -oG -"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    open_ports = []
    
    for line in result.stdout.splitlines():
        if "/open/" in line:
            ports = [entry.split("/")[0] for entry in line.split() if "/open/" in entry]
            open_ports.extend(ports)
    return open_ports

def main():
    scan_local = input("Do you want to scan the local area network first? (yes/no): ").strip().lower()
    if scan_local == "yes":
        scan_local_network()

if __name__ == "__main__":
    main()
    