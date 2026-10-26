"""
RAW (Read After Write) - true / data dependency.
Instruksi j MEMBACA register yang DITULIS oleh instruksi i (i < j).
Instruksi j harus menunggu hasil i. Tidak bisa dihilangkan dengan register renaming.

Contoh:
    I1: R1 = R2 + R3
    I2: R4 = R1 + R5   <- I2 membaca R1 yang ditulis I1
"""
from instruction import Dependency, no_write_between


def is_raw(inst1, inst2):
    """Cek pasangan: apakah inst2 membaca register yang ditulis inst1?"""
    return inst1.destination in inst2.sources


def detect_raw(instructions):
    deps = []
    for j, consumer in enumerate(instructions):
        for i in range(j):
            producer = instructions[i]
            reg = producer.destination
            if is_raw(producer, consumer) and no_write_between(instructions, i, j, reg):
                deps.append(Dependency(producer, consumer, "RAW", reg))
    return deps

if __name__ == "__main__":
    # Uji cepat modul RAW: python hazard_raw.py
    from instruction import Instruction as I
    contoh = [
        I("I1", "R1", ["R2", "R3"]),
        I("I2", "R4", ["R1", "R5"]),
        I("I3", "R6", ["R4", "R7"]),
    ]
    for d in detect_raw(contoh):
        print(d)


