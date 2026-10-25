"""
WAR (Write After Read) - anti-dependency (name dependency).
Instruksi j MENULIS register yang DIBACA oleh instruksi i (i < j).
Instruksi j tidak boleh menulis sebelum i selesai membaca, kalau tidak i
akan membaca nilai yang salah. Tidak ada aliran data antara i dan j: hanya
bentrok NAMA register, sehingga bisa dihilangkan dengan register renaming.

Contoh:
    I1: R4 = R2 + R3
    I2: R2 = R5 + R6   <- I2 menulis R2 yang dibaca I1
"""
from instruction import Dependency, no_write_between


def is_war(inst1, inst2):
    """Cek pasangan: apakah inst2 menulis register yang dibaca inst1?"""
    return inst2.destination in inst1.sources


def detect_war(instructions):
    deps = []
    for j, writer in enumerate(instructions):
        reg = writer.destination
        for i in range(j):
            reader = instructions[i]
            if is_war(reader, writer) and no_write_between(instructions, i, j, reg):
                # producer = pembaca (lebih awal), consumer = penulis (harus menunggu)
                deps.append(Dependency(reader, writer, "WAR", reg))
    return deps
