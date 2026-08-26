#!/usr/bin/env python3
"""Bounded sound CEGAR for the complete 1222-k4 support problem.

Each cut forbids only the support condition under which specified literal rows
have exactly the binomial monomials in an inconsistent Laurent circuit.  It
does not forbid their atoms when extra monomials make either row nonbinomial.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_balanced_base_oddset_luna import ONE  # noqa: E402
from audit_phase_m7_1222_k4_toric import parse_q  # noqa: E402
from audit_phase_m7_support_coefficients import replay_model  # noqa: E402
from emit_phase_m7_1222_k4_support_smt import build_polynomials  # noqa: E402
from screen_phase_m7_support import SEEDS  # noqa: E402


BASE_SMT = HERE / "phase_m7_1222_k4_support_exact_sat.smt2"
OUT = HERE / "results_phase_m7_1222_k4_cegar.json"
WORK_SMT = HERE / "phase_m7_1222_k4_support_cegar_current.smt2"
SMALL_CIRCUIT_BATCHES = (
    HERE / "results_phase_m7_1222_k4_cegar_iter14_small_circuits.json",
    HERE / "results_phase_m7_1222_k4_cegar_postbatch189_small_circuits.json",
    HERE / "results_phase_m7_1222_k4_cegar_postbatch779_small_circuits.json",
    HERE / "results_phase_m7_1222_k4_cegar_postbatch852_small_circuits.json",
    HERE / "results_phase_m7_1222_k4_cegar_postbatch1932_small_circuits.json",
    HERE / "results_phase_m7_1222_k4_cegar_postbatch2522_small_circuits.json",
    HERE / "results_phase_m7_1222_k4_cegar_postbatch3762_small_circuits.json",
    HERE / "results_phase_m7_1222_k4_cegar_postbatch3816_small_circuits.json",
    HERE / "results_phase_m7_1222_k4_cegar_postbatch3925_small_circuits.json",
)
LABEL = "1222_k4_C1222"
MODEL_PATTERN = re.compile(
    r"\(define-fun (x_[0-7]_[0-7]_[01]_[01]_[1-7]) \(\) Bool\s+(true|false)\)"
)
SOURCE_LABEL_PATTERN = re.compile(r"([0-7])([0-7]):([01])([01])@([1-7])")


def atom_name(item):
    return "x_%d_%d_%d_%d_%d" % item


def atom_tuple(name):
    return tuple(map(int, name.split("_")[1:]))


def source_label_to_atom_name(label):
    match = SOURCE_LABEL_PATTERN.fullmatch(label)
    if match is None:
        raise ValueError(label)
    return "x_" + "_".join(match.groups())


def term_names(monomial):
    return frozenset(atom_name(item) for item in monomial if item[4])


def activation(monomial):
    names = sorted(monomial)
    if len(names) == 1:
        return names[0]
    return f"(and {' '.join(names)})"


def qinv(value):
    a, b = value
    norm = a * a - a * b + b * b
    return (a - b) / norm, -b / norm


def qmul(left, right):
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c - b * d


def qneg(value):
    return -value[0], -value[1]


def qdiv(left, right):
    return qmul(left, qinv(right))


def qlabel(value):
    a, b = value
    pieces = []
    if a:
        pieces.append(str(a))
    if b:
        pieces.append(("+" if b > 0 and pieces else "") + str(b) + "*w")
    return "".join(pieces) or "0"


def model_support(stdout):
    return {name for name, value in MODEL_PATTERN.findall(stdout) if value == "true"}


def row_key(word, degree):
    return "".join(map(str, word)), degree


def cut_violated(cut, support, full_rows):
    for descriptor in cut["rows"]:
        key = (descriptor["word"], descriptor["degree"])
        active = {monomial for monomial in full_rows[key] if monomial <= support}
        desired = {frozenset(term) for term in descriptor["active_monomials"]}
        if active != desired:
            return False
    return True


def cut_smt(cut, full_rows):
    conditions = []
    for descriptor in cut["rows"]:
        key = (descriptor["word"], descriptor["degree"])
        desired = {frozenset(term) for term in descriptor["active_monomials"]}
        for monomial in desired:
            conditions.append(activation(monomial))
        for monomial in full_rows[key]:
            if monomial not in desired:
                conditions.append(f"(not {activation(monomial)})")
    return f"(assert (not (and {' '.join(conditions)})))"


def normalize_binomial(row, variables):
    index = {name: position for position, name in enumerate(variables)}
    left, right = row["terms"]
    vector = [0] * len(variables)
    for name in left["monomial"]:
        vector[index[name]] += 1
    for name in right["monomial"]:
        vector[index[name]] -= 1
    constant = qneg(qdiv(parse_q(right["coefficient"]),
                         parse_q(left["coefficient"])))
    first = next(value for value in vector if value)
    if first < 0:
        vector = [-value for value in vector]
        constant = qinv(constant)
    return tuple(vector), constant


def smallest_pair_circuit(replay):
    variables = replay["variables"]
    groups = defaultdict(list)
    for row in replay["equations"]:
        if len(row["terms"]) != 2:
            continue
        vector, constant = normalize_binomial(row, variables)
        groups[vector].append((constant, row))
    candidates = []
    for vector, entries in groups.items():
        for left_index in range(len(entries)):
            for right_index in range(left_index + 1, len(entries)):
                left_constant, left_row = entries[left_index]
                right_constant, right_row = entries[right_index]
                if left_constant == right_constant:
                    continue
                atoms = set(left_row["terms"][0]["monomial"])
                atoms.update(left_row["terms"][1]["monomial"])
                atoms.update(right_row["terms"][0]["monomial"])
                atoms.update(right_row["terms"][1]["monomial"])
                candidates.append((len(atoms), left_row["degree"] + right_row["degree"],
                                   left_row["word"], right_row["word"], vector,
                                   left_constant, right_constant, left_row, right_row))
    if not candidates:
        return None
    candidate = min(candidates)
    (_atom_count, _degree_sum, _left_word, _right_word, vector,
     left_constant, right_constant, left_row, right_row) = candidate
    return {
        "kind": "equal-exponent unequal-constant binomial pair",
        "normalized_exponent": list(vector),
        "left_constant": qlabel(left_constant),
        "right_constant": qlabel(right_constant),
        "rows": [
            {
                "word": row["word"], "degree": row["degree"],
                "active_monomials": [
                    [source_label_to_atom_name(name) for name in term["monomial"]]
                    for term in row["terms"]
                ],
                "equation_terms": row["terms"],
            }
            for row in (left_row, right_row)
        ],
    }


def greedy_shrink(selected, seed, rows, cuts, full_rows):
    # Literal row counts for exact deletion updates.
    active = []
    active_rows = []
    by_atom = defaultdict(list)
    row_counts = []
    for row_index, (_key, monomials) in enumerate(rows):
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
            if any(row_counts[row] - amount == 1 for row, amount in decrement.items()):
                continue
            trial = selected - {name}
            if any(cut_violated(cut, trial, full_rows) for cut in cuts):
                continue
            selected = trial
            changed = True
            for index in impacted:
                active[index] = False
                row_counts[active_rows[index]] -= 1
    return selected, passes


def initial_cut():
    return {
        "kind": "equal-exponent unequal-constant binomial pair",
        "left_constant": "-1",
        "right_constant": "1+1*w",
        "rows": [
            {"word": "00000100", "degree": 2, "active_monomials": [
                ["x_1_4_0_0_1", "x_2_5_0_1_1"],
                ["x_2_5_0_1_1", "x_3_7_0_0_1"],
            ]},
            {"word": "10000100", "degree": 2, "active_monomials": [
                ["x_0_5_1_1_1", "x_1_4_0_0_1"],
                ["x_0_5_1_1_1", "x_3_7_0_0_1"],
            ]},
        ],
    }


def second_cut():
    """Three-row SNF circuit from the first post-cut SAT support."""
    def x(label):
        return source_label_to_atom_name(label)
    return {
        "kind": "three-binomial SNF constant-failure circuit",
        "product_constant": "-1",
        "rows": [
            {"word": "10010110", "degree": 2, "active_monomials": [
                [x("05:11@1"), x("36:11@1")],
                [x("06:11@1"), x("35:11@1")],
            ]},
            {"word": "10011010", "degree": 2, "active_monomials": [
                [x("04:11@1"), x("36:11@1")],
                [x("06:11@1"), x("34:11@1")],
            ]},
            {"word": "11011100", "degree": 3, "active_monomials": [
                [x("04:11@1"), x("12:10@1"), x("35:11@1")],
                [x("05:11@1"), x("12:10@1"), x("34:11@1")],
            ]},
        ],
    }


def third_cut():
    """Three-row SNF circuit from the second post-cut SAT support."""
    def x(label):
        return source_label_to_atom_name(label)
    return {
        "kind": "three-binomial SNF constant-failure circuit",
        "product_constant": "-1",
        "rows": [
            {"word": "01000100", "degree": 2, "active_monomials": [
                [x("05:01@1"), x("14:10@1")],
                [x("05:01@1"), x("17:10@1")],
            ]},
            {"word": "01010000", "degree": 2, "active_monomials": [
                [x("14:10@1"), x("37:10@1")],
                [x("15:10@1"), x("37:10@1")],
            ]},
            {"word": "11101000", "degree": 3, "active_monomials": [
                [x("04:11@1"), x("15:10@1"), x("23:10@1")],
                [x("04:11@1"), x("17:10@1"), x("23:10@1")],
            ]},
        ],
    }


def fourth_cut():
    """Three-row SNF circuit from the third post-cut SAT support."""
    def x(label):
        return source_label_to_atom_name(label)
    return {
        "kind": "three-binomial SNF constant-failure circuit",
        "product_constant": "-1",
        "rows": [
            {"word": "00100000", "degree": 1, "active_monomials": [
                [x("02:01@1")], [x("23:10@1")],
            ]},
            {"word": "00100101", "degree": 3, "active_monomials": [
                [x("02:01@1"), x("17:01@1"), x("35:01@1")],
                [x("24:10@1"), x("35:01@1"), x("67:01@1")],
            ]},
            {"word": "10100101", "degree": 3, "active_monomials": [
                [x("05:11@1"), x("17:01@1"), x("23:10@1")],
                [x("05:11@1"), x("24:10@1"), x("67:01@1")],
            ]},
        ],
    }


def fifth_cut():
    """Three-row SNF circuit from the fourth post-cut SAT support."""
    def x(label):
        return source_label_to_atom_name(label)
    return {
        "kind": "three-binomial SNF constant-failure circuit",
        "product_constant": "-1",
        "rows": [
            {"word": "00111100", "degree": 2, "active_monomials": [
                [x("24:11@1"), x("35:11@1")],
                [x("25:11@1"), x("34:11@1")],
            ]},
            {"word": "01011110", "degree": 3, "active_monomials": [
                [x("17:10@1"), x("34:11@1"), x("56:11@1")],
                [x("17:10@1"), x("35:11@1"), x("46:11@1")],
            ]},
            {"word": "00101111", "degree": 4, "active_monomials": [
                [x("24:11@1"), x("37:01@2"), x("56:11@1")],
                [x("25:11@1"), x("37:01@2"), x("46:11@1")],
            ]},
        ],
    }


def sixth_cut():
    """Three-row SNF circuit from the fifth post-cut SAT support."""
    def x(label):
        return source_label_to_atom_name(label)
    return {
        "kind": "three-binomial SNF constant-failure circuit",
        "product_constant": "-1",
        "rows": [
            {"word": "01010100", "degree": 2, "active_monomials": [
                [x("14:10@1"), x("35:11@1")],
                [x("17:10@1"), x("35:11@1")],
            ]},
            {"word": "01011000", "degree": 2, "active_monomials": [
                [x("15:10@1"), x("34:11@1")],
                [x("17:10@1"), x("34:11@1")],
            ]},
            {"word": "11000001", "degree": 4, "active_monomials": [
                [x("02:10@1"), x("14:10@1"), x("37:01@2")],
                [x("02:10@1"), x("15:10@1"), x("37:01@2")],
            ]},
        ],
    }


def seventh_cut():
    """Three-row SNF circuit from the sixth post-cut SAT support."""
    def x(label):
        return source_label_to_atom_name(label)
    return {
        "kind": "three-binomial SNF constant-failure circuit",
        "product_constant": "-1",
        "rows": [
            {"word": "00000011", "degree": 2, "active_monomials": [
                [x("16:01@1"), x("27:01@1")],
                [x("16:01@1"), x("37:01@1")],
            ]},
            {"word": "01010101", "degree": 3, "active_monomials": [
                [x("01:01@1"), x("27:01@1"), x("35:11@1")],
                [x("14:10@1"), x("35:11@1"), x("67:01@1")],
            ]},
            {"word": "01100101", "degree": 3, "active_monomials": [
                [x("01:01@1"), x("25:11@1"), x("37:01@1")],
                [x("14:10@1"), x("25:11@1"), x("67:01@1")],
            ]},
        ],
    }


def eighth_cut():
    """Three-row SNF circuit from the seventh post-cut SAT support."""
    def x(label):
        return source_label_to_atom_name(label)
    return {
        "kind": "three-binomial SNF constant-failure circuit",
        "product_constant": "-1",
        "rows": [
            {"word": "00111100", "degree": 2, "active_monomials": [
                [x("24:11@1"), x("35:11@1")],
                [x("25:11@1"), x("34:11@1")],
            ]},
            {"word": "10011100", "degree": 2, "active_monomials": [
                [x("04:11@1"), x("35:11@1")],
                [x("05:11@1"), x("34:11@1")],
            ]},
            {"word": "11111100", "degree": 4, "active_monomials": [
                [x("04:11@1"), x("17:10@1"), x("25:11@1"), x("36:10@1")],
                [x("05:11@1"), x("17:10@1"), x("24:11@1"), x("36:10@1")],
            ]},
        ],
    }


def ninth_cut():
    """Three-row SNF circuit from the eighth post-cut SAT support."""
    def x(label):
        return source_label_to_atom_name(label)
    return {
        "kind": "three-binomial SNF constant-failure circuit",
        "product_constant": "-1",
        "rows": [
            {"word": "01000100", "degree": 2, "active_monomials": [
                [x("14:10@1"), x("35:01@1")],
                [x("17:10@1"), x("35:01@1")],
            ]},
            {"word": "01001000", "degree": 2, "active_monomials": [
                [x("15:10@1"), x("24:01@1")],
                [x("17:10@1"), x("24:01@1")],
            ]},
            {"word": "11010001", "degree": 4, "active_monomials": [
                [x("02:10@1"), x("14:10@1"), x("37:11@2")],
                [x("02:10@1"), x("15:10@1"), x("37:11@2")],
            ]},
        ],
    }


def tenth_cut():
    """Two-row equal-exponent circuit from the ninth post-cut SAT support."""
    def x(label):
        return source_label_to_atom_name(label)
    return {
        "kind": "equal-exponent unequal-constant binomial pair",
        "left_constant": "-1",
        "right_constant": "-1*w",
        "rows": [
            {"word": "00011000", "degree": 2, "active_monomials": [
                [x("15:00@1"), x("34:11@1")],
                [x("27:00@1"), x("34:11@1")],
            ]},
            {"word": "10000010", "degree": 2, "active_monomials": [
                [x("06:11@1"), x("15:00@1")],
                [x("06:11@1"), x("27:00@1")],
            ]},
        ],
    }


def eleventh_cut():
    """Three-row SNF circuit from the tenth post-cut SAT support."""
    def x(label):
        return source_label_to_atom_name(label)
    return {
        "kind": "three-binomial SNF constant-failure circuit",
        "product_constant": "-1",
        "rows": [
            {"word": "10010100", "degree": 2, "active_monomials": [
                [x("05:11@1"), x("34:10@1")],
                [x("05:11@1"), x("37:10@1")],
            ]},
            {"word": "10011000", "degree": 2, "active_monomials": [
                [x("04:11@1"), x("35:10@1")],
                [x("04:11@1"), x("37:10@1")],
            ]},
            {"word": "10010001", "degree": 3, "active_monomials": [
                [x("07:11@2"), x("34:10@1")],
                [x("07:11@2"), x("35:10@1")],
            ]},
        ],
    }


def twelfth_cut():
    """Three-row SNF circuit from the eleventh post-cut SAT support."""
    def x(label):
        return source_label_to_atom_name(label)
    return {
        "kind": "three-binomial SNF constant-failure circuit",
        "product_constant": "-1",
        "rows": [
            {"word": "00000110", "degree": 2, "active_monomials": [
                [x("06:01@1"), x("15:01@1")],
                [x("15:01@1"), x("26:01@1")],
            ]},
            {"word": "00001010", "degree": 2, "active_monomials": [
                [x("06:01@1"), x("24:01@1")],
                [x("16:01@1"), x("24:01@1")],
            ]},
            {"word": "10000110", "degree": 2, "active_monomials": [
                [x("05:11@1"), x("16:01@1")],
                [x("05:11@1"), x("26:01@1")],
            ]},
        ],
    }


def thirteenth_cut():
    """Two-row equal-exponent circuit from the twelfth post-cut SAT support."""
    def x(label):
        return source_label_to_atom_name(label)
    return {
        "kind": "equal-exponent unequal-constant binomial pair",
        "left_constant": "-1/3",
        "right_constant": "-1",
        "rows": [
            {"word": "11000000", "degree": 3, "active_monomials": [
                [x("02:10@1"), x("13:10@2")],
                [x("07:10@1"), x("14:10@2")],
            ]},
            {"word": "11000100", "degree": 7, "active_monomials": [
                [x("02:10@1"), x("13:10@2"), x("56:10@4")],
                [x("07:10@1"), x("14:10@2"), x("56:10@4")],
            ]},
        ],
    }


def fourteenth_cut():
    """Two-row magnitude circuit from the thirteenth post-cut SAT support."""
    def x(label):
        return source_label_to_atom_name(label)
    return {
        "kind": "equal-exponent unequal-constant binomial pair",
        "left_constant": "-1/3",
        "right_constant": "-1",
        "rows": [
            {"word": "11000000", "degree": 3, "active_monomials": [
                [x("02:10@1"), x("13:10@2")],
                [x("07:10@1"), x("14:10@2")],
            ]},
            {"word": "11000000", "degree": 4, "active_monomials": [
                [x("02:10@1"), x("13:10@2"), x("56:00@1")],
                [x("07:10@1"), x("14:10@2"), x("56:00@1")],
            ]},
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    polynomials, _raw = build_polynomials(False)
    full_rows = {
        row_key(word, degree): tuple(term_names(monomial) for monomial, _coefficient in terms)
        for (word, degree), terms in polynomials.items()
        if word not in ((0,) * 8, (1,) * 8) and terms
    }
    rows = sorted(full_rows.items(), key=lambda item: (item[0][1], item[0][0]))
    seed = {atom_name(item) for item in SEEDS[LABEL]}
    cuts = [initial_cut(), second_cut(), third_cut(), fourth_cut(), fifth_cut(), sixth_cut(), seventh_cut(), eighth_cut(), ninth_cut(), tenth_cut(), eleventh_cut(), twelfth_cut(), thirteenth_cut(), fourteenth_cut()]
    small_batch = []
    for path in SMALL_CIRCUIT_BATCHES:
        small_batch.extend(json.loads(path.read_text())["circuits"])
    cuts.extend(small_batch)
    initial_cut_count = len(cuts)
    iterations = []
    base = BASE_SMT.read_text()
    terminal = "batch exhausted"

    for iteration in range(args.iterations):
        assertions = "\n".join(cut_smt(cut, full_rows) for cut in cuts)
        smt = base.replace("(check-sat)", assertions + "\n(check-sat)", 1)
        WORK_SMT.write_text(smt)
        try:
            completed = subprocess.run(
                ["z3", "-smt2", WORK_SMT.name], cwd=HERE,
                capture_output=True, text=True, timeout=args.timeout, check=False,
            )
        except subprocess.TimeoutExpired:
            iterations.append({"iteration": iteration + 1, "status": "timeout",
                               "cuts_before_solve": len(cuts)})
            terminal = "solver timeout"
            break
        first_line = completed.stdout.splitlines()[0] if completed.stdout else ""
        if first_line == "unsat":
            iterations.append({"iteration": iteration + 1, "status": "unsat",
                               "cuts_before_solve": len(cuts)})
            terminal = "UNSAT"
            break
        if first_line != "sat":
            iterations.append({"iteration": iteration + 1, "status": "solver error",
                               "stdout_head": completed.stdout[:200],
                               "stderr_head": completed.stderr[:200]})
            terminal = "solver error"
            break
        dense = model_support(completed.stdout)
        support, passes = greedy_shrink(set(dense), seed, rows, cuts, full_rows)
        replay = replay_model(frozenset(atom_tuple(name) for name in support))
        circuit = smallest_pair_circuit(replay)
        record = {
            "iteration": iteration + 1,
            "status": "sat",
            "cuts_before_solve": len(cuts),
            "dense_live_atoms": len(dense),
            "inclusion_minimal_live_atoms": len(support),
            "greedy_passes": passes,
            "mixed_equations": replay["mixed_equation_count"],
            "term_profile": replay["mixed_term_count_profile"],
            "pure7_terms": replay["pure7_term_count"],
            "support": sorted(support),
            "pair_circuit": circuit,
        }
        iterations.append(record)
        if circuit is None:
            terminal = "pair-circuit-free coefficient target"
            break
        cuts.append(circuit)

    output = {
        "scope": "complete 696-Boolean fixed 1222-k4 support problem",
        "sound_cut_guard": (
            "Each cut requires exactly the active binomial monomials in every "
            "circuit row; supports activating any extra row monomial are not cut."
        ),
        "seed_stabilizer_order": 1,
        "initial_cuts": initial_cut_count,
        "batched_small_circuits": len(small_batch),
        "iterations": iterations,
        "cuts_after_batch": cuts,
        "distinct_circuit_orbits": len(cuts),
        "terminal": terminal,
    }
    OUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "terminal": terminal,
        "iterations": [
            {key: record.get(key) for key in (
                "iteration", "status", "cuts_before_solve", "dense_live_atoms",
                "inclusion_minimal_live_atoms", "mixed_equations", "pure7_terms",
            )}
            for record in iterations
        ],
        "circuit_orbits": len(cuts),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
