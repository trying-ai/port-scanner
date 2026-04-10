# Port Scanner

A multithreaded TCP port scanner built from scratch. Supports custom port ranges, timeout control, and service banner grabbing. Designed to understand how tools like Nmap work under the hood.

## Installation

1. Make sure you have Python 3 installed
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Make the file executable (Linux):
   ```
   chmod +x port_scanner.py
   ```

## Usage

Basic scan of default port range (1-1000):
```
python port_scanner.py example.com
```

Scan specific port range:
```
python port_scanner.py example.com --port-range 1 65535
```

Scan with custom thread count and timeout:
```
python port_scanner.py example.com --port-range 1 10000 --threads 100 --timeout 3
```

Scan only common ports:
```
python port_scanner.py example.com --common-ports
```

## Options

- `host`: Target host to scan
- `--port-range START END`: Port range to scan (default: 1-1000)
- `--threads N`: Number of worker threads (default: 50)
- `--timeout SECONDS`: Socket timeout in seconds (default: 2)
- `--common-ports`: Scan only common ports (21, 22, 80, 443, 3306, 5432, 8080, 8000, 9000)

## Example Output

```
Starting scan on example.com from port 1 to 100
Threads: 50, Timeout: 2s
------------------------------------------------------------
Open ports found: 2
Port 80: HTTP/1.1 200 OK
Port 443: Service not identified
------------------------------------------------------------
Scan completed in 4.32 seconds
```

## How it Works

1. Creates a thread pool based on the specified thread count
2. Distributes ports across threads using a queue
3. Each thread attempts to establish a TCP connection to each port
4. For open ports, attempts to grab the service banner
5. Results are collected and displayed with timing information

## Notes

- Requires appropriate permissions to scan hosts
- Use responsibly and only scan hosts you own or have permission to scan
- Timeout value affects scan speed (lower values = faster but may miss slow services)
- Thread count affects system resource usage (higher values = faster but more resource intensive)