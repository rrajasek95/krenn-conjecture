#!/usr/bin/env python3
"""Replay the source-faithful order-two audit for the orbit-85 branch.

This is deliberately a provenance/identity check, not an ideal-membership
solve.  It separates inside-free (FR) equations that can be divided by an
already audited live witness star from those whose star is not localized.
"""

from __future__ import annotations

import collections
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (ROOT / "computations/"
               "unaudited-codex-n8-diagonal-orbit85-extended-certificate-2026-08-23/"
               "certificate_dag.json")
FROZEN = Path(__file__).with_name("results.json")


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


class Poly:
    """Tiny sparse polynomial ring over Z used for the three generic checks."""

    def __init__(self, terms=None):
        self.terms = {tuple(sorted(m)): c for m, c in (terms or {}).items() if c}

    @staticmethod
    def constant(value: int) -> "Poly":
        return Poly({(): value})

    @staticmethod
    def variable(name: str) -> "Poly":
        return Poly({(name,): 1})

    def __add__(self, other):
        other = as_poly(other)
        terms = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            terms[monomial] = terms.get(monomial, 0) + coefficient
            if terms[monomial] == 0:
                del terms[monomial]
        return Poly(terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-as_poly(other))

    def __rsub__(self, other):
        return as_poly(other) - self

    def __mul__(self, other):
        other = as_poly(other)
        terms = {}
        for left, lc in self.terms.items():
            for right, rc in other.terms.items():
                monomial = tuple(sorted(left + right))
                terms[monomial] = terms.get(monomial, 0) + lc * rc
        return Poly(terms)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.terms == as_poly(other).terms

    def evaluate(self, values):
        total = 0
        for monomial, coefficient in self.terms.items():
            term = coefficient
            for variable in monomial:
                term *= values[variable]
            total += term
        return total


def as_poly(value):
    return value if isinstance(value, Poly) else Poly.constant(value)


def var(name: str) -> Poly:
    return Poly.variable(name)


def matchings(vertices):
    """Perfect matchings of a tuple, with no duplicate ordering."""
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in matchings(rest):
            yield ((first, second),) + tail


MATCHINGS8 = tuple(matchings(tuple(range(8))))
require(len(MATCHINGS8) == 105, "K8 perfect-matching census changed")


def tail2_terms(masks):
    colour = {}
    for c, mask in enumerate(masks):
        for site in range(8):
            if mask & (1 << site):
                require(site not in colour, "overlapping colour masks")
                colour[site] = c
    require(len(colour) == 8, "colour masks do not partition eight sites")
    return sum(
        1 for matching in MATCHINGS8
        if sum(colour[i] != colour[j] for i, j in matching) == 2
    )


def profile(masks):
    return tuple(sorted((int(mask).bit_count() for mask in masks), reverse=True))


def fr_source_masks(row):
    _, colour, site, first, second = row["tag"]
    masks = [0, 0, 0]
    masks[colour] = (1 << 7) | (1 << site)
    remaining = [c for c in range(3) if c != colour]
    masks[remaining[0]] = first
    masks[remaining[1]] = second
    require(sum(masks) == 255, "FR masks do not partition the sites")
    return tuple(masks)


def generic_identity_checks():
    # A live witness star x with inverse u source-lifts P through F=xP+e2 Q.
    x, u, p, q, e2 = map(var, ("x", "u", "P", "Q", "epsilon2"))
    full_row = x * p + e2 * q
    localizer = u * x - 1
    require(u * full_row - p == p * localizer + e2 * u * q,
            "live-star FR lift identity failed")

    # At a nonlocalized residual star, xP does not imply P.  This explicit
    # quotient point also permits arbitrary unrelated live/pure variables.
    values = {"x": 0, "P": 1, "Q": 0, "epsilon2": 0}
    require((x * p).evaluate(values) == 0 and p.evaluate(values) == 1,
            "residual-star nonmembership counterguard failed")

    # Generalized complement identity, including its true order-two term.
    r = [var(f"r{i}") for i in range(3)]
    ps = [var(f"P{i}") for i in range(3)]
    qs = [var(f"Q{i}") for i in range(3)]
    rows = [x * ps[i] + e2 * qs[i] for i in range(3)]
    complement = sum((r[i] * ps[i] for i in range(3)), Poly()) - 1
    derived = sum((r[i] * rows[i] for i in range(3)), Poly()) - x * complement
    expected = x + e2 * sum((r[i] * qs[i] for i in range(3)), Poly())
    require(derived == expected, "deformed complement identity failed")
    return {
        "live_witness_FR": "u*(x*P+epsilon^2*Q)-P=P*(u*x-1)+epsilon^2*u*Q",
        "residual_FR_counterguard": "x=0,P=1 sends x*P to 0 but P to 1",
        "complement": (
            "sum_j r_j*(x*P_j+epsilon^2*Q_j)-x*(sum_j r_j*P_j-1)"
            "=x+epsilon^2*sum_j r_j*Q_j"
        ),
    }


def build_result():
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    require(data["format"] == "n8diag-orbit85-extended-ns-dag-v1",
            "unexpected certificate format")
    require(data["case"] == [[3, 4, 5], [3, 4, 5, 6], [3, 4, 5, 6]],
            "orbit-85 case changed")

    antecedents = {row["id"]: row for row in data["antecedents"]}
    all_fr = [row for row in antecedents.values()
              if row["kind"] == "inside_free_product_zero"]
    all_complements = [row for row in antecedents.values()
                       if row["kind"] == "outside_free_complement_localizer"]
    all_guarded = [row for row in antecedents.values()
                   if row["kind"] == "selector_guarded_inverse"]
    all_open = [row for row in antecedents.values()
                if row["kind"] == "unguarded_open_localizer"]

    compile_nodes = [node for node in data["proof_nodes"]
                     if node["op"] == "compile_clause"]
    refs = [ref for node in compile_nodes
            for ref in node["compiler"]["antecedents"]]
    core_fr = [antecedents[ref] for ref in refs if ref.startswith("fr:")]
    require(len(core_fr) == len({row["id"] for row in core_fr}),
            "an FR antecedent unexpectedly repeats in the core")

    def classify_fr(rows):
        answer = {"witness": [], "residual": []}
        for row in rows:
            _, colour, site, _, _ = row["tag"]
            masks = fr_source_masks(row)
            record = {
                "id": row["id"],
                "colour": colour,
                "site": site,
                "profile": "+".join(map(str, profile(masks))),
                "tail2_terms": tail2_terms(masks),
            }
            answer["witness" if site == colour else "residual"].append(record)
        return answer

    all_classified = classify_fr(all_fr)
    core_classified = classify_fr(core_fr)
    require((len(all_classified["witness"]), len(all_classified["residual"]))
            == (96, 352), "full FR witness/residual census changed")
    require((len(core_classified["witness"]), len(core_classified["residual"]))
            == (19, 74), "core FR witness/residual census changed")

    core_profile_counts = {
        name: dict(sorted(collections.Counter(
            item["profile"] for item in records).items()))
        for name, records in core_classified.items()
    }
    core_tail_counts = {
        name: sum(item["tail2_terms"] for item in records)
        for name, records in core_classified.items()
    }
    require(core_profile_counts == {
        "witness": {"4+2+2": 19},
        "residual": {"4+2+2": 70, "6+2+0": 4},
    }, f"core FR profiles changed: {core_profile_counts}")
    require(core_tail_counts == {"witness": 570, "residual": 2460},
            f"core FR Tail2 support changed: {core_tail_counts}")

    ref_kind_occurrences = collections.Counter(
        antecedents[ref]["kind"] for ref in refs)
    distinct_ref_kinds = collections.Counter(
        antecedents[ref]["kind"] for ref in set(refs))
    complement_ref_counts = collections.Counter(
        ref for ref in refs if ref.startswith("comp:"))
    require(len(all_complements) == 7 and len(all_guarded) == 384
            and len(all_open) == 9, "localizer census changed")
    require((sum(complement_ref_counts.values()), len(complement_ref_counts))
            == (17, 5), "core complement-reference census changed")

    identities = generic_identity_checks()
    result = {
        "verdict": "BRANCH_RELATIVE_TAIL_GAP_IS_REAL",
        "orbit": 85,
        "substitution": "A_ij^(ab)=delta_ab*d_ij^a+epsilon*T_ij^(ab), a!=b for T",
        "identity_replay": identities,
        "antecedent_audit": {
            "FR_total": len(all_fr),
            "FR_witness_live_and_source_liftable": len(all_classified["witness"]),
            "FR_residual_not_source_liftable_without_new_open": len(all_classified["residual"]),
            "complement_localizers_total": len(all_complements),
            "selector_guarded_inverse_localizers": len(all_guarded),
            "unguarded_open_localizers": len(all_open),
            "ordinary_same_colour_localizer_epsilon2": 0,
            "complement_localizer_status": (
                "epsilon-constant only as retained constructible-branch hypothesis; "
                "not a literal X5 or pure-normalization equation"
            ),
        },
        "trimmed_core_audit": {
            "compiled_clauses": len(compile_nodes),
            "FR_total": len(core_fr),
            "FR_witness_liftable": len(core_classified["witness"]),
            "FR_residual_unresolved": len(core_classified["residual"]),
            "FR_profile_counts": core_profile_counts,
            "FR_Tail2_monomial_occurrences": core_tail_counts,
            "complement_reference_occurrences": sum(complement_ref_counts.values()),
            "distinct_complement_localizers_referenced": len(complement_ref_counts),
            "complement_reference_counts": dict(sorted(complement_ref_counts.items())),
            "antecedent_reference_kind_occurrences": dict(sorted(ref_kind_occurrences.items())),
            "distinct_antecedent_references_by_kind": dict(sorted(distinct_ref_kinds.items())),
        },
        "corrected_order_two_interface": {
            "direct_mixed_amplitude_leaf": "Tail2_w",
            "witness_FR_leaf": "u_x*Tail2_w",
            "residual_FR_leaf": "UNDEFINED_FROM_LITERAL_SOURCE_PACKET",
            "complement_C0_derived_star": "sum_j r_j*Tail2_wj",
            "complement_localizer": "0 if retained branch hypothesis is fixed",
            "other_same_colour_localizers": "0",
            "whole_core_coefficient": (
                "not source-defined from literal X5 plus pure normalization: "
                "74 compiled FR leaves lack a valid lift"
            ),
        },
        "minimal_new_hypothesis": (
            "for each residual FR occurrence either localize its star x and use "
            "u_x*F_w, or retain P=0 as an order-two branch equation; the latter "
            "is exactly branch persistence and is not supplied by literal X5"
        ),
        "scope": (
            "The x=0,P=1 quotient is a local provenance counterguard. It proves "
            "there is no uniform division-free lift from the corresponding row xP; "
            "it does not assert a global point of the full normalized X5 fibre."
        ),
    }
    return result


def main() -> None:
    result = build_result()
    if FROZEN.exists():
        require(json.loads(FROZEN.read_text(encoding="utf-8")) == result,
                "frozen results.json does not match replay")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
