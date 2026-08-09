#!/usr/bin/env python3
"""Exact normal-form and complete-shadow audit for N=8 D1 at m=11."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import itertools
import json
import math
import os
import subprocess
import sys
from collections import Counter
from functools import lru_cache
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_M10_SHA256 = (
    "a4c12df0d0ee339fc3a6341c7b977d404ebc2b5e201defedf70180b634350d07"
)
SOURCE = os.path.join(HERE, "verify_n8_d1_m10_334_full_shadow.py")
with open(SOURCE, "rb") as handle:
    if PINNED_M10_SHA256 != "TO_BE_PINNED":
        require(hashlib.sha256(handle.read()).hexdigest() == PINNED_M10_SHA256,
                "the committed complete m=10 closure changed")
B = importlib.import_module("verify_n8_d1_m10_334_full_shadow")
H, F, I, A, D = B.H, B.F, B.I, B.A, B.D
Q, N, V = I.A, I.A.N, F.V

PINNED_SIX_CLOSURE_SHA256 = (
    "e4c09bc532109109c42b286218d91fd8e0043a03377ce401ee77560872c0168e"
)
SIX_SOURCE = os.path.join(
    HERE, "verify_n8_d1_m11_six_candidate_closure.py"
)
with open(SIX_SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest()
            == PINNED_SIX_CLOSURE_SHA256,
            "the committed six-support coefficient closure changed")
K11 = importlib.import_module("verify_n8_d1_m11_six_candidate_closure")
M10_EXTRAS = K11.C.candidate_input()[1]
KNOWN_COEFFICIENT_SUPPORTS = frozenset(
    M10_EXTRAS | {extension} for extension in K11.EXTENSION_CELLS
)

PALETTE_PATH = os.path.join(
    HERE, "certificates", "n8_d1_m11_rup_palettes.json"
)
EXPECTED_PALETTE_SHA256 = (
    "7db4241383a41988fa0245900f4c3f13a2118f226987b97c5fe058c59e8ae096"
)
EXPECTED_LEDGER_SHA256 = (
    "d8f3a84b54abac22a110f2da0e52f7a269f10e790acee54e21957371bb83d44e"
)

FAMILY_SPECS = (
    ("335", "triple", "triple", 5, 5184, 132, 132),
    ("344", "triple", "special", 4, 2376, 64, 64),
    ("434", "special", "triple", 4, 2376, 64, 64),
    ("443", "special", "special", 3, 1089, 52, 25),
)


def monochrome_normal_forms_through_eight(colour, off_sigma):
    monochrome = sorted(entry for entry in off_sigma
                        if entry[2:] == (colour, colour))
    full_traces = {
        frozenset(V.cell(u, v, colour, colour) for u, v in matching
                  if V.cell(u, v, colour, colour) in off_sigma)
        for matching in V.MATCHINGS[V.SITES]
    }
    residue_matchings = {
        frozenset(V.cell(u, v, colour, colour) for u, v in matching)
        for matching in V.MATCHINGS[V.RESIDUE]
    }
    valid, minimal = {}, {}
    for size in range(2, 9):
        supports = set()
        for chosen in itertools.combinations(monochrome, size):
            support = frozenset(chosen)
            if not any(trace <= support for trace in full_traces):
                continue
            if sum(matching <= support
                   for matching in residue_matchings) == 1:
                continue
            supports.add(support)
        valid[size] = supports
        minimal[size] = {
            support for support in supports
            if not any(smaller <= support
                       for earlier in range(2, size)
                       for smaller in minimal[earlier])
        }
    require({size: len(rows) for size, rows in valid.items()} == {
        2: 0, 3: 72, 4: 1179, 5: 8382, 6: 34657,
        7: 95272, 8: 189990,
    }, "the one-colour support census through size eight changed")
    require({size: len(rows) for size, rows in minimal.items()} == {
        2: 0, 3: 72, 4: 27, 5: 0, 6: 0, 7: 0, 8: 0,
    }, "a new one-colour minimal form appeared through size eight")
    require(minimal[3] == {state[0] for state in N.triple_states(colour)}
            and minimal[4] == {
                state[0] for state in N.special_four_supports(colour)[0]
            }, "the constructive 3/4 normal forms are incomplete")
    known_minimal = minimal[3] | minimal[4]
    zero_residue_trace_checks = 0
    two_residue_trace_checks = 0
    for trace in full_traces:
        residue_count = sum(matching <= trace
                            for matching in residue_matchings)
        if residue_count == 0:
            require(len(trace) <= 4
                    and any(row <= trace for row in known_minimal),
                    "a zero-residue full trace escaped the minimal forms")
            zero_residue_trace_checks += 1
        for first, second in itertools.combinations(residue_matchings, 2):
            bounded = trace | first | second
            require(len(bounded) <= 8
                    and any(row <= bounded for row in known_minimal),
                    "a bounded two-residue subset escaped the minimal forms")
            two_residue_trace_checks += 1
    require(zero_residue_trace_checks > 0
            and two_residue_trace_checks == 3 * len(full_traces),
            "the global minimal-form reduction census changed")
    return {
        "valid_by_size": {size: len(rows)
                          for size, rows in sorted(valid.items())},
        "minimal_by_size": {size: len(rows)
                            for size, rows in sorted(minimal.items())},
        "global_minimal_form_certificate": {
            "zero_residue_full_trace_checks": zero_residue_trace_checks,
            "full_trace_two_residue_pair_checks": two_residue_trace_checks,
            "bounded_subset_size": 8,
            "conclusion": ("the 72 triples and 27 special fours are the "
                           "complete minimal forms at every support size"),
        },
    }


@lru_cache(maxsize=1)
def family_branches():
    admissible, sigma, off_sigma, _kinds = V.reconstruct_support_domains()
    off_cells = sorted(off_sigma)
    cell_index = {entry: index for index, entry in enumerate(off_cells)}
    group = V.d1_group()
    states = {
        "triple": [N.triple_states(colour) for colour in (0, 1)],
        "special": [N.special_four_supports(colour)[0]
                    for colour in (0, 1)],
    }
    result, census = [], {}
    for (family, left_kind, right_kind, additions, expected_labelled,
         expected_orbits, expected_survivors) in FAMILY_SPECS:
        labelled, representatives = A.M8.state_pair_orbits(
            states[left_kind][0], states[right_kind][1], group
        )
        require((labelled, len(representatives))
                == (expected_labelled, expected_orbits),
                "the %s anchor quotient changed" % family)
        survivors, nodes, zero = [], [], 0
        for index, state in enumerate(representatives):
            witness, certificate_count, memo_states = Q.repair_witness(
                state, additions, admissible, sigma, off_sigma,
                off_cells, cell_index,
            )
            nodes.append(memo_states)
            zero += certificate_count == 0
            if witness is not None:
                survivors.append((family, index, state, additions))
        require(len(survivors) == expected_survivors,
                "the %s repair-DNF survivor count changed" % family)
        base_size = len(representatives[0][0])
        census[family] = {
            "labelled_anchor_states": labelled,
            "anchor_state_orbits": len(representatives),
            "additional_cells": additions,
            "raw_addition_choices": sum(
                math.comb(len(off_sigma) - len(state[0]), additions)
                for state in representatives
            ),
            "repair_DNF_survivors": len(survivors),
            "repair_DNF_closures": len(representatives) - len(survivors),
            "zero_initial_certificate_branches": zero,
            "repair_memo_states": sum(nodes),
            "max_repair_memo_states": max(nodes),
            "base_cells": base_size,
        }
        result.extend(survivors)
    require(len(result) == 285,
            "the aggregate m=11 repair-DNF frontier changed")
    return result, admissible, sigma, off_sigma, census


def dynamic_residuals(state, additions, admissible, sigma, off_sigma):
    initial, anchor_units = state
    seen, residuals = set(), set()
    stats = Counter()

    def search(base, remaining):
        key = base, remaining
        if key in seen:
            return
        seen.add(key)
        stats["nodes"] += 1
        certificate = F.choose_dynamic_repair(
            (base, anchor_units), remaining,
            admissible, sigma, off_sigma,
        )
        if certificate is not None and certificate["repair"] is None:
            stats["dynamic_unique_closures"] += 1
            return
        if remaining == 0:
            residuals.add(base)
            return
        if certificate is not None:
            stats["repair_DNF_nodes"] += 1
            for repair in certificate["repair"]:
                search(frozenset(set(base) | set(repair)),
                       remaining - len(repair))
            return
        stats["free_extension_nodes"] += 1
        for entry in sorted(off_sigma - set(base)):
            search(base | {entry}, remaining - 1)

    search(initial, additions)
    return sorted(residuals, key=lambda row: tuple(sorted(row))), stats


def build_fixed_full_shadow(extras, anchor_units, admissible, sigma,
                            off_sigma, selected_fibres=None):
    extras = set(extras)
    require(len(extras) == 11 and extras <= off_sigma,
            "a specialized m=11 support does not have eleven cells")
    cnf = A.M8.CNF()
    sigma_ids = {entry: cnf.var(("SIGMA", entry))
                 for entry in sorted(sigma)}
    mandatory = set(V.BASE_UNITS) | set(anchor_units) | {
        V.cell(0, 2, 2, 2), V.cell(1, 3, 2, 2),
    }
    for entry in sorted(mandatory):
        cnf.add(sigma_ids[entry])
    cnf.clause_fibres = [None] * len(cnf.clauses)

    def matching_term(domain, values, word, matching):
        factors = []
        for u, v in matching:
            entry = V.cell(u, v, word[u], word[v])
            if entry not in admissible:
                return False
            if entry in off_sigma:
                if entry not in extras:
                    return False
            else:
                factors.append(sigma_ids[entry])
        return cnf.and_var(
            factors, ("TERM", tuple(domain), tuple(values), tuple(matching))
        )

    domains = (V.SITES, V.W1, V.W2, V.RESIDUE)
    fibre_count = sum(len(V.COLORS) ** len(domain) for domain in domains)
    require(fibre_count == 8100,
            "the specialized support-shadow fibre count changed")
    if selected_fibres is None:
        fibres = (
            (tuple(domain), tuple(values),
             (len(set(values)) == 1
              if domain == V.SITES else set(values) == {2}))
            for domain in domains
            for values in itertools.product(V.COLORS, repeat=len(domain))
        )
    else:
        fibres = sorted(selected_fibres,
                        key=lambda row: (row[0], row[1], row[2]))
    for domain, values, pure in fibres:
            require(tuple(domain) in V.MATCHINGS
                    and len(values) == len(domain)
                    and set(values) <= set(V.COLORS),
                    "a selected support-shadow fibre is malformed")
            expected_pure = (len(set(values)) == 1
                             if tuple(domain) == V.SITES
                             else set(values) == {2})
            require(pure == expected_pure,
                    "a selected support-shadow fibre has the wrong target")
            fibre_key = tuple(domain), tuple(values), pure
            clause_start = len(cnf.clauses)
            word = dict(zip(domain, values))
            terms, constants = [], 0
            for matching in V.MATCHINGS[tuple(domain)]:
                term = matching_term(domain, values, word, matching)
                if term is True:
                    constants += 1
                elif term is not False:
                    terms.append(term)

            def record_fibre_clauses():
                cnf.clause_fibres.extend(
                    [fibre_key] * (len(cnf.clauses) - clause_start)
                )

            if pure:
                if constants == 0:
                    cnf.add(*terms)
                record_fibre_clauses()
                continue
            if constants >= 2:
                record_fibre_clauses()
                continue
            if constants == 1:
                cnf.add(*terms)
                record_fibre_clauses()
                continue
            if len(terms) == 1:
                cnf.add(-terms[0])
                record_fibre_clauses()
                continue
            if not terms:
                record_fibre_clauses()
                continue
            prefix, current = [None] * len(terms), None
            for index, term in enumerate(terms):
                prefix[index] = current
                current = cnf.or_var(current, term,
                                     ("PRE", fibre_key, index))
            suffix, current = [None] * len(terms), None
            for index in range(len(terms) - 1, -1, -1):
                suffix[index] = current
                current = cnf.or_var(current, terms[index],
                                     ("SUF", fibre_key, index))
            for index, term in enumerate(terms):
                clause = [-term]
                if prefix[index] is not None:
                    clause.append(prefix[index])
                if suffix[index] is not None:
                    clause.append(suffix[index])
                cnf.add(*clause)
            record_fibre_clauses()
    require(len(cnf.clause_fibres) == len(cnf.clauses),
            "the specialized clause-to-fibre ledger changed")
    return cnf


def check_branch(family, index, palettes, discover=False):
    branches, admissible, sigma, off_sigma, _census = family_branches()
    row_by_key = {(name, branch): (state, additions)
                  for name, branch, state, additions in branches}
    state, additions = row_by_key[(family, index)]
    supports, stats = dynamic_residuals(
        state, additions, admissible, sigma, off_sigma
    )
    union = frozenset().union(*palettes) if palettes else frozenset()
    hits, direct, coefficient = 0, 0, 0
    for support in supports:
        certificate = F.direct_complete_support_certificate(
            (support, state[1]), admissible, sigma
        )
        if certificate is not None:
            direct += 1
            continue
        if union:
            compact = build_fixed_full_shadow(
                support, state[1], admissible, sigma, off_sigma, union
            )
            if A.M8.unit_refutation(compact.clauses) is not None:
                hits += 1
                continue
        if support in KNOWN_COEFFICIENT_SUPPORTS:
            coefficient += 1
            continue
        require(discover,
                "branch %s:%d has a complete-shadow survivor"
                % (family, index))
        full = build_fixed_full_shadow(
            support, state[1], admissible, sigma, off_sigma
        )
        core = F.unit_refutation_core_fibres(full)
        require(core is not None,
                "branch %s:%d has a complete-shadow SAT support"
                % (family, index))
        palette = core["fibres"]
        compact = build_fixed_full_shadow(
            support, state[1], admissible, sigma, off_sigma, palette
        )
        require(A.M8.unit_refutation(compact.clauses) is not None,
                "an extracted m=11 RUP palette failed its check")
        palettes.append(palette)
        union = frozenset(set(union) | set(palette))
        hits += 1
    require(direct + hits + coefficient == len(supports),
            "an m=11 complete support was not closed")
    return {
        "family": family,
        "branch": index,
        "dynamic_nodes": stats["nodes"],
        "dynamic_unique_closures": stats["dynamic_unique_closures"],
        "repair_DNF_nodes": stats["repair_DNF_nodes"],
        "free_extension_nodes": stats["free_extension_nodes"],
        "complete_support_residuals": len(supports),
        "direct_complete_support_closures": direct,
        "palette_RUP_closures": hits,
        "coefficient_ideal_closures": coefficient,
    }, palettes


def worker_command(family, index, discover):
    command = [sys.executable]
    if sys.flags.optimize:
        command.append("-O")
    command.extend([os.path.abspath(__file__), "--worker", family,
                    str(index)])
    if discover:
        command.append("--discover")
    return command


def run_worker(family, index, palettes, discover=False):
    payload = json.dumps(H.encode_palettes(palettes), separators=(",", ":"))
    result = subprocess.run(
        worker_command(family, index, discover), input=payload, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        cwd=HERE,
    )
    require(result.returncode == 0,
            "%s:%d worker failed: %s"
            % (family, index, result.stderr.strip()))
    output = json.loads(result.stdout)
    return output["row"], H.decode_palettes(output["palettes"])


def audit(rows):
    started = monotonic()
    coefficient_ledger, coefficient_digest, _seconds = K11.audit()
    branches, _admissible, _sigma, off_sigma, census = family_branches()
    with open(PALETTE_PATH, "rb") as handle:
        raw = handle.read()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_PALETTE_SHA256,
            "the frozen m=11 RUP palettes changed")
    palettes = H.decode_palettes(json.loads(raw.decode("ascii")))
    require(len(rows) == len(branches) == 285,
            "the complete m=11 batch census changed")
    normal_forms = {
        "b": monochrome_normal_forms_through_eight(0, off_sigma),
        "c": monochrome_normal_forms_through_eight(1, off_sigma),
    }
    ledger = {
        "pinned_m10_sha256": PINNED_M10_SHA256,
        "pinned_six_closure_sha256": PINNED_SIX_CLOSURE_SHA256,
        "six_support_closure_ledger_sha256": coefficient_digest,
        "normal_forms": normal_forms,
        "family_census": census,
        "palette_sha256": hashlib.sha256(raw).hexdigest(),
        "inherited_m10_palettes": 86,
        "total_root_RUP_palettes": len(palettes),
        "palette_sizes": [len(palette) for palette in palettes],
        "symbolic_branches_closed": len(rows),
        "dynamic_nodes": sum(row["dynamic_nodes"] for row in rows),
        "dynamic_unique_closures": sum(
            row["dynamic_unique_closures"] for row in rows
        ),
        "complete_support_residuals": sum(
            row["complete_support_residuals"] for row in rows
        ),
        "direct_complete_support_closures": sum(
            row["direct_complete_support_closures"] for row in rows
        ),
        "palette_RUP_closures": sum(
            row["palette_RUP_closures"] for row in rows
        ),
        "coefficient_ideal_closures": sum(
            row["coefficient_ideal_closures"] for row in rows
        ),
        "distinct_coefficient_supports": coefficient_ledger[
            "semantic_supports"
        ],
        "branch_rows": rows,
        "remaining_m11_symbolic_branches": 0,
        "characteristic_scope": coefficient_ledger["characteristic_scope"],
        "status": ("the complete m=11 D1 frontier is empty over every "
                   "field of characteristic != 2"),
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the complete m=11 ledger changed")
    return ledger, digest, monotonic() - started


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", nargs=2, metavar=("FAMILY", "INDEX"))
    parser.add_argument("--discover", action="store_true")
    parser.add_argument("--batch-start", type=int)
    parser.add_argument("--batch-end", type=int)
    parser.add_argument("--batch-output")
    parser.add_argument("--aggregate-dir")
    args = parser.parse_args()
    if args.worker is not None:
        family, index_text = args.worker
        palettes = H.decode_palettes(json.loads(sys.stdin.read()))
        row, palettes = check_branch(
            family, int(index_text), palettes, args.discover
        )
        print(json.dumps({"row": row,
                          "palettes": H.encode_palettes(palettes)},
                         sort_keys=True, separators=(",", ":")))
        return
    if args.batch_start is not None:
        require(args.batch_end is not None,
                "a batch end is required with a batch start")
        with open(PALETTE_PATH, "rb") as handle:
            palettes = H.decode_palettes(json.loads(handle.read()))
        branches, _admissible, _sigma, _off_sigma, _census = family_branches()
        rows = []
        for family, index, _state, _additions in branches[
                args.batch_start:args.batch_end]:
            row, returned = check_branch(family, index, list(palettes), False)
            require(returned == palettes,
                    "a checking worker mutated the frozen palettes")
            rows.append(row)
        payload = json.dumps(rows, sort_keys=True, separators=(",", ":"))
        if args.batch_output:
            with open(args.batch_output, "w") as handle:
                handle.write(payload)
        else:
            print(payload)
        return
    require(args.aggregate_dir is not None,
            "use --aggregate-dir after checking isolated batches")
    rows = []
    for filename in sorted(os.listdir(args.aggregate_dir),
                           key=lambda value: int(value.split(".")[0])):
        with open(os.path.join(args.aggregate_dir, filename), "r") as handle:
            rows.extend(json.load(handle))
    ledger, digest, seconds = audit(rows)
    print("n8 D1 m=11 complete shadow: PASS (exact)")
    print("branches closed:", ledger["symbolic_branches_closed"])
    print("dynamic nodes:", ledger["dynamic_nodes"])
    print("complete supports:", ledger["complete_support_residuals"])
    print("RUP palettes:", ledger["total_root_RUP_palettes"])
    print("coefficient support occurrences closed:",
          ledger["coefficient_ideal_closures"])
    print("remaining m=11 symbolic branches: 0")
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
