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


# RAW murni: I2 <- I1 (R1), I4 <- I2 (R4) dan I3 (R6), I6 <- I4 (R9) dan I5 (R10)
RAW_PROGRAM = [
    Instruction("I1", "R1", ["R2", "R3"]),
    Instruction("I2", "R4", ["R1", "R5"]),     # RAW dengan I1 (R1)
    Instruction("I3", "R6", ["R7", "R8"]),
    Instruction("I4", "R9", ["R4", "R6"]),     # RAW dengan I2 (R4) dan I3 (R6)
    Instruction("I5", "R10", ["R11", "R12"]),
    Instruction("I6", "R13", ["R9", "R10"]),   # RAW dengan I4 (R9) dan I5 (R10)
]

# WAR: I2 menulis R2 yang dibaca I1; I4 menulis R8 yang dibaca I3. I6 membaca R2 dan R8 (RAW).
WAR_PROGRAM = [
    Instruction("I1", "R4", ["R2", "R3"]),
    Instruction("I2", "R2", ["R5", "R6"]),     # WAR dengan I1 (R2)
    Instruction("I3", "R7", ["R8", "R9"]),
    Instruction("I4", "R8", ["R10", "R11"]),   # WAR dengan I3 (R8)
    Instruction("I5", "R12", ["R13", "R14"]),
    Instruction("I6", "R15", ["R2", "R8"]),    # RAW dengan I2 (R2) dan I4 (R8)
]
