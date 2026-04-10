# Port Scanner

A multithreaded TCP port scanner built from scratch in Python. Designed to understand how tools like Nmap work under the hood.

## Features

- Multithreaded scanning for speed
- Custom port ranges
- Service banner grabbing
- Configurable timeout and thread count
- Scan common ports option

## Installation

Clone the repository and ensure Python 3.x is installed.

## Usage

```bash
python port_scanner.py <host> [options]
```

### Examples

```bash
# Scan ports 1-1000 on example.com
python port_scanner.py example.com

# Scan specific range
python port_scanner.py example.com --port-range 80 443

# Scan common ports only
python port_scanner.py example.com --common-ports

# Increase threads for faster scanning
python port_scanner.py example.com --threads 100
```

## Options

- `--port-range START END`: Port range to scan (default: 1-1000)
- `--threads N`: Number of threads (default: 50)
- `--timeout T`: Socket timeout in seconds (default: 2)
- `--common-ports`: Scan only common ports (21, 22, 80, 443, 3306, 5432, 8080, 8000, 9000)

## License

MIT