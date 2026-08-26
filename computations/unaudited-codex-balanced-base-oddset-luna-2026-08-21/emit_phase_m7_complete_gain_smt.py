#!/usr/bin/env python3
"""Emit the complete support plus binomial-gain potential SMT.

The exact gain group is <3> times mu_6.  Each live source atom receives a real
log_3 potential and a real phase measured in sixth-turns.  When a literal row
has exactly two active monomials, one selector chooses either term; aggregate
sum identities impose equal magnitudes and a phase difference of 3 mod 6.
This avoids enumerating the 1.44 billion possible monomial pairs.
"""

from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_balanced_base_oddset_luna import qlabel  # noqa: E402
from emit_phase_m7_1222_k4_support_smt import build_polynomials  # noqa: E402
from screen_phase_m7_support import SEEDS  # noqa: E402


OUT = HERE / "phase_m7_1222_k4_complete_gain.smt2"
MANIFEST = HERE / "manifest_phase_m7_1222_k4_complete_gain.json"
LABEL = "1222_k4_C1222"
GAIN = {
    "1": (0, 0),
    "1*w": (0, 2),
    "-1-1*w": (0, 4),
    "3": (1, 0),
    "3*w": (1, 2),
    "-3-3*w": (1, 4),
}


def atom_name(item):
    return "x_%d_%d_%d_%d_%d" % item


def activation(names):
    ordered = sorted(names)
    if len(ordered) == 1:
        return ordered[0]
    return f"(and {' '.join(ordered)})"


def linear_sum(names, prefix, constant):
    pieces = [str(constant)] if constant else []
    pieces.extend(prefix + name[1:] for name in sorted(names))
    if not pieces:
        return "0"
    if len(pieces) == 1:
        return pieces[0]
    return f"(+ {' '.join(pieces)})"


def main():
    polynomials, raw = build_polynomials(False)
    rows = []
    early_pure = []
    atoms = set()
    monomial_records = []
    for (word, degree), terms in sorted(polynomials.items(),
                                         key=lambda item: (item[0][1], item[0][0])):
        if word == (1,) * 8 and degree < 7:
            destination = early_pure
        elif word not in ((0,) * 8, (1,) * 8) and terms:
            destination = []
        else:
            continue
        ids = []
        for monomial, coefficient in terms:
            names = frozenset(atom_name(item) for item in monomial if item[4])
            atoms.update(names)
            label = qlabel(coefficient)
            if label not in GAIN:
                raise RuntimeError(("gain outside census", label))
            index = len(monomial_records)
            monomial_records.append((names, *GAIN[label]))
            ids.append(index)
        if destination is early_pure:
            early_pure.extend(ids)
        else:
            rows.append((word, degree, ids))

    with OUT.open("w") as handle:
        write = lambda line: handle.write(line + "\n")
        write("(set-logic QF_LIRA)")
        write("(set-option :produce-models true)")
        for name in sorted(atoms):
            write(f"(declare-fun {name} () Bool)")
            write(f"(declare-fun l{name[1:]} () Real)")
            write(f"(declare-fun p{name[1:]} () Real)")
        for index, (names, magnitude, phase) in enumerate(monomial_records):
            write(f"(define-fun m{index} () Bool {activation(names)})")
            write(f"(define-fun g{index} () Real {linear_sum(names, 'l', magnitude)})")
            write(f"(define-fun h{index} () Real {linear_sum(names, 'p', phase)})")
        for item in SEEDS[LABEL]:
            write(f"(assert {atom_name(item)})")
        for index in early_pure:
            write(f"(assert (not m{index}))")
        for row_index, (_word, _degree, ids) in enumerate(rows):
            count = f"(+ {' '.join(f'(ite m{i} 1 0)' for i in ids)})"
            write(f"(define-fun c{row_index} () Int {count})")
            write(f"(assert (not (= c{row_index} 1)))")
            write(f"(declare-fun r{row_index} () Real)")
            write(f"(declare-fun q{row_index} () Real)")
            write(f"(declare-fun n{row_index} () Int)")
            choices = " ".join(
                f"(and m{i} (= r{row_index} g{i}) (= q{row_index} h{i}))"
                for i in ids
            )
            magnitude_sum = f"(+ {' '.join(f'(ite m{i} g{i} 0)' for i in ids)})"
            phase_sum = f"(+ {' '.join(f'(ite m{i} h{i} 0)' for i in ids)})"
            write(
                f"(assert (=> (= c{row_index} 2) (and (or {choices}) "
                f"(= {magnitude_sum} (* 2 r{row_index})) "
                f"(= (- (* 2 q{row_index}) {phase_sum}) "
                f"(+ 3 (* 6 n{row_index}))))))"
            )
        write("(check-sat)")
        write(f"(get-value ({' '.join(sorted(atoms))}))")
        write("(exit)")

    output = {
        "branch": LABEL,
        "logic": "QF_LIRA",
        "boolean_atoms": len(atoms),
        "potential_reals": 2 * len(atoms) + 2 * len(rows),
        "row_phase_integers": len(rows),
        "monomial_definitions": len(monomial_records),
        "mixed_rows": len(rows),
        "early_pure_monomials": len(early_pure),
        "raw_matching_terms": raw,
        "smt_bytes": OUT.stat().st_size,
        "gain_group": "Z<3> x Z/6",
        "soundness": (
            "For count=2, choosing either active term and using twice the "
            "chosen potential minus the active sum imposes magnitude difference "
            "0 and phase difference 3 mod 6. Divisibility of C* makes these "
            "potential equations equivalent to binomial Laurent consistency."
        ),
    }
    MANIFEST.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
