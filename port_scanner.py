#!/usr/bin/env python3
"""
Port Scanner
A multithreaded TCP port scanner that checks ports and attempts to grab service banners.
"""

import argparse
import socket
import sys
import threading
from datetime import datetime
from queue import Queue

class PortScanner:
    def __init__(self, host, threads=50, timeout=2):
        self.host = host
        self.timeout = timeout
        self.threads = threads
        self.queue = Queue()
        self.open_ports = []
        self.lock = threading.Lock()

    def scan_port(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self.host, port))

            if result == 0:
                banner = self.grab_banner(port)
                with self.lock:
                    self.open_ports.append((port, banner))
        except socket.error:
            pass

    def grab_banner(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                sock.connect((self.host, port))
                try:
                    sock.sendall(b"\r\n")
                except OSError:
                    pass
                banner = sock.recv(1024).decode(errors="ignore").strip()
            return banner if banner else "Service not identified"
        except OSError:
            return "Service not identified"

    def worker(self):
        while True:
            port = self.queue.get()
            if port is None:
                break
            self.scan_port(port)
            self.queue.task_done()

    def scan_range(self, start_port, end_port):
        print(f"Starting scan on {self.host} from port {start_port} to {end_port}")
        print(f"Threads: {self.threads}, Timeout: {self.timeout}s")
        print("-" * 60)

        start_time = datetime.now()

        thread_list = []
        for i in range(self.threads):
            t = threading.Thread(target=self.worker)
            t.start()
            thread_list.append(t)

        for port in range(start_port, end_port + 1):
            self.queue.put(port)

        self.queue.join()

        for i in range(self.threads):
            self.queue.put(None)
        for t in thread_list:
            t.join()

        end_time = datetime.now()
        duration = end_time - start_time

        self.print_results(duration)

    def print_results(self, duration):
        print("-" * 60)
        if self.open_ports:
            self.open_ports.sort(key=lambda x: x[0])
            print(f"Open ports found: {len(self.open_ports)}")
            for port, banner in self.open_ports:
                print(f"Port {port}: {banner}")
        else:
            print("No open ports found")
        print("-" * 60)
        print(f"Scan completed in {duration.total_seconds():.2f} seconds")

def main():
    parser = argparse.ArgumentParser(
        description='Port Scanner - Multithreaded TCP port scanner with banner grabbing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python port_scanner.py example.com
  python port_scanner.py example.com --port-range 1 1000
  python port_scanner.py example.com --port-range 80 443 --threads 100
  python port_scanner.py example.com --common-ports
        """
    )
    parser.add_argument('host', help='Host to scan')
    parser.add_argument('--port-range', nargs=2, type=int, default=[1, 1000],
                        metavar=('START', 'END'), help='Port range to scan (default: 1-1000)')
    parser.add_argument('--threads', type=int, default=50, help='Number of threads (default: 50)')
    parser.add_argument('--timeout', type=float, default=2, help='Socket timeout in seconds (default: 2)')
    parser.add_argument('--common-ports', action='store_true',
                        help='Scan only common ports (21, 22, 80, 443, 3306, 5432, 8080)')

    args = parser.parse_args()

    if args.timeout <= 0:
        print("Timeout must be greater than 0")
        sys.exit(1)

    if args.threads < 1:
        print("Threads must be at least 1")
        sys.exit(1)

    try:
        resolved_host = socket.gethostbyname(args.host)
    except socket.gaierror:
        print(f"Failed to resolve host: {args.host}")
        sys.exit(1)

    print(f"Resolved {args.host} -> {resolved_host}")

    if args.common_ports:
        common_ports = [21, 22, 80, 443, 3306, 5432, 8000, 8080, 9000]
        scanner = PortScanner(resolved_host, args.threads, args.timeout)
        for port in common_ports:
            scanner.queue.put(port)

        print(f"Starting scan on {args.host} ({resolved_host}) for common ports")
        print(f"Threads: {args.threads}, Timeout: {args.timeout}s")
        print("-" * 60)

        start_time = datetime.now()
        threads = []
        for _ in range(args.threads):
            t = threading.Thread(target=scanner.worker)
            t.start()
            threads.append(t)

        scanner.queue.join()

        for _ in range(args.threads):
            scanner.queue.put(None)
        for thread in threads:
            thread.join()

        duration = datetime.now() - start_time
        scanner.print_results(duration)
    else:
        start_port, end_port = args.port_range
        if start_port > end_port:
            print("Start port must be less than or equal to end port")
            sys.exit(1)
        if start_port < 1 or end_port > 65535:
            print("Port range must be between 1 and 65535")
            sys.exit(1)

        scanner = PortScanner(resolved_host, args.threads, args.timeout)
        try:
            scanner.scan_range(start_port, end_port)
        except KeyboardInterrupt:
            print("\nScan interrupted by user")
            sys.exit(130)

if __name__ == '__main__':
    main()