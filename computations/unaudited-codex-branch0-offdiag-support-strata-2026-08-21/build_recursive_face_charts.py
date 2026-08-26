#!/usr/bin/env python3
"""Build four canonical lower-defect branch0 permanent-face charts.

For a state (B=0,T,D), a term bit one selects the offdiagonal permanent
term and a term bit zero selects the diagonal permanent term.  The canonical
cycle-boundary states considered here all have D subset T, so only selected
offdiagonal edges can remain both-live:

  T_e=1,e in D: [[a,b],[-(1+a*d)/b,d]]
  T_e=1,e not D: [[a,b],[-1/b,0]]
  T_e=0: [[a,b],[0,-1/a]].

The site torus gauges a spanning tree of selected offdiagonal b entries to
one and its residual common scale gauges the first live d to one.  This is a
lossless algebraic-closure normalization on the localized chart.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "build_support_strata_interface.py"
OUT = HERE / "results_recursive_face_charts.json"
STATES = ((0, 31, 13), (0, 15, 3), (0, 30, 12), (0, 13, 1))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


BASE = load("n8_recursive_face_base", BASE_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


class FaceContext(BASE.Context):
    def __init__(self, term_mask, full_mask):
        self.term_mask = term_mask
        self.full_mask = full_mask
        full = tuple(edge for edge in range(6) if full_mask >> edge & 1)
        require(full_mask & ~term_mask == 0,
                "this interface expects D subset T")
        super().__init__(full)

    def entries(self):
        answer = []
        for edge in range(6):
            a, b = self.variable(edge), self.variable(6 + edge)
            if self.term_mask >> edge & 1:
                if edge in self.d_index:
                    d = self.variable(self.d_index[edge])
                    c = self.add(self.variable(6 + edge, -1, -1),
                                 self.multiply(
                                     a, d,
                                     self.variable(6 + edge, -1, -1)))
                else:
                    c = self.variable(6 + edge, -1, -1)
                    d = {}
            else:
                c = {}
                d = self.variable(edge, -1, -1)
            answer.extend((a, b, c, d))
        return tuple(answer)

    def clear_denominators(self, poly):
        if not poly:
            return {}, self.zero_exponent
        shift = tuple(-min([exponent[index] for exponent in poly] + [0])
                      for index in range(self.n))
        require(not any(shift[index] for index in range(12, self.n)),
                "a live d denominator appeared")
        cleared = {
            tuple(exponent[index] + shift[index]
                  for index in range(self.n)): coefficient
            for exponent, coefficient in poly.items()
        }
        return BASE.clean(cleared), shift


def power(context, poly, exponent):
    answer = context.one
    for _ in range(exponent):
        answer = context.multiply(answer, poly)
    return answer


def substitute(context, poly, replacements):
    answer = {}
    for exponent, coefficient in poly.items():
        term = context.scale(context.one, coefficient)
        for index, multiplicity in enumerate(exponent):
            if multiplicity:
                term = context.multiply(
                    term, power(context, replacements[index], multiplicity))
        answer = context.add(answer, term)
    return answer


def spanning_tree(term_mask):
    parent = list(range(4))

    def find(value):
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    selected = []
    for edge, (left, right) in enumerate(BASE.EDGES):
        if not term_mask >> edge & 1:
            continue
        left_root, right_root = find(left), find(right)
        if left_root == right_root:
            continue
        parent[left_root] = right_root
        selected.append(edge)
    require(len(selected) == 3, "selected offdiagonal graph is disconnected")
    return tuple(selected)


def encode_poly(poly):
    return [{"exponents": list(exponent),
             "coefficient": [coefficient.numerator, coefficient.denominator]}
            for exponent, coefficient in sorted(poly.items())]


def build_state(state):
    branch, term_mask, full_mask = state
    require(branch == 0 and full_mask, "unexpected canonical state")
    context = FaceContext(term_mask, full_mask)
    equations, raw_h = BASE.PROBE.equations((0,) * 6)
    labels = BASE.raw_labels()
    raw_rows = []
    for label, equation in zip(labels, equations):
        value = context.substitute(equation)
        if value:
            value, shift = context.clear_denominators(value)
        else:
            shift = context.zero_exponent
        raw_rows.append((label, value, shift))
    require(not any(value for _, value, _ in raw_rows[:6]),
            "a permanent row survived solved substitution")
    raw_h = context.substitute(raw_h)
    raw_h, h_shift = context.clear_denominators(raw_h)
    require(raw_h, "pure H vanished identically")

    tree = spanning_tree(term_mask)
    first_full = min(context.support)
    gauge = {index: context.variable(index) for index in range(context.n)}
    for edge in tree:
        gauge[6 + edge] = context.one
    gauge[context.d_index[first_full]] = context.one
    rows = []
    for raw_index, (label, value, shift) in enumerate(raw_rows):
        gauged = substitute(context, value, gauge)
        if gauged:
            rows.append({"raw_index": raw_index, "label": label,
                         "clearing_shift": list(shift),
                         "polynomial": context.singular(gauged),
                         "terms": encode_poly(gauged)})
    h_value = substitute(context, raw_h, gauge)

    base_factors = []
    for edge in range(6):
        base_factors.append(context.variable(6 + edge)
                            if term_mask >> edge & 1
                            else context.variable(edge))
    base_live = context.multiply(*base_factors)
    both_live = context.multiply(*(
        context.multiply(context.variable(edge),
                         context.variable(context.d_index[edge]))
        for edge in context.support
    ))
    c_live = context.multiply(*(
        context.add(context.one,
                    context.multiply(context.variable(edge),
                                     context.variable(context.d_index[edge])))
        for edge in context.support
    ))
    base_live = substitute(context, base_live, gauge)
    both_live = substitute(context, both_live, gauge)
    c_live = substitute(context, c_live, gauge)

    return {
        "key": ":".join(map(str, state)),
        "branch_mask": branch,
        "selected_term_mask": term_mask,
        "both_live_edge_mask": full_mask,
        "selected_offdiagonal_edges": [edge for edge in range(6)
                                        if term_mask >> edge & 1],
        "selected_diagonal_edges": [edge for edge in range(6)
                                     if not term_mask >> edge & 1],
        "both_live_edges": list(context.support),
        "variable_names": list(context.variable_names),
        "gauge_b_edges": list(tree),
        "gauge_d_edge": first_full,
        "raw_source_row_count": len(equations),
        "nonzero_gauged_source_row_count": len(rows),
        "rows": rows,
        "pure_H": {"clearing_shift": list(h_shift),
                   "polynomial": context.singular(h_value),
                   "terms": encode_poly(h_value)},
        "localizers": {
            "H": "u*(" + context.singular(h_value) + ")-1",
            "selected_base_terms": (
                "z*(" + context.singular(base_live) + ")-1"),
            "both_live_a_d": (
                "w*(" + context.singular(both_live) + ")-1"),
            "both_live_c_numerators": (
                "v*(" + context.singular(c_live) + ")-1"),
        },
        "scope_guard": (
            "All four localizers define the exact H-live interior of this "
            "recursive face.  Dropping a localizer is a stronger test; a "
            "zero of one remaining c numerator routes to a deeper node."
        ),
    }


def main():
    records = [build_state(state) for state in STATES]
    require([record["key"] for record in records]
            == ["0:31:13", "0:15:3", "0:30:12", "0:13:1"],
            "canonical state order changed")
    result = {
        "status": "UNAUDITED exact four recursive face chart interfaces",
        "edge_order": ["".join(map(str, edge)) for edge in BASE.EDGES],
        "states": records,
        "torus_action": (
            "diag(t_i,t_i^-1): a_ij->t_i*t_j*a_ij, "
            "b_ij->t_i/t_j*b_ij, c_ij->t_j/t_i*c_ij, "
            "d_ij->d_ij/(t_i*t_j)"
        ),
        "gauge_scope": (
            "Every selected offdiagonal graph is connected.  Three live b "
            "entries on a spanning tree are set to one; the residual common "
            "scale sets one live d to one over the algebraic closure."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("four recursive branch0 face charts: PASS")
    print([(record["key"], record["nonzero_gauged_source_row_count"],
            record["gauge_b_edges"], record["gauge_d_edge"])
           for record in records])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
