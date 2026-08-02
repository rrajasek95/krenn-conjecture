#!/usr/bin/env python3
"""Exact two-inequality Groebner-cone obstruction for a squarefree d6 lead.

The first squarefree monomial after the t-last lexicographic leading term of
the 546-term degree-six compatibility cell is 0948cfd9e1ef.  Making it
strictly beat the old lead requires one additive-weight inequality.  A
single frozen degree-five transport cell requires the reverse weak
inequality in order to retain its certified lead.  Their exponent-difference
vectors are exact negatives, giving a two-row integral Farkas certificate.
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
    "d280168e9619d796ed0e695652b540895230b5f5918fdb5df625aa2a59fcc534"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def exponent_difference(first, second):
    difference = Counter(first)
    difference.subtract(second)
    return {variable: value for variable, value in difference.items() if value}


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


def audit():
    degree6 = reconstruct_degree6_cell()
    old_lead = bytes.fromhex("0948cfcfebef")
    squarefree_candidate = bytes.fromhex("0948cfd9e1ef")
    require(FIRST.leading_monomial(degree6) == old_lead,
            "degree-six old lead changed")
    require(old_lead in degree6 and squarefree_candidate in degree6,
            "degree-six comparison terms changed")
    require(len(old_lead) != len(set(old_lead)),
            "old degree-six lead unexpectedly became squarefree")
    require(len(squarefree_candidate) == len(set(squarefree_candidate)),
            "candidate degree-six term is not squarefree")

    originals, original_lead_to_code = FIRST.original_basis()
    code_to_original_lead = {
        code: lead for lead, code in original_lead_to_code.items()
    }
    cell_lcm = bytes(sorted(
        set(code_to_original_lead[1459]) | set(code_to_original_lead[1466])
    ))
    require(len(cell_lcm) == 5,
            "Farkas degree-five source pair lost LCM degree five")
    degree5 = COMPLETE.s_polynomial(
        cell_lcm, 1459, 1466, originals, code_to_original_lead
    )
    degree5_lead = FIRST.leading_monomial(degree5)
    degree5_term = bytes.fromhex("0275d9e1fb")
    require(degree5_lead.hex() == "0275cfebfb",
            "Farkas degree-five lead changed")
    require(degree5_term in degree5,
            "Farkas degree-five comparison term disappeared")
    require(degree5_lead != degree5_term,
            "Farkas degree-five inequality collapsed")

    # Candidate > old lead is encoded as
    #     <old-candidate,w> <= -1.
    # Preserving the degree-five lead is encoded as
    #     <term-lead,w> <= 0.
    candidate_row = exponent_difference(old_lead, squarefree_candidate)
    preservation_row = exponent_difference(degree5_term, degree5_lead)
    require(candidate_row and preservation_row,
            "a Farkas row became zero")
    require({key: -value for key, value in candidate_row.items()}
            == preservation_row,
            "the two Farkas rows are no longer exact negatives")
    summed_row = Counter(candidate_row)
    summed_row.update(preservation_row)
    summed_row = {key: value for key, value in summed_row.items() if value}
    require(not summed_row, "Farkas row sum is not zero")
    summed_bound = -1 + 0
    require(summed_bound == -1,
            "Farkas bound sum no longer gives a contradiction")

    ledger = {
        "degree6_old_lead": old_lead.hex(),
        "degree6_old_lead_squarefree": False,
        "degree6_squarefree_candidate": squarefree_candidate.hex(),
        "degree6_candidate_coefficient": degree6[
            squarefree_candidate
        ].numerator,
        "degree5_source_codes": [1459, 1466],
        "degree5_lead": degree5_lead.hex(),
        "degree5_comparison_term": degree5_term.hex(),
        "candidate_inequality_row": [
            [key, value] for key, value in sorted(candidate_row.items())
        ],
        "candidate_inequality_upper_bound": -1,
        "preservation_inequality_row": [
            [key, value] for key, value in sorted(preservation_row.items())
        ],
        "preservation_inequality_upper_bound": 0,
        "farkas_multipliers": [1, 1],
        "summed_row": [],
        "summed_upper_bound": summed_bound,
        "conclusion": (
            "no additive weight in the certified degree4/degree5 "
            "Groebner cone selects squarefree term 0948cfd9e1ef"
        ),
        "scope_guard": (
            "this certificate excludes one squarefree degree6 term, not "
            "all 350 squarefree terms in the compatibility cell"
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
                "frozen chart26 weight-cone Farkas ledger changed")
    print(
        "n=8 chart26 weight-cone Farkas obstruction: PASS; "
        "rows=2, multipliers=(1,1), summed bound=-1"
    )
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
