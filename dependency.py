"""
Penggabung deteksi hazard: RAW, WAR, dan WAW.
Dipakai oleh simulator.py melalui find_dependencies(instructions, kinds).
"""
from hazard_raw import detect_raw
from hazard_war import detect_war


def find_dependencies(instructions, kinds=("RAW", "WAR", "WAW")):
    """Kumpulkan semua dependensi dari jenis `kinds`, urut menurut instruksi consumer."""
    deps = []
    if "RAW" in kinds:
        deps += detect_raw(instructions)
    if "WAR" in kinds:
        deps += detect_war(instructions)
    if "WAW" in kinds:
        # import di sini supaya repo tetap bisa dipakai sebelum hazard_waw.py ditambahkan
        try:
            from hazard_waw import detect_waw
        except ImportError as e:
            raise ImportError("hazard_waw.py (detect_waw) belum ada di repo") from e
        deps += detect_waw(instructions)
    order = {inst.name: n for n, inst in enumerate(instructions)}
    deps.sort(key=lambda d: (order[d.consumer.name], order[d.producer.name]))
    return deps
