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
| `!start Budi Santoso` | Simpan ID Discord dan nama Budi Santoso di tabel `owner`. |
| `!list` | Tampilkan semua task milik pengguna. |
| `!add Belajar Python` | Tambahkan task bernama Belajar Python dengan status `todo`. |
| `!update 1 on progress` | Ubah status task dengan ID 1 menjadi `on progress`. |
| `!delete 1` | Hapus task dengan ID 1. |
| `!help` | Tampilkan bantuan. |

Semua perintah langsung ditulis di chat. Nama pengguna, nama task, dan status
yang mengandung spasi dapat ditulis langsung tanpa tanda kutip.
Status tersedia: `todo`, `on progress`, dan `done`.

Contoh alur penggunaan:

```text
!start Budi Santoso
!add Belajar Python
!list
!update 1 on progress
!update 1 done
!delete 1
```

Ganti `1` dengan ID task yang muncul dari `!list`.

## Perilaku bot saat ini

- Pengguna harus terdaftar melalui `!start` sebelum menambah task. Mengirim
  `!start` lagi tidak mengganti nama pengguna yang sudah tersimpan.
- `!list` menampilkan ID, nama, dan status task milik pengirim perintah dalam
  satu pesan. Jika belum ada task, bot meminta pengguna menambah task.
- `!add` menghapus spasi di awal/akhir nama task dan menyimpan status `todo`.
- `!update` menghapus spasi di awal/akhir status dan mengubahnya menjadi huruf
  kecil. Update hanya berhasil jika status tersedia dan task milik pengguna.
- `!delete` hanya menghapus task milik pengguna yang mengirim perintah.
- Nama pengguna dan nama task belum memiliki batas panjang khusus dalam kode.
  Daftar task juga belum dibagi menjadi beberapa pesan jika terlalu panjang.
- Argumen seperti ID task dikonversi oleh `discord.py`. Belum ada penanganan
  khusus untuk membalas perintah dengan argumen yang kurang atau salah.

Pesan gagal `!add` di `bot.py` masih menyarankan `!register`. Perintah registrasi
yang tersedia saat ini adalah `!start`.

## Alur mengajar 20 menit

- 3 menit: imports, intents, prefix `!`, dan `DatabaseManager`.
- 4 menit: `!start`, `ctx.author.id`, dan pemanggilan fungsi database.
- 8 menit: perintah `!list`, `!add`, `!update`, dan `!delete`.
  Jelaskan `ctx.author.id`, `await ctx.send`, dan parameter setelah `*` yang
  menangkap sisa pesan, termasuk spasi.
- 2 menit: nilai `True`/`False` dari fungsi database dan balasan berhasil/gagal.
- 3 menit: praktik alur registrasi, tambah, lihat, update, dan hapus task.

Siapkan database dan token sebelum kelas. Bagian setup dapat disediakan sebagai
kode awal agar siswa fokus menulis lima perintah bot.

## Membaca kode

- `logic.py`: semua SQL ada dalam fungsi-fungsi `DatabaseManager`. Fungsi yang
  mengakses database membuka koneksi, menjalankan query di dalam `with conn`,
  lalu menutup koneksi. Query yang mengubah data memanggil `commit()`.
- `bot.py`: perintah teks, pemanggilan `DatabaseManager`, dan pesan Discord.
- `config.py`: token bot dan nama file database.
- `task_manager.db`: tabel `owner`, `task`, dan `status`.

`owner.id` menyimpan ID Discord. `task.owner_id` menghubungkan task dengan pemilik,
sedangkan `task.status_id` menghubungkan task dengan nama status di tabel `status`.
Query update/delete selalu memeriksa ID task sekaligus ID pemiliknya.

Fungsi database yang dipanggil setiap perintah:

| Perintah | Fungsi di `DatabaseManager` |
| --- | --- |
| `!start` | `add_owner(user_id, user_name)` |
| `!list` | `get_tasks(user_id)` |
| `!add` | `add_task(user_id, task_name)`, yang memeriksa `get_owner(user_id)` |
| `!update` | `update_task(user_id, task_id, status_name)`, yang memeriksa `get_statuses()` |
| `!delete` | `delete_task(user_id, task_id)` |
