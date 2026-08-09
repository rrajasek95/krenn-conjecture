#!/usr/bin/env python3
"""Independently check four additional deletion-free m=10 RUP proofs."""

from __future__ import annotations

import gzip
import hashlib
import importlib
import os
import sys
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_AUDIT_SHA256 = (
    "40500a706dd0ba82a25df26cea95ff8231245c367f4350b9c2d9363ff1ffb64a"
)
PINNED_RUP_CHECKER_SHA256 = (
    "5b9a8f2ba5d5ce4e9a511396a78041bbd76b87b64741dd8adbc3391dfa7f97dc"
)
for path, expected in (
    (os.path.join(HERE, "audit_n8_d1_m10_support_frontier.py"),
     PINNED_AUDIT_SHA256),
    (os.path.join(HERE, "verify_n8_d1_m10_first_core_rup.py"),
     PINNED_RUP_CHECKER_SHA256),
):
    with open(path, "rb") as handle:
        require(hashlib.sha256(handle.read()).hexdigest() == expected,
                "a pinned m=10 proof dependency changed")

A = importlib.import_module("audit_n8_d1_m10_support_frontier")
R = importlib.import_module("verify_n8_d1_m10_first_core_rup")
V, N, D = A.V, A.N, A.D

BRANCH_SPECS = (
    ("34_0", "triple", "special", 0),
    ("43_0", "special", "triple", 0),
    ("44_0", "special", "special", 0),
    ("44_1", "special", "special", 1),
)

EXPECTED = {
    "34_0": (2798, 10193,
              "7b0fcb99adbe92a44296aef33c07b84e9c2be42b71d6dc07516254da876d23c6",
              931,
              "7a7e72c352577a113414e20711197da321e52a73d55c680582a77cd7df387197",
              "cfe2d9e2756d1ee7121e58a4d773b78e5c175c6c911bfedb48ec77f0fa49ade4",
              881115, 0, False),
    "43_0": (3006, 10965,
              "54a56bf97bffc80680d43e08e42791f07e4ecb09611cfa3f8d854928641b8e13",
              717,
              "bea9675047f75ef31a9d3608e7a0272200ba9af7471122e5e8236ee8da04e636",
              "a933293fb1f42effce3e4bffd76164aef3c21cd8d876f4625f63e349659cbbca",
              632809, 0, True),
    "44_0": (2256, 8235,
              "2de97cf4db686890ecd938feac4b23b0ae83683ada6ae795929860a41b7b8767",
              345,
              "863b082b9958bb7d01d98b71ed88b24aa4fdbd6cbe8dd5d915fee61a895c8316",
              "0c0a089ec56cf04c7b354b0275c5540b4290dbfcbfb68cce9ffdcf9c752af985",
              286513, 0, False),
    "44_1": (2256, 8235,
              "983fa117158948150ed895cfe604816c943fb6693384a5d2e4991aaab3e145a3",
              172,
              "34d4dc5615f0c93c42533442d32e408b31a21b4a40263ce1845224f86e86fa33",
              "e4aba809b604328a32c172795b34a63400329f8547e7767c23f256d83423ac53",
              128954, 1, True),
}
EXPECTED_LEDGER_SHA256 = (
    "bf4a7452e2da1e3b4815b240cec961c1485205ed33609a27fe65434abd7fd00b"
)


def support_bases():
    group = V.d1_group()
    triples = [{state[0] for state in N.triple_states(colour)}
               for colour in (0, 1)]
    special = [{state[0] for state in N.special_four_supports(colour)[0]}
               for colour in (0, 1)]
    kinds = {"triple": triples, "special": special}
    result = []
    for label, left_kind, right_kind, index in BRANCH_SPECS:
        representatives = A.support_pair_orbits(
            kinds[left_kind][0], kinds[right_kind][1], group
        )
        left, right = representatives[index]
        result.append((label, left | right))
    return result


def build_core_cnf(base, admissible, sigma, off_sigma):
    """Build the exact same 16-fibre relaxation for any m=10 base."""
    base = set(base)
    require(6 <= len(base) <= 8 and base <= off_sigma,
            "an additional core has a malformed support base")
    cnf = A.M8.CNF()
    free = sorted(off_sigma - base)
    sigma_ids = {entry: cnf.var(("SIGMA", entry))
                 for entry in sorted(sigma)}
    off_ids = {entry: cnf.var(("EXTRA", entry)) for entry in free}
    A.add_exact(cnf, [off_ids[entry] for entry in free], 10 - len(base))
    mandatory = set(V.BASE_UNITS) | {
        V.cell(0, 2, 2, 2), V.cell(1, 3, 2, 2),
    }
    for entry in sorted(mandatory):
        cnf.add(sigma_ids[entry])

    def matching_term(domain, values, word, matching):
        factors = []
        for u, v in matching:
            entry = V.cell(u, v, word[u], word[v])
            if entry not in admissible:
                return False
            if entry in base:
                continue
            factors.append(sigma_ids[entry] if entry in sigma
                           else off_ids[entry])
        return cnf.and_var(
            factors, ("TERM", tuple(domain), tuple(values), tuple(matching))
        )

    for domain, values, pure in A.CORE_FIBRES:
        word = dict(zip(domain, values))
        terms, constants = [], 0
        for matching in V.MATCHINGS[tuple(domain)]:
            term = matching_term(domain, values, word, matching)
            if term is True:
                constants += 1
            elif term is not False:
                terms.append(term)
        if pure:
            if constants == 0:
                cnf.add(*terms)
            continue
        if constants >= 2:
            continue
        if constants == 1:
            cnf.add(*terms)
            continue
        if len(terms) == 1:
            cnf.add(-terms[0])
            continue
        if not terms:
            continue
        fibre_key = tuple(domain), tuple(values), pure
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
    return cnf


def proof_path(label):
    return os.path.join(
        HERE, "certificates",
        "n8_d1_m10_core_%s.glucose42.drup.gz" % label,
    )


def audit():
    started = monotonic()
    _frontier, frontier_digest, _encoded, _seconds = A.audit()
    admissible, sigma, off_sigma, _kinds = V.reconstruct_support_domains()
    off_cells = sorted(off_sigma)
    cell_index = {entry: index for index, entry in enumerate(off_cells)}
    state_kinds = {
        "triple": [N.triple_states(colour) for colour in (0, 1)],
        "special": [N.special_four_supports(colour)[0]
                    for colour in (0, 1)],
    }
    branch_specs = {spec[0]: spec for spec in BRANCH_SPECS}
    rows = []
    for label, base in support_bases():
        cnf = build_core_cnf(base, admissible, sigma, off_sigma)
        encoded_sha = hashlib.sha256(A.dimacs_bytes(cnf)).hexdigest()
        with open(proof_path(label), "rb") as handle:
            compressed = handle.read()
        raw = gzip.decompress(compressed)
        proof = R.parse_proof(raw)
        checker = R.RUPDatabase(cnf.clauses, cnf.variable_count)
        require(not checker.root_conflict,
                "%s unexpectedly unit-refutes before its proof" % label)
        for index, clause in enumerate(proof):
            require(checker.check_and_add(clause),
                    "%s proof addition %d is not RUP" % (label, index))
        require(proof and proof[-1] == () and checker.root_conflict,
                "%s does not end in a checked empty clause" % label)
        _label, left_kind, right_kind, _support_index = branch_specs[label]
        _labelled, state_representatives = A.M8.state_pair_orbits(
            state_kinds[left_kind][0], state_kinds[right_kind][1],
            V.d1_group(),
        )
        state_rows = [(index, state)
                      for index, state in enumerate(state_representatives)
                      if state[0] == base]
        require(len(state_rows) == 1,
                "%s no longer selects one anchor-state orbit" % label)
        state_index, state = state_rows[0]
        witness, certificate_count, memo_states = A.repair_witness(
            state, 10 - len(base), admissible, sigma, off_sigma,
            off_cells, cell_index,
        )
        row = {
            "label": label,
            "base": [list(entry) for entry in sorted(base)],
            "input_variables": cnf.variable_count,
            "input_clauses": len(cnf.clauses),
            "input_dimacs_sha256": encoded_sha,
            "proof_additions": len(proof),
            "proof_raw_sha256": hashlib.sha256(raw).hexdigest(),
            "proof_gzip_sha256": hashlib.sha256(compressed).hexdigest(),
            "unit_propagations": checker.propagations,
            "anchor_state_branch": state_index,
            "repair_DNF_survivor": witness is not None,
            "repair_certificate_count": certificate_count,
            "repair_memo_states": memo_states,
        }
        observed = (
            row["input_variables"], row["input_clauses"],
            row["input_dimacs_sha256"], row["proof_additions"],
            row["proof_raw_sha256"], row["proof_gzip_sha256"],
            row["unit_propagations"], row["anchor_state_branch"],
            row["repair_DNF_survivor"],
        )
        require(observed == EXPECTED[label],
                "the checked %s proof ledger changed" % label)
        rows.append(row)
    ledger = {
        "pinned_audit_sha256": PINNED_AUDIT_SHA256,
        "pinned_rup_checker_sha256": PINNED_RUP_CHECKER_SHA256,
        "frontier_ledger_sha256": frontier_digest,
        "branches": rows,
        "certificate": ("every deletion-free proof addition is RUP; each "
                        "last addition is the empty clause"),
        "conclusion": ("four additional m=10 support-base families are "
                       "empty under the exact 16-fibre relaxation"),
        "new_repair_DNF_survivors_closed": sum(
            row["repair_DNF_survivor"] for row in rows
        ),
    }
    digest = D.content_hash(ledger)
    require(digest == EXPECTED_LEDGER_SHA256,
            "the additional m=10 RUP ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 m=10 additional-core RUPs: PASS (independently checked)")
    for row in ledger["branches"]:
        print("%s: %d variables; %d clauses; %d proof additions"
              % (row["label"], row["input_variables"],
                 row["input_clauses"], row["proof_additions"]))
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
