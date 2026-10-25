"""
Struktur data dasar simulator ILP.
Diadaptasi dari: https://github.com/harshitasingh4863/instruction-level-parallelism-simulator
"""
from dataclasses import dataclass


@dataclass
class Instruction:
    name: str          # nama instruksi, mis. "I1"
    destination: str   # register tujuan (ditulis)
    sources: list      # register sumber (dibaca)

    def __str__(self):
        return f"{self.name}: {self.destination} = {' + '.join(self.sources)}"


@dataclass
class Dependency:
    producer: Instruction   # instruksi yang lebih awal
    consumer: Instruction   # instruksi yang lebih akhir (harus menunggu)
    kind: str               # "RAW", "WAR", atau "WAW"
    register: str           # register penyebab dependensi

    def __str__(self):
        return (f"{self.consumer.name} bergantung pada {self.producer.name} "
                f"[{self.kind}] (Register: {self.register})")


def no_write_between(instructions, i, j, register):
    """
    True jika tidak ada instruksi di antara indeks i dan j yang menulis `register`.
    Dipakai agar dependensi hanya dicatat ke penulis/pembaca TERDEKAT;
    dependensi yang lebih jauh sudah tercakup secara transitif.
    """
    return all(instructions[k].destination != register for k in range(i + 1, j))
