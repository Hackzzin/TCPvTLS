# TCPvTLS
A repository made for a university project that implements a client-server connection in both TCP and TLS, allowing comparison between them.

---

## How to generate certificates and keys
You must have [OpenSSL](https://slproweb.com/products/Win32OpenSSL.html) installed to run the scripts.  
This project was developed with **Windows PowerShell** in mind.

After installing OpenSSL, from the root directory, run:

```powershell
.\gen_certificates.ps1
````

This will generate the required TLS certificates and keys for the server.

---

## How to run the server and client

Before running any scripts, make sure you are in the **root directory** of the project (`TCPvTLS`).

### Run the server

You can run one instance of each type of server:

* **Plain TCP server (without TLS):**

```bash
python .\servidor\server_plain.py
```

* **TLS server:**

```bash
python .\servidor\server_tls.py
```

All server configurations are in:

```
TCPvTLS\servidor\config.py
```

### Run the client

To send messages to the server, run:

```bash
python .\cliente\main.py
```

All client configurations are in:

```
TCPvTLS\cliente\config.py
```

---

## PyShark Setup and Network Capture

To analyze packets and measure overhead:

### 1. Install Wireshark

Download and install [Wireshark](https://www.wireshark.org/download.html) for your operating system.
Make sure the **TShark command-line tool** is installed (usually included with Wireshark).

### 2. Install Python dependencies

```bash
pip install pyshark
pip install python-dotenv
```

### 3. Create a `.env` file

In the root directory of the project, create a file named `.env` containing the paths to your local OpenSSL and TShark installations:

```dotenv
OPENSSL_PATH=C:\path\to\openssl.exe
TSHARK_PATH=C:\path\to\Wireshark\tshark.exe
```

* `OPENSSL_PATH`: the full path to the OpenSSL executable on your system.
* `TSHARK_PATH`: the full path to TShark.

### 4. Run the PyShark capture script

```bash
python .\pyshark\pyshark_analysis.py
```

This script will:

* Capture packets for both TCP and TLS connections.
* Calculate the number of packets, total size, average size, and latency.
* Allow comparison between plain TCP and TLS overhead.

---

