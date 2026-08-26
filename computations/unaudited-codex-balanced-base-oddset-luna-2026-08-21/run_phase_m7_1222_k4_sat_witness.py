#!/usr/bin/env python3
"""Capture, verify, and greedily shrink the exact 1222-k4 support witness."""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from emit_phase_m7_1222_k4_support_smt import (  # noqa: E402
    LABEL, build_polynomials,
)
from screen_phase_m7_support import SEEDS  # noqa: E402


SMT = HERE / "phase_m7_1222_k4_support_exact_sat.smt2"
OUT = HERE / "results_phase_m7_1222_k4_sat_witness.json"
ATOM_PATTERN = re.compile(r"x_([0-7])_([0-7])_([01])_([01])_([1-7])")


def atom_name(item):
    return "x_%d_%d_%d_%d_%d" % item


def parse_model(stdout):
    blocks = re.findall(
        r"\(define-fun (x_[0-7]_[0-7]_[01]_[01]_[1-7]) \(\) Bool\s+(true|false)\)",
        stdout,
    )
    return {name for name, value in blocks if value == "true"}


def monomial_names(monomial):
    return frozenset(atom_name(item) for item in monomial if item[4])


def main():
    completed = subprocess.run(
        ["z3", "-smt2", SMT.name], cwd=HERE, capture_output=True,
        text=True, timeout=120, check=False,
    )
    if completed.returncode != 0 or not completed.stdout.startswith("sat\n"):
        raise RuntimeError((completed.returncode, completed.stdout[:200], completed.stderr[:200]))
    selected = parse_model(completed.stdout)
    polynomials, _raw_count = build_polynomials(False)
    rows = []
    pure_early = []
    for (word, degree), terms in polynomials.items():
        monomials = [monomial_names(monomial) for monomial, _coefficient in terms]
        if word == (1,) * 8 and degree < 7:
            pure_early.extend(monomials)
        elif word not in ((0,) * 8, (1,) * 8) and monomials:
            rows.append((word, degree, monomials))
    seed = {atom_name(item) for item in SEEDS[LABEL]}

    def verify(support):
        bad_mixed = []
        for word, degree, monomials in rows:
            count = sum(monomial <= support for monomial in monomials)
            if count == 1:
                bad_mixed.append(("".join(map(str, word)), degree))
        bad_pure = sum(monomial <= support for monomial in pure_early)
        return bad_mixed, bad_pure, seed <= support

    before = verify(selected)
    if before != ([], 0, True):
        raise RuntimeError(("model verification failed", before))

    # Inclusion-minimal deterministic deletion.  Maintain the currently live
    # monomials, so each deletion only touches rows containing that atom.
    active = []
    active_rows = []
    by_atom = defaultdict(list)
    row_counts = []
    for row_index, (_word, _degree, monomials) in enumerate(rows):
        count = 0
        for monomial in monomials:
            if monomial <= selected:
                index = len(active)
                active.append(True)
                active_rows.append(row_index)
                for name in monomial:
                    by_atom[name].append(index)
                count += 1
        row_counts.append(count)
    changed = True
    passes = 0
    while changed:
        changed = False
        passes += 1
        for name in sorted(selected - seed):
            impacted = [index for index in by_atom[name] if active[index]]
            decrement = Counter(active_rows[index] for index in impacted)
            if any(row_counts[row] - amount == 1
                   for row, amount in decrement.items()):
                continue
            selected.remove(name)
            changed = True
            for index in impacted:
                active[index] = False
                row_counts[active_rows[index]] -= 1
    after = verify(selected)
    output = {
        "solver": "z3 plain SAT on complete exact-Q(omega) support encoding",
        "solver_exit": completed.returncode,
        "initial_live_atoms": len(parse_model(completed.stdout)),
        "greedy_passes": passes,
        "inclusion_minimal_live_atoms": len(selected),
        "support": sorted(selected),
        "fixed_seed": sorted(seed),
        "verified_mixed_singletons": len(after[0]),
        "verified_early_pure_monomials": after[1],
        "verified_seed_live": after[2],
        "guard": "Inclusion-minimal is not minimum-cardinality; coefficients are not yet solved.",
    }
    OUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
