#!/usr/bin/env python3
"""Pair-cap closure for the round-1 four-extra-cell varied-q census.

Input region (from search_n8_varied_q_round_1_census.py): quadruples
e1<e2<e3<e4 of cells outside supp(q) such that

    z*(q + t1*e1 + t2*e2 + t3*e3 + t4*e4)^[3] = Delta_{8,3}       (*)

has solutions with t in (C^*)^4 -- either identically (the 1,222,812
compatible quadruples) or on the explicit cancellation locus of the
10,611 cancellation families.  For every such family this driver decides
whether the pair-cap preimage can exist on the locus:

    (a*Q + 4*p*s) * Q^[3] = Delta_{8,3},   Q = q + sum_i t_i e_i,   (**)

for a scalar a and site-linear forms p, s.  Writing (**) as
4*p*s*Q^[3] + 4*a*Q^[4] = Delta, the driver first applies the
parameter-safe projective Gram-parity argument of the recorded two- and
three-cell rounds, extended to four tags:

  * a non-target coordinate with no Q^[4] term and exactly one tagged Gram
    contributor m(t)*beta(x_X, x_Y) forces beta(x_X, x_Y) = 0, because the
    Laurent monomial m is nonzero on the torus;
  * each pure target coordinate with no Q^[4] term needs a nonzero Gram
    contributor; the driver branches over the finite contributor list;
  * an odd zero path between the endpoints of a required-nonzero edge, or
    an odd zero cycle in their component, is contradictory on projective
    lines of C^2 with the polarization form beta((r,w),(r',w')) = rw'+wr'.

Families not closed by parity go to saturated characteristic-zero ideals:
all top-word coordinates of (**) over Q, the cancellation-locus equations
of the family (none for compatible quadruples), and the torus localization
h*t1*t2*t3*t4 = 1, in the 54 variables p, s, a, t1..t4, h.  A Groebner
basis equal to [1] excludes the family exactly over C; any non-unit ideal
is reported as a candidate hit for lifting.

Because a = 1/4, p = s = 0 turns (**) into Q^[4] = Delta_{8,3}, every
exclusion also excludes the literal unrestricted aggregate system
H_8(A) = Delta_{8,3} on the family.  The driver additionally records the
free support-level test of that direct aggregate system (base
q^[4] = e_11000000 + e_22212111, so both padding words need a tagged
cancellation and all three pure words need tagged support).

Large per-family ledgers are written to --scratch-dir, never to the
repository.  The repository output is a small JSON summary.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
from itertools import combinations, product
import json
from multiprocessing import Pool
import os
import shutil
import subprocess
import time

SITES = tuple(range(8))
COLOURS = (0, 1, 2)
EDGES = tuple(combinations(SITES, 2))
ALL_CELLS = tuple(
    (left, right, left_colour, right_colour)
    for left, right in EDGES
    for left_colour, right_colour in product(COLOURS, repeat=2)
)
BASE_Q = (
    (2, 3, 0, 0), (4, 5, 0, 0), (6, 7, 0, 0),
    (0, 1, 1, 1), (3, 6, 1, 1), (5, 7, 1, 1),
    (0, 2, 2, 2), (1, 4, 2, 2), (5, 6, 2, 2),
)
DISPLAYED_Z = ((0, 1, 0, 0), (2, 4, 1, 1), (3, 7, 2, 2))
PURE_WORDS = tuple((colour,) * 8 for colour in COLOURS)
DELTA_WORDS = frozenset(PURE_WORDS)
PADDING_WORDS = ((1, 1, 0, 0, 0, 0, 0, 0), (2, 2, 2, 1, 2, 1, 1, 1))
EXTRAS = tuple(cell for cell in ALL_CELLS if cell not in BASE_Q)

TAG_MONOMIAL = {0: ""}
for _mask in range(1, 16):
    TAG_MONOMIAL[_mask] = "*".join(
        name for bit, name in enumerate(("t1", "t2", "t3", "t4")) if _mask >> bit & 1
    )


def cells_are_disjoint(cells):
    endpoints = tuple(site for cell in cells for site in cell[:2])
    return len(endpoints) == len(set(endpoints))


def partial_word(cells):
    word = [-1] * 8
    for left, right, left_colour, right_colour in cells:
        word[left] = left_colour
        word[right] = right_colour
    return tuple(word)


def tagged_forms(quad_cells):
    """The p*s*Q^[3] Gram forms and the Q^[4] terms, tagged by extra subset."""
    weighted = tuple((cell, 0) for cell in BASE_Q) + tuple(
        (cell, 1 << position) for position, cell in enumerate(quad_cells)
    )
    forms = defaultdict(Counter)
    for chosen in combinations(weighted, 3):
        cells = tuple(item[0] for item in chosen)
        if not cells_are_disjoint(cells):
            continue
        tag = 0
        for _cell, item_tag in chosen:
            tag |= item_tag
        word = list(partial_word(cells))
        missing = tuple(index for index, value in enumerate(word) if value == -1)
        for first_colour, second_colour in product(COLOURS, repeat=2):
            full = list(word)
            full[missing[0]] = first_colour
            full[missing[1]] = second_colour
            edge = tuple(sorted((
                (missing[0], first_colour), (missing[1], second_colour)
            )))
            forms[tuple(full)][edge, tag] += 1

    q_four = defaultdict(Counter)
    for chosen in combinations(weighted, 4):
        cells = tuple(item[0] for item in chosen)
        if not cells_are_disjoint(cells):
            continue
        tag = 0
        for _cell, item_tag in chosen:
            tag |= item_tag
        q_four[partial_word(cells)][tag] += 1
    return dict(forms), dict(q_four)


def graph_certificate_kind(required, zero_edges):
    modes = frozenset(mode for edge in required for mode in edge)
    graph = {mode: set() for mode in modes}
    for left, right in zero_edges:
        if left in modes and right in modes:
            graph[left].add(right)
            graph[right].add(left)
    component = {}
    parity = {}
    bipartite = []
    for root in sorted(modes):
        if root in component:
            continue
        cid = len(bipartite)
        component[root] = cid
        parity[root] = 0
        queue = deque([root])
        is_bipartite = True
        while queue:
            vertex = queue.popleft()
            for neighbour in graph[vertex]:
                if neighbour not in component:
                    component[neighbour] = cid
                    parity[neighbour] = parity[vertex] ^ 1
                    queue.append(neighbour)
                elif parity[neighbour] == parity[vertex]:
                    is_bipartite = False
        bipartite.append(is_bipartite)
    for left, right in required:
        if component[left] != component[right]:
            continue
        if not bipartite[component[left]]:
            return "isotropic_component"
        if parity[left] != parity[right]:
            return "odd_zero_path"
    return None


def projective_closure(forms, q_four):
    pure_options = []
    for word in PURE_WORDS:
        if q_four.get(word):
            return False, 0, "pure_direct"
        edges = tuple(sorted({edge for edge, _tag in forms.get(word, {})}))
        if not edges:
            return False, 0, "pure_missing"
        pure_options.append(edges)
    zeros = set()
    for word, terms in forms.items():
        if word in DELTA_WORDS or q_four.get(word) or len(terms) != 1:
            continue
        (edge, _tag), coefficient = next(iter(terms.items()))
        assert coefficient > 0
        zeros.add(edge)
    branches = 0
    for required in product(*pure_options):
        branches += 1
        if graph_certificate_kind(required, zeros) is None:
            return False, branches, "open_branch"
    return True, branches, "closed"


def aggregate_support_status(q_four):
    """Support test of the direct aggregate system Q^[4] = Delta_{8,3}."""
    for word in PURE_WORDS:
        if not q_four.get(word):
            return "reject_pure_uncovered"
    for word in PADDING_WORDS:
        tags = q_four.get(word, {})
        assert tags.get(0) == 1
        if not any(tag for tag in tags):
            return "reject_padding_uncancellable"
    for word, tags in q_four.items():
        if word in DELTA_WORDS or word in PADDING_WORDS:
            continue
        if len(tags) == 1:
            return "reject_singleton"
    return "aggregate_support_survivor"


def close_quadruple(indices):
    quad_cells = tuple(EXTRAS[index] for index in indices)
    forms, q_four = tagged_forms(quad_cells)
    closed, branches, reason = projective_closure(forms, q_four)
    return tuple(indices), closed, branches, reason, aggregate_support_status(q_four)


def mode_variable(prefix, mode):
    return f"{prefix}{mode[0]}{mode[1]}"


def beta_expression(edge):
    left, right = edge
    return (
        f"({mode_variable('p', left)}*{mode_variable('s', right)}"
        f"+{mode_variable('s', left)}*{mode_variable('p', right)})"
    )


def ring_variables():
    return [
        mode_variable(prefix, (site, colour))
        for prefix in ("p", "s")
        for site in SITES
        for colour in COLOURS
    ] + ["a", "t1", "t2", "t3", "t4", "h"]


def append_term(terms, coefficient, factors):
    pieces = []
    if coefficient != 1:
        pieces.append(str(coefficient))
    pieces.extend(factor for factor in factors if factor)
    terms.append("*".join(pieces) if pieces else "1")


def singular_program(indices, locus_polynomials):
    """Saturated coordinate ideal of one family.

    Besides the literal top-word coordinates, the ideal includes the
    parameter-safe zero Gram entries derived exactly as in the projective
    pass: a non-target word with no Q^[4] term and a single tagged
    contributor m(t)*beta forces beta = 0.  Because the Laurent monomial
    m(t) is a unit modulo h*t1*t2*t3*t4 - 1, each such beta already lies in
    the saturated ideal generated by the coordinates, so adding it does not
    change the ideal; it only accelerates the Groebner run.  The basis is
    computed by slimgb.
    """
    quad_cells = tuple(EXTRAS[index] for index in indices)
    forms, q_four = tagged_forms(quad_cells)
    equations = []
    zeros = []
    for word in sorted(set(forms) | set(q_four) | set(DELTA_WORDS)):
        terms = []
        for (edge, tag), coefficient in sorted(forms.get(word, {}).items()):
            append_term(
                terms, 4 * coefficient, (TAG_MONOMIAL[tag], beta_expression(edge))
            )
        for tag, coefficient in sorted(q_four.get(word, {}).items()):
            append_term(terms, 4 * coefficient, ("a", TAG_MONOMIAL[tag]))
        if word in DELTA_WORDS:
            terms.append("-1")
        if terms:
            equations.append("+".join(terms))
        if (word not in DELTA_WORDS and not q_four.get(word)
                and len(forms.get(word, {})) == 1):
            (edge, _tag), _coefficient = next(iter(forms[word].items()))
            zeros.append(beta_expression(edge))
    equations.extend(sorted(set(zeros)))
    equations.extend(locus_polynomials)
    equations.append("h*t1*t2*t3*t4-1")
    variables = ring_variables()
    program = (
        f"ring r=0,({','.join(variables)}),dp;\n"
        f"ideal I={','.join(equations)};\n"
        "ideal G=slimgb(I);\n"
        'print("BASIS_SIZE");\nprint(size(G));\n'
        'print("BASIS_FIRST");\nprint(G[1]);\n'
    )
    return program, len(equations)


def singular_job(executable, key, indices, locus_polynomials, timeout):
    program, equation_count = singular_program(indices, locus_polynomials)
    start = time.monotonic()
    result = subprocess.run(
        [executable, "-q"], input=program, text=True, capture_output=True,
        check=True, timeout=timeout,
    )
    elapsed = time.monotonic() - start
    if result.stderr.strip():
        raise AssertionError(result.stderr)
    lines = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
    size = lines[lines.index("BASIS_SIZE") + 1]
    first = lines[lines.index("BASIS_FIRST") + 1]
    return key, size == first == "1", equation_count, elapsed


def mask_polynomial(masks):
    return "+".join(TAG_MONOMIAL[mask] for mask in masks)


def load_families(scratch_dir):
    with open(os.path.join(scratch_dir, "n8_round1_survivors_full.json")) as handle:
        records = json.load(handle)
    families = []
    for record in records:
        if record["status"] != "cancellation_family":
            continue
        locus = tuple(
            mask_polynomial(equation["masks"]) for equation in record["system"]
        )
        families.append((tuple(record["indices"]), locus))
    assert len(families) == 10_611
    return families


def load_compatible(scratch_dir):
    quads = []
    with open(os.path.join(scratch_dir, "n8_round1_compatible_quads.txt")) as handle:
        for line in handle:
            quads.append(tuple(int(part) for part in line.split()))
    assert len(quads) == 1_222_812
    return quads


def run_projective(tasks, workers, label, ledger_path):
    counts = Counter()
    aggregate_counts = Counter()
    survivors = []
    digest = hashlib.sha256()
    start = time.monotonic()
    done = 0
    with Pool(processes=workers) as pool, open(ledger_path, "w") as ledger:
        for indices, closed, branches, reason, aggregate in pool.imap(
            close_quadruple, tasks, chunksize=512
        ):
            counts[closed, reason] += 1
            aggregate_counts[aggregate] += 1
            if not closed:
                survivors.append((indices, reason))
            record = (indices, closed, branches, reason, aggregate)
            ledger.write(repr(record) + "\n")
            digest.update(repr(record).encode())
            digest.update(b"\n")
            done += 1
            if done % 100_000 == 0:
                print(
                    f"[{label}] {done} processed, "
                    f"{time.monotonic() - start:.0f}s", flush=True,
                )
    print(f"[{label}] projective ledger:", dict(sorted(counts.items())))
    print(f"[{label}] aggregate support ledger:", dict(sorted(aggregate_counts.items())))
    print(f"[{label}] projective survivors:", len(survivors))
    print(f"[{label}] ledger sha256:", digest.hexdigest())
    print(f"[{label}] wall seconds: {time.monotonic() - start:.1f}", flush=True)
    return counts, aggregate_counts, survivors, digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scratch-dir",
        default=os.environ.get("N8_ROUND1_SCRATCH", "/tmp"),
    )
    parser.add_argument("--workers", type=int, default=14)
    parser.add_argument("--stage", choices=("families", "compatible", "ideals"),
                        required=True)
    parser.add_argument("--ideal-timeout", type=int, default=1800)
    parser.add_argument("--limit", type=int, default=0,
                        help="optional cap on ideal jobs for smoke tests")
    args = parser.parse_args()

    assert len(EXTRAS) == 243
    scratch = args.scratch_dir
    os.makedirs(scratch, exist_ok=True)

    if args.stage == "families":
        families = load_families(scratch)
        tasks = [indices for indices, _locus in families]
        counts, aggregate_counts, survivors, digest = run_projective(
            tasks, args.workers, "families",
            os.path.join(scratch, "n8_round1_families_projective.txt"),
        )
        locus_map = {indices: locus for indices, locus in families}
        with open(os.path.join(scratch, "n8_round1_families_ideal_jobs.json"), "w") as handle:
            json.dump(
                [
                    {"indices": list(indices), "locus": list(locus_map[indices]),
                     "reason": reason}
                    for indices, reason in sorted(survivors)
                ],
                handle,
            )
            handle.write("\n")

    elif args.stage == "compatible":
        quads = load_compatible(scratch)
        counts, aggregate_counts, survivors, digest = run_projective(
            quads, args.workers, "compatible",
            os.path.join(scratch, "n8_round1_compatible_projective.txt"),
        )
        with open(os.path.join(scratch, "n8_round1_compatible_ideal_jobs.json"), "w") as handle:
            json.dump(
                [
                    {"indices": list(indices), "locus": [], "reason": reason}
                    for indices, reason in sorted(survivors)
                ],
                handle,
            )
            handle.write("\n")

    else:
        executable = shutil.which("Singular")
        assert executable is not None
        jobs = []
        for name in ("n8_round1_families_ideal_jobs.json",
                     "n8_round1_compatible_ideal_jobs.json"):
            path = os.path.join(scratch, name)
            if os.path.exists(path):
                with open(path) as handle:
                    for record in json.load(handle):
                        jobs.append(
                            (name, tuple(record["indices"]), tuple(record["locus"]))
                        )
        if args.limit:
            jobs = jobs[: args.limit]
        print("ideal jobs:", len(jobs), flush=True)

        # Restartable: previously checkpointed jobs are not rerun.
        checkpoint_path = os.path.join(scratch, "n8_round1_ideal_checkpoint.txt")
        finished = {}
        if os.path.exists(checkpoint_path):
            with open(checkpoint_path) as handle:
                for line in handle:
                    row = eval(line)
                    if row[1] in ("unit", "nonunit"):
                        finished[row[0]] = row
        pending = [
            (source, indices, locus) for source, indices, locus in jobs
            if (source, indices) not in finished
        ]
        print("checkpointed:", len(finished), "pending:", len(pending), flush=True)

        start = time.monotonic()
        checkpoint = open(checkpoint_path, "a", buffering=1)
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {
                pool.submit(
                    singular_job, executable, (source, indices), indices, locus,
                    args.ideal_timeout,
                ): (source, indices)
                for source, indices, locus in pending
            }
            done = 0
            for future in as_completed(futures):
                key = futures[future]
                try:
                    _key, unit, equation_count, elapsed = future.result()
                    status = "unit" if unit else "nonunit"
                    row = (key, status, equation_count, round(elapsed, 3))
                    if not unit:
                        print("NON-UNIT IDEAL (candidate!):", key, flush=True)
                except subprocess.TimeoutExpired:
                    row = (key, "timeout", 0, args.ideal_timeout)
                    print("TIMEOUT:", key, flush=True)
                except Exception as error:  # noqa: BLE001 - checkpoint and go on
                    row = (key, f"error:{type(error).__name__}", 0, 0)
                    print("ERROR:", key, error, flush=True)
                checkpoint.write(repr(row) + "\n")
                done += 1
                if done % 250 == 0:
                    print(
                        f"[ideals] {done}/{len(pending)} done, "
                        f"{time.monotonic() - start:.0f}s", flush=True,
                    )
        checkpoint.close()

        results = []
        with open(checkpoint_path) as handle:
            for line in handle:
                results.append(eval(line))
        status_counter = Counter(row[1] for row in results)
        latest = {}
        for row in results:
            latest[row[0]] = row
        results = sorted(latest.values(), key=repr)
        # The outcome digest covers only (source, indices, status), so it is
        # stable across reruns, worker counts, and Groebner engines.
        digest = hashlib.sha256()
        with open(os.path.join(scratch, "n8_round1_ideal_results.txt"), "w") as handle:
            for row in results:
                handle.write(repr(row) + "\n")
                digest.update(repr((row[0], row[1])).encode())
                digest.update(b"\n")
        unit_count = sum(1 for row in results if row[1] == "unit")
        nonunit = [row[0] for row in results if row[1] == "nonunit"]
        unresolved = [row[0] for row in results if row[1] not in ("unit", "nonunit")]
        print("ideal status counts:", dict(status_counter))
        print("ideals unit:", unit_count, "/", len(results))
        print("candidates (non-unit):", nonunit)
        print("unresolved (timeout/error):", len(unresolved))
        for key in unresolved:
            print("  unresolved:", key)
        print("ideal results sha256:", digest.hexdigest())
        print(f"ideal wall seconds: {time.monotonic() - start:.1f}")


if __name__ == "__main__":
    main()
