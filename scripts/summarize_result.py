"""Merge Locust CSV output and resource samples into one reproducible summary row."""

import argparse
import csv
import json
from pathlib import Path

import pandas as pd


def value(row, *names, default=0):
    for name in names:
        if name in row and pd.notna(row[name]):
            return row[name]
    return default


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stats", type=Path, required=True)
    parser.add_argument("--resources", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    stats = pd.read_csv(args.stats)
    aggregate = stats.loc[stats["Name"] == "Aggregated"].iloc[0]
    resources = pd.read_csv(args.resources)
    metadata = json.loads(args.metadata.read_text(encoding="utf-8-sig"))
    requests = float(value(aggregate, "Request Count"))
    failures = float(value(aggregate, "Failure Count"))
    result = {
        **metadata,
        "total_requests": int(requests), "failed_requests": int(failures),
        "error_rate_percent": round((failures / requests * 100) if requests else 0, 4),
        "throughput_rps": round(float(value(aggregate, "Requests/s")), 4),
        "latency_p50_ms": float(value(aggregate, "50%", "Median Response Time")),
        "latency_p90_ms": float(value(aggregate, "90%")),
        "latency_p95_ms": float(value(aggregate, "95%")),
        "latency_p99_ms": float(value(aggregate, "99%")),
        "latency_max_ms": float(value(aggregate, "Max Response Time")),
        "avg_cpu_percent": round(float(resources["cpu_percent"].mean()), 3) if not resources.empty else 0,
        "max_cpu_percent": round(float(resources["cpu_percent"].max()), 3) if not resources.empty else 0,
        "avg_ram_mb": round(float(resources["rss_bytes"].mean()) / 1024**2, 3) if not resources.empty else 0,
        "max_ram_mb": round(float(resources["rss_bytes"].max()) / 1024**2, 3) if not resources.empty else 0,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=result.keys())
        writer.writeheader()
        writer.writerow(result)


if __name__ == "__main__":
    main()
