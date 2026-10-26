"""
simulasi_semua.py
Menjalankan simulator ILP untuk ketiga hazard (RAW, WAR, WAW) memakai program
uji di programs.py, lalu menyimpan hasilnya ke hasil_simulasi_semua.txt dan
membuat dependency graph RAW dan WAR (graph_raw.png, graph_war.png,
graph_war_renaming.png) dengan graph.py.

Jalankan:  python simulasi_semua.py
"""
import contextlib
import io

from dependency import find_dependencies
from simulator import (sequential_execution, parallel_execution,
                       print_performance, rename_registers)
from graph import draw_dependency_graph
from programs import RAW_PROGRAM, WAR_PROGRAM, WAW_PROGRAM

# (label, program, hazard yang diperiksa)
SKENARIO = [
    ("RAW", RAW_PROGRAM, ("RAW",)),
    ("WAR", WAR_PROGRAM, ("RAW", "WAR")),
    ("WAW", WAW_PROGRAM, ("RAW", "WAW")),
]


def jalankan(label, program, kinds):
    print("#" * 60)
    print(f"# HASIL SIMULASI {label}")
    print("#" * 60)
    print("\nInstruction Set:")
    for inst in program:
        print(inst)

    print("\nDependency:")
    for d in find_dependencies(program, kinds):
        print(d)

    sequential_execution(program)
    parallel_execution(program, kinds)
    print_performance(program, kinds)

    # register renaming: WAR dan WAW hilang, hanya RAW yang tersisa
    renamed = rename_registers(program)
    print("\n--- Setelah register renaming ---")
    for inst in renamed:
        print(inst)
    parallel_execution(renamed, ("RAW",))
    print_performance(renamed, ("RAW",))
    print("\n")
    return renamed


def buat_graph():
    draw_dependency_graph(RAW_PROGRAM, find_dependencies(RAW_PROGRAM, ("RAW",)),
                          "graph_raw.png", "RAW Dependency Graph")
    draw_dependency_graph(WAR_PROGRAM, find_dependencies(WAR_PROGRAM, ("RAW", "WAR")),
                          "graph_war.png", "WAR Dependency Graph")
    war_renamed = rename_registers(WAR_PROGRAM)
    draw_dependency_graph(war_renamed, find_dependencies(war_renamed, ("RAW",)),
                          "graph_war_renaming.png",
                          "WAR Dependency Graph setelah Register Renaming")


if __name__ == "__main__":
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        for label, program, kinds in SKENARIO:
            jalankan(label, program, kinds)
    hasil = buffer.getvalue()
    print(hasil)
    with open("hasil_simulasi_semua.txt", "w") as f:
        f.write(hasil)
    buat_graph()
    print("Selesai: hasil_simulasi_semua.txt, graph_raw.png, graph_war.png, graph_war_renaming.png")
