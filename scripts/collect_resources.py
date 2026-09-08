"""Sample aggregate CPU and memory use of processes listening on selected ports."""

import argparse
import csv
import time
from pathlib import Path

import psutil


def listener_pids(ports: set[int]) -> set[int]:
    pids = set()
    for connection in psutil.net_connections(kind="inet"):
        if connection.status == psutil.CONN_LISTEN and connection.laddr and connection.laddr.port in ports and connection.pid:
            pids.add(connection.pid)
    return pids


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ports", required=True, help="Comma-separated listening ports, e.g. 8001,8002,8080")
    parser.add_argument("--duration", type=float, required=True, help="Sampling duration in seconds")
    parser.add_argument("--interval", type=float, default=2, help="Seconds between samples")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    ports = {int(port.strip()) for port in args.ports.split(",")}

    args.output.parent.mkdir(parents=True, exist_ok=True)
    processes = {}
    started = time.monotonic()
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["elapsed_s", "pids", "cpu_percent", "rss_bytes"])
        writer.writeheader()
        while time.monotonic() - started < args.duration:
            for pid in listener_pids(ports):
                try:
                    processes[pid] = psutil.Process(pid)
                except psutil.Error:
                    pass
            cpu = 0.0
            rss = 0
            active = []
            for pid, process in list(processes.items()):
                try:
                    cpu += process.cpu_percent(interval=None)
                    rss += process.memory_info().rss
                    active.append(str(pid))
                except psutil.Error:
                    processes.pop(pid, None)
            writer.writerow({"elapsed_s": round(time.monotonic() - started, 2), "pids": ";".join(active), "cpu_percent": round(cpu, 2), "rss_bytes": rss})
            handle.flush()
            time.sleep(args.interval)


if __name__ == "__main__":
    main()
