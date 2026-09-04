# API Serving File dengan FastAPI dan Nginx Load Balancer

Project ini merupakan implementasi REST API untuk **melayani file TXT dengan berbagai ukuran** dan menyediakan **3 instance API** di belakang **Nginx sebagai load balancer**.

Project ini dapat digunakan untuk melakukan pengujian performa/load testing dengan membandingkan:

1. API tanpa load balancer
2. API dengan load balancer

## Ukuran File

File yang disediakan:

- 1 KB
- 10 KB
- 1 MB
- 10 MB
- 100 MB

## Arsitektur

### Tanpa Load Balancer

Request dikirim langsung ke salah satu instance FastAPI.

```text
Client / Load Tester
        |
        v
  FastAPI API 1
    127.0.0.1:8001
        |
        v
     File TXT
```

### Dengan Load Balancer

Request dikirim ke Nginx. Nginx kemudian membagi request ke 3 instance API.

```text
                    Client / Load Tester
                            |
                            v
                    Nginx Load Balancer
                       127.0.0.1:8080
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
           API 1         API 2         API 3
           :8001         :8002         :8003
              |             |             |
              +-------------+-------------+
                            |
                            v
                         File TXT
```

Nginx menggunakan metode **round-robin** secara default untuk membagi request ke backend.

---

# 1. Requirements

Pastikan software berikut sudah tersedia:

- Python 3.12
- VS Code (opsional, tetapi direkomendasikan)
- Nginx
- PowerShell / Command Prompt

Untuk load testing, project dapat menggunakan Locust.

> Python 3.14 juga dapat tetap ter-install di komputer. Virtual environment project ini secara khusus dibuat menggunakan Python 3.12.

---

# 2. Struktur Project

Struktur project:

```text
APIServingFile/
│
├── venv/
│
├── app/
│   ├── main.py
│   ├── generate_files.py
│   └── files/
│       ├── 1kb.txt
│       ├── 10kb.txt
│       ├── 1mb.txt
│       ├── 10mb.txt
│       └── 100mb.txt
│
├── requirements.txt
└── README.md
```

Nginx di-install secara terpisah, misalnya:

```text
C:\nginx
```

File konfigurasi Nginx berada di:

```text
C:\nginx\conf\nginx.conf
```

---

# 3. Clone / Copy Project

Jika project diperoleh dari repository:

```powershell
git clone <URL-REPOSITORY>
```

Masuk ke folder project:

```powershell
cd APIServingFile
```

Jika project hanya berupa folder yang sudah di-copy, masuk ke folder tersebut menggunakan `cd`.

Contoh:

```powershell
cd "D:\KULIAH\SEMESTER 5\DABD\Tugas DABD\APIServingFile"
```

---

# 4. Membuat Virtual Environment

Disarankan menggunakan Python 3.12.

Cek Python:

```powershell
py -0p
```

Buat virtual environment:

```powershell
py -3.12 -m venv venv
```

Aktifkan:

```powershell
.\venv\Scripts\Activate.ps1
```

Jika berhasil, akan muncul:

```text
(venv) PS ...
```

Cek versi:

```powershell
python --version
```

Pastikan hasilnya Python 3.12.x.

Untuk keluar dari virtual environment:

```powershell
deactivate
```

> Virtual environment hanya berlaku pada terminal/session tempat environment tersebut diaktifkan.

---

# 5. Install Dependency

Pastikan virtual environment aktif:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependency:

```powershell
pip install -r requirements.txt
```

Jika `requirements.txt` belum tersedia, dependency utama yang dibutuhkan adalah:

```powershell
pip install fastapi uvicorn
```

Kemudian dapat dibuat:

```powershell
pip freeze > requirements.txt
```

---

# 6. Generate File TXT

File TXT tidak perlu dibuat satu per satu secara manual.

Gunakan:

```text
app/generate_files.py
```

Jalankan dari root project:

```powershell
python app/generate_files.py
```

Script akan membuat:

```text
app/files/
├── 1kb.txt
├── 10kb.txt
├── 1mb.txt
├── 10mb.txt
└── 100mb.txt
```

Periksa ukuran file:

```powershell
Get-ChildItem .\app\files\ | Select-Object Name, Length
```

Ukuran yang diharapkan:

| File | Ukuran |
|---|---:|
| 1kb.txt | 1,024 bytes |
| 10kb.txt | 10,240 bytes |
| 1mb.txt | 1,048,576 bytes |
| 10mb.txt | 10,485,760 bytes |
| 100mb.txt | 104,857,600 bytes |

---

# 7. Menjalankan API

Semua instance API menggunakan file:

```text
app/main.py
```

Tidak perlu membuat file Python terpisah untuk setiap API.

Yang membedakan setiap instance adalah:

- `API_INSTANCE`
- port

## API 1

Buka Terminal 1:

```powershell
cd "D:\KULIAH\SEMESTER 5\DABD\Tugas DABD\APIServingFile"
.\venv\Scripts\Activate.ps1

$env:API_INSTANCE="API-1"
uvicorn app.main:app --host 127.0.0.1 --port 8001
```

API 1:

```text
http://127.0.0.1:8001
```

Swagger:

```text
http://127.0.0.1:8001/docs
```

## API 2

Buka Terminal 2:

```powershell
cd "D:\KULIAH\SEMESTER 5\DABD\Tugas DABD\APIServingFile"
.\venv\Scripts\Activate.ps1

$env:API_INSTANCE="API-2"
uvicorn app.main:app --host 127.0.0.1 --port 8002
```

API 2:

```text
http://127.0.0.1:8002
```

Swagger:

```text
http://127.0.0.1:8002/docs
```

## API 3

Buka Terminal 3:

```powershell
cd "D:\KULIAH\SEMESTER 5\DABD\Tugas DABD\APIServingFile"
.\venv\Scripts\Activate.ps1

$env:API_INSTANCE="API-3"
uvicorn app.main:app --host 127.0.0.1 --port 8003
```

API 3:

```text
http://127.0.0.1:8003
```

Swagger:

```text
http://127.0.0.1:8003/docs
```

Ketiga terminal API harus tetap berjalan selama pengujian.

---

# 8. Testing API Secara Langsung

Setelah API berjalan, buka:

```text
http://127.0.0.1:8001/
```

```text
http://127.0.0.1:8002/
```

```text
http://127.0.0.1:8003/
```

Response akan menunjukkan instance API.

Contoh:

```json
{
    "message": "File Serving API",
    "instance": "API-1",
    "available_files": [
        "1kb",
        "10kb",
        "1mb",
        "10mb",
        "100mb"
    ]
}
```

Tes file:

```text
http://127.0.0.1:8001/files/1kb
http://127.0.0.1:8001/files/10kb
http://127.0.0.1:8001/files/1mb
http://127.0.0.1:8001/files/10mb
http://127.0.0.1:8001/files/100mb
```

Untuk API 2 dan API 3, ubah port menjadi `8002` atau `8003`.

---

# 9. Install Nginx

Nginx merupakan software terpisah dari Python virtual environment.

Download dan extract Nginx, misalnya ke:

```text
C:\nginx
```

Pastikan terdapat:

```text
C:\nginx\nginx.exe
```

Cek:

```powershell
cd C:\nginx
.\nginx.exe -v
```

---

# 10. Konfigurasi Nginx

Edit file:

```text
C:\nginx\conf\nginx.conf
```

Gunakan konfigurasi berikut:

```nginx
#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;


    # ==========================================
    # LOAD BALANCER
    # ==========================================
    upstream file_api {
        server 127.0.0.1:8001;
        server 127.0.0.1:8002;
        server 127.0.0.1:8003;
    }


    # ==========================================
    # SERVER / LOAD BALANCER
    # ==========================================
    server {
        listen       8080;
        server_name  localhost;

        location / {
            proxy_pass http://file_api;

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        error_page   500 502 503 504  /50x.html;

        location = /50x.html {
            root   html;
        }
    }


    # HTTPS server
    #
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;

    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;

    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;

    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}

}
```

---

# 11. Test Konfigurasi Nginx

Buka terminal baru.

```powershell
cd C:\nginx
```

Test konfigurasi:

```powershell
.\nginx.exe -t
```

Jika berhasil:

```text
syntax is ok
test is successful
```

Jalankan Nginx:

```powershell
.\nginx.exe
```

Periksa proses:

```powershell
tasklist | findstr nginx
```

Periksa port:

```powershell
netstat -ano | findstr :8080
```

Pastikan port `8080` berada dalam status `LISTENING`.

---

# 12. Jika Nginx Sudah Berjalan Sebelumnya

Jika Nginx sudah berjalan dan konfigurasi diubah, tidak perlu menjalankan Nginx kedua kali.

Setelah konfigurasi berhasil dites:

```powershell
.\nginx.exe -s reload
```

Perintah tersebut memuat ulang konfigurasi Nginx.

---

# 13. Testing Load Balancer

Buka:

```text
http://127.0.0.1:8080/
```

Refresh beberapa kali.

Response dapat menunjukkan:

```text
API-1
API-2
API-3
```

Hal ini dapat digunakan untuk memeriksa bahwa request diteruskan ke beberapa backend.

---

# 14. Testing File melalui Load Balancer

Gunakan endpoint Nginx:

```text
http://127.0.0.1:8080/files/1kb
http://127.0.0.1:8080/files/10kb
http://127.0.0.1:8080/files/1mb
http://127.0.0.1:8080/files/10mb
http://127.0.0.1:8080/files/100mb
```

Jika file dapat diakses/download, berarti alur berikut berhasil:

```text
Client
  ↓
Nginx :8080
  ↓
API 1 / API 2 / API 3
  ↓
File TXT
```

---

# 15. Endpoint untuk Pengujian

## Tanpa Load Balancer

Untuk pengujian tanpa load balancer, request diarahkan langsung ke API.

Contoh:

```text
http://127.0.0.1:8001/files/1mb
```

## Dengan Load Balancer

Untuk pengujian dengan load balancer:

```text
http://127.0.0.1:8080/files/1mb
```

Pada skenario dengan load balancer, request harus diarahkan ke Nginx, bukan langsung ke port API.

---

# 16. Load Testing dengan Locust

Install Locust:

```powershell
pip install locust
```

Pastikan instalasi berhasil:

```powershell
locust --version
```

Buat file:

```text
locustfile.py
```

Locust digunakan untuk menjalankan skenario:

- 100 user selama 5 menit
- 1.000 user selama 5 menit
- 10.000 user selama 5 menit

Setiap skenario diuji untuk masing-masing ukuran file.

---

# 17. Skenario Pengujian

Ukuran file:

```text
1 KB
10 KB
1 MB
10 MB
100 MB
```

Jumlah user:

```text
100
1.000
10.000
```

Skenario:

```text
Tanpa Load Balancer
Dengan Load Balancer
```

Total kombinasi:

```text
5 ukuran file × 3 jumlah user × 2 skenario = 30 pengujian
```

Setiap pengujian berlangsung selama 5 menit.

---

# 18. Metrik yang Dicatat

Metrik utama:

- P50 latency
- P90 latency
- P95 latency
- P99 latency
- Maximum latency
- Throughput / requests per second
- Total requests
- Successful requests
- Failed requests
- Error rate

Jika diperlukan, dapat ditambahkan:

- CPU usage
- RAM usage

---

# 19. Checklist Sebelum Pengujian

Pastikan semua hal berikut sudah siap:

- [ ] Python 3.12
- [ ] Virtual environment
- [ ] FastAPI
- [ ] Uvicorn
- [ ] File 1 KB
- [ ] File 10 KB
- [ ] File 1 MB
- [ ] File 10 MB
- [ ] File 100 MB
- [ ] API 1 :8001
- [ ] API 2 :8002
- [ ] API 3 :8003
- [ ] Nginx :8080
- [ ] Nginx terhubung ke ketiga API
- [ ] Semua endpoint file dapat diakses
- [ ] Locust
- [ ] Skenario load testing

---

# 20. Troubleshooting

## Port API sudah digunakan

Jika muncul error bahwa port `8001`, `8002`, atau `8003` sudah digunakan, periksa proses yang menggunakan port tersebut:

```powershell
netstat -ano | findstr :8001
netstat -ano | findstr :8002
netstat -ano | findstr :8003
```

Hentikan proses yang tidak diperlukan atau gunakan port lain.

Jika port diubah, sesuaikan juga konfigurasi Nginx.

---

## Nginx gagal start

Jalankan:

```powershell
cd C:\nginx
.\nginx.exe -t
```

Periksa pesan error yang diberikan.

Pastikan API 1, API 2, dan API 3 sudah berjalan sebelum melakukan pengujian melalui Nginx.

---

## Nginx tidak bisa meneruskan request

Pastikan ketiga API dapat diakses langsung:

```text
http://127.0.0.1:8001/
http://127.0.0.1:8002/
http://127.0.0.1:8003/
```

Kemudian pastikan konfigurasi memiliki:

```nginx
upstream file_api {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}
```

dan:

```nginx
proxy_pass http://file_api;
```

---

## Perubahan konfigurasi Nginx tidak terbaca

Setelah mengubah `nginx.conf`:

```powershell
.\nginx.exe -t
```

Jika berhasil:

```powershell
.\nginx.exe -s reload
```

---

# 21. Menghentikan Sistem

## Menghentikan FastAPI

Pada setiap terminal API:

```text
Ctrl + C
```

## Menghentikan Nginx

```powershell
cd C:\nginx
.\nginx.exe -s quit
```

## Keluar dari virtual environment

```powershell
deactivate
```

---

# 22. Ringkasan Port

| Komponen | Port |
|---|---:|
| API 1 | 8001 |
| API 2 | 8002 |
| API 3 | 8003 |
| Nginx Load Balancer | 8080 |

---

# 23. Ringkasan Menjalankan Project

Urutan paling sederhana:

### Terminal 1

```powershell
cd "<PROJECT_PATH>"
.\venv\Scripts\Activate.ps1
$env:API_INSTANCE="API-1"
uvicorn app.main:app --host 127.0.0.1 --port 8001
```

### Terminal 2

```powershell
cd "<PROJECT_PATH>"
.\venv\Scripts\Activate.ps1
$env:API_INSTANCE="API-2"
uvicorn app.main:app --host 127.0.0.1 --port 8002
```

### Terminal 3

```powershell
cd "<PROJECT_PATH>"
.\venv\Scripts\Activate.ps1
$env:API_INSTANCE="API-3"
uvicorn app.main:app --host 127.0.0.1 --port 8003
```

### Terminal 4

```powershell
cd C:\nginx
.\nginx.exe -t
.\nginx.exe
```

Setelah semuanya berjalan:

```text
http://127.0.0.1:8001/   → API 1
http://127.0.0.1:8002/   → API 2
http://127.0.0.1:8003/   → API 3
http://127.0.0.1:8080/   → Load Balancer
```

---

# 24. Catatan

Project ini menggunakan satu source code FastAPI untuk tiga instance API. Penambahan atau pengurangan instance cukup dilakukan dengan menjalankan source code pada port yang berbeda dan menyesuaikan daftar backend pada konfigurasi Nginx.

Untuk penggunaan di komputer lain, bagian yang perlu disesuaikan terutama adalah:

1. `<PROJECT_PATH>` sesuai lokasi project.
2. Lokasi instalasi Nginx.
3. Python yang tersedia.
4. Port yang mungkin sedang digunakan aplikasi lain.
