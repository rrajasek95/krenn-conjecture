#!/usr/bin/env python3
"""Exact fixed-interior theorem for arbitrary A_23 and A_25=E_00+tE_10.

The moving character is coupled: wt(t) = wt(x10) - wt(x00), so no
independent normalization of t exists and the fully nonzero stratum keeps
the invariant lambda = t*x00/x10.  Every quotient case below therefore
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


CELL = (1, 0)
CUTS = lib.CUTS

# name -> cut -> (active pair, locks, generators, sha256, normal dimension)
FROZEN = {
    "old_no_x00": {
        0: ((0, 2), False, 260, "64975ec460f64dc73f0b4affc7d009014b10f410915b1980d6bebd2b3a856c68", 2),
        1: ((0, 2), False, 260, "64975ec460f64dc73f0b4affc7d009014b10f410915b1980d6bebd2b3a856c68", 2),
        5: ((0, 2), False, 260, "64975ec460f64dc73f0b4affc7d009014b10f410915b1980d6bebd2b3a856c68", 2),
    },
    "old_x00_no_x11_no_x21": {
        0: ((1, 2), False, 316, "7220172ee88343e5d848e83aa9bb1aacf46b34bdd34826a23c50b3da470e9716", 2),
        1: ((1, 2), False, 316, "7220172ee88343e5d848e83aa9bb1aacf46b34bdd34826a23c50b3da470e9716", 2),
        5: ((1, 2), False, 316, "7220172ee88343e5d848e83aa9bb1aacf46b34bdd34826a23c50b3da470e9716", 2),
    },
    "old_x00_no_x11_with_x21": {
        0: ((1, 2), False, 440, "bafb813cbff9e186b1ffd390fa9c641517e2b93675ea693716ae512ce81fa494", 3),
        1: ((1, 2), False, 440, "bafb813cbff9e186b1ffd390fa9c641517e2b93675ea693716ae512ce81fa494", 3),
        5: ((1, 2), False, 444, "df6b75f7e51fb423b1becbc9ac2641352b147e6013b2c313c65d61f9dd8541b9", 2),
    },
    "old_x00_x11_no_x21": {
        0: ((1, 2), False, 428, "19e363dbcccf1e3bed7bd0a24a08294d04414cebb8fba533c36aa164028e608f", 3),
        1: ((1, 2), False, 428, "19e363dbcccf1e3bed7bd0a24a08294d04414cebb8fba533c36aa164028e608f", 3),
        5: ((1, 2), False, 432, "b3dfde2fd9bca93d1ea9610d9740c47415f671e4b4be2f5cdb80ce6e4402fbfe", 2),
    },
    "old_x00_x11_with_x21": {
        0: ((1, 2), False, 440, "da871f8a7125d9f15d2f04b230f3faae5f6436e805fbd17fa7831903ab17d496", 3),
        1: ((1, 2), False, 440, "da871f8a7125d9f15d2f04b230f3faae5f6436e805fbd17fa7831903ab17d496", 3),
        5: ((1, 2), False, 444, "1e9083dd342156d97c38199295c32022c748988370749d87d02fe4661c2c6fe8", 2),
    },
    "outside_x10_d0_b0": {
        0: ((1, 2), False, 300, "c21d4a1896a6e6704787bff7135ba800d0014cf0afd88db71c7148559c160009", 2),
        1: ((1, 2), False, 300, "c21d4a1896a6e6704787bff7135ba800d0014cf0afd88db71c7148559c160009", 2),
        5: ((1, 2), False, 300, "c21d4a1896a6e6704787bff7135ba800d0014cf0afd88db71c7148559c160009", 2),
    },
    "outside_x10_d0_b1": {
        0: ((1, 2), False, 332, "2fc8b79c540ed6b4f651f8be2fe3ba1d6ecca95fae7d3655f1f33de41d01cbc6", 2),
        1: ((1, 2), False, 332, "2fc8b79c540ed6b4f651f8be2fe3ba1d6ecca95fae7d3655f1f33de41d01cbc6", 2),
        5: ((1, 2), False, 332, "2fc8b79c540ed6b4f651f8be2fe3ba1d6ecca95fae7d3655f1f33de41d01cbc6", 2),
    },
    "outside_x10_d2_b0": {
        0: ((1, 2), False, 300, "268eb63799e4350fe2809f31eaada9a2999814bb553588e3e428d021fb23f522", 2),
        1: ((1, 2), False, 300, "268eb63799e4350fe2809f31eaada9a2999814bb553588e3e428d021fb23f522", 2),
        5: ((1, 2), False, 300, "268eb63799e4350fe2809f31eaada9a2999814bb553588e3e428d021fb23f522", 2),
    },
    "outside_x10_d2_b1": {
        0: ((1, 2), False, 332, "aa5340b940c33c227691d49fc67749a574d3b7fc34a7cb10aa5bde183e9054bf", 2),
        1: ((1, 2), False, 332, "aa5340b940c33c227691d49fc67749a574d3b7fc34a7cb10aa5bde183e9054bf", 2),
        5: ((1, 2), False, 332, "aa5340b940c33c227691d49fc67749a574d3b7fc34a7cb10aa5bde183e9054bf", 2),
    },
    "outside_x10_d4_b0": {
        0: ((1, 2), False, 356, "e72b5626530e63037ffa7a241ab11a686f03483fd295cd9159fdbf88e0985557", 2),
        1: ((1, 2), False, 356, "e72b5626530e63037ffa7a241ab11a686f03483fd295cd9159fdbf88e0985557", 2),
        5: ((1, 2), False, 356, "e72b5626530e63037ffa7a241ab11a686f03483fd295cd9159fdbf88e0985557", 2),
    },
    "outside_x10_d4_b1": {
        0: ((1, 2), False, 360, "6fb93e8714a6dd34730cf1eb4c7692ba35bbf4b820d9b75e21c87228179dce07", 2),
        1: ((1, 2), False, 360, "6fb93e8714a6dd34730cf1eb4c7692ba35bbf4b820d9b75e21c87228179dce07", 2),
        5: ((1, 2), False, 360, "6fb93e8714a6dd34730cf1eb4c7692ba35bbf4b820d9b75e21c87228179dce07", 2),
    },
    "outside_x10_d6_b0": {
        0: ((1, 2), False, 356, "1ead2d2e2d5bc9dab40b3afad7715014fb17b48387e571bf89b18913daef549f", 2),
        1: ((1, 2), False, 356, "1ead2d2e2d5bc9dab40b3afad7715014fb17b48387e571bf89b18913daef549f", 2),
        5: ((1, 2), False, 356, "1ead2d2e2d5bc9dab40b3afad7715014fb17b48387e571bf89b18913daef549f", 2),
    },
    "outside_x10_d6_b1": {
        0: ((1, 2), False, 360, "233e92e32ae882a0ec7aa8b713a92f764fa5b5cbc592eb1db929de3b1cd3e0f9", 2),
        1: ((1, 2), False, 360, "233e92e32ae882a0ec7aa8b713a92f764fa5b5cbc592eb1db929de3b1cd3e0f9", 2),
        5: ((1, 2), False, 360, "233e92e32ae882a0ec7aa8b713a92f764fa5b5cbc592eb1db929de3b1cd3e0f9", 2),
    },
    "outside_x12_crossratio": {
        0: ((1, 2), True, 1876, "d5d4f6d7f19915c35c09a983e9bf6bf846c060563329b8fdba9e147756aaeeef", 4),
        1: ((1, 2), True, 1868, "01551eab45cc93d6fa9f13f2a43901666b8383cb827bf86ed531647f785bdea0", 4),
        5: ((1, 2), True, 1964, "786b9f708eb504d10544e12940e5a1119c3add1f09a269ca62d126f0673da60c", 3),
    },
    "outside_x12_d0_b0": {
        0: ((1, 2), False, 296, "8103ebd06e2c20c07ced1d421fba6e6f7d62fc7f304d8172363ea2aaa5e9c47d", 3),
        1: ((1, 2), False, 296, "8103ebd06e2c20c07ced1d421fba6e6f7d62fc7f304d8172363ea2aaa5e9c47d", 3),
        5: ((1, 2), False, 300, "6fd09f6d5a155a0389cff7e9fe0caea666a7be408d339bbb026c567fc75c9b2e", 2),
    },
    "outside_x12_d0_b1": {
        0: ((1, 2), False, 344, "7f4d815396c46c26b77cf8d3a3fa369878e526df90f26f7283e8324b7acff3f6", 3),
        1: ((1, 2), False, 344, "7f4d815396c46c26b77cf8d3a3fa369878e526df90f26f7283e8324b7acff3f6", 3),
        5: ((1, 2), False, 348, "a668b369cf66372c86239cf0c98f370ceca3d34039a257fd87d5c3cf239d05b3", 2),
    },
    "outside_x12_d2_b0": {
        0: ((1, 2), False, 312, "a2ea8b0843645ebc426403753ef7c8e4fabb94e903fd13479e67fc83e30815fb", 3),
        1: ((1, 2), False, 312, "a2ea8b0843645ebc426403753ef7c8e4fabb94e903fd13479e67fc83e30815fb", 3),
        5: ((1, 2), False, 316, "1b9f9f92700300d986996e377c4c708e1a3eb3c9992a77b3d3807a4326909a9a", 2),
    },
    "outside_x12_d2_b1": {
        0: ((1, 2), False, 344, "677a32accdeff9eea6dc0d5df10098be8396b454c3b5085370ae300bc975a9ea", 3),
        1: ((1, 2), False, 344, "677a32accdeff9eea6dc0d5df10098be8396b454c3b5085370ae300bc975a9ea", 3),
        5: ((1, 2), False, 348, "18da1ed21852bcb538c5d59708b0e7fc4e8dbdfa9714c67cc7be868b2aba4d68", 2),
    },
    "outside_x12_d4_b0": {
        0: ((1, 2), False, 352, "5dff711c55f295fc36aacb712dd8f25bd354a01c7357b8d1b4f4efe168d97794", 3),
        1: ((1, 2), False, 352, "5dff711c55f295fc36aacb712dd8f25bd354a01c7357b8d1b4f4efe168d97794", 3),
        5: ((1, 2), False, 356, "9dfba964b4e89898f6b7f2a311b81ccff67d8f793b7dc962c33b0f5c3e2b2128", 2),
    },
    "outside_x12_d4_b1": {
        0: ((1, 2), False, 372, "5b1a0e70f1046111b8f1a931bf663e7eb3f3393505a7f1a39eaf21eb126c3da1", 3),
        1: ((1, 2), False, 372, "5b1a0e70f1046111b8f1a931bf663e7eb3f3393505a7f1a39eaf21eb126c3da1", 3),
        5: ((1, 2), False, 376, "29fee33b00908f4c90a49063aed6c037fd2ddb89e06590eda51908dd5447f90d", 2),
    },
    "outside_x12_d6_b0": {
        0: ((1, 2), False, 368, "6815ffe559be6591e105eb7dd879907c2f1141acd0f4d47d73379e73d7dd6c8a", 3),
        1: ((1, 2), False, 368, "6815ffe559be6591e105eb7dd879907c2f1141acd0f4d47d73379e73d7dd6c8a", 3),
        5: ((1, 2), False, 372, "44faf77530d1ef6b1a169cea84b53eb880869774cf5b2f6d0268275552197c53", 2),
    },
    "outside_x20_d0_b0": {
        0: ((1, 2), False, 356, "779b8f9e5f14a7f4e2291503c0d2fc2ea6b9c8eec9bd4a02c6ec99ab97e315e9", 2),
        1: ((1, 2), False, 356, "779b8f9e5f14a7f4e2291503c0d2fc2ea6b9c8eec9bd4a02c6ec99ab97e315e9", 2),
        5: ((1, 2), False, 356, "779b8f9e5f14a7f4e2291503c0d2fc2ea6b9c8eec9bd4a02c6ec99ab97e315e9", 2),
    },
    "outside_x20_d0_b1": {
        0: ((1, 2), False, 368, "3679e2e553073afd11fceceec695fbfac75eee954a8322ad784d633cef2bf70e", 2),
        1: ((1, 2), False, 368, "3679e2e553073afd11fceceec695fbfac75eee954a8322ad784d633cef2bf70e", 2),
        5: ((1, 2), False, 368, "3679e2e553073afd11fceceec695fbfac75eee954a8322ad784d633cef2bf70e", 2),
    },
    "outside_x20_d2_b0": {
        0: ((1, 2), False, 356, "6a6a7161c5da69990af0d9a2023537aef7763da1c8d6c982891fca00117e25de", 2),
        1: ((1, 2), False, 356, "6a6a7161c5da69990af0d9a2023537aef7763da1c8d6c982891fca00117e25de", 2),
        5: ((1, 2), False, 356, "6a6a7161c5da69990af0d9a2023537aef7763da1c8d6c982891fca00117e25de", 2),
    },
    "outside_x20_d2_b1": {
        0: ((1, 2), False, 368, "5a751dbdc402ec265fbf7ef0a0114c6113099f805e7d5af8799185c2c5ed3e48", 2),
        1: ((1, 2), False, 368, "5a751dbdc402ec265fbf7ef0a0114c6113099f805e7d5af8799185c2c5ed3e48", 2),
        5: ((1, 2), False, 368, "5a751dbdc402ec265fbf7ef0a0114c6113099f805e7d5af8799185c2c5ed3e48", 2),
    },
    "outside_x20_d4_b0": {
        0: ((1, 2), False, 368, "6352ab5a1136d4d538c73608d5e92fd3c7b27303285a31c6a3479574d55e370c", 2),
        1: ((1, 2), False, 368, "6352ab5a1136d4d538c73608d5e92fd3c7b27303285a31c6a3479574d55e370c", 2),
        5: ((1, 2), False, 368, "6352ab5a1136d4d538c73608d5e92fd3c7b27303285a31c6a3479574d55e370c", 2),
    },
    "outside_x20_d4_b1": {
        0: ((1, 2), False, 368, "7e1782cac5a0fed0e32b77e467c663f585381a2c4d814a43358222907775456c", 2),
        1: ((1, 2), False, 368, "7e1782cac5a0fed0e32b77e467c663f585381a2c4d814a43358222907775456c", 2),
        5: ((1, 2), False, 368, "7e1782cac5a0fed0e32b77e467c663f585381a2c4d814a43358222907775456c", 2),
    },
    "outside_x20_d6_b0": {
        0: ((1, 2), False, 368, "129d598b553f570e2f2bab5f8b3d0a7b86eabf370a86405af2a45f101053f1f1", 2),
        1: ((1, 2), False, 368, "129d598b553f570e2f2bab5f8b3d0a7b86eabf370a86405af2a45f101053f1f1", 2),
        5: ((1, 2), False, 368, "129d598b553f570e2f2bab5f8b3d0a7b86eabf370a86405af2a45f101053f1f1", 2),
    },
    "outside_x20_d6_b1": {
        0: ((1, 2), False, 368, "5c0740f499d0fe5714481a8c736eb6b50b7c7b9a78ed3793161d1f7e8975a627", 2),
        1: ((1, 2), False, 368, "5c0740f499d0fe5714481a8c736eb6b50b7c7b9a78ed3793161d1f7e8975a627", 2),
        5: ((1, 2), False, 368, "5c0740f499d0fe5714481a8c736eb6b50b7c7b9a78ed3793161d1f7e8975a627", 2),
    },
    "outside_x22_d4_b0": {
        0: ((1, 2), False, 412, "0e0c93a97155b414e6da309f0c04283265fcd5917ca9ccdba55b357a5ac7c3d3", 3),
        1: ((1, 2), False, 412, "0e0c93a97155b414e6da309f0c04283265fcd5917ca9ccdba55b357a5ac7c3d3", 3),
        5: ((1, 2), False, 416, "f8a994e5325a4766b9c16162b9fcadb8334ea2205171e8ae74aaa03cb49a4fdc", 2),
    },
    "outside_x22_d4_b1": {
        0: ((1, 2), False, 432, "6933a7fd0ec0fdcf0b87b5849d64d8efd1639b5e9ecb0938d91c93bec44deb7c", 3),
        1: ((1, 2), False, 432, "6933a7fd0ec0fdcf0b87b5849d64d8efd1639b5e9ecb0938d91c93bec44deb7c", 3),
        5: ((1, 2), False, 436, "cae39477fe537a622badd57136d3e98175101b74c43ea238d7b1caef33db031f", 2),
    },
    "outside_x22_d6_b0": {
        0: ((1, 2), False, 428, "9cb0d3a25d43a2e1a8e6995fd82a8e0b99ba5816a5cbfbb8b9c0f3adb99d53dc", 3),
        1: ((1, 2), False, 428, "9cb0d3a25d43a2e1a8e6995fd82a8e0b99ba5816a5cbfbb8b9c0f3adb99d53dc", 3),
        5: ((1, 2), False, 432, "563742e3d46b628c208dd05f98a93d0247f26a9dc68f4fe226b36f0a40d5e843", 2),
    },
    "outside_x22_d6_b1": {
        0: ((1, 2), False, 432, "f107d92a34abd31e0055c9771f8da56bd7e88d88ca725a4021dd76ffe35195e3", 3),
        1: ((1, 2), False, 432, "f107d92a34abd31e0055c9771f8da56bd7e88d88ca725a4021dd76ffe35195e3", 3),
        5: ((1, 2), False, 436, "01d0b621cc0d08b316867ebce0ecbef771fe05a64c825a97ca777b53432259b0", 2),
    },
}

EXPECTED_LEDGER_SHA256 = (
    "4e416cc3692242531735f9e5a66dbb4082a2bfdae3f938103a4580e045792abd"
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

    print("A23 arbitrary plus A25=E00+tE10 local fourth-cut obstruction: PASS")
    print("coupled character wt(t)=wt(x10)-wt(x00); t kept symbolic: PASS")
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
