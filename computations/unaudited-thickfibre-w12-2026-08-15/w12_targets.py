#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- target loaders + the (SC+) activity filter."""

from __future__ import annotations

import glob
import json
import os

import w12_core as C

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
W8 = os.path.join(ROOT, "computations", "unaudited-template-kill-w8-2026-08-15")
W11 = os.path.join(ROOT, "computations", "unaudited-sat-pair-w11-2026-08-15")


def load_w11_witnesses():
    """[(name, template)] for W11's 44 verified admissible witnesses."""
    geo = C.geometry()
    out = []
    for path in sorted(glob.glob(os.path.join(W11, "witnesses", "*.json"))):
        if os.path.basename(path) == "summary.json":
            continue
        with open(path) as fh:
            data = json.load(fh)
        edges = [tuple(e) for e in data["edges"]]
        template = [0] * len(geo.edges)
        for e, cells in zip(edges, data["blocks"]):
            idx = geo.eindex[tuple(sorted(e))]
            mask = 0
            for (i, j) in cells:
                mask |= C.bit(i, j)
            template[idx] = mask
        out.append((os.path.basename(path)[:-5], tuple(template)))
    return out


def load_w8_m17_classes():
    with open(os.path.join(W8, "results_enumerate_m17.json")) as fh:
        data = json.load(fh)
    return [(f"m17_class{n}", tuple(e["template"]), e["verdict"])
            for n, e in enumerate(data["classes"])]


# ------------------------------------------------------------- (SC+)


def has_perfect_matching(geo, template, avoid):
    """Does the template's support graph restricted to B\\avoid have a PM?"""
    rest = [v for v in range(geo.size) if v not in avoid]
    if len(rest) % 2:
        return False
    for pm in C.perfect_matchings(tuple(rest)):
        if all(template[geo.eindex[e]] for e in pm):
            return True
    return False


def sc_plus(geo, template):
    """(SC+) [W11]: every (vertex,colour) demand needs a SERVING edge pj whose
    cofactor C_pj is not identically zero, i.e. B\\{p,j} must still carry a
    template perfect matching.  Returns (ok, failing demands)."""
    dem = C.fie_demands(geo, template)
    bad = []
    for (p, r), servers in dem.items():
        live = []
        for e in servers:
            u, v = geo.edges[e]
            j = v if u == p else u
            if has_perfect_matching(geo, template, {p, j}):
                live.append(e)
        if not live:
            bad.append([p, r])
    return (not bad), bad
