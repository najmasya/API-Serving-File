"""Create comparison charts and an all-runs table from results/*/summary.csv."""
from pathlib import Path
import argparse
import matplotlib.pyplot as plt
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=Path("results"))
    args = parser.parse_args()
    summaries = list(args.results.glob("*/summary.csv"))
    if not summaries:
        raise SystemExit("No summary.csv found. Run scripts/run_test.ps1 first.")
    output = args.results / "evaluation"
    output.mkdir(parents=True, exist_ok=True)
    data = pd.concat([pd.read_csv(file) for file in summaries], ignore_index=True)
    data.to_csv(output / "all_results.csv", index=False)
    for metric, label in [("throughput_rps", "Throughput (requests/s)"), ("latency_p95_ms", "P95 latency (ms)"), ("error_rate_percent", "Error rate (%)")]:
        figure, axis = plt.subplots(figsize=(11, 6))
        pivot = data.pivot_table(index=["file_size", "users"], columns="mode", values=metric, aggfunc="mean")
        pivot.plot(kind="bar", ax=axis)
        axis.set_ylabel(label)
        axis.set_xlabel("File size / concurrent users")
        axis.set_title(f"File-serving API: {label}")
        axis.tick_params(axis="x", rotation=35)
        figure.tight_layout()
        figure.savefig(output / f"{metric}.png", dpi=160)
        plt.close(figure)

if __name__ == "__main__":
    main()