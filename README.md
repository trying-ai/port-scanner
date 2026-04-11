# Port Scanner

A small multithreaded TCP scanner for quick host checks.

It resolves the target, scans a port range, and tries to grab a simple banner on open ports.

## Requirements

- Python 3.8+
- No external packages

## Quick start

```bash
python port_scanner.py example.com
```

## Common commands

```bash
python port_scanner.py example.com --port-range 1 2000
python port_scanner.py example.com --threads 100 --timeout 1.5
python port_scanner.py example.com --common-ports
```

## CLI options

- `host` target host or IP
- `--port-range START END` (default: `1 1000`)
- `--threads` worker count (default: `50`)
- `--timeout` socket timeout in seconds (default: `2`)
- `--common-ports` scan a short predefined list

## Example output

```text
Resolved example.com -> 93.184.216.34
Starting scan on 93.184.216.34 from port 80 to 81
Open ports found: 1
Port 80: Service not identified
```

## Common issues

- **Name resolution failed**: check DNS/network access.
- **No open ports found**: target may filter traffic, or timeout is too low.
- **Slow scan**: reduce range, lower threads, or tune timeout.

## Responsible use

Use only on systems you own or are explicitly authorized to test.

## License

MIT.