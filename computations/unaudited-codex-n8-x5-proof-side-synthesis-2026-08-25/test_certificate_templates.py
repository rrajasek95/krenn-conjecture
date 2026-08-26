#!/usr/bin/env python3
"""Cheap exact coefficient/template tests on sealed X5 integer duals."""

from collections import Counter
import hashlib
import json
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
T = 361
BRANCHES = ("direct", "triangle_endpoint_colour", "third_colour", "cap_endpoint_colour")
ROOTS = {
    6: REPO / "computations/unaudited-codex-n8-x5-four-blocker-d6-rational-lift-2026-08-25",
    7: REPO / "computations/unaudited-codex-n8-x5-four-blocker-d7-two-prime-lift-2026-08-25",
    8: REPO / "computations/unaudited-codex-n8-x5-four-blocker-d8-two-prime-lift-2026-08-25",
    9: REPO / "computations/unaudited-codex-n8-x5-coloured-d9-seeded-support-repair-2026-08-25",
    10: REPO / "computations/unaudited-codex-n8-x5-four-d10-seeded-support-repair-2026-08-25",
    11: REPO / "computations/unaudited-codex-n8-x5-four-d11-seeded-support-repair-2026-08-25",
}
DIRECT_D9 = REPO / "computations/unaudited-codex-n8-x5-four-dual-degree-recurrence-audit-2026-08-25/d9_span_dual_direct.tsv"
PINS = {
    (6, "direct"): "0731e711f19d01423a157aba9c1a43a314e41b4a6bd3fe95c0b6b7935546236e",
    (6, "triangle_endpoint_colour"): "f30015fbd60a02534dbdf6cc89095cd0349a0c8ac4ed6a5696fc9776f47744f4",
    (6, "third_colour"): "c553b574cab24e7b3075933684ba1254eba7669447b1cabb129e4b40c97097f8",
    (6, "cap_endpoint_colour"): "e9396507cbdc12a2ac46348c04b82bf5bef807f9bb6a7f7e821f6126b664089b",
    (7, "direct"): "662c39682d30c6728b828bb7954c071c2bf5c1803993bfdf937cd9ebee4731c8",
    (7, "triangle_endpoint_colour"): "0cee88baef937e32a4f66db10feecec9e3f7531eefbb0e093862179a88de22eb",
    (7, "third_colour"): "9a19b037f7fe8889a69022de1838415fea1901ec3cde1699c990359411580e0f",
    (7, "cap_endpoint_colour"): "7900f745279e14dbcb4549f6da7b6ddc6dee276509c49fdc9d83914c873d92be",
    (8, "direct"): "ee8cc561fc660774ad3cdc9c5607af937f3084642ae1e03c8dcc26e60d0c42a9",
    (8, "triangle_endpoint_colour"): "5dd800c60fd8ac25c8aa4a315bec69d6ee8685ba25d5d1f0e769bc081d411095",
    (8, "third_colour"): "181f1b799ed2b7b5018e719a94acc5f39ad541706f2baadb204afa67ab6eafd1",
    (8, "cap_endpoint_colour"): "a5b5b518ec4feeeab1c7b48584bbc97db0715db548ae32482ddc431cd9e010bf",
    (9, "direct"): "8ee0166568fb24ce8f664ac2c0006991eca4dbbb929164e3620e5a106cc2c265",
    (9, "triangle_endpoint_colour"): "93889d6212108f371d95f504be0b8f5b06a9f02fca3139881fb2289d8a40fa12",
    (9, "third_colour"): "ff23df3477d8d1784b9cfe40c53698a4acd56a35917c40d0bc94b45383033b94",
    (9, "cap_endpoint_colour"): "b59d2d6f4619f24fb77f01475c0980ad30ddb979e76042a978748992dffee7ac",
    (10, "direct"): "c639faa986903b66d003dc4513bb9ad029f5b0027dd15714d8c5449a494c8246",
    (10, "triangle_endpoint_colour"): "67daf29cdbf5e2919441f1227c01b933f37ac7dfe6e832a5d09779218d758174",
    (10, "third_colour"): "5a9e86a19980b77da51925b4d78be2c198aa3c7ef9f41a3ffc92ac016551517d",
    (10, "cap_endpoint_colour"): "d90a6270359cbf79520caff7be64b1a4f99f3b66d9a8aa630e850dde3ee9f567",
    (11, "direct"): "d631677cef2be77de0f2f28e815bdb50ef93da484e0d2a548c6f8287f22f4c87",
}


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def path_for(degree, branch):
    if degree == 9 and branch == "direct":
        return DIRECT_D9
    return ROOTS[degree] / f"exact_lift_{branch}/integer_dual.tsv"


def load(degree, branch):
    path = path_for(degree, branch)
    assert sha(path) == PINS[(degree, branch)]
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    assert int(header[1]) == len(lines) - 1 and int(header[2]) == 1
    answer, previous = {}, None
    for line in lines[1:]:
        kind, raw, raw_value = line.split("\t")
        row, value = tuple(map(int, raw.split(","))), int(raw_value)
        assert kind == "ROW" and len(row) == degree and row == tuple(sorted(row))
        assert previous is None or previous < row
        assert row not in answer and value != 0
        answer[row], previous = value, row
    assert answer[(T,) * degree] == 1
    return answer


def shift(mapping, count=1):
    return {tuple(sorted(row + (T,) * count)): value for row, value in mapping.items()}


def linear(*terms):
    answer = Counter()
    for scalar, mapping in terms:
        for row, value in mapping.items():
            answer[row] += scalar * value
    return {row: value for row, value in answer.items() if value}


def residual(destination, source):
    return linear((1, destination), (-1, shift(source)))


def stats(mapping):
    values = list(mapping.values())
    return {"support": len(mapping), "coefficient_set": sorted(set(values)),
            "l1_norm": sum(map(abs, values)), "max_abs": max(map(abs, values), default=0)}


def t_valuation_histogram(mapping):
    return {str(key): value for key, value in sorted(Counter(
        sum(entry == T for entry in row) for row in mapping).items())}


def main():
    maps = {(degree, branch): load(degree, branch)
            for degree in range(6, 11) for branch in BRANCHES}
    maps[(11, "direct")] = load(11, "direct")
    transitions, corrections = [], {}
    for branch in BRANCHES:
        for degree in range(7, 11):
            source, destination = maps[(degree - 1, branch)], maps[(degree, branch)]
            transported = shift(source)
            correction = residual(destination, source)
            corrections[(degree, branch)] = correction
            exact_matches = sum(destination.get(row) == value for row, value in transported.items())
            transitions.append({
                "branch": branch, "source_degree": degree - 1, "destination_degree": degree,
                "pure_transport_equal": transported == destination,
                "transport_support": len(transported),
                "exact_transport_rows_in_destination": exact_matches,
                "correction": stats(correction),
            })
    direct_10_11_equal = shift(maps[(10, "direct")]) == maps[(11, "direct")]
    assert direct_10_11_equal

    residual_recurrence = []
    for branch in BRANCHES:
        for degree in (9, 10):
            current = corrections[(degree, branch)]
            previous = corrections[(degree - 1, branch)]
            shifted_previous = shift(previous)
            common_exact = sum(current.get(row) == value for row, value in shifted_previous.items())
            residual_recurrence.append({
                "branch": branch, "degree": degree,
                "correction_equals_shift_previous_correction": current == shifted_previous,
                "previous_correction_rows_matching": common_exact,
                "previous_correction_support": len(previous),
                "current_correction_support": len(current),
            })

    cross_branch = []
    coloured = BRANCHES[1:]
    for degree in (9, 10):
        items = [corrections[(degree, branch)] for branch in coloured]
        common_keys = set.intersection(*(set(item) for item in items))
        exact_common = {row for row in common_keys if len({item[row] for item in items}) == 1}
        cross_branch.append({
            "degree": degree,
            "correction_supports": {branch: len(corrections[(degree, branch)]) for branch in coloured},
            "common_support_rows": len(common_keys),
            "common_equal_coefficient_rows": len(exact_common),
            "all_three_corrections_equal": items[0] == items[1] == items[2],
        })

    d10_items = [corrections[(10, branch)] for branch in coloured]
    d10_common_keys = set.intersection(*(set(item) for item in d10_items))
    d10_common = {row: d10_items[0][row] for row in d10_common_keys
                  if len({item[row] for item in d10_items}) == 1}
    d10_common_decomposition = {
        "common_core": {**stats(d10_common),
                        "t_valuation_histogram": t_valuation_histogram(d10_common)},
        "branch_tails": {},
    }
    for branch in coloured:
        tail = linear((1, corrections[(10, branch)]), (-1, d10_common))
        d8_carrier = linear((1, maps[(8, branch)]), (-1, maps[(8, "direct")]))
        shifted_d8_carrier = shift(d8_carrier, 2)
        d10_common_decomposition["branch_tails"][branch] = {
            **stats(tail),
            "t_valuation_histogram": t_valuation_histogram(tail),
            "d8_carrier_support": len(d8_carrier),
            "equals_two_t_shift_of_d8_carrier": tail == shifted_d8_carrier,
            "matching_shifted_d8_carrier_rows": sum(
                tail.get(row) == value for row, value in shifted_d8_carrier.items()),
        }

    # Test the smallest scalar two-step recurrence family
    # lambda_d = a E(lambda_(d-1)) + b E^2(lambda_(d-2)), a+b=1.
    scalar_two_step = []
    for branch in BRANCHES:
        for degree in (8, 9, 10):
            hits = []
            for a in range(-2, 4):
                b = 1 - a
                candidate = linear((a, shift(maps[(degree - 1, branch)])),
                                   (b, shift(maps[(degree - 2, branch)], 2)))
                if candidate == maps[(degree, branch)]:
                    hits.append([a, b])
            scalar_two_step.append({"branch": branch, "degree": degree, "solutions": hits})

    seed_audits = {}
    seed_column_sets = {}
    for branch in BRANCHES:
        path = ROOTS[11] / f"seed_{branch}_p1073741827/seed_audit.json"
        data = json.loads(path.read_text())
        selected_path = ROOTS[11] / f"seed_{branch}_p1073741827/selected.tsv"
        selected_lines = selected_path.read_text().splitlines()
        assert selected_lines[0] == "KRENN_X5_BLOCKER_D11_SELECTED_COLUMNS_V1"
        seed_column_sets[branch] = set(selected_lines[1:])
        seed_audits[branch] = {
            "sha256": sha(path),
            "selected_sha256": sha(selected_path),
            "transported_support": data["transported_support"],
            "transported_incident_columns": data["transported_incident_columns"],
            "exact_transport_pairing_failures": data["exact_transport_pairing_failures"],
            "all_offenders_t_free_c1": data["all_offenders_t_free_c1"],
            "offending_generator_histogram": data["offending_generator_histogram"],
        }
    coloured_seed_overlap = {
        f"{left}__{right}": len(seed_column_sets[left] & seed_column_sets[right])
        for index, left in enumerate(coloured) for right in coloured[index + 1:]
    }

    result = {
        "schema": "KRENN_X5_CERTIFICATE_TEMPLATE_IDENTITY_AUDIT_V1",
        "status": "PASS_EXACT_SMALL_TEMPLATE_TESTS",
        "certificate_pins": {f"D{degree}:{branch}": PINS[(degree, branch)] for degree, branch in PINS},
        "certificate_stats": {f"D{degree}:{branch}": stats(mapping)
                              for (degree, branch), mapping in maps.items()},
        "transitions_d6_d10": transitions,
        "direct_d10_to_d11_pure_transport_equal": direct_10_11_equal,
        "correction_shift_recurrence": residual_recurrence,
        "cross_coloured_correction_identity": cross_branch,
        "d10_common_t_free_correction_decomposition": d10_common_decomposition,
        "scalar_two_step_recurrence": scalar_two_step,
        "d11_transport_seed_audits": seed_audits,
        "d11_identity_coordinate_offender_intersections": coloured_seed_overlap,
        "scope": "COEFFICIENT_SUPPORT_IDENTITIES_ONLY_NO_PROVIDER_REPLAY",
        "degree_twelve_read": False,
    }
    temporary = HERE / "results_template_identity_audit.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_template_identity_audit.json")
    print(json.dumps({
        "status": result["status"],
        "pure_transport_hits": [item for item in transitions if item["pure_transport_equal"]],
        "direct_d10_to_d11": direct_10_11_equal,
        "cross_branch": cross_branch,
        "two_step_hits": [item for item in scalar_two_step if item["solutions"]],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
