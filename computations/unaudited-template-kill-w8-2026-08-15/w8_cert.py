#!/usr/bin/env python3
"""UNAUDITED PROBE (W8) -- extractable, independently checkable kill
certificates, and the nogoods they license.

Pinned HEAD: a1196b4dca9f83452483734a3273c0c43d5cf3b5

A certificate is an ORDERED list of deductions.  Each one is a statement
about the exact fibre of one word (checkable directly from the template) plus
exact integer/rational bookkeeping.  Relations are numbered by their position
in the certificate's own relation list, so the certificate is self-contained.

  K0        a constant fibre is empty                      -> 0 = 1
  O2        fibre(w) = {M}                                 -> x^a = 0
  relation  fibre(w) = {M1, M2}      -> new relation x^{a(M1)-a(M2)} = -1
  derived   fibre(w) = terms, which fall into exactly two live classes
            modulo the relations so far -> new relation x^{d} = gamma
  collapse  fibre(w) = terms, which fall into classes whose totals are zero
            except one                 -> q x^{a} = 0 with q != 0
  holonomy  an integer dependency among the relations carrying a nontrivial
            character                  -> 1 = gamma != 1
  K3        a CONSTANT fibre whose class totals all vanish -> 0 = 1

SOUNDNESS of the class arithmetic: a class whose signed total is 0 contributes
exactly 0 to the equation whatever its monomial value is, and a class whose
members are all provably equal to gamma_i times the representative
contributes (sum gamma_i) x^{a_rep}.  So a "collapse" really does reduce the
mixed equation to q x^{a} = 0 with q != 0 and x^a != 0.

verify() re-checks every deduction from the raw template with a pure-Python
fibre computation (independent of the numpy engine) and exact arithmetic.
"""

from __future__ import annotations

from fractions import Fraction

import w8_core as C


def raw_fibre(geo, template, word):
    """Pure Python: the matchings compatible with a word (no numpy)."""
    out = []
    for n, matching in enumerate(geo.matchings):
        ok = True
        for u, v in matching:
            e = geo.index[(u, v)]
            if not (template[e] >> (3 * word[u] + word[v])) & 1:
                ok = False
                break
        if ok:
            out.append(n)
    return out


def class_data(character, vectors):
    """Partition terms into character classes.

    combos are SPARSE dicts {original relation index: coefficient}.
    """
    classes = []
    for index, vector in enumerate(vectors):
        placed = False
        for entry in classes:
            diff = [a - b for a, b in zip(vector, vectors[entry["rep"]])]
            gamma = character.value(diff)
            if gamma is not None:
                lam = character.solve(diff) or []
                entry["combos"][index] = {k: int(x) for k, x
                                          in enumerate(lam) if x}
                entry["total"] += gamma
                placed = True
                break
        if not placed:
            classes.append({"rep": index, "combos": {index: {}},
                            "total": Fraction(1)})
    return classes


def used_relations(classes):
    return sorted({k for cl in classes for combo in cl["combos"].values()
                   for k in combo})


def certify(geo, template, coords=None, max_rounds=8, compat=None):
    """Run the closure engine while recording an extractable certificate."""
    if compat is None:
        compat = C.compat_matrix(geo, template)
    table = C.fibre_table(geo, template, compat)
    for row in geo.constant_rows:
        if not table.get(row):
            return {"verdict": "K0-missing-constant",
                    "deductions": [{"type": "K0", "word": list(geo.words[row]),
                                    "wid": int(row)}]}
    mixed = {w: v for w, v in table.items() if bool(geo.mixed[w])}
    for w, members in sorted(mixed.items()):
        if len(members) == 1:
            return {"verdict": "O2-literal-singleton",
                    "deductions": [{"type": "O2", "word": list(geo.words[w]),
                                    "wid": int(w), "terms": list(members)}]}
    if coords is None:
        coords = C.CellCoords(geo, template)
    cache = {}

    def expo(w, mnum):
        key = (w, mnum)
        if key not in cache:
            cache[key] = coords.exponent(mnum, geo.words[w])
        return cache[key]

    character = C.Character(coords.width)
    provenance = []

    def closure(seed):
        """Dependency closure: a derived relation drags in the relations that
        justify its class decomposition."""
        need = set(seed)
        frontier = list(seed)
        while frontier:
            index = frontier.pop()
            item = provenance[index]
            if item["type"] != "derived":
                continue
            for cl in item["classes"]:
                for combo in cl["combos"].values():
                    for k in combo:
                        if k not in need:
                            need.add(k)
                            frontier.append(k)
        return sorted(need)

    def densify(classes, position):
        """Sparse combos -> dense vectors over the final relation ordering."""
        out = []
        for entry in classes:
            combos = {}
            for index, combo in entry["combos"].items():
                dense = [0] * len(position)
                for k, coefficient in combo.items():
                    dense[position[k]] = coefficient
                combos[str(index)] = dense
            out.append({"rep": entry["rep"], "combos": combos,
                        "total": str(entry["total"])})
        return out

    def emit(kind, seed, extra, final_classes=None, coefficients=None):
        used = closure(seed)
        position = {index: p for p, index in enumerate(used)}
        deductions = []
        for index in used:
            item = dict(provenance[index])
            if item["type"] == "derived":
                item["classes"] = densify(item["classes"], position)
                item.pop("used", None)
            deductions.append(item)
        final = dict(extra)
        final["type"] = kind
        if final_classes is not None:
            final["classes"] = densify(final_classes, position)
        if coefficients is not None:
            dense = [0] * len(used)
            for index, value in coefficients.items():
                dense[position[index]] = value
            final["coefficients"] = dense
        deductions.append(final)
        return deductions

    for w, members in sorted(mixed.items()):
        if len(members) == 2:
            first, second = members
            diff = [a - b for a, b in zip(expo(w, first), expo(w, second))]
            character.add(diff, Fraction(-1))
            provenance.append({"type": "relation", "word": list(geo.words[w]),
                               "wid": int(w), "terms": [first, second]})
    relation = character.odd_relation()
    if relation is not None:
        used = [i for i, x in enumerate(relation) if x]
        return {"verdict": "O1-odd-holonomy",
                "deductions": emit("holonomy", used, {},
                                   coefficients={i: relation[i]
                                                 for i in used})}

    for _ in range(max_rounds):
        changed = False
        for w, members in sorted(mixed.items()):
            if len(members) == 2:
                continue
            vectors = [expo(w, m) for m in members]
            classes = class_data(character, vectors)
            live = [cl for cl in classes if cl["total"] != 0]
            if len(live) == 1:
                return {"verdict": "O2-one-live-class",
                        "deductions": emit(
                            "collapse", used_relations(classes),
                            {"word": list(geo.words[w]), "wid": int(w),
                             "terms": list(members)}, classes)}
            if len(live) == 2:
                i, j = live[0]["rep"], live[1]["rep"]
                diff = [a - b for a, b in zip(vectors[i], vectors[j])]
                gamma = Fraction(-1) * live[1]["total"] / live[0]["total"]
                character.add(diff, gamma)
                provenance.append({"type": "derived",
                                   "word": list(geo.words[w]), "wid": int(w),
                                   "terms": list(members),
                                   "reps": [i, j], "gamma": str(gamma),
                                   "classes": classes})
                relation = character.odd_relation()
                if relation is not None:
                    picked = [k for k, x in enumerate(relation) if x]
                    return {"verdict": "O1-odd-holonomy",
                            "deductions": emit(
                                "holonomy", picked, {},
                                coefficients={k: relation[k]
                                              for k in picked})}
                changed = True
        if not changed:
            break

    for row in geo.constant_rows:
        members = table[row]
        vectors = [expo(row, m) for m in members]
        classes = class_data(character, vectors)
        if all(cl["total"] == 0 for cl in classes):
            return {"verdict": "K3-pure-vanishing",
                    "deductions": emit("K3", used_relations(classes),
                                       {"word": list(geo.words[row]),
                                        "wid": int(row),
                                        "terms": list(members)}, classes)}

    return {"verdict": "survivor", "deductions": [],
            "relations": len(character.rows)}


def verify(geo, template, certificate):
    """Independent exact re-check.  Returns (ok, notes)."""
    notes = []
    deductions = certificate["deductions"]
    if not deductions:
        return certificate["verdict"] == "survivor", ["no deductions"]
    coords = C.CellCoords(geo, template)
    relations, gammas = [], []
    ok = True

    def fibre_of(item):
        return raw_fibre(geo, template, tuple(item["word"]))

    def check_fibre(item):
        got = fibre_of(item)
        if sorted(got) != sorted(item["terms"]):
            notes.append(f"fibre mismatch on {item['word']}")
            return False
        return True

    def class_totals(item, vectors):
        """Recompute each class's total from the relations built so far."""
        covered, totals = [], []
        good = True
        for entry in item["classes"]:
            base = entry["rep"]
            total = Fraction(0)
            for key, combo in entry["combos"].items():
                index = int(key)
                covered.append(index)
                diff = [a - b for a, b in zip(vectors[index], vectors[base])]
                rebuilt = [0] * coords.width
                gamma = Fraction(1)
                for k, coefficient in enumerate(combo):
                    if coefficient:
                        for c in range(coords.width):
                            rebuilt[c] += coefficient * relations[k][c]
                        gamma *= gammas[k] ** coefficient
                if rebuilt != diff:
                    good = False
                    notes.append(f"combo does not reproduce term {index}")
                total += gamma
            if str(total) != entry["total"]:
                good = False
                notes.append(f"class total mismatch {total} vs "
                             f"{entry['total']}")
            totals.append(total)
        if sorted(covered) != list(range(len(item["terms"]))):
            good = False
            notes.append("classes do not partition the fibre")
        return good, totals

    for item in deductions:
        kind = item["type"]
        if kind == "K0":
            got = fibre_of(item)
            ok &= (got == [])
            notes.append(f"K0: constant {item['word']} has fibre {got}")
        elif kind == "O2":
            got = fibre_of(item)
            ok &= (got == item["terms"])
            notes.append(f"O2: mixed fibre {got} is a singleton")
        elif kind == "relation":
            ok &= check_fibre(item)
            first, second = item["terms"]
            a = coords.exponent(first, tuple(item["word"]))
            b = coords.exponent(second, tuple(item["word"]))
            relations.append([x - y for x, y in zip(a, b)])
            gammas.append(Fraction(-1))
        elif kind == "derived":
            ok &= check_fibre(item)
            vectors = [coords.exponent(m, tuple(item["word"]))
                       for m in item["terms"]]
            good, totals = class_totals(item, vectors)
            live = [t for t in totals if t != 0]
            if len(live) != 2:
                good = False
                notes.append(f"derived: {len(live)} live classes, need 2")
            i, j = item["reps"]
            expected = Fraction(-1) * live[1] / live[0] if len(live) == 2 \
                else None
            if expected is None or str(expected) != item["gamma"]:
                good = False
                notes.append("derived: gamma mismatch")
            relations.append([x - y for x, y in zip(vectors[i], vectors[j])])
            gammas.append(Fraction(item["gamma"]))
            ok &= good
        elif kind == "holonomy":
            total = [0] * coords.width
            product = Fraction(1)
            for k, coefficient in enumerate(item["coefficients"]):
                for c in range(coords.width):
                    total[c] += coefficient * relations[k][c]
                product *= gammas[k] ** coefficient
            good = (not any(total)) and product != 1
            ok &= good
            notes.append(f"holonomy: dependency={not any(total)}, "
                         f"character={product} (need != 1)")
        elif kind in ("collapse", "K3"):
            ok &= check_fibre(item)
            vectors = [coords.exponent(m, tuple(item["word"]))
                       for m in item["terms"]]
            good, totals = class_totals(item, vectors)
            live = [t for t in totals if t != 0]
            if kind == "collapse":
                good &= len(live) == 1
                notes.append(f"collapse: {len(item['terms'])} terms, class "
                             f"totals {totals} -> {len(live)} live (need 1)")
            else:
                good &= len(live) == 0
                notes.append(f"K3: class totals {totals} (need all zero)")
            ok &= good
        else:
            ok = False
            notes.append(f"unknown deduction {kind}")
    return bool(ok), notes


def certificate_words(certificate):
    """[(word id, exact fibre)] the certificate depends on."""
    out = []
    for item in certificate["deductions"]:
        if item["type"] in ("O2", "relation", "derived", "collapse", "K3"):
            out.append((item["wid"], tuple(sorted(item["terms"]))))
        elif item["type"] == "K0":
            out.append((item["wid"], ()))
    return out
