#!/usr/bin/env python3
"""T2: the representation-stability fingerprint of the centered occurrence
transfer.

Objects (all defined for every h, all computed exactly):

  O1 = k_f      the one-step full-endpoint transfer Gram row at order h+1,
  O2 = k2_f     the SAME construction iterated once (order h+2) -- i.e. the
                object the induction on h actually has to control,

decomposed fibrewise (ordered endpoints fixed) into the isotypic summands
S^{2lam} of the residual perfect-matching module.

Reported per h:
  * the shape list occurring in each object, in padded form,
  * whether the note's matching projector (A-lambda)/(2h-1) flattens the row,
  * whether the note's composite projector Pi_end Pi_match sends the row to a
    constant (the uniformity clause of the endgame),
  * the fibre constants, for polynomial fitting in h.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_stress import (  # noqa: E402
    edge, marked_occurrence, occurrence_count, occurrences, perfect_matchings,
)
from scheme import Scheme  # noqa: E402
from transfer import one_step_row, two_step_row  # noqa: E402

SCHEMES = {}


def get_scheme(order, full=True):
    if order not in SCHEMES:
        SCHEMES[order] = Scheme(order, full=full)
    return SCHEMES[order]


def fibre_type(p, s, marked):
    mp, ms, matching = marked
    def code(v):
        return "pf" if v == mp else ("sf" if v == ms else "r")
    tag = (code(p), code(s))
    if tag == ("r", "r"):
        mates = any(p in e and s in e for e in matching)
        return tag + ("mates" if mates else "apart",)
    return tag


def fibre_vectors(row, order, marked, sites, types_only=False):
    """Split a row over order-`order` occurrences into ordered-endpoint fibres.

    Returns {(p,s): (vector over the residual scheme's point order, type)}.
    The residual matchings are relabelled to 0..2(order-1)-1 by position, which
    is harmless: the isotypic decomposition is S-equivariant.
    """
    residual_order = order - 1
    scheme = get_scheme(residual_order)
    out = {}
    seen_types = set()
    for p in sites:
        for s in sites:
            if p == s:
                continue
            tag = fibre_type(p, s, marked)
            if types_only and tag in seen_types:
                continue
            seen_types.add(tag)
            rest = tuple(v for v in sites if v not in (p, s))
            relabel = {v: i for i, v in enumerate(rest)}
            vector = [Q(0)] * len(scheme.points)
            for m in perfect_matchings(rest):
                canonical = tuple(sorted(edge(relabel[a], relabel[b]) for a, b in m))
                vector[scheme.index[canonical]] = Q(row.get((p, s, m), 0))
            out[(p, s)] = (tuple(vector), tag)
    return out


def padded(shape, order):
    """Rewrite a partition of 2*order as a padded family label."""
    tail = tuple(shape[1:])
    return f"[2m-{2 * order - shape[0]}" + ("".join("," + str(t) for t in tail)
                                            ) + "]", tail


def analyse_row(name, row, order, marked, sites, types_only=False, verbose=True):
    scheme = get_scheme(order - 1)
    h_eff = order - 1                      # residual matching order
    lam = h_eff * h_eff - 3 * h_eff + 1
    fibres = fibre_vectors(row, order, marked, sites, types_only=types_only)

    by_type = defaultdict(list)
    for key, (vector, tag) in fibres.items():
        by_type[tag].append((key, vector))

    shape_content = {}
    flat_values = {}
    for tag, entries in by_type.items():
        chosen = entries if not types_only else entries[:1]
        contents = set()
        for key, vector in chosen:
            contents.add(tuple(scheme.shape_content(vector)))
        assert len(contents) == 1, ("fibres of one type differ in content", tag)
        shape_content[tag] = sorted(contents)[0]
        # matching projector: is (A - lambda) applied to the fibre constant?
        vector = chosen[0][1]
        image = scheme.space.apply_A(vector)
        flattened = tuple(a - lam * b for a, b in zip(image, vector, strict=True))
        constant = len(set(flattened)) == 1
        flat_values[tag] = (constant, str(flattened[0]) if constant else None)

    families = sorted({tuple(shape[1:]) for content in shape_content.values()
                       for shape in content})
    if verbose:
        print(f"  [{name}] order={order}, residual scheme order={h_eff}")
        for tag in sorted(shape_content, key=str):
            content = shape_content[tag]
            flat, value = flat_values[tag]
            print(f"    fibre {str(tag):<22} shapes={[list(c) for c in content]}"
                  f"  matching-flat={flat} value={value}")
        print(f"    padded families mu (shape = [2m-|2mu|, 2mu]): "
              f"{[list(f) for f in families]}")
    return {
        "object": name,
        "order": order,
        "residual_scheme_order": h_eff,
        "lambda_used": lam,
        "shape_content": {str(k): [list(c) for c in v]
                          for k, v in shape_content.items()},
        "matching_flat": {str(k): v for k, v in flat_values.items()},
        "padded_families": [list(f) for f in families],
    }


def endpoint_projector_check(row, order, marked, sites):
    """Does Pi_end Pi_match send the row to a constant, uniformly in h?

    h here is the residual matching order = order-1; the note's B_h has degree
    4h and nonconstant eigenvalues {-2, 2h-2, 2h} on the matching-flat module.
    """
    from lib_stress import endpoint_neighbors
    h = order - 1
    lam = h * h - 3 * h + 1
    occ = occurrences(sites)
    index = {o: i for i, o in enumerate(occ)}
    vector = tuple(Q(row.get(o, 0)) for o in occ)
    A = tuple(tuple(index[(o[0], o[1], m)] for m in _switches(o[2])) for o in occ)
    B = tuple(tuple(index[n] for n in endpoint_neighbors(o, sites)) for o in occ)
    image = tuple(sum(vector[j] for j in r) for r in A)
    flat = tuple(a - lam * b for a, b in zip(image, vector, strict=True))
    fibre_constant = all(
        len({flat[index[(p, s, m)]]
             for m in perfect_matchings(tuple(v for v in sites
                                              if v not in (p, s)))}) == 1
        for p in sites[:2] for s in sites if s != p
    )
    current = flat
    for theta in (-2, 2 * h - 2, 2 * h):
        img = tuple(sum(current[j] for j in r) for r in B)
        current = tuple(a - theta * b for a, b in zip(img, current, strict=True))
    constant = len(set(current)) == 1
    denominator = 8 * h * (h + 1) * (2 * h + 1)
    return {
        "matching_projector_flattens_all_fibres": _all_fibres_flat(flat, index,
                                                                   sites),
        "sampled_fibre_constant": fibre_constant,
        "composite_projector_gives_constant": constant,
        "constant_value": str(current[0]) if constant else None,
        "distinct_values_after_composite": len(set(current)),
        "endpoint_denominator": denominator,
    }


def _switches(matching):
    from lib_stress import switch_neighbors
    return switch_neighbors(matching)


def _all_fibres_flat(flat, index, sites):
    for p in sites:
        for s in sites:
            if p == s:
                continue
            rest = tuple(v for v in sites if v not in (p, s))
            values = {flat[index[(p, s, m)]] for m in perfect_matchings(rest)}
            if len(values) != 1:
                return False
    return True


def run(h, do_two_step=True, types_only=False):
    print(f"=== h={h} ===")
    result = {"h": h}

    big_sites = tuple(range(2 * h + 2))
    marked = marked_occurrence(h)
    row, columns = one_step_row(h, marked, big_sites)
    assert columns == 7 * h
    assert row[marked] == 4 * h * h + 5 * h
    assert sum(row.values()) == 7 * h * occurrence_count(h)
    print(f"  one-step row: columns={columns}=7h, k_f(f)={row[marked]}=4h^2+5h,"
          f" sum={sum(row.values())}=7h*N_h")
    result["one_step"] = analyse_row("k_f", row, h + 1, marked, big_sites,
                                     types_only=types_only)
    result["one_step_projector"] = endpoint_projector_check(row, h + 1, marked,
                                                            big_sites)
    print(f"    projector check: {result['one_step_projector']}")

    if do_two_step:
        big2 = tuple(range(2 * h + 4))
        marked2 = marked_occurrence(h + 1)
        row2, columns2 = two_step_row(h, marked2, big2)
        print(f"  two-step row: weighted columns={columns2}, "
              f"k2_f(f)={row2[marked2]}, sum={sum(row2.values())}")
        result["two_step_columns"] = columns2
        result["two_step_diagonal"] = row2[marked2]
        result["two_step_sum"] = sum(row2.values())
        result["two_step"] = analyse_row("k2_f", row2, h + 2, marked2, big2,
                                         types_only=types_only)
    return result


def main():
    hs = [int(x) for x in sys.argv[1:] if not x.startswith("-")] or [3, 4]
    two = "--no-two-step" not in sys.argv
    types_only = "--types-only" in sys.argv
    out = {}
    for h in hs:
        out[h] = run(h, do_two_step=two, types_only=types_only)
    tag = "".join(str(h) for h in hs)
    path = Path(__file__).resolve().parent / f"t2_transfer_residuals_h{tag}.json"
    path.write_text(json.dumps(out, indent=1, sort_keys=True))
    print("wrote", path)


if __name__ == "__main__":
    main()
