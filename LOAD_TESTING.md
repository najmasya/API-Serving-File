# Panduan Load Testing dan Evaluasi

Deliverable ini membandingkan **tanpa load balancer** (langsung ke API-1 pada `:8001`) dengan **load balancer + 2 API** (Nginx pada `:8081`, backend API-1 `:8001` dan API-2 `:8002`). Semua run memakai durasi default **300 detik / 5 menit**.

## 1. Instalasi

Dari root proyek, buat dan aktifkan virtual environment lalu pasang dependency:

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app/generate_files.py
```

## 2. Menjalankan sistem yang diuji

Terminal 1:

```powershell
$env:API_INSTANCE="API-1"
uvicorn app.main:app --host 127.0.0.1 --port 8001
```

Terminal 2 (hanya diperlukan untuk mode LB):

```powershell
$env:API_INSTANCE="API-2"
uvicorn app.main:app --host 127.0.0.1 --port 8002
```

Konfigurasi Nginx untuk pembandingan ini harus menggunakan dua backend:

```nginx
upstream file_api { server 127.0.0.1:8001; server 127.0.0.1:8002; }
server { listen 8080; location / { proxy_pass http://file_api; proxy_set_header Host $host; } }
```

Pastikan `http://127.0.0.1:8080/` berhasil dibuka sebelum menjalankan mode `lb-2-api`.

## 3. Menjalankan tiap skenario

Runner menghentikan Locust otomatis setelah 5 menit. Hasil berada di `results/<mode>-<file>-<users>-<timestamp>/`.

```powershell
# API langsung, 100 users, file 1 MB
.\scripts\run_test.ps1 -Mode no-lb -Users 100 -FileSize 1mb

# Nginx + 2 API, 100 users, file 1 MB
.\scripts\run_test.ps1 -Mode lb-2-api -Users 100 -FileSize 1mb
```

Ulangi untuk `-Users 100`, `1000`, `10000` dan `-FileSize 1kb`, `10kb`, `1mb`, `10mb`, `100mb`. Agar ramp-up terkontrol, misalnya 1.000 users naik 100 user/detik:

```powershell
.\scripts\run_test.ps1 -Mode lb-2-api -Users 1000 -FileSize 1mb -SpawnRate 100
```

Jalankan satu skenario pada satu waktu dan, untuk hasil yang lebih kuat, ulangi setiap kombinasi tiga kali. Jangan menjalankan 10.000 user dari satu laptop tanpa mencatat bahwa generator load bisa menjadi bottleneck.

## 4. Output dan metrik

Setiap run menghasilkan:

- `locust-report.html`: laporan visual Locust dan error yang terjadi.
- `locust_stats.csv`: statistik sumber.
- `resources.csv`: sampel CPU/RAM setiap dua detik pada port API/LB.
- `summary.csv`: p50, p90, p95, p99, throughput, error rate, CPU/RAM rata-rata dan maksimum.

Setelah seluruh run selesai, buat tabel gabungan dan grafik:

```powershell
python scripts/make_charts.py
```

Outputnya ada di `results/evaluation/`: `all_results.csv`, `throughput_rps.png`, `latency_p95_ms.png`, dan `error_rate_percent.png`.

## 5. Tabel laporan

Salin baris dari `all_results.csv` ke laporan. Kolom inti berikut wajib diulas:

| Mode | File | Users | p50 | p90 | p95 | p99 | Throughput | Error rate | Avg/Max CPU | Avg/Max RAM | Titik kegagalan |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| no-lb |  |  |  |  |  |  |  |  |  |  |  |
| lb-2-api |  |  |  |  |  |  |  |  |  |  |  |

Titik kegagalan dicatat saat error rate mulai naik, p99 melonjak tajam, koneksi ditolak/timeout, atau CPU/RAM mencapai batas praktis. Sertakan pesan dari `locust-report.html` dan waktu kejadian dari `resources.csv` sebagai bukti.
