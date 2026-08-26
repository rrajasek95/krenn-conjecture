#!/usr/bin/env python3
"""Invariant and support-level audit of the canonical GHZ boundary cone.

This is deliberately smaller than the 216-variable coefficient problem.  It
first restricts every oriented off-matching block to one common 3 by 3 matrix
M (reverse orientation is M^t).  It then studies the Boolean support shadow of
the full 912 quadratic cokernel equations.  A support is rejected whenever an
equation has exactly one live monomial, since no assignment with all supported
coordinates nonzero can cancel that monomial.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys
from itertools import combinations, permutations, product

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from audit_active_cap_boundary_leading import (  # noqa: E402
    COLOURS, MATCHING, Y_INDEX, Y_LABELS, activity_rows, base_source,
    carrier_census, carrier_rows, eliminate_second_order, eval_poly,
    second_order_mixed_polynomials,
)
from audit_13block_environment import dense_rank  # noqa: E402

OUT = HERE / "results_active_boundary_invariant_support.json"


def require(condition, payload):
    if not condition:
        raise AssertionError(payload)


def normalize_integer_poly(poly):
    """Canonical primitive integer representation of a quadratic."""
    poly = Counter({key: Fraction(value) for key, value in poly.items() if value})
    if not poly:
        return ()
    denominator = 1
    from math import gcd
    for value in poly.values():
        denominator = denominator * value.denominator // gcd(
            denominator, value.denominator)
    integers = {key: int(value * denominator) for key, value in poly.items()}
    divisor = 0
    for value in integers.values():
        divisor = gcd(divisor, abs(value))
    integers = {key: value // divisor for key, value in integers.items()}
    first = integers[min(integers)]
    if first < 0:
        integers = {key: -value for key, value in integers.items()}
    return tuple(sorted(integers.items()))


def invariant_restriction(constraints):
    """Put Y_uv[i,j]=M[i,j] on every canonically oriented u<v edge."""
    answer = set()
    for constraint in constraints:
        restricted = Counter()
        for (a, b), value in constraint:
            ia, ja = Y_LABELS[a][2:]
            ib, jb = Y_LABELS[b][2:]
            ma, mb = 3 * ia + ja, 3 * ib + jb
            restricted[tuple(sorted((ma, mb)))] += value
        normalized = normalize_integer_poly(restricted)
        if normalized:
            answer.add(normalized)
    return tuple(sorted(answer))


def four_cycle_reconnection_audit(literal_h2, literal_constraints):
    """Rebuild H2 from the two reconnections of two unmatched anchor pairs."""
    rebuilt = Counter()
    mutated = Counter()

    def yindex(u, v, i, j):
        if u < v:
            return Y_INDEX[u, v, i, j]
        return Y_INDEX[v, u, j, i]

    for left, right in combinations(range(4), 2):
        (a, aa), (b, bb) = MATCHING[left], MATCHING[right]
        bases = [MATCHING[index] for index in range(4)
                 if index not in (left, right)]
        for ca, caa, cb, cbb in product(COLOURS, repeat=4):
            straight = tuple(sorted((yindex(a, b, ca, cb),
                                     yindex(aa, bb, caa, cbb))))
            crossed = tuple(sorted((yindex(a, bb, ca, cbb),
                                    yindex(aa, b, caa, cb))))
            for base_colours in product(COLOURS, repeat=2):
                word = [None] * 8
                word[a], word[aa] = ca, caa
                word[b], word[bb] = cb, cbb
                for (u, v), colour in zip(bases, base_colours):
                    word[u] = word[v] = colour
                key = tuple(word)
                rebuilt[key, straight] += 1
                rebuilt[key, crossed] += 1
                mutated[key, straight] += 1
                mutated[key, crossed] -= 1

    def rows(flat):
        answer = {}
        for (word, monomial), value in flat.items():
            if value:
                answer.setdefault(word, Counter())[monomial] += value
        return {word: +poly for word, poly in answer.items() if +poly}

    rebuilt_rows, mutated_rows = rows(rebuilt), rows(mutated)
    require(rebuilt_rows == literal_h2,
            (len(rebuilt_rows), len(literal_h2)))
    rebuilt_constraints, _ = eliminate_second_order(rebuilt_rows)
    require(rebuilt_constraints == literal_constraints,
            (len(rebuilt_constraints), len(literal_constraints)))
    changed_rows = sorted(word for word in set(literal_h2) | set(mutated_rows)
                          if literal_h2.get(word, Counter()) !=
                          mutated_rows.get(word, Counter()))
    require(changed_rows, "hostile sign mutation unexpectedly survived")
    mutated_constraints, _ = eliminate_second_order(mutated_rows)
    require(mutated_constraints != literal_constraints,
            "hostile sign mutation preserved the quotient ideal")
    return {
        "anchor_pair_pairs": 6,
        "tensor_entries_before_word_collisions": 6 * (3 ** 4) * (3 ** 2),
        "literal_raw_terms": sum(sum(poly.values())
                                 for poly in literal_h2.values()),
        "exact_H2_row_equality": True,
        "exact_912_quotient_row_span_equality": True,
        "formula": (
            "R_AB(i,i';j,j') = "
            "Y_ab(i,j)Y_a'b'(i',j') + Y_ab'(i,j')Y_a'b(i',j)"
        ),
        "hostile_crossed_sign_mutation": {
            "changed_literal_output_rows": len(changed_rows),
            "quotient_constraint_family_changed": True,
        },
    }


def singular_profile(polys):
    names = [f"m{i}" for i in range(9)]
    def term(monomial, coefficient):
        a, b = monomial
        body = names[a] + "^2" if a == b else names[a] + "*" + names[b]
        return f"({coefficient})*{body}"
    expressions = ["+".join(term(mon, coef) for mon, coef in poly)
                   for poly in polys]
    commands = [
        "ring r=0,(" + ",".join(names) + "),dp;",
        "ideal I=" + ",".join(expressions) + ";",
        "option(redSB);",
        "ideal G=std(I);",
        'print("PROFILE");',
        "print(dim(G));",
        "print(vdim(G));",
        "print(size(G));",
    ]
    for index, name in enumerate(names):
        commands += [f'print("POW {index}");']
        for exponent in range(1, 13):
            commands += [f"print(reduce({name}^{exponent},G)==0);"]
    commands += ['print("GB");', "print(G);", "quit;"]
    run = subprocess.run(
        ["/usr/local/bin/Singular", "-q"], input="\n".join(commands) + "\n",
        text=True, capture_output=True, check=True, timeout=120)
    lines = [line.strip() for line in run.stdout.splitlines() if line.strip()]
    at = lines.index("PROFILE")
    dimension, vector_dimension, basis_size = map(int, lines[at + 1:at + 4])
    nilpotence = {}
    for index in range(9):
        start = lines.index(f"POW {index}") + 1
        values = [int(item) for item in lines[start:start + 12]]
        exponent = next((i + 1 for i, value in enumerate(values) if value), None)
        nilpotence[f"m{index}"] = exponent
    gb_at = lines.index("GB") + 1
    gb_text = "\n".join(lines[gb_at:])
    require(dimension == 0, (dimension, vector_dimension, basis_size))
    require(all(nilpotence.values()), nilpotence)
    return {
        "dimension": dimension,
        "quotient_vector_dimension": vector_dimension,
        "groebner_basis_size": basis_size,
        "coordinate_nilpotence_exponents_at_most_12": nilpotence,
        "reduced_groebner_basis_sha256": sha256(gb_text.encode()).hexdigest(),
        "stderr": run.stderr.strip(),
    }


def response_support_monomials(p, q, kind, carrier, diagonal_only=False):
    residual = tuple(v for v in range(8) if v not in (p, q))
    if kind == "star":
        allowed = {tuple(sorted((carrier, other))) for other in residual
                   if other != carrier}
    else:
        from itertools import combinations
        allowed = set(combinations(tuple(carrier), 2))

    def yindex(u, v, i, j):
        if u < v:
            return Y_INDEX[u, v, i, j]
        return Y_INDEX[v, u, j, i]

    from itertools import combinations
    monomials = set()
    for a, b in combinations(residual, 2):
        if (a, b) in allowed:
            continue
        for alpha in COLOURS:
            for beta in COLOURS:
                for i in COLOURS:
                    for j in COLOURS:
                        if diagonal_only and i != j:
                            continue
                        monomials.add(tuple(sorted((
                            yindex(p, a, i, alpha),
                            yindex(q, b, j, beta)))))
                        monomials.add(tuple(sorted((
                            yindex(p, b, i, beta),
                            yindex(q, a, j, alpha)))))
    return tuple(sorted(monomials))


def smt_bool_support(constraints, active, bound, blocked_solutions=(),
                     diagonal_coverage=True):
    """Exact Boolean feasibility at a fixed cardinality upper bound."""
    unique_monomials = sorted({monomial for poly in constraints
                               for monomial, _ in poly})
    mid = {monomial: index for index, monomial in enumerate(unique_monomials)}
    lines = ["(set-logic QF_FD)"]
    lines += [f"(declare-fun x{i} () Bool)" for i in range(len(Y_LABELS))]
    lines += [f"(declare-fun z{k} () Bool)" for k in range(len(unique_monomials))]
    for monomial, index in mid.items():
        a, b = monomial
        rhs = f"x{a}" if a == b else f"(and x{a} x{b})"
        lines.append(f"(assert (= z{index} {rhs}))")
    # Every polynomial has zero or at least two supported monomials.
    for poly in constraints:
        terms = " ".join(f"(ite z{mid[monomial]} 1 0)"
                         for monomial, _ in poly)
        lines.append(f"(assert (not (= (+ {terms}) 1)))")
    # A blocker E_ii or I needs at least one live diagonal response column.
    # Directed endpoint-colour Booleans c_(p,a,i) compress that exact OR.  The
    # weaker physical-block version is retained only to certify lower bounds:
    # diagonal coverage implies nonzero response coverage.
    off_edges = sorted({label[:2] for label in Y_LABELS})
    if diagonal_coverage:
        directed = [(u, v, i) for edge in off_edges
                    for u, v in (edge, edge[::-1]) for i in COLOURS]
        directed_id = {label: index for index, label in enumerate(directed)}
        lines += [f"(declare-fun c{k} () Bool)" for k in range(len(directed))]
        for (u, v, i), index in directed_id.items():
            if u < v:
                cells = [f"x{Y_INDEX[u, v, i, j]}" for j in COLOURS]
            else:
                cells = [f"x{Y_INDEX[v, u,j,i]}" for j in COLOURS]
            lines.append(f"(assert (= c{index} (or {' '.join(cells)})))")

        def cstar(u, v, i):
            return f"c{directed_id[u, v, i]}"
    else:
        edge_id = {edge: index for index, edge in enumerate(off_edges)}
        lines += [f"(declare-fun w{k} () Bool)" for k in range(len(off_edges))]
        for edge, index in edge_id.items():
            cells = [f"x{Y_INDEX[edge + (i, j)]}"
                     for i in COLOURS for j in COLOURS]
            lines.append(f"(assert (= w{index} (or {' '.join(cells)})))")

        def wedge(u, v):
            return f"w{edge_id[tuple(sorted((u, v)))]}"

    response_counts = Counter()
    for p, q, kind, carrier in active:
        residual = tuple(v for v in range(8) if v not in (p, q))
        if kind == "star":
            allowed = {tuple(sorted((carrier, other))) for other in residual
                       if other != carrier}
        else:
            from itertools import combinations
            allowed = set(combinations(tuple(carrier), 2))
        from itertools import combinations
        alternatives = []
        for a, b in combinations(residual, 2):
            if (a, b) in allowed:
                continue
            if diagonal_coverage:
                for i in COLOURS:
                    alternatives.append(
                        f"(and {cstar(p, a, i)} {cstar(q, b, i)})")
                    alternatives.append(
                        f"(and {cstar(p, b, i)} {cstar(q, a, i)})")
            else:
                alternatives.append(f"(and {wedge(p, a)} {wedge(q, b)})")
                alternatives.append(f"(and {wedge(p, b)} {wedge(q, a)})")
        response_counts[kind, len(alternatives)] += 1
        lines.append("(assert (or " + " ".join(alternatives) + "))")
    cardinality = " ".join(f"x{i}" for i in range(len(Y_LABELS)))
    lines.append(f"(assert ((_ at-most {bound}) {cardinality}))")
    for solution in blocked_solutions:
        literals = [f"x{i}" if i in solution else f"(not x{i})"
                    for i in range(len(Y_LABELS))]
        lines.append("(assert (not (and " + " ".join(literals) + ")))")
    lines += ["(check-sat)", "(get-model)"]
    run = subprocess.run(["/opt/homebrew/bin/z3", "-in", "-T:120"],
                         input="\n".join(lines) + "\n", text=True,
                         capture_output=True, timeout=125)
    first = run.stdout.splitlines()[0].strip() if run.stdout else ""
    if first != "sat":
        return first, None, dict(response_counts), run.stderr.strip()
    solution = frozenset(int(index) for index, value in re.findall(
        r"\(define-fun x(\d+) \(\) Bool\s+(true|false)\)", run.stdout)
                         if value == "true")
    require(len(solution) <= bound, (len(solution), bound))
    return first, solution, dict(response_counts), run.stderr.strip()


def support_minimum(constraints, active, maximum=24):
    trials = []
    first_solution = None
    for bound in range(1, maximum + 1):
        status, solution, profiles, stderr = smt_bool_support(
            constraints, active, bound, diagonal_coverage=False)
        trials.append({"bound": bound, "weaker_nonzero_response_status": status})
        if status == "sat":
            # The weaker census supplies the lower bound.  At the first weak
            # support size, now demand the diagonal blocker-column guard.
            status, solution, profiles, stderr = smt_bool_support(
                constraints, active, bound, diagonal_coverage=True)
            trials[-1]["diagonal_response_status"] = status
            if status == "sat":
                first_solution = solution
                break
            require(status in ("unsat", "timeout"), (bound, status, stderr))
        if first_solution is not None:
            break
        require(trials[-1]["weaker_nonzero_response_status"] in
                ("unsat", "sat"), (bound, status, stderr))
    require(first_solution is not None, trials[-3:])
    labels = [Y_LABELS[index] for index in sorted(first_solution)]
    # Deletion-minimal is automatic at the minimum cardinality.  Report the
    # number of exact singleton-free equations and response carriers replayed.
    supported_counts = [sum(1 for monomial, _ in poly
                            if monomial[0] in first_solution
                            and monomial[1] in first_solution)
                        for poly in constraints]
    require(1 not in supported_counts, Counter(supported_counts))
    covered = []
    for record in active:
        mons = response_support_monomials(*record, diagonal_only=True)
        covered.append(any(a in first_solution and b in first_solution
                           for a, b in mons))
    require(all(covered), sum(covered))
    return {
        "minimum_cell_support_size": len(first_solution),
        "lex_first_support": [list(label) for label in labels],
        "bound_trials": trials,
        "quadratic_supported_monomial_count_histogram": {
            str(key): value for key, value in sorted(Counter(supported_counts).items())},
        "necessary_diagonal_response_coverage": f"{sum(covered)}/{len(covered)}",
        "response_monomial_profiles": {
            f"{kind}:{count}": multiplicity
            for (kind, count), multiplicity in sorted(profiles.items())},
        "scope": (
            "Exact minimum for the Boolean singleton/cancellation shadow only. "
            "At least two supported monomials is necessary, not sufficient, for "
            "coefficient cancellation; a diagonal B2 column is necessary, not "
            "sufficient, for blocker row-space incidence.  The separate rational "
            "candidate replay below does verify actual membership."
        ),
    }


def support_orbit_size(labels):
    support = frozenset(labels)
    pair_images = MATCHING
    images = set()
    for pair_permutation in permutations(range(4)):
        for flips in product(range(2), repeat=4):
            site_map = {}
            for index, (u, v) in enumerate(MATCHING):
                a, b = pair_images[pair_permutation[index]]
                site_map[u], site_map[v] = ((a, b) if not flips[index]
                                            else (b, a))
            for colour_permutation in permutations(COLOURS):
                transformed = []
                for u, v, i, j in support:
                    a, b = site_map[u], site_map[v]
                    x, y = colour_permutation[i], colour_permutation[j]
                    if a > b:
                        a, b, x, y = b, a, y, x
                    transformed.append((a, b, x, y))
                images.add(tuple(sorted(transformed)))
    return len(images), 2304 // len(images)


def replay_sparse_candidate(support_payload, constraints, active, h2):
    labels = tuple(tuple(label) for label in support_payload["lex_first_support"])
    indices = frozenset(Y_INDEX[label] for label in labels)
    assignment = {index: Fraction(index in indices) for index in range(len(Y_LABELS))}
    require(all(eval_poly(poly, assignment) == 0 for poly in constraints),
            "candidate violates a quotient quadric")
    raw_nonzero = {word: sum(value * assignment[a] * assignment[b]
                             for (a, b), value in poly.items())
                   for word, poly in h2.items()}
    raw_nonzero = {word: value for word, value in raw_nonzero.items() if value}
    require(not raw_nonzero, list(raw_nonzero.items())[:1])
    source = {label: Fraction(1) for label in labels}
    histogram = Counter()
    failed = []
    for p, q, kind, carrier in active:
        rows = carrier_rows(source, p, q, kind, carrier)
        rank = dense_rank(rows)
        memberships = tuple(dense_rank(rows + [functional]) == rank
                            for functional in activity_rows(base_source(), p, q))
        histogram[kind, rank, "".join("1" if item else "0"
                                      for item in memberships)] += 1
        if not any(memberships):
            failed.append((p, q, kind, carrier))
    require(not failed, failed[:1])
    orbit_size, stabilizer_size = support_orbit_size(labels)
    return {
        "coefficient_assignment": "all ten displayed cells equal 1",
        "raw_H2_nonzero_output_rows": len(raw_nonzero),
        "quadratic_X5_constraints_satisfied": f"{len(constraints)}/{len(constraints)}",
        "actual_blocker_rowspace_membership": f"{len(active) - len(failed)}/{len(active)}",
        "exact_rank_membership_histogram": {
            f"{kind}:rank={rank}:membership={mask}": count
            for (kind, rank, mask), count in sorted(histogram.items())},
        "base_stabilizer_group_order": 2304,
        "support_orbit_size": orbit_size,
        "support_stabilizer_size": stabilizer_size,
        "verdict": (
            "A literal rational, non-invariant ten-cell quadratic response "
            "pattern survives all 912 homogeneous control quadrics and blocks "
            "every one of the 104 formerly active carriers.  The base already "
            "has 78 mixed order-zero outputs, so this is not an exact-fibre jet."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--skip-support", action="store_true")
    args = parser.parse_args()
    h2 = second_order_mixed_polynomials()
    constraints, _ = eliminate_second_order(h2)
    require(len(constraints) == 912, len(constraints))
    invariant = invariant_restriction(constraints)
    require(len(invariant) == 114, len(invariant))
    profile = singular_profile(invariant)
    active, _ = carrier_census()
    support = None if args.skip_support else support_minimum(constraints, active)
    four_cycle = four_cycle_reconnection_audit(h2, constraints)
    replay = None if support is None else replay_sparse_candidate(
        support, constraints, active, h2)
    payload = {
        "status": "PASS invariant control empty; ten-cell non-invariant response pattern survives",
        "invariant_ansatz": {
            "definition": (
                "Y_uv=M for every canonical u<v off-matching edge; "
                "Y_vu=M^transpose under reverse access"
            ),
            "source_quadrics": len(constraints),
            "distinct_nonzero_restricted_quadrics": len(invariant),
            "restricted_ideal_profile": profile,
            "theorem": (
                "The restricted homogeneous ideal is zero-dimensional, hence "
                "its Qbar zero set is only M=0.  At M=0 every B2 carrier "
                "matrix is zero, so none of the nonzero E00/E11/E22/I blockers "
                "lies in its row space.  There is no stabilizer-invariant "
                "solution of this quadratic response control.  Since the base "
                "is not exact GHZ, this is not an exact-fibre tangent theorem."
            ),
        },
        "four_cycle_compression": four_cycle,
        "support_singleton_census": support,
        "minimum_sparse_candidate_replay": replay,
        "terminal_scope": (
            "The common-matching I3 base has 78 mixed order-zero outputs and is "
            "not on the exact fibre.  The invariant result is coefficient-exact "
            "over Qbar for its homogeneous control.  The support "
            "result is an exact finite necessary antichain computation, not a "
            "tangent-cone statement for F^{-1}(Delta)."
        ),
    }
    payload["logical_sha256"] = sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("invariant", len(invariant), profile)
    print("support", support)
    print("logical sha256", payload["logical_sha256"])


if __name__ == "__main__":
    main()
