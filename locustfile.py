"""Locust workload for the file-serving API.

Set FILE_SIZE to one of: 1kb, 10kb, 1mb, 10mb, 100mb.
Set WAIT_TIME_SECONDS to tune the delay between completed requests (default: 0).
"""

import os

from locust import HttpUser, between, task


FILE_SIZE = os.getenv("FILE_SIZE", "1mb")
WAIT_TIME_SECONDS = float(os.getenv("WAIT_TIME_SECONDS", "0"))
VALID_SIZES = {"1kb", "10kb", "1mb", "10mb", "100mb"}

if FILE_SIZE not in VALID_SIZES:
    raise ValueError(f"FILE_SIZE must be one of {sorted(VALID_SIZES)}, got {FILE_SIZE!r}")


class FileServingUser(HttpUser):
    """A user repeatedly downloads the selected file and records HTTP failures."""

    wait_time = between(WAIT_TIME_SECONDS, WAIT_TIME_SECONDS)

    @task
    def download_file(self):
        # `name` keeps the Locust report stable even when the base URL changes.
        with self.client.get(f"/files/{FILE_SIZE}", name=f"GET /files/{FILE_SIZE}", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")
            elif not response.content:
                response.failure("Empty response body")
