# ILP Hazard Simulator

Tugas kelompok **INF-1316 Organisasi dan Arsitektur Komputer** (Informatika ITSB).
Topik: Paralelisme CPU - mitigasi *data hazards* pada Instruction-Level Parallelism (ILP).

Simulator ini dikembangkan dari
[instruction-level-parallelism-simulator](https://github.com/harshitasingh4863/instruction-level-parallelism-simulator),
lalu ditambah deteksi tiga jenis data hazard: **RAW**, **WAR**, dan **WAW**, masing-masing dengan dependency graph.

## Anggota dan pembagian tugas

| Anggota | Bagian | Nama | NIM |
|---|---|---|---|
| 1 | RAW (Read After Write) | Siti Nor Hamidah | 51240022 |
| 2 | WAR (Write After Read) | Naila Nur Azizah Musgamy | 51240034 |
| 3 | WAW (Write After Write), README, laporan | Siti Nahdia Nahda | 51240025 |

## Tiga jenis data hazard

Contoh dari materi (I1 lebih dulu dari I2):

| Hazard | Penjelasan | Contoh | Jenis dependensi |
|---|---|---|---|
| **RAW** | I2 membaca register yang ditulis I1 | `I1: R1 = R2 + R3` / `I2: R4 = R1 + R5` | True data dependence |
| **WAR** | I2 menulis register yang dibaca I1 | `I1: R1 = R2 + R3` / `I2: R2 = R4 + R5` | Anti-dependence (name dependence) |
| **WAW** | I1 dan I2 menulis register yang sama | `I1: R1 = R2 + R3` / `I2: R1 = R4 + R5` | Output dependence (name dependence) |

RAW adalah dependensi data asli yang tidak bisa dihindari. WAR dan WAW adalah *name dependence*,
sehingga dapat dihilangkan dengan **register renaming**.

## Struktur repository

| File / folder | Fungsi |
|---|---|
| `instruction.py` | Struktur data `Instruction` dan `Dependency` |
| `hazard_raw.py` | Deteksi RAW |
| `hazard_war.py` | Deteksi WAR |
| `hazard_waw.py` | Deteksi WAW (`detect_waw`), register renaming, eksekusi sequential dan ILP bagian WAW |
| `dependency.py` | Menggabungkan deteksi RAW, WAR, WAW (`find_dependencies`) |
| `simulator.py` | Eksekusi sequential, paralel (ILP), register renaming, perbandingan performa |
| `graph.py` | Menggambar dependency graph |
| `programs.py` | Program contoh RAW, WAR, dan WAW |
| `main.py` | Program utama simulasi WAW |
| `ILP_Hazard_Simulator.ipynb` | Notebook (Google Colab) bagian WAW |
| `simulasi_semua.py` | Menjalankan simulasi RAW, WAR, WAW dan membuat dependency graph RAW dan WAR |
| `graph_*.png`, `dependency_graph_waw*.png` | Dependency graph RAW, WAR, WAW (sebelum dan sesudah register renaming) |
| `hasil_simulasi.txt`, `hasil_simulasi_semua.txt` | Hasil simulasi WAW (`main.py`) dan RAW, WAR, WAW (`simulasi_semua.py`) |
| `Laporan_RAW_WAR_WAW_ .pdf` | Laporan tugas (dependency graph dan link GitHub) |
| `requirements.txt` | Library yang dibutuhkan |

## Cara menjalankan

```bash
pip install -r requirements.txt
python main.py            # simulasi WAW + register renaming
python simulasi_semua.py  # simulasi RAW, WAR, WAW + dependency graph RAW dan WAR
python hazard_raw.py      # uji cepat deteksi RAW
```

## Hasil bagian WAW

Program uji memuat WAW pada R1 (I1 dan I3) dan R4 (I2 dan I5):

| Skenario | Cycle | Speedup |
|---|---|---|
| Sequential | 6 | 1.00x |
| ILP + penanganan WAW (stall) | 3 | 2.00x |
| ILP + register renaming | 2 | 3.00x |

Jika WAW diabaikan, dua instruksi yang menulis register sama berjalan bersamaan sehingga urutan
penulisan tidak terjamin (hazard). Register renaming menghilangkan WAW dan memberi paralelisme terbaik.
