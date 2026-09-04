import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse


app = FastAPI(
    title="File Serving API",
    version="1.0.0"
)

FILES_DIR = Path(__file__).parent / "files"

FILES = {
    "1kb": "1kb.txt",
    "10kb": "10kb.txt",
    "1mb": "1mb.txt",
    "10mb": "10mb.txt",
    "100mb": "100mb.txt",
}


@app.get("/")
def root():
    return {
        "message": "File Serving API",
        "instance": os.getenv("API_INSTANCE", "unknown"),
        "available_files": list(FILES.keys())
    }


@app.get("/files/{size}")
def get_file(size: str):

    if size not in FILES:
        raise HTTPException(
            status_code=404,
            detail="Ukuran file tidak tersedia"
        )

    file_path = FILES_DIR / FILES[size]

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File tidak ditemukan"
        )

    return FileResponse(
        path=file_path,
        media_type="text/plain",
        filename=FILES[size]
    )