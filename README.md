# Hunter350

Hunter350 is an advanced network scanning tool that detects active devices on a local network, identifies their types, and scans for open ports.

## Features
- Detects the local subnet automatically
- Scans for active devices on the LAN
- Identifies device types (PC, Mobile, Camera, Router) based on MAC address
- Scans for open ports on each detected device

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/Hunter350.git
   cd Hunter350
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Run the tool:
   ```sh
   python Hunter350.py
   ```

## Requirements
- Python 3.x
- `netifaces`, `nmap`, `arp-scan`
- Root privileges for scanning

## License
This project is licensed under the MIT License.
    