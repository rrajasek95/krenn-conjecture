#!/usr/bin/env python3
"""Exact, solver-free sparse analysis of the consumed rep2 group16 chart."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-referee-comparison-2026-08-26/rep2_group016_torus_A67zero_A12zero_guardpivot_k0_Q.sing"
TERMINAL = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-combined-smallest-modular-terminal-referee-2026-08-26/results_referee.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_top(text: str) -> list[str]:
    out, depth, start = [], 0, 0
    for i, char in enumerate(text):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            out.append(text[start:i].strip())
            start = i + 1
    out.append(text[start:].strip())
    assert depth == 0
    return out


# A monomial is the sorted tuple of variable indices, with repetition.
Poly = dict[tuple[int, ...], int]


def add(left: Poly, right: Poly, scale: int = 1) -> Poly:
    out = dict(left)
    for mono, coeff in right.items():
        value = out.get(mono, 0) + scale * coeff
        if value:
            out[mono] = value
        else:
            out.pop(mono, None)
    return out


def mul(left: Poly, right: Poly) -> Poly:
    if not left or not right:
        return {}
    out: Poly = {}
    for lm, lc in left.items():
        for rm, rc in right.items():
            mono = tuple(sorted(lm + rm))
            out[mono] = out.get(mono, 0) + lc * rc
    return {mono: coeff for mono, coeff in out.items() if coeff}


TOKEN = re.compile(r"\s*([A-Za-z_][A-Za-z0-9_]*|[0-9]+|[-+*()])")


class Parser:
    def __init__(self, source: str, variable_index: dict[str, int]):
        self.tokens = TOKEN.findall(source)
        compact = re.sub(r"\s+", "", source)
        assert "".join(self.tokens) == compact, (source, self.tokens)
        self.pos = 0
        self.variable_index = variable_index

    def peek(self) -> str | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def pop(self, expected: str | None = None) -> str:
        token = self.tokens[self.pos]
        self.pos += 1
        if expected is not None:
            assert token == expected, (expected, token)
        return token

    def parse(self) -> Poly:
        value = self.expression()
        assert self.pos == len(self.tokens), self.tokens[self.pos:]
        return value

    def expression(self) -> Poly:
        value = self.term()
        while self.peek() in ("+", "-"):
            op = self.pop()
            value = add(value, self.term(), 1 if op == "+" else -1)
        return value

    def term(self) -> Poly:
        value = self.factor()
        while self.peek() == "*":
            self.pop("*")
            value = mul(value, self.factor())
        return value

    def factor(self) -> Poly:
        if self.peek() == "-":
            self.pop("-")
            return {mono: -coeff for mono, coeff in self.factor().items()}
        if self.peek() == "+":
            self.pop("+")
            return self.factor()
        if self.peek() == "(":
            self.pop("(")
            value = self.expression()
            self.pop(")")
            return value
        token = self.pop()
        if token.isdigit():
            return {} if int(token) == 0 else {(): int(token)}
        return {(self.variable_index[token],): 1}


def rank_mod(rows: list[dict[int, int]], prime: int) -> int:
    pivots: dict[int, dict[int, int]] = {}
    for raw in rows:
        row = {col: value % prime for col, value in raw.items() if value % prime}
        while row:
            col = min(row)
            if col not in pivots:
                inv = pow(row[col], prime - 2, prime)
                row = {c: (v * inv) % prime for c, v in row.items() if (v * inv) % prime}
                pivots[col] = row
                break
            scale = row[col]
            pivot = pivots[col]
            for c, value in pivot.items():
                nv = (row.get(c, 0) - scale * value) % prime
                if nv:
                    row[c] = nv
                else:
                    row.pop(c, None)
    return len(pivots)


def rank_q(rows: list[dict[int, int]]) -> int:
    pivots: dict[int, dict[int, Fraction]] = {}
    for raw in rows:
        row = {col: Fraction(value) for col, value in raw.items() if value}
        while row:
            col = min(row)
            if col not in pivots:
                lead = row[col]
                row = {c: v / lead for c, v in row.items() if v}
                pivots[col] = row
                break
            scale = row[col]
            pivot = pivots[col]
            for c, value in pivot.items():
                new = row.get(c, Fraction(0)) - scale * value
                if new:
                    row[c] = new
                else:
                    row.pop(c, None)
    return len(pivots)


def poly_text(poly: Poly, variables: list[str]) -> str:
    if not poly:
        return "0"
    terms = []
    for mono in sorted(poly, key=lambda m: (len(m), m)):
        coeff = poly[mono]
        atom = "*".join(variables[i] for i in mono) if mono else "1"
        if not mono:
            term = str(abs(coeff))
        elif abs(coeff) == 1:
            term = atom
        else:
            term = f"{abs(coeff)}*{atom}"
        if not terms:
            terms.append(("-" if coeff < 0 else "") + term)
        else:
            terms.append(("-" if coeff < 0 else "+") + term)
    return "".join(terms)


def substitute(poly: Poly, replacements: list[Poly]) -> Poly:
    out: Poly = {}
    for mono, coeff in poly.items():
        term: Poly = {(): coeff}
        for index in mono:
            term = mul(term, replacements[index])
        out = add(out, term)
    return out


def materialize_stratum(
    name: str,
    old_variables: list[str],
    old_polys: list[Poly],
    removed: set[str],
    added: list[str],
    replacement_text: dict[str, str],
    extra_generators: list[str],
) -> dict:
    new_variables = [v for v in old_variables if v not in removed] + added
    new_index = {name: i for i, name in enumerate(new_variables)}
    replacements = []
    for variable in old_variables:
        expression = replacement_text.get(variable, variable)
        replacements.append(Parser(expression, new_index).parse())
    # The six factored first guards are eliminated by the stratum identities.
    retained = list(range(6561)) + list(range(6567, 6574))
    transformed = [substitute(old_polys[i], replacements) for i in retained]
    transformed.extend(Parser(g, new_index).parse() for g in extra_generators)
    zero_count = sum(not p for p in transformed)
    transformed = [p for p in transformed if p]
    unique = []
    seen = set()
    for poly in transformed:
        key = tuple(sorted(poly.items()))
        if key not in seen:
            seen.add(key)
            unique.append(poly)
    source_path = HERE / f"rep2_group016_67_{name}_Q.sing"
    source = (
        "// DESIGN-ONLY reversible stratum; no solve authorized.\n"
        "option(noredefine);\n"
        f"ring r=0,({','.join(new_variables)}),dp;\n"
        "ideal I=" + ",\n".join(poly_text(p, new_variables) for p in unique) + ";\n"
        'print("INPUT_VARIABLES="+string(nvars(r)));\n'
        'print("INPUT_GENERATORS="+string(size(I)));\n'
        "quit;\n"
    )
    source_path.write_text(source)
    return {
        "name": name,
        "variables": len(new_variables),
        "generators": len(unique),
        "zero_after_substitution": zero_count,
        "duplicates_after_substitution": len(transformed) - len(unique),
        "source": source_path.name,
        "sha256": sha256(source_path),
        "bytes": len(source.encode()),
        "removed_variables": sorted(removed),
        "added_variables": added,
        "replacement_text": replacement_text,
        "extra_generators": extra_generators,
    }


def main() -> None:
    assert sha256(SOURCE) == "2403105f5c6bf4860525220d0d2d036099b79ace67297c864767ae71b9e97339"
    assert sha256(TERMINAL) == "d0f48380558bb663567083c744667f76fad18cb85cc47e0e93b857dc05cac68f"
    text = SOURCE.read_text()
    variables = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
    assert len(variables) == 67
    body = text.split("ideal I=", 1)[1].split(";\n", 1)[0]
    generators = split_top(body)
    assert len(generators) == 6574
    variable_index = {name: i for i, name in enumerate(variables)}

    polys = []
    for index, generator in enumerate(generators):
        polys.append(Parser(generator, variable_index).parse())
        if index % 1000 == 0:
            print(f"parsed {index}", flush=True)

    monomials = sorted(set().union(*(poly.keys() for poly in polys)))
    monomial_index = {mono: i for i, mono in enumerate(monomials)}
    amplitude_rows = [
        {monomial_index[m]: c for m, c in poly.items()} for poly in polys[:6561]
    ]
    rank_primes = [1000003, 1000033]
    amplitude_ranks = {str(p): rank_mod(amplitude_rows, p) for p in rank_primes}

    support_rows = []
    for poly in polys[:6561]:
        used = set(i for mono in poly for i in mono)
        support_rows.append({i: 1 for i in used})
    support_ranks = {str(p): rank_mod(support_rows, p) for p in rank_primes}

    exponent_rows = []
    for mono in monomials:
        counts = Counter(mono)
        exponent_rows.append(dict(counts))
    exponent_ranks = {str(p): rank_mod(exponent_rows, p) for p in rank_primes}

    linear_columns = [()] + [(i,) for i in range(len(variables))]
    linear_index = {mono: i for i, mono in enumerate(linear_columns)}
    linear_rows = [
        {linear_index[m]: c for m, c in poly.items() if m in linear_index}
        for poly in polys[:6561]
    ]
    linear_ranks = {str(p): rank_mod(linear_rows, p) for p in rank_primes}
    exact_small_ranks = {
        "amplitude_variable_support_incidence_Q": rank_q(support_rows),
        "monomial_exponent_incidence_Q": rank_q(exponent_rows),
        "amplitude_affine_linear_part_Q": rank_q(linear_rows),
    }

    incidence = {}
    for i, name in enumerate(variables):
        amp_count = sum(any(i in mono for mono in poly) for poly in polys[:6561])
        tail_count = sum(any(i in mono for mono in poly) for poly in polys[6561:])
        incidence[name] = {"amplitude_generators": amp_count, "tail_generators": tail_count}

    monic_graphs = []
    for generator_index, poly in enumerate(polys):
        for variable, variable_name in enumerate(variables):
            coefficient = poly.get((variable,), 0)
            if abs(coefficient) != 1:
                continue
            if any(variable in mono for mono in poly if mono != (variable,)):
                continue
            monic_graphs.append({
                "generator": generator_index,
                "variable": variable_name,
                "coefficient": coefficient,
            })

    degree_histogram = Counter(max(map(len, p)) if p else -1 for p in polys[:6561])
    term_histogram = Counter(len(p) for p in polys[:6561])

    # The first six guards have an exact two-row factorization.
    H10 = Parser(
        "(-xn2*a57_01+a57_02)*a57_10+(-xn0*a57_02+xn2)*a57_11+(xn0*a57_01-1)*a57_12",
        variable_index,
    ).parse()
    H20 = Parser(
        "(-xn2*a57_01+a57_02)*a57_20+(-xn0*a57_02+xn2)*a57_21+(xn0*a57_01-1)*a57_22",
        variable_index,
    ).parse()
    identities = {
        6561: add(Parser("a57_01*a57_10-a57_11", variable_index).parse(), mul(Parser("t0", variable_index).parse(), H10)),
        6562: add(Parser("a57_01*a57_20-a57_21", variable_index).parse(), mul(Parser("t0", variable_index).parse(), H20)),
        6563: mul(Parser("t1", variable_index).parse(), H10),
        6564: mul(Parser("t1", variable_index).parse(), H20),
        6565: mul(Parser("t2", variable_index).parse(), H10),
        6566: mul(Parser("t2", variable_index).parse(), H20),
    }
    assert all(polys[index] == expected for index, expected in identities.items())

    simplified = []
    prefix = text.split("ideal I=", 1)[0] + "ideal I="
    suffix = text.split(";\n", 1)[1]
    for poly in polys:
        simplified.append(poly_text(poly, variables))
    simplified_text = prefix + ",\n".join(simplified) + ";\n" + suffix
    simplified_path = HERE / "rep2_group016_67_canonical_expanded_reference_Q.sing"
    simplified_path.write_text(simplified_text)

    tail_path = HERE / "tail13_expanded.json"
    tail_path.write_text(json.dumps({
        str(i): {
            "expanded": poly_text(polys[i], variables),
            "monomials": len(polys[i]),
            "total_degree": max(map(len, polys[i])) if polys[i] else -1,
        }
        for i in range(6561, 6574)
    }, indent=2, sort_keys=True) + "\n")

    graph_replacements = {
        "a57_11": "a57_01*a57_10",
        "a57_12": "a57_02*a57_10",
        "a57_21": "a57_01*a57_20",
        "a57_22": "a57_02*a57_20",
    }
    strata = []
    strata.append(materialize_stratum(
        "Dt1", variables, polys,
        set(graph_replacements), ["it1"], graph_replacements,
        ["t1*it1-1"],
    ))
    strata.append(materialize_stratum(
        "Vt1_Dt2", variables, polys,
        set(graph_replacements) | {"t1"}, ["it2"],
        graph_replacements | {"t1": "0"}, ["t2*it2-1"],
    ))
    b0 = "(a26_00+a26_01*a57_01+a26_02*a57_02)"
    id_expr = f"({b0}*sat)"
    K10 = "((-xn2*a57_01+a57_02)*a57_10+(-xn0*a57_02+xn2)*a57_11)"
    K20 = "((-xn2*a57_01+a57_02)*a57_20+(-xn0*a57_02+xn2)*a57_21)"
    dt0_replacements = {
        "t1": "0", "t2": "0",
        "a57_12": f"-{id_expr}*(it0*(a57_01*a57_10-a57_11)+{K10})",
        "a57_22": f"-{id_expr}*(it0*(a57_01*a57_20-a57_21)+{K20})",
    }
    strata.append(materialize_stratum(
        "Vt1_Vt2_Dt0", variables, polys,
        {"t1", "t2", "a57_12", "a57_22"}, ["it0"],
        dt0_replacements, ["t0*it0-1"],
    ))
    closed_replacements = {
        "t0": "0", "t1": "0", "t2": "0",
        "a57_11": "a57_01*a57_10", "a57_21": "a57_01*a57_20",
    }
    strata.append(materialize_stratum(
        "Vt0_Vt1_Vt2", variables, polys,
        {"t0", "t1", "t2", "a57_11", "a57_21"}, [],
        closed_replacements, [],
    ))

    result = {
        "schema": "KRENN_X5_REP2_GROUP16_67_TIMEOUT_REDUCTION_DESIGN_V1",
        "status": "PASS_DESIGN_ONLY_NO_SOLVE",
        "source": {"path": str(SOURCE.relative_to(ROOT)), "sha256": sha256(SOURCE)},
        "terminal_referee": {"path": str(TERMINAL.relative_to(ROOT)), "sha256": sha256(TERMINAL)},
        "counts": {
            "variables": len(variables), "generators": len(polys),
            "amplitudes": 6561, "guards": 12, "saturation": 1,
            "unique_expanded_monomials_all": len(monomials),
            "expanded_terms_amplitudes": sum(len(p) for p in polys[:6561]),
            "expanded_terms_tail": sum(len(p) for p in polys[6561:]),
            "source_bytes": len(text.encode()), "simplified_source_bytes": len(simplified_text.encode()),
        },
        "ranks": {
            "exact_Q": exact_small_ranks | {"amplitude_coefficient_span_Q": 6561},
            "amplitude_coefficient_span_mod_primes": amplitude_ranks,
            "amplitude_variable_support_incidence_mod_primes": support_ranks,
            "monomial_exponent_incidence_mod_primes": exponent_ranks,
            "amplitude_affine_linear_part_mod_primes": linear_ranks,
            "interpretation": "Q ranks use exact Fraction elimination for the <=68-column incidence matrices; coefficient-span rank is exactly 6561 because either modular rank reaches the 6561-row upper bound",
        },
        "variable_incidence": incidence,
        "amplitude_structure": {
            "word_indexing": "6561=3^8 literal color words",
            "all_67_coordinates_active": all(v["amplitude_generators"] > 0 for v in incidence.values()),
            "expanded_total_degree_histogram": dict(sorted(degree_histogram.items())),
            "expanded_term_count_histogram": dict(sorted(term_histogram.items())),
            "monic_graph_candidates_all_generators": monic_graphs,
            "exact_linear_redundancy": 0,
            "reason": "the 6561 amplitude coefficient rows have exact rank 6561 over Q",
        },
        "guard_factorization": {
            "H10": poly_text(H10, variables), "H20": poly_text(H20, variables),
            "verified_indices": list(identities),
        },
        "canonical_expanded_reference": {
            "path": simplified_path.name,
            "sha256": sha256(simplified_path),
            "warning": "algebraically canonical but byte-larger than the factored parent; not a recommended runtime source",
        },
        "tail_expansion": {"path": tail_path.name, "sha256": sha256(tail_path)},
        "exact_stratified_cover": {
            "partition": ["D(t1)", "V(t1) intersect D(t2)", "V(t1,t2) intersect D(t0)", "V(t0,t1,t2)"],
            "strata": strata,
            "proof": {
                "unit_d": "d=xn0*a57_01-1 is a unit because d*b0*sat=1",
                "first_guard_rows": "g0_r=a57_01*a57_r0-a57_r1+t0*H_r; g1_r=t1*H_r; g2_r=t2*H_r",
                "Dt1_or_Dt2": "the open t forces H_r=0; g0 gives a57_r1=a57_01*a57_r0; then H_r=d*(a57_r2-a57_02*a57_r0), so the unit d gives the second graph",
                "Dt0": "after t1=t2=0, t0 and d are units and g0_r uniquely solves a57_r2; id=b0*sat is d^{-1} and it0 is t0^{-1}",
                "closed": "at t0=t1=t2=0, g0_r is exactly a57_01*a57_r0-a57_r1 and the other four first guards vanish",
            },
        },
        "solver_run": False,
        "unit_certificate": False,
        "minimal_literal_unit_subset": None,
    }
    (HERE / "results_design.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["counts"], sort_keys=True))
    print(json.dumps(result["ranks"], sort_keys=True))


if __name__ == "__main__":
    main()
