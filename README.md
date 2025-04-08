# SocketShroud

> **Ghost in the Wire**  
> Cloak, reroute, and hijack network sockets like a shadow.

SocketShroud is an advanced LAN-level socket cloak and manipulation toolkit designed for offensive security professionals and red teamers. It provides a suite of modules to:

- **Recon:** Real-time socket discovery and analysis using psutil.
- **Cloak:** Hide socket traffic from userland tools via iptables.
- **Hijack:** Inject custom payloads into live TCP sessions using Scapy.
- **Proxy:** Set up a transparent TCP proxy for man-in-the-middle attacks.
- **Decoy:** Deploy fake services (honeypots) to misdirect and bait adversaries.

---

## Features

- **Real-time recon:** Enumerate active TCP/UDP sessions with detailed process info.
- **Socket cloaking:** Automatically drop packets on targeted ports to hide connections.
- **Session hijacking:** Forge TCP packets to inject data into an existing session.
- **Transparent proxy:** Forward traffic between local and remote hosts seamlessly.
- **Decoy services:** Listen on ports and serve realistic banners to attract attackers.
- **Modular design:** Each module is self-contained for easy integration and extension.
- **DEB Package Ready:** Install via Debian package for seamless deployment on Linux.

---

## Installation

### Prerequisites

- A Debian/Ubuntu-based system (apt package manager)
- Required apt packages will be installed automatically:
  - `iptables`, `nmap`, `net-tools`, `lsof`, `python3`, `python3-venv`, etc.
- External tools from the [impacket](https://github.com/SecureAuthCorp/impacket) suite
  (for remote execution and NTLM relaying) should be installed and in your PATH.

### From Source

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/John0n1/SocketShroud.git
   cd SocketShroud
   ```

2. **Make the Launcher Executable:**

   ```bash
   chmod +x socketshroud.sh
   ```

3. **Run as Root:**

   ```bash
   sudo ./socketshroud.sh recon
   ```

   On first run, the tool sets up a local Python virtual environment (`venv/`) and installs required Python modules.

### Debian Package

1. Install the package:

   ```bash
   sudo dpkg -i socketshroud_1.0_all.deb
   ```

   The executable will be installed to `/usr/local/bin/socketshroud`.

---

## Usage Examples

- **Socket Recon:**

  List active connections:
  ```bash
  sudo socketshroud.sh recon
  ```

- **Cloak a Port:**

  Hide traffic on port 443:
  ```bash
  sudo socketshroud.sh cloak 443
  ```

- **Hijack a Session:**

  Inject data into a session (parameters: target IP, target port, spoofed source IP, source port, TCP seq, TCP ack, payload):
  ```bash
  sudo socketshroud.sh hijack 10.0.0.5 10.0.0.100 4444 1000 2000 "Injected Payload"
  ```

- **Proxy Traffic:**

  Set up a proxy that listens on port 8080 and forwards to 10.0.0.8:80:
  ```bash
  sudo socketshroud.sh proxy 8080 10.0.0.8:80
  ```

- **Deploy a Decoy Service:**

  Run a decoy honeypot on port 22:
  ```bash
  sudo socketshroud.sh decoy 22
  ```

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for any improvements or additional features.

---

## License

Released under the [MIT License](./LICENSE).

---

## Disclaimer

Use SocketShroud only on networks you are authorized to test. Unauthorized use is illegal and unethical.

---

Happy socket stalking!
