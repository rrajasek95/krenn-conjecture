#!/usr/bin/env python3
"""H1 / BLOCKER 4 (extension) -- run the ledger-13 NO-SHADOWING TEST on every
Singular script in the promotion queue.

UNAUDITED.  Hygiene agent H1, 2026-08-15.  Static analysis only; no script
is executed and nothing is modified.

Ledger item 13 (SEVERE): declaring `poly g11 = ...;` inside a ring that has
a variable named `g11` silently REBINDS the identifier -- no warning, no `?`
line, return code 0 -- and in W16 that turned a feasible system into a
reported unit ideal (a FALSE KILL).  The required practice is a reserved
`zzg*` prefix plus a no-shadowing guard.

The portability scan established that 0 of the 13 cited Singular routes run
such a guard.  "No guard" is a process debt; it is not yet a false kill.
This module runs the guard that nobody ran, so the queue's Singular kills
can be reported as either
    SHADOWING PRESENT   (a concrete false-kill risk to re-verify), or
    NO COLLISION FOUND  (the debt is procedural only).

Method: for each `.sing` file, parse the `ring <name> = <char>,(<vars>),<ord>;`
declarations to get the variable names in scope, then parse every
declaration `<type> <ident> = ...` / `<type> <ident>;` for the Singular
declaration types, and report any declared identifier that equals a ring
variable of the ring in force at that point.

Usage:  python3 h1_b4_zzguard.py
Writes  results_b4_zzguard.json
"""

from __future__ import annotations

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

DECL_TYPES = ("poly", "ideal", "matrix", "vector", "module", "int",
              "number", "list", "intvec", "intmat", "string", "map",
              "resolution", "proc", "bigint", "def")

RING_RE = re.compile(r"\bring\s+(\w+)\s*=\s*(.+?);", re.S)
DECL_RE = re.compile(r"^\s*(" + "|".join(DECL_TYPES) + r")\s+(\w+)\s*[=;]",
                     re.M)
SETRING_RE = re.compile(r"\bsetring\s+(\w+)\s*;")


def ring_vars(body):
    """Variable names from the parenthesised list of a ring declaration."""
    m = re.search(r"\((.*)\)", body, re.S)
    if not m:
        return []
    return [v.strip() for v in m.group(1).split(",") if v.strip()]


def scan(path):
    src = open(path, encoding="utf-8", errors="replace").read()
    # strip // comments so commented-out declarations do not count
    src = re.sub(r"//[^\n]*", "", src)
    rings = {}
    for m in RING_RE.finditer(src):
        rings[m.group(1)] = ring_vars(m.group(2))
    # the ring in force: last `ring` declaration or `setring` before the decl
    events = []
    for m in RING_RE.finditer(src):
        events.append((m.start(), m.group(1)))
    for m in SETRING_RE.finditer(src):
        events.append((m.start(), m.group(1)))
    events.sort()

    def ring_at(pos):
        cur = None
        for p, name in events:
            if p <= pos:
                cur = name
            else:
                break
        return cur

    collisions = []
    declared = 0
    zz = 0
    for m in DECL_RE.finditer(src):
        typ, ident = m.group(1), m.group(2)
        declared += 1
        if ident.startswith("zzg"):
            zz += 1
        r = ring_at(m.start())
        if r and ident in rings.get(r, []):
            collisions.append({"identifier": ident, "type": typ,
                               "ring": r,
                               "line": src[:m.start()].count("\n") + 1})
    has_lib_elim = bool(re.search(r'LIB\s*"elim\.lib"', src))
    sat_trap = len(re.findall(r"sat\s*\([^)]*\)\s*\[\s*1\s*\]", src))
    sat_calls = len(re.findall(r"\bsat\s*\(", src))
    list_form = len(re.findall(r"list\s+\w+\s*=\s*sat\s*\(", src))
    return {"declarations": declared, "zzg_prefixed": zz,
            "rings": {k: len(v) for k, v in rings.items()},
            "collisions": collisions,
            "shadowing_present": bool(collisions),
            "LIB_elim_lib": has_lib_elim,
            "sat_calls": sat_calls,
            "sat_bracket1_trap": sat_trap,
            "sat_list_form": list_form}


def main():
    sings = []
    for dirpath, dirnames, filenames in os.walk(
            os.path.join(ROOT, "computations")):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for f in filenames:
            if f.endswith(".sing"):
                sings.append(os.path.join(dirpath, f))
    sings.sort()
    out = {"agent": "H1", "blocker": "4-zzguard",
           "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")
                               ).read().split()[0],
           "files_scanned": len(sings), "files": {}}
    n_shadow = n_trap = n_nolib = 0
    print(f"scanning {len(sings)} .sing files under computations/\n")
    print(f"{'file':72s} {'decls':>5s} {'zzg':>4s} {'SHADOW':>7s} "
          f"{'elim':>5s} {'sat':>4s} {'[1]':>4s} {'list':>4s}")
    for p in sings:
        r = scan(p)
        rel = os.path.relpath(p, ROOT)
        out["files"][rel] = r
        n_shadow += r["shadowing_present"]
        n_trap += r["sat_bracket1_trap"] > 0
        if r["sat_calls"] and not r["LIB_elim_lib"]:
            n_nolib += 1
        print(f"{rel[-72:]:72s} {r['declarations']:5d} {r['zzg_prefixed']:4d} "
              f"{str(r['shadowing_present']):>7s} "
              f"{str(r['LIB_elim_lib']):>5s} {r['sat_calls']:4d} "
              f"{r['sat_bracket1_trap']:4d} {r['sat_list_form']:4d}")
        for c in r["collisions"]:
            print(f"    !! SHADOWING: {c['type']} {c['identifier']} "
                  f"shadows a variable of ring {c['ring']} at line {c['line']}")
    out["summary"] = {"files_with_shadowing": n_shadow,
                      "files_with_sat_bracket1_trap": n_trap,
                      "files_calling_sat_without_elim_lib": n_nolib,
                      "files_using_zzg_prefix": sum(
                          1 for r in out["files"].values()
                          if r["zzg_prefixed"])}
    print(f"\nSUMMARY: {out['summary']}")
    with open(os.path.join(HERE, "results_b4_zzguard.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote results_b4_zzguard.json")


if __name__ == "__main__":
    main()
