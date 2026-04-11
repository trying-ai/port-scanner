# Port Scanner (Python)

Multithreaded TCP port scanner with optional banner grabbing.

## Features

- Hostname resolution with clear startup output
- Configurable thread count and socket timeout
- Port range scanning (`1-65535`) and common-port mode
- Basic service banner attempt on open ports

## Requirements

- Python 3.8+
- No external Python dependencies

## Usage

```bash
python port_scanner.py <host>
```

Examples:

```bash
python port_scanner.py example.com
python port_scanner.py example.com --port-range 1 2000
python port_scanner.py example.com --threads 100 --timeout 1.5
python port_scanner.py example.com --common-ports
```

## CLI Options

- `host` target host or IP
- `--port-range START END` port range (default: `1 1000`)
- `--threads` worker threads (default: `50`)
- `--timeout` socket timeout in seconds (default: `2`)
- `--common-ports` scan a small predefined common list

## Notes

- Use only with explicit authorization.
- Lower timeout = faster scans but may miss slow services.
- Very high thread counts can overload your machine or network.

## License

MIT (see `LICENSE`).