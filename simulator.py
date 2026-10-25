"""Eksekusi sekuensial, eksekusi paralel (ILP), dan register renaming."""
from instruction import Instruction
from dependency import find_dependencies


def sequential_execution(instructions, verbose=True):
    if verbose:
        print("\n" + "=" * 50)
        print("SEQUENTIAL EXECUTION")
        print("=" * 50)
        for cycle, inst in enumerate(instructions, start=1):
            print(f"Cycle {cycle}: Executing {inst}")
        print(f"\nTotal Sequential Cycles: {len(instructions)}")
    return len(instructions)


def schedule(instructions, kinds=("RAW", "WAR", "WAW")):
    """
    Penjadwalan ILP: sebuah instruksi boleh dieksekusi pada suatu cycle
    jika semua instruksi yang menjadi sumber dependensinya (sesuai `kinds`)
    sudah selesai pada cycle sebelumnya. Hasil: {nama_instruksi: cycle}.
    """
    deps = find_dependencies(instructions, kinds)
    cycle_of = {}
    for inst in instructions:
        preds = [d.producer.name for d in deps if d.consumer.name == inst.name]
        cycle_of[inst.name] = 1 + max((cycle_of[p] for p in preds), default=0)
    return cycle_of


def parallel_execution(instructions, kinds=("RAW", "WAR", "WAW"), verbose=True):
    cycle_of = schedule(instructions, kinds)
    total = max(cycle_of.values())
    if verbose:
        print("\n" + "=" * 50)
        print(f"INSTRUCTION-LEVEL PARALLEL EXECUTION (hazard: {', '.join(kinds)})")
        print("=" * 50)
        for c in range(1, total + 1):
            print(f"\nCycle {c}:")
            for inst in instructions:
                if cycle_of[inst.name] == c:
                    print(f"  -> {inst}")
        print(f"\nTotal ILP Cycles: {total}")
    return total


def rename_registers(instructions, prefix="P"):
    """
    Register renaming: setiap penulisan diberi register fisik baru (P1, P2, ...).
    Akibatnya WAR dan WAW hilang; hanya RAW (dependensi sejati) yang tersisa.
    """
    mapping, renamed, counter = {}, [], 0
    for inst in instructions:
        srcs = [mapping.get(r, r) for r in inst.sources]
        counter += 1
        new_dest = f"{prefix}{counter}"
        mapping[inst.destination] = new_dest
        renamed.append(Instruction(inst.name, new_dest, srcs))
    return renamed


def performance(instructions, kinds=("RAW", "WAR", "WAW")):
    seq = sequential_execution(instructions, verbose=False)
    par = parallel_execution(instructions, kinds, verbose=False)
    return {"sequential": seq, "ilp": par, "speedup": seq / par, "ipc": len(instructions) / par}


def print_performance(instructions, kinds=("RAW", "WAR", "WAW")):
    p = performance(instructions, kinds)
    print("\n" + "=" * 50)
    print("PERFORMANCE COMPARISON")
    print("=" * 50)
    print(f"Sequential Cycles : {p['sequential']}")
    print(f"ILP Cycles        : {p['ilp']}")
    print(f"Speedup           : {p['speedup']:.2f}x")
    print(f"Instr. per Cycle  : {p['ipc']:.2f}")
    return p
