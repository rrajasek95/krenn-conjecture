#!/usr/bin/env python3
"""Complete support-SMT encoding for the phase-base 1222 k4 packet.

There is one Boolean for every binary source coefficient of valuation 1..7.
For every literal binary output coefficient through order seven, matching
monomials are first combined over Q(omega).  A mixed coefficient is required
not to have exactly one active Laurent monomial.  Earlier pure-1 monomials are
forbidden and the canonical pure-7 seed is fixed live.

This is a necessary support screen: SAT is only a coefficient target.  UNSAT
is a complete certificate for this fixed primitive packet and valuation cap.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations, product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_balanced_base_oddset_luna import (  # noqa: E402
    ONE, ZERO, W, W2, PM8, qadd, qmul,
)
from screen_phase_m7_support import SEEDS, base_available  # noqa: E402


SMT = HERE / "phase_m7_1222_k4_support_exact.smt2"
MANIFEST = HERE / "manifest_phase_m7_1222_k4_support_smt.json"
LABEL = "1222_k4_C1222"

PHASE = {
    (0, 1): ONE, (2, 3): ONE,
    (0, 2): ONE, (1, 3): W,
    (0, 3): ONE, (1, 2): W2,
    (4, 5): ONE, (4, 6): ONE, (4, 7): ONE,
    (5, 6): ONE, (5, 7): ONE, (6, 7): ONE,
}


def positive_compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for first in range(1, total - length + 2):
        for tail in positive_compositions(total - first, length - 1):
            yield (first,) + tail


def matching_terms(matching, word):
    """Yield (degree, monomial, phase coefficient) through degree seven."""
    forced = []
    optional = []
    for edge in matching:
        u, v = edge
        if base_available(u, v, word[u], word[v]):
            optional.append(edge)
        else:
            forced.append(edge)
    for extra_count in range(len(optional) + 1):
        for extra in combinations(optional, extra_count):
            perturbed = tuple(forced) + tuple(extra)
            if not perturbed:
                # The only degree-zero term is the all-zero base output.
                yield 0, (), phase_of_unperturbed(matching, frozenset())
                continue
            count = len(perturbed)
            for degree in range(count, 8):
                for values in positive_compositions(degree, count):
                    entries = []
                    for (u, v), valuation in zip(perturbed, values):
                        entries.append((u, v, word[u], word[v], valuation))
                    frozen = frozenset(perturbed)
                    yield degree, tuple(sorted(entries)), phase_of_unperturbed(matching, frozen)


def phase_of_unperturbed(matching, perturbed):
    coefficient = ONE
    for edge in matching:
        if edge not in perturbed:
            coefficient = qmul(coefficient, PHASE[edge])
    return coefficient


def build_polynomials(raw_terms=False):
    polynomials = {}
    raw_count = 0
    for word in product(range(2), repeat=8):
        by_degree = defaultdict(lambda: defaultdict(lambda: ZERO))
        raw_by_degree = defaultdict(list)
        for matching in PM8:
            for degree, monomial, coefficient in matching_terms(matching, word):
                raw_count += 1
                if raw_terms:
                    # Hostile mutation: distinguish base matching completions.
                    raw_by_degree[degree].append((monomial, coefficient, matching))
                else:
                    old = by_degree[degree][monomial]
                    by_degree[degree][monomial] = qadd(old, coefficient)
        if raw_terms:
            for degree, terms in raw_by_degree.items():
                polynomials[(word, degree)] = tuple(
                    (monomial + ((8 + index, 8 + index, 0, 0, 0),), coefficient)
                    for index, (monomial, coefficient, _matching) in enumerate(terms)
                )
        else:
            for degree, terms in by_degree.items():
                polynomials[(word, degree)] = tuple(
                    (monomial, coefficient) for monomial, coefficient in terms.items()
                    if coefficient != ZERO
                )
    return polynomials, raw_count


def atom_name(item):
    u, v, a, b, valuation = item
    return f"x_{u}_{v}_{a}_{b}_{valuation}"


def activation(monomial):
    names = [atom_name(item) for item in monomial if item[4] != 0]
    if not names:
        return "true"
    if len(names) == 1:
        return names[0]
    return f"(and {' '.join(names)})"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-matching-terms", action="store_true")
    parser.add_argument("--satisfy-only", action="store_true")
    parser.add_argument("--max-live", type=int)
    parser.add_argument("--output", type=Path, default=SMT)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    args = parser.parse_args()
    polynomials, raw_count = build_polynomials(args.raw_matching_terms)
    atoms = {
        item
        for terms in polynomials.values()
        for monomial, _coefficient in terms
        for item in monomial if item[4] != 0 and item[0] < 8
    }
    mixed_rows = []
    singleton_rows = 0
    pure_early = []
    term_profile = Counter()
    for (word, degree), terms in sorted(polynomials.items(), key=lambda item: (item[0][1], item[0][0])):
        if word == (1,) * 8 and degree < 7:
            pure_early.extend(monomial for monomial, _coefficient in terms)
        elif word not in ((0,) * 8, (1,) * 8) and terms:
            mixed_rows.append((word, degree, terms))
            term_profile[len(terms)] += 1
            singleton_rows += int(len(terms) == 1)
    lines = ["(set-logic QF_LIA)", "(set-option :produce-models true)"]
    for item in sorted(atoms):
        lines.append(f"(declare-fun {atom_name(item)} () Bool)")
    seed = tuple(SEEDS[LABEL])
    for item in seed:
        lines.append(f"(assert {atom_name(item)})")
    for monomial in pure_early:
        lines.append(f"(assert (not {activation(monomial)}))")
    for _word, _degree, terms in mixed_rows:
        acts = [activation(monomial) for monomial, _coefficient in terms]
        if len(acts) == 1:
            lines.append(f"(assert (not {acts[0]}))")
        else:
            count = " ".join(f"(ite {active} 1 0)" for active in acts)
            lines.append(f"(assert (not (= (+ {count}) 1)))")
    objective = " ".join(f"(ite {atom_name(item)} 1 0)" for item in sorted(atoms))
    if args.max_live is not None:
        lines.append(f"(assert (<= (+ {objective}) {args.max_live}))")
    if args.satisfy_only:
        lines.extend(["(check-sat)", "(get-model)", "(exit)"])
    else:
        lines.extend([
            f"(minimize (+ {objective}))",
            "(check-sat)",
            "(get-objectives)",
            "(get-model)",
            "(exit)",
        ])
    args.output.write_text("\n".join(lines) + "\n")
    manifest = {
        "branch": LABEL,
        "mutation_raw_matching_terms": args.raw_matching_terms,
        "satisfy_only": args.satisfy_only,
        "max_live": args.max_live,
        "boolean_atoms": len(atoms),
        "fixed_seed_atoms": [atom_name(item) for item in seed],
        "literal_polynomial_rows": len(polynomials),
        "mixed_rows": len(mixed_rows),
        "mixed_singleton_rows": singleton_rows,
        "early_pure_monomials": len(pure_early),
        "raw_matching_terms_generated": raw_count,
        "mixed_term_count_profile": {str(k): v for k, v in sorted(term_profile.items())},
        "smt_bytes": len(("\n".join(lines) + "\n").encode()),
        "scope": "all binary words and every coefficient of tail valuation 0..7",
        "guard": "SAT is support feasibility only; UNSAT is complete for the fixed 1222-k4 seed and valuation cap.",
    }
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
