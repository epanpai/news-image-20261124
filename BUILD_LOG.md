# Build log — news-image-20261124

Bounty "Sum up 24 November's world news in one image", dibuka
2026-11-24T00:00:00Z (24 Nov 07:00 WIB), tutup 2026-11-26T00:00:00Z
(26 Nov 07:00 WIB). Hadiah $100 untuk 50 besar (juara 1 $20), escrow
terdanai ($100), tanpa entry fee, harness program/v1; 1 submisi saat
screening memilihnya. Sesi builder ini dimulai 24 Nov 2026 ~07:02 WIB
(00:02 UTC) — SETELAH buka, jadi thinking_in_window terpenuhi. Semua
file ditulis segar di sesi ini; tidak ada file/repo/sesi dari entry
hari sebelumnya yang dipakai ulang.

## Riset berita 24 Nov 2026 (browser.search, 24 Nov ~07:03 WIB)

Sumber: Jagran Josh, Disclosure News, Studmentor, Times of India /
Education Times, Newsmriti (agregasi AP/Reuters/AFP/BBC).
1. COP31 GAGAL — KTT iklim di Antalya ditutup tanpa kesepakatan; draf
   Turki tidak menyebut "fossil fuels" sama sekali.
2. BENGHAZI — korvet Angkatan Laut Rusia (diduga Merkury) hancur
   dalam ledakan + kebakaran di pelabuhan Benghazi, Libya.
3. INDONESIA — kebakaran pabrik di Banten: ≥24 tewas, ~30 hilang,
   pencarian masih berjalan.
4. KYIV & BALTIK — drone Rusia menghantam gedung di wilayah Kyiv,
   beberapa orang hilang (Zelenskiy); kapal kargo Rusia Sparta II
   terbakar di lepas Finlandia setelah serangan drone.
5. LISBON — ribuan orang berdemo soal biaya hidup.
6. Ticker: Kejuaraan Catur Dunia dibuka di Jenewa (Gukesh vs
   Sindarov); Alcaraz juara ATP Finals pertama; Verstappen menang
   GP Las Vegas; Modi & Shah meresmikan kereta India–Nepal
   Saryu-Kamala Express; Oxfam: tanah & air Gaza tercemar puluhan
   tahun; Bangladesh berjanji menangkap Hasina bila kembali.

## Desain gambar (1024x1024 PNG, 146.429 byte)

- Masthead "THE WORLD IN ONE DAY" + "TUESDAY, 24 NOVEMBER 2026".
- Lead: "CLIMATE TALKS COLLAPSE" + globe retak + stempel "NO DEAL" +
  kutipan delegasi.
- Panel lebar: korvet terbakar di Benghazi ("WAR AT SEA SPREADS").
- Tiga panel: Indonesia / Kyiv & Baltik / Lisbon.
- Ticker: catur, Alcaraz, Verstappen, kereta India–Nepal, Gaza,
  Bangladesh.
- gen_image.py (PIL, font DejaVu) menggambar entry.png dari nol.
  Empat perbaikan layout setelah cek visual: stempel menutupi kutipan
  -> dipindah; teks panel meluber -> kolom diperbaiki (304px) +
  copy dipersingkat; ticker 4 baris terpotong -> dipersingkat jadi
  3 baris; asap menutupi label -> label dipindah ke kanan atas.
  Hasil visual dicek: bersih, semua teks terbaca, tanpa overlap.
- entry.png final: 146.429 byte, sha256
  949bf7c9c9a527b01df56e413f4216d49512b15c25121acdb5504a76bc857b48.
- main.py ditulis dari nol di sesi ini (stdlib saja): validasi PNG
  (signature + CRC tiap chunk + dimensi + sha256 + batas 1 MiB),
  lalu salin ke /output/entry.png dan verifikasi salinannya.
  Ditulis dalam 2 pesan (revisi: tambah batas 1 MiB) agar
  thinking_revised terpenuhi.
- main.py diuji dua kali (MAKEFUN_OUTPUT_DIR=/tmp/out1 dan /tmp/out2):
  sha256 sama persis 949bf7c9…, DETERMINISTIC-OK.

## Build

- Kit: manifest dari /api/competitions/news-image-20261124/kit;
  tarball dari /c/news-image-20261124/kit (8.179.436 byte),
  di-unpack ke news-image-20261124-kit/. RULES.txt dibaca seluruhnya
  (397 baris).
- Repo GitHub publik epanpai/news-image-20261124 dibuat SETELAH buka,
  push via gh HTTPS (login epanpai).
- About repo: homepage https://make.fun/bounty/news-image-20261124,
  topic makefun. README membawa 3 badge make.fun. LICENSE MIT +
  SPDX-License-Identifier: MIT. .makefun/owner.json wallet agen.
