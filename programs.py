"""
programs.py
Program contoh (kumpulan instruksi) untuk menguji WAW.
Sengaja tidak memuat WAR agar yang dianalisis murni WAW.
"""

from hazard_waw import Instruction

# WAW pada R1 (I1 -> I3) dan R4 (I2 -> I5). I6 membaca R1 dan R4 (RAW).
WAW_PROGRAM = [
    Instruction("I1", "R1", ["R2", "R3"]),
    Instruction("I2", "R4", ["R5", "R6"]),
    Instruction("I3", "R1", ["R7", "R8"]),     # WAW dengan I1 (R1)
    Instruction("I4", "R9", ["R10", "R11"]),
    Instruction("I5", "R4", ["R12", "R13"]),   # WAW dengan I2 (R4)
    Instruction("I6", "R14", ["R1", "R4"]),    # RAW ke I3 dan I5
]
