# Task Manager Discord

Bot sederhana untuk belajar Python, SQLite, dan perintah teks Discord.
Gunakan Python 3.10 atau lebih baru.

## Menjalankan bot

1. Buat virtual environment: `python3 -m venv venv`.
2. Aktifkan: `source venv/bin/activate` (Windows: `venv\Scripts\activate`).
3. Pasang library: `python -m pip install -r requirements.txt`.
4. Isi `TOKEN` di `config.py` dengan token bot milikmu. Jangan membagikan token.
   Pastikan `DATABASE = 'task_manager.db'`.
5. Di [Discord Developer Portal](https://discord.com/developers/applications),
   buka aplikasi bot → **Bot** → aktifkan **Message Content Intent**.
6. Undang bot ke server dengan scope `bot` dan izin **View Channels**,
   **Send Messages**, dan **Read Message History**.
7. Jalankan `python bot.py` dari folder repo ini.

Database `task_manager.db` harus sudah berisi tabel `owner`, `task`, dan `status`.
Tabel `status` harus sudah berisi `todo`, `on progress`, dan `done`.

## Perintah

| Perintah | Kegunaan |
| --- | --- |
| `!register Budi Santoso` | Simpan ID Discord dan nama Budi Santoso di tabel `owner`. |
| `!list` | Tampilkan semua task milik pengguna. |
| `!add Belajar Python` | Tambahkan task bernama Belajar Python dengan status `todo`. |
| `!update 1 on progress` | Ubah status task dengan ID 1 menjadi `on progress`. |
| `!delete 1` | Hapus task dengan ID 1. |
| `!help` | Tampilkan bantuan. |

Semua perintah langsung ditulis di chat. Gunakan `!list` untuk melihat ID task
sebelum update/delete. Nama pengguna, nama task, dan status yang mengandung spasi
dapat ditulis langsung tanpa tanda kutip. Nama pengguna dibatasi 1–80 karakter,
sedangkan nama task 1–100 karakter. Daftar panjang dikirim dalam beberapa pesan.
Status tersedia: `todo`, `on progress`, dan `done`.

## Alur mengajar 20 menit

- 3 menit: imports, intents, prefix `!`, dan `DatabaseManager`.
- 4 menit: `!register`, `ctx.author.id`, dan pemanggilan fungsi database.
- 8 menit: perintah `!list`, `!add`, `!update`, dan `!delete`.
  Jelaskan `ctx.author.id`, `await ctx.send`, dan parameter setelah `*` yang
  menangkap sisa pesan, termasuk spasi.
- 2 menit: pengecekan registrasi dan penanganan input yang salah.
- 3 menit: praktik alur registrasi, tambah, lihat, update, dan hapus task.

Siapkan database dan token sebelum kelas. Bagian setup dapat disediakan sebagai
kode awal agar siswa fokus menulis lima perintah bot.

## Membaca kode

- `logic.py`: semua SQL ada dalam fungsi-fungsi `DatabaseManager`. Setiap fungsi
  membuka koneksi, menjalankan query di dalam `with conn`, lalu menutup koneksi.
  Query yang mengubah data memanggil `commit()`.
- `bot.py`: perintah teks, validasi input, dan pesan Discord.
- `config.py`: token bot dan nama file database.
- `task_manager.db`: tabel `owner`, `task`, dan `status`.

`owner.id` menyimpan ID Discord. `task.owner_id` menghubungkan task dengan pemilik,
sedangkan `task.status_id` menghubungkan task dengan nama status di tabel `status`.
Query update/delete selalu memeriksa ID task sekaligus ID pemiliknya.
