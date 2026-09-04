from pathlib import Path

BASE_DIR = Path(__file__).parent / "files"
BASE_DIR.mkdir(exist_ok=True)


def generate_file(filename, size_bytes):
    path = BASE_DIR / filename

    chunk = b"A" * 1024 * 1024  # 1 MB
    remaining = size_bytes

    with open(path, "wb") as f:
        while remaining > 0:
            write_size = min(remaining, len(chunk))
            f.write(chunk[:write_size])
            remaining -= write_size

    print(f"Created {filename}: {size_bytes} bytes")


files = {
    "1kb.txt": 1 * 1024,
    "10kb.txt": 10 * 1024,
    "1mb.txt": 1 * 1024 * 1024,
    "10mb.txt": 10 * 1024 * 1024,
    "100mb.txt": 100 * 1024 * 1024,
}

for filename, size in files.items():
    generate_file(filename, size)