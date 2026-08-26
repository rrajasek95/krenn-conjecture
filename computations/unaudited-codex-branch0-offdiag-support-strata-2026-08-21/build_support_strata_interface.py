#!/usr/bin/env python3
"""Build the symmetry-complete branch0/all-offdiagonal support interface.

For a chosen edge support S, retain d_e only for e in S and substitute

    [[a_e,b_e],[-(1+a_e*d_e)/b_e,d_e]]  (e in S),
    [[a_e,b_e],[-1/b_e,0]]              (e not in S).

The packet uses the literal branch-0 6 permanent, 4 triangle, and 12
diagonal-cofactor rows.  Denominators are cleared by b monomials only.  The
localized chart inverts H, product b_e, and product_{e in S} a_e*d_e; it does
not invert c_e or 1+a_e*d_e.  A partial c_e=0 face changes the permanent term
on that edge and must be routed recursively as a joint (branch,term) chart;
it is not automatically one of the all-six aligned charts.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import permutations
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = (ROOT / "computations" /
          "unaudited-codex-n8-orbit0-normalized-78-2026-08-20")
PROBE_PATH = SOURCE / "screen_lowq_joint_branch_orbits.py"
OUT = HERE / "results_support_strata_interface.json"
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


PROBE_MODULE = load("n8_offdiag_strata_probe", PROBE_PATH)
PROBE = PROBE_MODULE.PROBE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def clean(poly):
    return {monomial: coefficient for monomial, coefficient in poly.items()
            if coefficient}


class Context:
    def __init__(self, support):
        self.support = tuple(sorted(support))
        self.d_index = {edge: 12 + position
                        for position, edge in enumerate(self.support)}
        self.variable_names = (tuple(f"a{edge}" for edge in range(6))
                               + tuple(f"b{edge}" for edge in range(6))
                               + tuple(f"d{edge}" for edge in self.support))
        self.n = len(self.variable_names)
        self.zero_exponent = (0,) * self.n
        self.one = {self.zero_exponent: Fraction(1)}

    def add(self, *polys):
        answer = Counter()
        for poly in polys:
            answer.update(poly)
        return clean(answer)

    def scale(self, poly, coefficient):
        coefficient = Fraction(coefficient)
        return clean({monomial: coefficient * value
                      for monomial, value in poly.items()})

    def multiply(self, *polys):
        answer = self.one
        for poly in polys:
            updated = Counter()
            for left, left_coefficient in answer.items():
                for right, right_coefficient in poly.items():
                    exponent = tuple(a + b for a, b in zip(left, right))
                    updated[exponent] += left_coefficient * right_coefficient
            answer = clean(updated)
        return answer

    def variable(self, index, exponent=1, coefficient=1):
        powers = [0] * self.n
        powers[index] = exponent
        return {tuple(powers): Fraction(coefficient)}

    def entries(self):
        answer = []
        for edge in range(6):
            a, b = self.variable(edge), self.variable(6 + edge)
            if edge in self.d_index:
                d = self.variable(self.d_index[edge])
                c = self.add(self.variable(6 + edge, -1, -1),
                             self.multiply(a, d,
                                           self.variable(6 + edge, -1, -1)))
            else:
                c, d = self.variable(6 + edge, -1, -1), {}
            answer.extend((a, b, c, d))
        return tuple(answer)

    def substitute(self, raw_poly):
        entries = self.entries()
        answer = {}
        for monomial, coefficient in raw_poly.items():
            term = self.scale(self.one, coefficient)
            for raw_variable in monomial:
                term = self.multiply(term, entries[raw_variable])
            answer = self.add(answer, term)
        return answer

    def clear_denominators(self, poly):
        if not poly:
            return {}, self.zero_exponent
        shift = tuple(-min([exponent[index] for exponent in poly] + [0])
                      for index in range(self.n))
        require(not any(shift[index] for index in range(6))
                and not any(shift[index] for index in range(12, self.n)),
                "a or d denominator appeared")
        cleared = {
            tuple(exponent[index] + shift[index] for index in range(self.n)):
                coefficient
            for exponent, coefficient in poly.items()
        }
        return clean(cleared), shift

    def singular(self, poly):
        if not poly:
            return "0"
        pieces = []
        for exponent, coefficient in sorted(poly.items()):
            factors = []
            for index, power in enumerate(exponent):
                if power:
                    name = self.variable_names[index]
                    factors.append(name + (f"^{power}" if power != 1 else ""))
            body = "*".join(factors) or "1"
            magnitude = abs(coefficient)
            if magnitude != 1:
                body = f"{magnitude.numerator}/{magnitude.denominator}*{body}"
            prefix = "-" if coefficient < 0 else ("+" if pieces else "")
            pieces.append(prefix + body)
        return "".join(pieces)


def raw_labels():
    labels = ["e_" + "".join(map(str, edge)) for edge in EDGES]
    labels += ["t_012", "t_013", "t_023", "t_123"]
    labels += [f"cofactor_{edge}_{position}"
               for edge in range(6) for position in (0, 3)]
    return tuple(labels)


def act_mask(mask, permutation):
    answer = 0
    for edge, (left, right) in enumerate(EDGES):
        if not (mask >> edge) & 1:
            continue
        target_pair = tuple(sorted((permutation[left], permutation[right])))
        answer |= 1 << EDGE_INDEX[target_pair]
    return answer


def support_orbits():
    group = tuple(permutations(range(4)))
    unseen = set(range(64))
    records = []
    while unseen:
        representative = min(unseen)
        orbit = {act_mask(representative, permutation)
                 for permutation in group}
        unseen -= orbit
        stabilizer = tuple(permutation for permutation in group
                           if act_mask(representative, permutation)
                           == representative)
        records.append((representative, orbit, stabilizer))
    require(len(records) == 11 and sum(len(orbit) for _, orbit, _ in records) == 64,
            "six-edge S4 support orbit census changed")
    return tuple(records)


def encode_poly(poly):
    return [{"exponents": list(exponent),
             "coefficient": [coefficient.numerator, coefficient.denominator]}
            for exponent, coefficient in sorted(poly.items())]


def build_record(mask, orbit, stabilizer):
    support = tuple(edge for edge in range(6) if (mask >> edge) & 1)
    context = Context(support)
    equations, raw_h = PROBE.equations((0,) * 6)
    labels = raw_labels()
    require(len(equations) == len(labels) == 22,
            "raw branch0 source row count changed")
    rows = []
    permanent_zero = []
    for index, (label, raw) in enumerate(zip(labels, equations)):
        specialized, shift = context.clear_denominators(context.substitute(raw))
        if index < 6:
            permanent_zero.append(not specialized)
        if specialized:
            rows.append({"label": label,
                         "clearing_shift": list(shift),
                         "polynomial": context.singular(specialized),
                         "terms": encode_poly(specialized)})
    require(permanent_zero == [True] * 6,
            "a permanent row survived its solved substitution")
    h_poly, h_shift = context.clear_denominators(context.substitute(raw_h))
    require(h_poly, "pure H vanished identically")
    live_b = "*".join(f"b{edge}" for edge in range(6))
    live_ad = "*".join(f"a{edge}*d{edge}" for edge in support) or "1"
    live_c_numerators = "*".join(
        f"(1+a{edge}*d{edge})" for edge in support) or "1"
    return {
        "mask": mask,
        "support_edges": list(support),
        "support_edge_labels": ["".join(map(str, EDGES[edge])) for edge in support],
        "k": len(support),
        "orbit_size": len(orbit),
        "stabilizer_order": len(stabilizer),
        "orbit_masks": sorted(orbit),
        "variable_names": list(context.variable_names),
        "raw_source_rows": 22,
        "nonzero_specialized_rows": len(rows),
        "rows": rows,
        "pure_H": {"clearing_shift": list(h_shift),
                   "polynomial": context.singular(h_poly),
                   "terms": encode_poly(h_poly)},
        "localizers": {
            "H": "u*(" + context.singular(h_poly) + ")-1",
            "all_b": "z*" + live_b + "-1",
            "selected_a_d": "w*" + live_ad + "-1",
            "selected_c_numerators_optional_interior": (
                "v*" + live_c_numerators + "-1"
            ),
        },
        "scope_guard": (
            "The broad stratum uses H/all_b/selected_a_d only. The true "
            "all-offdiagonal selected-term interior additionally uses the "
            "optional selected_c_numerators localizer. Its complement is a "
            "union of partial c_e=0 faces, each requiring a separate joint "
            "(branch,term) orbit reduction; it is not automatically aligned."
        ),
    }


def main():
    orbit_records = support_orbits()
    records = [build_record(mask, orbit, stabilizer)
               for mask, orbit, stabilizer in orbit_records]
    # Stable ordering by k then mask is easier for downstream status tables.
    records.sort(key=lambda row: (row["k"], row["mask"]))
    require([record["mask"] for record in records]
            == [0, 1, 3, 12, 7, 11, 13, 15, 30, 31, 63],
            "unexpected canonical orbit representative list")
    result = {
        "status": "UNAUDITED symmetry-complete branch0 offdiag stratum interface",
        "edge_order": ["".join(map(str, edge)) for edge in EDGES],
        "substitution": {
            "selected": "[[a_e,b_e],[-(1+a_e*d_e)/b_e,d_e]]",
            "unselected": "[[a_e,b_e],[-1/b_e,0]]",
        },
        "group": "S4 on supervertices, order 24",
        "support_orbit_count": len(records),
        "support_orbits": records,
        "methodology": (
            "Each row is rebuilt from the raw branch0 endpoint ordering; "
            "only b denominators are cleared. The broad closure has three "
            "localizers (H, all b, selected a*d); an explicitly separated "
            "fourth localizer selects the c-nonzero interior."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch0 offdiag support interface: PASS")
    print("orbits:", [(row["support_edges"], row["orbit_size"])
                      for row in records])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
