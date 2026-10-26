"""
hazard_waw.py
Deteksi dan penanganan WAW (Write After Write) pada simulator ILP.

WAW (output dependence): dua instruksi menulis ke register yang SAMA.
  I(i): Rx = ...
  I(j): Rx = ...   (j > i)  -> I(j) tidak boleh selesai menulis lebih dulu dari I(i).
WAW termasuk name dependence, sehingga dapat dihilangkan dengan register renaming.
"""

# Instruction dipakai bersama modul lain (RAW, WAR) lewat instruction.py
from instruction import Instruction, Dependency, no_write_between


# ---------------------------------------------------------------- deteksi
def has_raw(i1, i2):
    """RAW: i2 membaca register yang ditulis i1."""
    return i1.destination in i2.sources


def has_waw(i1, i2):
    """WAW: i1 dan i2 menulis ke register yang sama."""
    return i1.destination == i2.destination


def dependency_type(i1, i2, use_waw=True):
    """Jenis dependensi i2 terhadap i1 (i1 lebih dulu)."""
    result = []
    if has_raw(i1, i2):
        result.append("RAW")
    if use_waw and has_waw(i1, i2):
        result.append("WAW")
    return result


def get_dependencies(instrs, use_waw=True):
    """List (dari, ke, jenis, register). Dipakai untuk dependency graph."""
    edges = []
    for a in range(len(instrs)):
        for b in range(a + 1, len(instrs)):
            for t in dependency_type(instrs[a], instrs[b], use_waw):
                if t == "RAW":
                    # RAW sejati hanya ke penulis TERAKHIR sebelum pembaca
                    overwritten = any(
                        instrs[m].destination == instrs[a].destination
                        for m in range(a + 1, b)
                    )
                    if overwritten:
                        continue
                edges.append((instrs[a].name, instrs[b].name, t, instrs[a].destination))
    return edges


def detect_waw(instructions):
    """Deteksi WAW untuk dependency.py: kembalikan list Dependency.
    Instruksi j menulis register yang sama dengan instruksi i (i < j).
    Hanya dicatat ke penulis TERDEKAT (yang lebih jauh tercakup transitif)."""
    deps = []
    for j, later in enumerate(instructions):
        reg = later.destination
        for i in range(j):
            earlier = instructions[i]
            if has_waw(earlier, later) and no_write_between(instructions, i, j, reg):
                deps.append(Dependency(earlier, later, "WAW", reg))
    return deps


def show_dependencies(instrs, title, use_waw=True):
    print("\n" + "=" * 55)
    print(title)
    print("=" * 55)
    edges = get_dependencies(instrs, use_waw)
    if not edges:
        print("Tidak ada dependensi.")
    for src, dst, t, reg in edges:
        print(f"{dst} bergantung pada {src}  [{t}]  (register {reg})")
    return edges


def detect_waw_violation(instrs):
    """Simulasi jika simulator HANYA mengecek RAW: cari dua penulis register
    yang sama di cycle yang sama (urutan tulis tidak terjamin = hazard)."""
    completed, remaining, cycle, violations = set(), instrs.copy(), 0, []
    while remaining:
        cycle += 1
        this_cycle = []
        for ins in remaining:
            ok = True
            for prev in instrs:
                if prev.name == ins.name:
                    break
                if has_raw(prev, ins) and prev.name not in completed:
                    ok = False
                    break
            if ok:
                this_cycle.append(ins)
        for a in range(len(this_cycle)):
            for b in range(a + 1, len(this_cycle)):
                if has_waw(this_cycle[a], this_cycle[b]):
                    violations.append((cycle, this_cycle[a].name,
                                       this_cycle[b].name, this_cycle[a].destination))
        for ins in this_cycle:
            completed.add(ins.name)
            remaining.remove(ins)
    return violations


def final_writer(instrs):
    """Instruksi yang seharusnya menentukan nilai akhir tiap register."""
    last = {}
    for ins in instrs:
        last[ins.destination] = ins.name
    return last


# ------------------------------------------------------- register renaming
def register_renaming(instrs):
    """Beri nama baru tiap penulisan (R1 -> R1_1, R1_2, ...). WAW hilang."""
    counter, mapping, renamed = {}, {}, []
    for ins in instrs:
        new_src = [mapping.get(s, s) for s in ins.sources]
        counter[ins.destination] = counter.get(ins.destination, 0) + 1
        new_dst = f"{ins.destination}_{counter[ins.destination]}"
        mapping[ins.destination] = new_dst
        renamed.append(Instruction(ins.name, new_dst, new_src))
    return renamed


# --------------------------------------------------------------- eksekusi
def sequential_execution(instrs):
    print("\n" + "=" * 55)
    print("SEQUENTIAL EXECUTION")
    print("=" * 55)
    cycle = 0
    for ins in instrs:
        cycle += 1
        print(f"Cycle {cycle}: {ins.name} ({ins.destination} = {' + '.join(ins.sources)})")
    print(f"\nTotal Sequential Cycles: {cycle}")
    return cycle


def parallel_execution(instrs, title, use_waw=True):
    """ILP: instruksi jalan paralel bila dependensinya (RAW + WAW) sudah selesai."""
    print("\n" + "=" * 55)
    print(title)
    print("=" * 55)
    completed, remaining, cycle = set(), instrs.copy(), 0
    while remaining:
        cycle += 1
        this_cycle = []
        for ins in remaining:
            ok = True
            for prev in instrs:
                if prev.name == ins.name:
                    break
                if dependency_type(prev, ins, use_waw) and prev.name not in completed:
                    ok = False
                    break
            if ok:
                this_cycle.append(ins)
        print(f"\nCycle {cycle}:")
        for ins in this_cycle:
            print(f"  -> {ins.name}: {ins.destination} = {' + '.join(ins.sources)}")
        for ins in this_cycle:
            completed.add(ins.name)
            remaining.remove(ins)
    print(f"\nTotal Cycles: {cycle}")
    return cycle
