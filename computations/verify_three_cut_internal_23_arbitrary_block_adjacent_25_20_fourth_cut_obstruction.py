#!/usr/bin/env python3
"""Exact fixed-interior theorem for arbitrary A_23 and A_25=E_00+tE_20.

The moving character is coupled: wt(t) = wt(x20) - wt(x00), so no
independent normalization of t exists and the fully nonzero stratum keeps
the invariant lambda = t*x00/x20.  Every quotient case below therefore
keeps t as an ordinary polynomial variable; a unit ideal over Q[t,...]
covers every complex t, including t=0 and every cross-ratio value, so no
separate inheritance of the t=0 theorem is required.

The 512 A_23 supports split into the 32-mask old five-cell locus (five
classes) and 480 outside masks (27 finite retained charts and one
Q[t,lam] chart on the x12+x21=x11+x22 circuit).  Each case kills the
coordinate blocks of its non-retained cells, making those coefficients
provably arbitrary, and tests the selected two-colour shared-star packet
against the parameter-independent expanded cylinder overspace; the
Q[t,lam] chart additionally uses exact pointwise lock functionals.  All
99 case/cut systems reduce to the unit ideal over characteristic zero.

The conclusion is local to the displayed fixed six-site interior.  It is
not a theorem for arbitrary A_25 and not the global Krenn conjecture.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import time

import derive_three_cut_internal_23_adjacent_25_coupled_quotient_systems as lib
import explore_three_cut_internal_23_full_supports as full
import verify_three_cut_internal_23_arbitrary_block_fourth_cut_obstruction as old_full
import verify_three_cut_internal_23_plane_support_fourth_cut_obstruction as old_locus


CELL = (2, 0)
CUTS = lib.CUTS

# name -> cut -> (active pair, locks, generators, sha256, normal dimension)
FROZEN = {
    "old_no_x00": {
        0: ((0, 2), False, 276, "3b1b9c377c29da60f4284b41b511d9dba8a1072b6de013f75e256765e3f3c0f7", 1),
        1: ((0, 2), False, 276, "3b1b9c377c29da60f4284b41b511d9dba8a1072b6de013f75e256765e3f3c0f7", 1),
        5: ((0, 2), False, 276, "3b1b9c377c29da60f4284b41b511d9dba8a1072b6de013f75e256765e3f3c0f7", 1),
    },
    "old_x00_no_x11_no_x21": {
        0: ((1, 2), False, 332, "650486191da24fc05cf150c9e038ecb2cc1cef1deb4ac99106d2e30c1febca7d", 1),
        1: ((1, 2), False, 332, "650486191da24fc05cf150c9e038ecb2cc1cef1deb4ac99106d2e30c1febca7d", 1),
        5: ((1, 2), False, 332, "650486191da24fc05cf150c9e038ecb2cc1cef1deb4ac99106d2e30c1febca7d", 1),
    },
    "old_x00_no_x11_with_x21": {
        0: ((1, 2), False, 444, "f0bdd11667381fc389b94e2e523453ae6b6c2f693929f3798f498aa7fbae4837", 2),
        1: ((1, 2), False, 444, "f0bdd11667381fc389b94e2e523453ae6b6c2f693929f3798f498aa7fbae4837", 2),
        5: ((1, 2), False, 444, "f0bdd11667381fc389b94e2e523453ae6b6c2f693929f3798f498aa7fbae4837", 2),
    },
    "old_x00_x11_no_x21": {
        0: ((1, 2), False, 452, "c0716fe7a69bb26850257a4030143e5e3b53e8a3273a93fc87a27853667d5bce", 3),
        1: ((1, 2), False, 452, "c0716fe7a69bb26850257a4030143e5e3b53e8a3273a93fc87a27853667d5bce", 3),
        5: ((1, 2), False, 452, "c0716fe7a69bb26850257a4030143e5e3b53e8a3273a93fc87a27853667d5bce", 3),
    },
    "old_x00_x11_with_x21": {
        0: ((1, 2), False, 452, "a27c1c7b9d8b96ff857102410222fd38c51427da9132cb5d3e714240d80b7906", 3),
        1: ((1, 2), False, 452, "a27c1c7b9d8b96ff857102410222fd38c51427da9132cb5d3e714240d80b7906", 3),
        5: ((1, 2), False, 452, "a27c1c7b9d8b96ff857102410222fd38c51427da9132cb5d3e714240d80b7906", 3),
    },
    "outside_x10_d0_b0": {
        0: ((1, 2), False, 336, "27389359df3f9fe32d435ec7adc47cc441908ce4110f5f0d9af5212c1203fcee", 3),
        1: ((1, 2), False, 336, "27389359df3f9fe32d435ec7adc47cc441908ce4110f5f0d9af5212c1203fcee", 3),
        5: ((1, 2), False, 336, "27389359df3f9fe32d435ec7adc47cc441908ce4110f5f0d9af5212c1203fcee", 3),
    },
    "outside_x10_d0_b1": {
        0: ((1, 2), False, 356, "82d54acc3d2a8cca2268a80711ab8682ac96b1af3602d3da71c444eaa6938b50", 3),
        1: ((1, 2), False, 356, "82d54acc3d2a8cca2268a80711ab8682ac96b1af3602d3da71c444eaa6938b50", 3),
        5: ((1, 2), False, 356, "82d54acc3d2a8cca2268a80711ab8682ac96b1af3602d3da71c444eaa6938b50", 3),
    },
    "outside_x10_d2_b0": {
        0: ((1, 2), False, 336, "e8b2eac4397ab4feb42068b5809cb5cea5627d978e9590f68ad6269c2ccc6bca", 3),
        1: ((1, 2), False, 336, "e8b2eac4397ab4feb42068b5809cb5cea5627d978e9590f68ad6269c2ccc6bca", 3),
        5: ((1, 2), False, 336, "e8b2eac4397ab4feb42068b5809cb5cea5627d978e9590f68ad6269c2ccc6bca", 3),
    },
    "outside_x10_d2_b1": {
        0: ((1, 2), False, 356, "bcd2c3ece703a622013c47c558b863259beaa51be71bf8b556ba530b0190c02f", 3),
        1: ((1, 2), False, 356, "bcd2c3ece703a622013c47c558b863259beaa51be71bf8b556ba530b0190c02f", 3),
        5: ((1, 2), False, 356, "bcd2c3ece703a622013c47c558b863259beaa51be71bf8b556ba530b0190c02f", 3),
    },
    "outside_x10_d4_b0": {
        0: ((1, 2), False, 352, "98997f248f895c9154eeae179d9e8cfb9dfdd772002b43e9134df63abb9b13a6", 3),
        1: ((1, 2), False, 352, "98997f248f895c9154eeae179d9e8cfb9dfdd772002b43e9134df63abb9b13a6", 3),
        5: ((1, 2), False, 352, "98997f248f895c9154eeae179d9e8cfb9dfdd772002b43e9134df63abb9b13a6", 3),
    },
    "outside_x10_d4_b1": {
        0: ((1, 2), False, 356, "ce69699cf0958ca6df1f304e25c820d5ad242a55bbe1c12544469c64fb43243f", 3),
        1: ((1, 2), False, 356, "ce69699cf0958ca6df1f304e25c820d5ad242a55bbe1c12544469c64fb43243f", 3),
        5: ((1, 2), False, 356, "ce69699cf0958ca6df1f304e25c820d5ad242a55bbe1c12544469c64fb43243f", 3),
    },
    "outside_x10_d6_b0": {
        0: ((1, 2), False, 352, "7bb2b38a6f476cf511c2a2c7ce4a9cef3afb31a83e8c89daa08ad56e187f14b7", 3),
        1: ((1, 2), False, 352, "7bb2b38a6f476cf511c2a2c7ce4a9cef3afb31a83e8c89daa08ad56e187f14b7", 3),
        5: ((1, 2), False, 352, "7bb2b38a6f476cf511c2a2c7ce4a9cef3afb31a83e8c89daa08ad56e187f14b7", 3),
    },
    "outside_x10_d6_b1": {
        0: ((1, 2), False, 356, "f68c732cd59bcee3f6a2fd03042a407a9fbd4520dce26fe87e63460cb53d7960", 3),
        1: ((1, 2), False, 356, "f68c732cd59bcee3f6a2fd03042a407a9fbd4520dce26fe87e63460cb53d7960", 3),
        5: ((1, 2), False, 356, "f68c732cd59bcee3f6a2fd03042a407a9fbd4520dce26fe87e63460cb53d7960", 3),
    },
    "outside_x12_crossratio": {
        0: ((1, 2), True, 1932, "a2c75e37a38f8e8a4fa8f13b415f9765cd33238cf0b2a82818b60006dea8dcd3", 3),
        1: ((1, 2), True, 1908, "517f6e06e938e3c874d8dfa2e98a0e4c36bbb6966865e94b54653559de12e030", 3),
        5: ((1, 2), True, 1976, "4b103ddb943cf924f27cd43426c7318d19faedc73a70ff1d75f56ab1bd33b71a", 5),
    },
    "outside_x12_d0_b0": {
        0: ((1, 2), False, 340, "c647842a2ededf78e751aae713beb8b9863bfc885bbce0253ff37d3225ad889d", 2),
        1: ((1, 2), False, 340, "c647842a2ededf78e751aae713beb8b9863bfc885bbce0253ff37d3225ad889d", 2),
        5: ((1, 2), False, 340, "c647842a2ededf78e751aae713beb8b9863bfc885bbce0253ff37d3225ad889d", 2),
    },
    "outside_x12_d0_b1": {
        0: ((1, 2), False, 376, "d2e9aae81e8c774ba09b057c6765f8e662bf20cde3f736ec4ff744edd00d8c79", 2),
        1: ((1, 2), False, 376, "d2e9aae81e8c774ba09b057c6765f8e662bf20cde3f736ec4ff744edd00d8c79", 2),
        5: ((1, 2), False, 376, "d2e9aae81e8c774ba09b057c6765f8e662bf20cde3f736ec4ff744edd00d8c79", 2),
    },
    "outside_x12_d2_b0": {
        0: ((1, 2), False, 356, "95a7e8944d234e2631d0952a5f2c86bfc67a4fb8b39f76882356a0a01a9f5692", 2),
        1: ((1, 2), False, 356, "95a7e8944d234e2631d0952a5f2c86bfc67a4fb8b39f76882356a0a01a9f5692", 2),
        5: ((1, 2), False, 356, "95a7e8944d234e2631d0952a5f2c86bfc67a4fb8b39f76882356a0a01a9f5692", 2),
    },
    "outside_x12_d2_b1": {
        0: ((1, 2), False, 376, "f23107841034f4265df00d9272b0af174d6c5696c4a6df9158ebcb2706a9a4a8", 2),
        1: ((1, 2), False, 376, "f23107841034f4265df00d9272b0af174d6c5696c4a6df9158ebcb2706a9a4a8", 2),
        5: ((1, 2), False, 376, "f23107841034f4265df00d9272b0af174d6c5696c4a6df9158ebcb2706a9a4a8", 2),
    },
    "outside_x12_d4_b0": {
        0: ((1, 2), False, 356, "0071236f7f41d870751dd8e3bcf360c68d2b0e6e9837e4703799488136265476", 2),
        1: ((1, 2), False, 356, "0071236f7f41d870751dd8e3bcf360c68d2b0e6e9837e4703799488136265476", 2),
        5: ((1, 2), False, 356, "0071236f7f41d870751dd8e3bcf360c68d2b0e6e9837e4703799488136265476", 2),
    },
    "outside_x12_d4_b1": {
        0: ((1, 2), False, 376, "2e4975e33ed90527e452b78b4e834e297b512396c65f19b9c39ca7fd1cc86723", 2),
        1: ((1, 2), False, 376, "2e4975e33ed90527e452b78b4e834e297b512396c65f19b9c39ca7fd1cc86723", 2),
        5: ((1, 2), False, 376, "2e4975e33ed90527e452b78b4e834e297b512396c65f19b9c39ca7fd1cc86723", 2),
    },
    "outside_x12_d6_b0": {
        0: ((1, 2), False, 372, "52aab3c0b1584e6db09489cb760bc2613649efbd5c77d4360d06b0bdf52d3d69", 2),
        1: ((1, 2), False, 372, "52aab3c0b1584e6db09489cb760bc2613649efbd5c77d4360d06b0bdf52d3d69", 2),
        5: ((1, 2), False, 372, "52aab3c0b1584e6db09489cb760bc2613649efbd5c77d4360d06b0bdf52d3d69", 2),
    },
    "outside_x20_d0_b0": {
        0: ((1, 2), False, 372, "e34cdaa50d6cf041f963ede1f155bdca53c7d8f5c5ec59455edbce93c9216dc3", 3),
        1: ((1, 2), False, 372, "e34cdaa50d6cf041f963ede1f155bdca53c7d8f5c5ec59455edbce93c9216dc3", 3),
        5: ((1, 2), False, 372, "e34cdaa50d6cf041f963ede1f155bdca53c7d8f5c5ec59455edbce93c9216dc3", 3),
    },
    "outside_x20_d0_b1": {
        0: ((1, 2), False, 372, "d3096cc6622db5ec8998711fee12173de86e606f672d63f3082f7f8c2bb0779e", 3),
        1: ((1, 2), False, 372, "d3096cc6622db5ec8998711fee12173de86e606f672d63f3082f7f8c2bb0779e", 3),
        5: ((1, 2), False, 372, "d3096cc6622db5ec8998711fee12173de86e606f672d63f3082f7f8c2bb0779e", 3),
    },
    "outside_x20_d2_b0": {
        0: ((1, 2), False, 372, "e7a6a6ac10ce868ce704ba04a7bb967c60cafab78324d6baa6b9058881190caf", 3),
        1: ((1, 2), False, 372, "e7a6a6ac10ce868ce704ba04a7bb967c60cafab78324d6baa6b9058881190caf", 3),
        5: ((1, 2), False, 372, "e7a6a6ac10ce868ce704ba04a7bb967c60cafab78324d6baa6b9058881190caf", 3),
    },
    "outside_x20_d2_b1": {
        0: ((1, 2), False, 372, "aa55bc3fdb32105efd0abe5b37fe703db5f1b6ebb066cbcae055e641278c8089", 3),
        1: ((1, 2), False, 372, "aa55bc3fdb32105efd0abe5b37fe703db5f1b6ebb066cbcae055e641278c8089", 3),
        5: ((1, 2), False, 372, "aa55bc3fdb32105efd0abe5b37fe703db5f1b6ebb066cbcae055e641278c8089", 3),
    },
    "outside_x20_d4_b0": {
        0: ((1, 2), False, 372, "08478c38f44bbae3b2a782601607579ba6b79f9883026d6bbb81d9515c3cc842", 3),
        1: ((1, 2), False, 372, "08478c38f44bbae3b2a782601607579ba6b79f9883026d6bbb81d9515c3cc842", 3),
        5: ((1, 2), False, 372, "08478c38f44bbae3b2a782601607579ba6b79f9883026d6bbb81d9515c3cc842", 3),
    },
    "outside_x20_d4_b1": {
        0: ((1, 2), False, 372, "a4a597fe53f11fee32778fde7821282475eedbebbfdb3f906e9999dd7c75c8f9", 3),
        1: ((1, 2), False, 372, "a4a597fe53f11fee32778fde7821282475eedbebbfdb3f906e9999dd7c75c8f9", 3),
        5: ((1, 2), False, 372, "a4a597fe53f11fee32778fde7821282475eedbebbfdb3f906e9999dd7c75c8f9", 3),
    },
    "outside_x20_d6_b0": {
        0: ((1, 2), False, 372, "5d953642c13467b4cfbacf3bd31d5eb9883c62368c929ba96dd2e2d4179a8eee", 3),
        1: ((1, 2), False, 372, "5d953642c13467b4cfbacf3bd31d5eb9883c62368c929ba96dd2e2d4179a8eee", 3),
        5: ((1, 2), False, 372, "5d953642c13467b4cfbacf3bd31d5eb9883c62368c929ba96dd2e2d4179a8eee", 3),
    },
    "outside_x20_d6_b1": {
        0: ((1, 2), False, 372, "922e0dd645b73f11948d7b033455e95f0d99b63bc1872ffaaf744c056b5189af", 3),
        1: ((1, 2), False, 372, "922e0dd645b73f11948d7b033455e95f0d99b63bc1872ffaaf744c056b5189af", 3),
        5: ((1, 2), False, 372, "922e0dd645b73f11948d7b033455e95f0d99b63bc1872ffaaf744c056b5189af", 3),
    },
    "outside_x22_d4_b0": {
        0: ((1, 2), False, 392, "6eeced8b29f1a7c3452f792fb699284ad937f26e7c58c205c8b1f620967d1b4a", 3),
        1: ((1, 2), False, 392, "6eeced8b29f1a7c3452f792fb699284ad937f26e7c58c205c8b1f620967d1b4a", 3),
        5: ((1, 2), False, 396, "cdb91267d09a9af57bc35371aa8172da5acf4fb12b8fd64ef16fd421bbf32496", 2),
    },
    "outside_x22_d4_b1": {
        0: ((1, 2), False, 412, "d517a1cabce9855f781767f50f38b4fbbf60b2ad6f28675b21764e666c66ea61", 3),
        1: ((1, 2), False, 412, "d517a1cabce9855f781767f50f38b4fbbf60b2ad6f28675b21764e666c66ea61", 3),
        5: ((1, 2), False, 416, "522d285ad1823312f917e29c78b7c63fa5b3b241a7e1d6be9d4a74406ad67988", 2),
    },
    "outside_x22_d6_b0": {
        0: ((1, 2), False, 416, "c7a1e6f1ddf86e290efc4daaae2a43e825747aa66542a7acdf903df26eaca8e2", 3),
        1: ((1, 2), False, 416, "c7a1e6f1ddf86e290efc4daaae2a43e825747aa66542a7acdf903df26eaca8e2", 3),
        5: ((1, 2), False, 420, "f08e7d97fc7f28ff08463d2da963b08afb8daeee36ce97ac1b31969589e053fd", 2),
    },
    "outside_x22_d6_b1": {
        0: ((1, 2), False, 420, "a5225dbf3f626a88185976d171fb511787f6c6b086bac590f190d677e20df0e3", 3),
        1: ((1, 2), False, 420, "a5225dbf3f626a88185976d171fb511787f6c6b086bac590f190d677e20df0e3", 3),
        5: ((1, 2), False, 424, "0e5f738f5fb2601e3fb6ad56b43a196d07a463a36e6d2479e532dc544d74ac36", 2),
    },
}

EXPECTED_LEDGER_SHA256 = (
    "c3adc733e5ae2003f8b5a79987edc97106fb27524f817fca04443ab34ee7335e"
)


def ledger_hash():
    rows = []
    for name in sorted(FROZEN):
        for cut in sorted(FROZEN[name]):
            rows.append((name, cut) + tuple(FROZEN[name][cut]))
    return hashlib.sha256("\n".join(map(repr, rows)).encode()).hexdigest()


def audit_partition_census():
    """Every A_23 support mask reaches exactly one case family."""
    outside_order = (3, 5, 6, 8)
    family_for_outside = dict(zip(outside_order, ("x10", "x12", "x20", "x22")))
    census = {}
    for mask in range(1 << 9):
        present = [bit for bit in outside_order if mask & (1 << bit)]
        if present:
            name = family_for_outside[present[0]]
            spec = old_full.FAMILIES[name]
            pattern = (2 if mask & (1 << 4) else 0) + (
                4 if mask & (1 << 8) and spec["outside"] != 8 else 0
            )
            if name == "x22":
                pattern |= 4
            x21 = 1 if mask & (1 << 7) else 0
            if name == "x12" and pattern == 6 and x21:
                case = "outside_x12_crossratio"
            else:
                case = f"outside_{name}_d{pattern}_b{x21}"
        else:
            local_mask = 0
            for local, bit in enumerate(lib.LOCAL_TO_FULL):
                if mask & (1 << bit):
                    local_mask |= 1 << local
            assert sum(
                1 for bit in range(9) if mask & (1 << bit)
            ) == local_mask.bit_count()
            case = "old_" + old_locus.class_name(local_mask)
        census[case] = census.get(case, 0) + 1
    assert sum(census.values()) == 512
    assert sum(v for k, v in census.items() if k.startswith("old_")) == 32
    assert sum(v for k, v in census.items() if k.startswith("outside_")) == 480
    for case in census:
        assert case in FROZEN, case
    assert set(census) == set(FROZEN)
    return census


def check_case(case):
    case.prepare()
    if case.name.startswith("outside_"):
        lib.audit_outside_killed_arbitrary(case)
    else:
        spec = {
            "old_" + record[0]: record for record in old_locus.CLASS_SPECS
        }[case.name]
        lib.audit_old_members(case, spec[1], spec[2])
    jobs = []
    for cut in CUTS:
        active, locks, generators, sha256, normal_dim = FROZEN[case.name][cut]
        assert len(case.normals[cut]) == normal_dim, (case.name, cut)
        assert tuple(active) in case.admissible_pairs(cut), (case.name, cut)
        program, generator_count = case.system(cut, tuple(active), locks)
        assert generator_count == generators, (
            case.name, cut, generator_count,
        )
        digest = hashlib.sha256(program.encode()).hexdigest()
        assert digest == sha256, (case.name, cut, digest)
        jobs.append((case.name, cut, program, digest))
    return jobs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--timeout", type=int, default=3600)
    parser.add_argument("--skip-singular", action="store_true")
    args = parser.parse_args()

    started = time.monotonic()
    assert ledger_hash() == EXPECTED_LEDGER_SHA256, ledger_hash()
    lib.select_direction(CELL)
    lib.audit_direction_geometry(CELL)
    lib.audit_coupled_stabilizer(CELL)
    lib.audit_literal_boundary_identity()
    old_full.audit_support_partition_and_torus()
    old_locus.audit_torus_and_discrete_symmetry()
    census = audit_partition_census()
    print("GEOMETRY", "pass=1", f"cases={len(census)}", flush=True)

    cases = lib.outside_cases() + lib.old_cases()
    assert {case.name for case in cases} == set(FROZEN)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        job_lists = list(executor.map(check_case, cases))
    jobs = [job for jobs in job_lists for job in jobs]
    assert len(jobs) == 99
    templates = {}
    for _name, _cut, program, digest in jobs:
        templates.setdefault(digest, program)
    print(
        "SYSTEMS", f"jobs={len(jobs)}", f"unique={len(templates)}", flush=True,
    )
    if args.skip_singular:
        return

    exact_started = time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = dict(zip(
            templates,
            executor.map(
                lambda program: lib.run_program(program, args.timeout),
                templates.values(),
            ),
        ))
    for digest, (unit, size, _elapsed) in results.items():
        assert (unit, size) == (1, 1), (digest, unit, size)
    exact_wall = time.monotonic() - exact_started

    print("A23 arbitrary plus A25=E00+tE20 local fourth-cut obstruction: PASS")
    print("coupled character wt(t)=wt(x20)-wt(x00); t kept symbolic: PASS")
    print("512 masks partitioned 32+480; five classes, 27+1 outside charts: PASS")
    print("99 case/cut systems, all exact characteristic-zero units: PASS")
    print("every unit ideal is over Q[t(,lam)]: covers all complex t: PASS")
    print("endpoint order, shared stars, ordered fibres, arbitrary A67: PASS")
    print(f"ledger SHA256: {ledger_hash()}")
    print(f"unique Singular programs: {len(templates)}")
    print(f"maximum Singular time: {max(r[2] for r in results.values()):.3f}s")
    print(f"parallel Singular wall time: {exact_wall:.3f}s")
    print(f"total wall time: {time.monotonic() - started:.3f}s")


if __name__ == "__main__":
    main()
