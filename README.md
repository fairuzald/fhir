## FHIR Simulation Server

Panduan singkat untuk menjalankan proyek ini secara lokal menggunakan Docker Compose.

### Prasyarat

- Docker dan Docker Compose terpasang
- Opsional: make (untuk menggunakan perintah ringkas dari `backend/Makefile`)

### Jalankan Cepat (Disarankan)

Di root proyek:

```bash
docker compose up -d --build
```

Atau menggunakan Makefile:

```bash
make -C backend up
```

Setelah kontainer berjalan:

- API tersedia di `http://localhost:8000`
- Dokumentasi Swagger di `http://localhost:8000/docs`
- Dokumentasi ReDoc di `http://localhost:8000/redoc`

### Layanan yang Berjalan

- `postgres` (PostgreSQL 15), port 5432, kredensial default:
  - DB: `fhir_db`
  - User: `fhir_user`
  - Password: `fhir_password`
- `app` (FastAPI + Uvicorn), port 8000

Konfigurasi tersebut didefinisikan di `docker-compose.yml`. Aplikasi membaca konfigurasi dari environment variables (lihat `backend/src/config/settings.py`).

### Perintah Umum (Makefile)

Jalankan dari root proyek dengan `-C backend` atau masuk ke folder `backend` terlebih dahulu.

```bash
# Start app (build bila perlu)
make -C backend up

# Hentikan semua layanan
make -C backend down

# Lihat log service app
make -C backend logs

# Jalankan migrasi (alembic upgrade head)
make -C backend migrate

# Seed data contoh
make -C backend seed

# Format & lint (black, ruff)
make -C backend fmt

# Type checking (mypy)
make -C backend typecheck

# Build image
make -C backend build

# Rebuild tanpa cache dan naikkan layanan
make -C backend rebuild
```

### Variabel Lingkungan Utama

Anda dapat menyesuaikan melalui `docker-compose.yml` atau file `.env` (dibaca oleh `pydantic-settings`). Nilai default:

- `DATABASE_URL`: `postgresql://fhir_user:fhir_password@postgres:5432/fhir_db`
- `SECRET_KEY`: ganti di produksi
- `ALGORITHM`: `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`
- `CORS_ORIGINS`: `[*]`

Untuk pengembangan lokal tanpa Docker (opsional), contoh menjalankan Uvicorn:

```bash
cd backend
pip install -e .
uvicorn src.interfaces.api.main:app --reload
```

Pastikan `DATABASE_URL` mengarah ke instance PostgreSQL Anda (default lokal: `postgresql://fhir_user:fhir_password@localhost:5432/fhir_db`).

### Seeding dan Migrasi

- Seed data: `make -C backend seed` (menjalankan `scripts/load_seed.py` di dalam kontainer)
- Migrasi: `make -C backend migrate`

### Koleksi Postman

Tersedia di `client/postman_collection.json` untuk mencoba endpoint API.

### Endpoint Dasar

- Prefix API: `/api`
- Contoh: dokumentasi otomatis di `/docs` menampilkan semua route (auth, patient, observation, encounter, dsb.)

### Troubleshooting

- Jika `app` gagal konek ke DB, pastikan service `postgres` healthy (Compose memiliki healthcheck) dan port tidak bentrok.
- Gunakan `make -C backend logs` untuk melihat log aplikasi.
- Jika terjadi perubahan dependensi, jalankan `make -C backend rebuild`.

---

Selamat mencoba!
