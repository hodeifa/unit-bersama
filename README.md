# Unit Bersama

Situs statis untuk platform kepemilikan bersama motor premium (6 anggota per unit). Satu file HTML, tanpa server dan tanpa dependensi saat berjalan. Dibuat sebagai Claude Artifact, lalu diekspor ke repo ini.

> **Status:** draf. Halaman hukum (Ketentuan, Perlindungan, Privasi) dan jawaban FAQ nomor 8 dan 9 belum final dan perlu ditinjau notaris atau penasihat hukum sebelum situs dibuka ke publik.

## Isi repo

| Path | Fungsi |
| --- | --- |
| `index.html` | Situs final, siap deploy statis. **Sekaligus sumber data**: teks, foto, kebijakan, dan slot tersimpan di dalamnya. |
| `public/katalog.html` | Basis awal (katalog model, kalkulator, dialog). |
| `public/site.html` | Basis + desain komersial + halaman. Dibuat oleh `tools/patch_site.py`. |
| `public/site_final.html` | `site.html` + data dari `index.html`. Dibuat oleh `tools/build_final.py`. |
| `public/site_nophoto.html` | Salinan tanpa foto pendiri, hanya untuk `test_founder.py`. |
| `tools/site_css.css`, `tokens.css`, `commercial.css`, `site_block.js` | Sumber gaya dan skrip halaman. |
| `tools/test_*.py`, `shots.py` | Tes Playwright dan pembuat tangkapan layar. |
| `fixtures/` | Berkas pendukung tes. |

Alur build: `katalog.html` → (`patch_site.py`) → `site.html` → (`build_final.py`, menggabungkan data dari `index.html` yang ada) → `site_final.html` → (`build_index.py`) → `index.html`.

## Mengubah isi situs (mode kelola lokal)

Tanpa Claude, perubahan disimpan dengan mengunduh `index.html` baru:

1. Buka `index.html#kelola` di browser, dari file di laptop atau dari alamat hosting. Kalau halaman sudah terbuka, tambahkan `#kelola` lalu **muat ulang**; penanda ini hanya dibaca saat halaman dibuka.
2. Klik **Kelola situs**. Ubah Pengaturan, Info pengelola, Ketentuan, model, slot, FAQ, atau profil pendiri.
3. Klik **Unduh HTML**. Browser mengunduh `index.html` (bisa bernama `index (1).html` bila sudah ada di folder unduhan).
4. Timpa `index.html` di repo dengan file itu, lalu commit dan push. Hosting memperbarui situs otomatis.

Hal yang perlu diingat:

- Perubahan **belum tersimpan** sampai file diunduh dan menimpa `index.html` di repo. Tombol **Batalkan** membuang perubahan yang belum diunduh.
- Build ulang (di bawah) membaca data dari `index.html` yang ada, jadi perubahan dari mode lokal tidak hilang saat kode situs dibangun ulang.
- Tampilan kelola bisa dibuka siapa saja yang menambahkan `#kelola`, tetapi hasil kerjanya hanya berkas yang diunduh ke komputernya sendiri. Situs yang tayang hanya berubah bila ada yang mem-push ke repo. Bila ingin tampilan itu tidak ada sama sekali di situs tayang, hapus baris `try { if (location.hash === '#kelola') UI.canEdit = true; } catch (e) {}` di `public/katalog.html` pada build produksi, dan simpan salinan yang masih memuatnya untuk mengelola.
- Artifact di Claude tidak ikut berubah. Pilih satu tempat sebagai sumber utama; bila repo yang dipilih, jangan ubah lagi lewat Claude, supaya dua versi tidak berselisih.
- Data pribadi anggota jangan ditaruh di situs ini. Seluruh isi `index.html` bisa dilihat siapa saja lewat view-source, dan form slot hanya menerima inisial.

## Uji coba di laptop

Klik dua kali `index.html`, atau buka `file:///…/index.html#kelola` untuk masuk ke mode kelola. Tidak perlu server, domain, atau koneksi untuk melihat isi dan mencoba mode kelola; hanya font Barlow yang dimuat dari Google Fonts, dan tanpa internet halaman memakai font cadangan.

## Deploy

`index.html` sudah berisi semuanya (CSS, JS, data, gambar).

- **Cloudflare Pages / Netlify:** hubungkan repo, build command kosong, output directory `/` (root). Keduanya memberi alamat gratis (`*.pages.dev` atau `*.netlify.app`) dan bisa memakai repo privat. Domain sendiri bisa ditambahkan nanti tanpa mengubah situs.
- **GitHub Pages:** aktifkan Pages dari branch `main`, folder `/ (root)`. Pada akun gratis, Pages umumnya hanya untuk repo publik.

Navigasi memakai hash (`#biaya`, `#faq`, dan seterusnya), jadi tidak perlu pengaturan rewrite.

## Build ulang

Butuh Python 3. Perlu hanya bila kode situs (`tools/*.css`, `tools/site_block.js`, `public/katalog.html`) diubah; perubahan isi cukup lewat mode kelola lokal.

```bash
python3 tools/patch_site.py
python3 tools/build_final.py
python3 tools/build_index.py
```

## Tes

```bash
pip install playwright pillow && playwright install chromium
(cd fonts && npm install)   # font Barlow lokal agar tata letak tes sama dengan produksi

python3 tools/test_commercial.py
python3 tools/test_site.py
python3 tools/test_regress.py
python3 tools/test_founder.py public/site_nophoto.html
python3 tools/test_local.py   # mode kelola lokal: ubah, unduh, buka hasilnya, build ulang
```

Hasil terakhir: 60/60, 72/72, 50/50, 20/20, dan 26 pemeriksaan mode lokal lulus. Tes mode Claude memakai stub untuk fitur simpan Claude, jadi alur pengelola di dalam tampilan Claude yang asli belum teruji.

## Catatan sebelum dipublikasikan

- **Hak atas foto:** foto pendiri dan foto model "Street Rod" yang terunggah tampak berupa tangkapan layar dengan watermark aplikasi lain, dan foto hero berupa tangkapan layar video. Ganti dengan foto milik sendiri atau berlisensi sebelum situs dibuka ke publik.
- **Repo sebaiknya privat** sampai konten dan foto di atas dibereskan. Data kontak dan nama perusahaan ada di dalam berkas.
- **Data yang masih perlu diisi:** NIB, alamat, email, jam layanan, detail enam kebijakan (Ketentuan), jumlah denda dan sanksi.

## Simpan ke GitHub

```bash
git init -b main
git add .
git commit -m "Situs Unit Bersama"
git remote add origin git@github.com:<akun>/<nama-repo>.git
git push -u origin main
```
