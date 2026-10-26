# Simulator ILP - Bagian WAW (Write After Write)

Tugas kelompok INF-1316 Organisasi dan Arsitektur Komputer (Informatika ITSB).
Dikembangkan dari simulator: https://github.com/harshitasingh4863/instruction-level-parallelism-simulator

## Apa itu WAW?
WAW terjadi ketika dua instruksi menulis ke register yang sama.
Instruksi yang lebih akhir tidak boleh selesai menulis lebih dulu, kalau tidak nilai akhir register salah.
WAW adalah *output dependence* dan termasuk *name dependence*, sehingga bisa dihilangkan dengan *register renaming*.

## Isi file (bagian WAW)
| File | Fungsi |
|---|---|
| `hazard_waw.py` | Deteksi WAW, dependency, register renaming, eksekusi sequential dan ILP |
| `programs.py` | Program contoh yang memuat WAW (R1: I1->I3, R4: I2->I5) |
| `main.py` | Program utama, menjalankan seluruh simulasi |
| `README.md` | Dokumentasi ini |

## Cara menjalankan
```bash
python main.py
```

## Hasil
| Skenario | Cycle | Speedup |
|---|---|---|
| Sequential | 6 | 1.00x |
| ILP + penanganan WAW (stall) | 3 | 2.00x |
| ILP + register renaming | 2 | 3.00x |

Jika WAW diabaikan, I1 dan I3 (R1) serta I2 dan I5 (R4) berjalan bersamaan sehingga urutan penulisan tidak terjamin (hazard).
