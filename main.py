"""
main.py
Program utama simulasi WAW.  Jalankan:  python main.py
"""

from hazard_waw import (
    show_dependencies, detect_waw_violation, final_writer,
    register_renaming, sequential_execution, parallel_execution,
)
from programs import WAW_PROGRAM


def main():
    instructions = WAW_PROGRAM

    print("\n" + "*" * 60)
    print("   ILP SIMULATOR - IMPLEMENTASI WAW (Write After Write)")
    print("*" * 60)

    print("\nInstruction Set:")
    for ins in instructions:
        print(f"{ins.name}: {ins.destination} = {' + '.join(ins.sources)}")

    # 1. Dependency analysis
    show_dependencies(instructions, "DEPENDENCY ANALYSIS (RAW + WAW)")

    # 2. Hazard jika WAW diabaikan
    print("\n" + "=" * 55)
    print("DETEKSI HAZARD WAW (jika simulator hanya cek RAW)")
    print("=" * 55)
    for cyc, a, b, reg in detect_waw_violation(instructions):
        print(f"[HAZARD] Cycle {cyc}: {a} dan {b} sama-sama menulis {reg} "
              f"-> urutan penulisan tidak terjamin!")
    print("Penulis akhir yang benar:", final_writer(instructions))

    # 3. Eksekusi
    seq = sequential_execution(instructions)
    waw = parallel_execution(instructions,
                             "ILP EXECUTION - DENGAN PENANGANAN WAW (stall)", True)

    # 4. Register renaming
    renamed = register_renaming(instructions)
    print("\nSetelah Register Renaming:")
    for ins in renamed:
        print(f"{ins.name}: {ins.destination} = {' + '.join(ins.sources)}")
    show_dependencies(renamed, "DEPENDENCY ANALYSIS SETELAH RENAMING (WAW hilang)")
    ren = parallel_execution(renamed, "ILP EXECUTION - SETELAH REGISTER RENAMING", True)

    # 5. Perbandingan
    print("\n" + "=" * 55)
    print("PERFORMANCE COMPARISON")
    print("=" * 55)
    print(f"Sequential              : {seq} cycle")
    print(f"ILP + WAW stall         : {waw} cycle  (speedup {seq / waw:.2f}x)")
    print(f"ILP + Register Renaming : {ren} cycle  (speedup {seq / ren:.2f}x)")


if __name__ == "__main__":
    main()
