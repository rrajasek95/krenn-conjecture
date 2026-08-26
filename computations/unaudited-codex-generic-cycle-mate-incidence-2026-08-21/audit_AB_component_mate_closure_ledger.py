#!/usr/bin/env python3
"""Freeze the exhaustive four-stratum A=B component mate-coverage ledger."""

from hashlib import sha256
import json
from itertools import permutations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "results_AB_component_mate_closure_ledger.json"
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: i for i, edge in enumerate(EDGES)}


def require(value, detail):
    if not value:
        raise RuntimeError(detail)


def read(name):
    path = HERE / name
    return path, json.loads(path.read_text())


def cell_action(index, permutation, flips):
    edge_index, cell = divmod(index, 4)
    i, j = EDGES[edge_index]
    a, b = divmod(cell, 2)
    ni, nj = permutation[i], permutation[j]
    na, nb = a ^ flips[i], b ^ flips[j]
    if ni > nj:
        ni, nj, na, nb = nj, ni, nb, na
    return 4*EDGE_INDEX[(ni, nj)] + 2*na + nb


def q_action(index, permutation, flips):
    old = tuple((index >> (3-site)) & 1 for site in range(4))
    new = [0]*4
    for site in range(4):
        new[permutation[site]] = old[site] ^ flips[site]
    return sum(bit << (3-site) for site, bit in enumerate(new))


def main():
    inputs = {}
    for key, name in {
        "component": "results_AB_component_localizer_faces.json",
        "faces": "results_localizer_face_signatures.json",
        "compact": "results_mate_compact_identity.json",
        "q3": "results_Q3_fixed_left_mate_core_exact_audit.json",
        "intersection": "results_Q3_C6_intersection_mate_core_exact_audit.json",
        "qcover": "results_generic_Qcover_fraction_field_unit.json",
        "generic_support": "results_generic_cycle_left_slices_mate_export.json",
        "weak_export": "results_AB_component_weak_mate_export.json",
        "weak_exact": "results_AB_component_weak_mate_exact_audit.json",
        "weak_p1": "results_AB_component_weak_mate_explicit_p1073741827.manifest.json",
        "weak_p2": "results_AB_component_weak_mate_explicit_p1073741789.manifest.json",
    }.items():
        path, data = read(name)
        inputs[key] = (path, data)

    component = inputs["component"][1]
    faces = inputs["faces"][1]
    compact = inputs["compact"][1]
    q3 = inputs["q3"][1]
    intersection = inputs["intersection"][1]
    qcover = inputs["qcover"][1]
    generic = inputs["generic_support"][1]["records"][0]
    weak_export = inputs["weak_export"][1]
    weak_exact = inputs["weak_exact"][1]
    weak_manifests = (inputs["weak_p1"][1], inputs["weak_p2"][1])

    require(component["component_parametrization"]["all_source_rows_replay"],
            "exact source parametrization ceased to replay")
    face_labels = {label for row in component["minimal_face_antichain"]
                   for label in row["localizers"]}
    require(face_labels == {"Q3", "C6", "C10", "C14", "C18"},
            "minimal localizer face set changed")
    require(compact["identity"]["literal_replay"] and
            compact["identity"]["mutation_control"],
            "compact exact identity audit changed")
    require(q3["exact_basis"] == "[1]" and q3["literal_replay"],
            "Q3 exact unit audit changed")
    require(intersection["exact_basis"] == "[1]" and
            intersection["literal_replay"] and
            intersection["common_H_live_signature"],
            "Q3=C6 exact unit audit changed")
    require(qcover["literal_replay"] and qcover["mutation_control"],
            "exact Q-cover identity audit changed")

    entry = frozenset(generic["entry_support"])
    cofactor = frozenset(generic["cofactor_support"])
    qsupport = frozenset(generic["Q_support"])
    stabilizer = []
    for permutation in permutations(range(4)):
        for flips in product((0, 1), repeat=4):
            if ({cell_action(i, permutation, flips) for i in entry} == entry and
                {cell_action(i, permutation, flips) for i in cofactor} == cofactor and
                {q_action(i, permutation, flips) for i in qsupport} == qsupport):
                stabilizer.append((permutation, flips))
    require(len(stabilizer) == 4, "component incidence stabilizer changed")
    transport = {}
    for target in (6, 10, 14, 18):
        witnesses = [(permutation, flips) for permutation, flips in stabilizer
                     if cell_action(6, permutation, flips) == target and
                     q_action(3, permutation, flips) == 3]
        require(len(witnesses) == 1,
                f"unique C6->C{target}, Q3-fixed witness changed")
        permutation, flips = witnesses[0]
        transport[f"C6_to_C{target}"] = {
            "permutation": list(permutation), "flips": list(flips),
            "Q3_fixed": True,
        }

    # The five localizer factors give a literal truth-table partition.
    strata = [
        {"name": "generic", "Q3_zero": False, "C_orbit_zero": False,
         "exact_certificate": "compact c3 11-row identity"},
        {"name": "Q3-only", "Q3_zero": True, "C_orbit_zero": False,
         "exact_certificate": "Q3 fixed-left 9-row mate unit"},
        {"name": "C-orbit-only", "Q3_zero": False, "C_orbit_zero": True,
         "exact_certificate": (
             "C6 generic Q-cover plus exact 8-row fixed-left unit on its "
             "declared common signature, transported by the stabilizer")},
        {"name": "Q3-intersect-C-orbit", "Q3_zero": True,
         "C_orbit_zero": True,
         "exact_certificate": (
             "Q3=C6 exact 8-row mate unit, transported by the stabilizer")},
    ]
    require({(row["Q3_zero"], row["C_orbit_zero"]) for row in strata} ==
            set(product((False, True), repeat=2)),
            "four-stratum truth table ceased to be exhaustive")

    # Stronger discovery: use only data forced everywhere by chart units.
    require(weak_export["zero_cells"] == [1, 2, 21, 22],
            "component-wide forced cofactor support changed")
    weak_units = []
    for manifest, record in zip(weak_manifests, weak_export["outputs"]):
        stage = manifest["stages"][0]
        require(stage["status"] == "completed" and stage["basis"]["unit"],
                "component-wide modular weak mate unit changed")
        require(manifest["input"]["file_sha256"] == record["sha256"],
                "component-wide modular input hash mismatch")
        weak_units.append({"characteristic": stage["basis"]["characteristic"],
                           "basis": "[1]", "input_sha256": record["sha256"]})
    require(weak_exact["exact_basis"] == "[1]" and
            weak_exact["literal_replay"] and
            weak_exact["all_source_rows_replay"] and
            weak_exact["all_localizers_are_chart_units"] and
            weak_exact["left_H_not_inferred"] and
            weak_exact["mate_H_localized_literally"],
            "component-wide exact weak mate audit changed")

    result = {
        "status": "UNAUDITED exhaustive four-stratum A=B mate ledger PASS",
        "proof_status": "exact_component_wide_mate_closure",
        "source_component": {
            "field": "Q(s,t)[r]/(r^2+2r-1)",
            "all_literal_source_rows_replay": True,
            "chart_factors_preserved": True,
            "left_H_not_inferred": True,
            "mate_H_localized_literally": True,
        },
        "minimal_divisor_labels": sorted(face_labels),
        "four_strata": strata,
        "component_stabilizer_size": len(stabilizer),
        "stabilizer_transport": transport,
        "exact_certificate_digests": {
            "compact_c3": compact["result_sha256"],
            "Q3_only": q3["result_sha256"],
            "generic_Qcover": qcover["result_sha256"],
            "Q3_C6_intersection": intersection["result_sha256"],
            "component_wide_weak_unit": weak_exact["result_sha256"],
        },
        "component_wide_closure": {
            "description": (
                "The mate ideal using only component-wide chart-forced "
                "cofactor, entry, and Q support is exactly unit over Q."),
            "ordinary_rows": weak_export["ordinary_row_count"],
            "modular_units": weak_units,
            "exact_lift": True,
            "exact_basis": "[1]",
            "exact_audit_sha256": weak_exact["result_sha256"],
            "covers_all_four_strata": True,
            "covers_deeper_C_orbit_self_intersections": True,
        },
        "scope_guard": (
            "The truth-table is exhaustive for the compact certificate's "
            "minimal localizer divisor set, while the exact component-wide "
            "weak unit no longer depends on any of those localizers and "
            "therefore covers their intersections as well. Scope remains "
            "the frozen full-source A=B component and original live chart; "
            "no left H equation is assumed."
        ),
        "source_hashes": {key: sha256(path.read_bytes()).hexdigest()
                          for key, (path, _) in inputs.items()},
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("AB component mate closure ledger PASS")
    print("stabilizer", len(stabilizer), "strata", len(strata))
    print("global weak modular", len(weak_units), "exact", True)
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
