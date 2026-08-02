#!/usr/bin/env python3
"""Verify an exact weight preserving d4/d5 and selecting a squarefree d6 lead.

The term order compares homogeneous total degree, then off-support y degree
(so t is last), then the integral weight below, then the original lex order.
The checker exhausts all 6,558 original polynomials and all 84,005 cells in
the complete degree-five Buchberger layer.  Their certified leading terms
are retained.  On the 546-term degree-six compatibility cell, the unique
weighted lead is the squarefree monomial 0951b4c7ebf5.
"""

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
D6_PATH = HERE / "verify_n8_chart26_first_degree6_compatibility.py"
SPEC = importlib.util.spec_from_file_location("n8_degree6_cell", D6_PATH)
D6 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(D6)
FIRST = D6.FIRST
COMPLETE = D6.COMPLETE

EXPECTED_LEDGER_SHA256 = (
    "b866eb8a08b09a9cefdc65171422adbb1e7d9339b2c72f08ea943a13f69b1e80"
)

# Zero is understood for every omitted byte identifier.
NONZERO_WEIGHTS = {
    1: 27, 2: 27, 3: 12, 4: 19, 5: 19, 6: 12, 7: 19, 8: 19,
    9: 20, 10: 19, 11: 20, 12: 13, 13: 11, 14: 12, 15: 13,
    16: 11, 17: 12, 18: 7, 19: 7, 20: 7,
    64: 4, 65: 5, 75: 7, 76: 7, 77: 7, 78: 7, 79: 7, 80: 7,
    90: -2, 91: -2, 92: -1, 99: -9, 100: -7, 101: -7,
    108: -9, 109: -10, 110: -9,
    117: 13, 118: 13, 119: 13, 120: 11, 121: 11, 122: 11,
    123: 11, 124: 11, 126: 9, 127: 7, 128: 5, 129: 9,
    131: 8, 132: 11, 133: 9, 134: 9, 138: 7, 139: 5,
    140: 5, 141: 7, 142: 5, 143: 5,
    163: 2, 166: 2, 169: 2, 170: 2, 171: 1, 173: 1,
    174: 1, 176: 1, 177: 2, 178: 1, 179: 1,
    189: -2, 190: -1, 191: -1, 192: -2, 193: -1, 194: -1,
    195: -2, 196: -1, 197: -1,
    198: 9, 199: 7, 200: 7, 201: 7, 202: 5, 203: 5, 204: 5,
    205: 3, 206: 3, 207: 2, 208: 1, 209: 1, 210: 2, 211: 2,
    212: 2, 213: 2, 214: 2, 215: 2,
    226: 1, 227: 1, 229: 1, 230: 1, 232: 1, 244: -1,
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def weight(row):
    return sum(NONZERO_WEIGHTS.get(variable, 0) for variable in row)


def weighted_lead(polynomial):
    maximum_y_degree = max(map(len, polynomial))
    top = [row for row in polynomial if len(row) == maximum_y_degree]
    maximum_weight = max(map(weight, top))
    return min(row for row in top if weight(row) == maximum_weight)


def comparison_census(polynomial, certified_lead):
    top = [row for row in polynomial if len(row) == len(certified_lead)]
    lead_weight = weight(certified_lead)
    differences = [lead_weight - weight(row)
                   for row in top if row != certified_lead]
    require(all(value >= 0 for value in differences),
            "an integer-weight preservation inequality failed")
    return Counter(differences)


def reconstruct_degree6_cell():
    basis = D6.initial_basis()
    schedule = D6.degree6_schedule(basis)
    remainder = None
    for schedule_index, (lcm, first_index, second_index) in enumerate(
            schedule[:3], 1):
        recomputed_lcm, spoly = D6.s_polynomial(
            basis[first_index], basis[second_index]
        )
        require(recomputed_lcm == lcm, "degree-six schedule changed")
        remainder, _certificate = D6.reduce_polynomial(spoly, basis)
        remainder, lead = D6.normalize(remainder)
        basis.append({
            "kind": "degree6",
            "label": schedule_index,
            "total_degree": 6,
            "polynomial": remainder,
            "lead": lead,
        })
    return remainder


def histogram_record(histogram):
    return [[value, count] for value, count in sorted(histogram.items())]


def audit():
    require(len(NONZERO_WEIGHTS) == 103,
            "nonzero weight support changed")
    originals, original_lead_to_code = FIRST.original_basis()
    code_to_original_lead = {
        code: lead for lead, code in original_lead_to_code.items()
    }

    original_difference_histogram = Counter()
    for code, polynomial in originals.items():
        certified_lead = code_to_original_lead[code]
        require(weighted_lead(polynomial) == certified_lead,
                "an original degree-four lead changed")
        original_difference_histogram.update(
            comparison_census(polynomial, certified_lead)
        )

    pairs, _cores, _core_histogram = COMPLETE.build_pairs(
        code_to_original_lead
    )
    degree5_difference_histogram = Counter()
    distinct_degree5_leads = set()
    for lcm, first_code, second_code in pairs:
        polynomial = COMPLETE.s_polynomial(
            lcm,
            first_code,
            second_code,
            originals,
            code_to_original_lead,
        )
        certified_lead = FIRST.leading_monomial(polynomial)
        require(weighted_lead(polynomial) == certified_lead,
                "a completed degree-five lead changed")
        distinct_degree5_leads.add(certified_lead)
        degree5_difference_histogram.update(
            comparison_census(polynomial, certified_lead)
        )
    require(len(distinct_degree5_leads) == 84005,
            "completed degree-five leading census changed")

    degree6 = reconstruct_degree6_cell()
    candidate = bytes.fromhex("0951b4c7ebf5")
    require(candidate in degree6, "weighted degree-six candidate disappeared")
    require(len(candidate) == len(set(candidate)) == 6,
            "weighted degree-six candidate is not squarefree")
    require(weighted_lead(degree6) == candidate,
            "integer weight lost the squarefree degree-six lead")
    degree6_difference_histogram = comparison_census(degree6, candidate)
    require(degree6_difference_histogram.get(0, 0) == 0,
            "degree-six weighted lead is not unique")
    require(min(degree6_difference_histogram) == 1,
            "degree-six strict weight margin changed")

    ordered_weights = [
        [variable, value] for variable, value in sorted(NONZERO_WEIGHTS.items())
    ]
    weight_digest = sha256(json.dumps(
        ordered_weights, separators=(",", ":")
    ).encode()).hexdigest()
    ledger = {
        "term_order": (
            "homogeneous total degree, y degree, integral weight, old lex"
        ),
        "nonzero_weight_coordinates": len(NONZERO_WEIGHTS),
        "minimum_weight": min(NONZERO_WEIGHTS.values()),
        "maximum_weight": max(NONZERO_WEIGHTS.values()),
        "weight_vector_sha256": weight_digest,
        "original_generators_replayed": len(originals),
        "original_weight_difference_histogram": histogram_record(
            original_difference_histogram
        ),
        "degree5_cells_replayed": len(pairs),
        "distinct_degree5_leads_preserved": len(distinct_degree5_leads),
        "degree5_weight_difference_histogram": histogram_record(
            degree5_difference_histogram
        ),
        "degree6_terms": len(degree6),
        "degree6_top_terms": sum(len(row) == 6 for row in degree6),
        "degree6_squarefree_top_terms": sum(
            len(row) == len(set(row)) == 6 for row in degree6
        ),
        "degree6_weighted_lead": candidate.hex(),
        "degree6_weighted_lead_squarefree": True,
        "degree6_weighted_lead_margin": min(degree6_difference_histogram),
        "degree6_weight_difference_histogram": histogram_record(
            degree6_difference_histogram
        ),
        "conclusion": (
            "the certified degree4/degree5 Groebner cone contains an "
            "integral weight selecting a squarefree lead for the first "
            "degree6 compatibility cell"
        ),
        "scope_guard": (
            "this is a finite-subsystem order, not a completed degree6 "
            "Groebner basis or a radicality proof"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main():
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen feasible squarefree-weight ledger changed")
    print(
        "n=8 chart26 feasible squarefree weight: PASS; "
        "d4/d5=6558/84005, d6 lead=0951b4c7ebf5, margin=1"
    )
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
