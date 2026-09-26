#!/usr/bin/env python3
"""Offline exact replay. Analytic all-order proofs remain human-readable inputs."""

from __future__ import annotations

import argparse
from contextlib import redirect_stdout
from copy import deepcopy
import hashlib
import io
from itertools import combinations, product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
IDS = {"CF", "BM", "HP", "EV", "GD", "RV", "BC", "NB", "SD", "TR", "CR", "H10"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def check_hash(data, expected, name):
    require(digest(data) == expected, "SHA-256 mismatch: " + name)


def check_manifest():
    manifest = read_json(ROOT / "manifest.json")
    require(manifest["format"] == 1, "Unknown manifest format")
    files = manifest["files"]
    required = {"nodes.json", "provenance.json", "THEOREMS.md", "README.md",
                "verify.py", "build_matching_certificate.py", "matching8.json",
                "checks/foundation.py", "checks/triangle.py", "checks/boundary.py",
                "audits/FOUNDATION.md"}
    required |= {f"{directory}/{name}.md" for name in IDS for directory in ("sources", "audits")}
    require(required <= files.keys(), "Incomplete manifest")
    for name, expected in files.items():
        path = ROOT / name
        require(not Path(name).is_absolute() and ".." not in Path(name).parts,
                "Unsafe manifest path")
        require(path.is_file() and not path.is_symlink(), "Missing or linked artifact: " + name)
        check_hash(path.read_bytes(), expected, name)
    nodes = read_json(ROOT / "nodes.json")
    require(len(nodes) == len(IDS) and {n["id"] for n in nodes} == IDS, "Wrong node inventory")
    indexed = {n["id"]: n for n in nodes}
    audit_text = "\n".join((ROOT / "audits" / f"{name}.md").read_text() for name in IDS)
    audit_text += (ROOT / "audits/FOUNDATION.md").read_text()
    done, active = set(), set()

    def visit(name):
        require(name in indexed, "Missing dependency: " + name)
        require(name not in active, "Circular proof dependencies")
        if name in done:
            return
        active.add(name)
        node = indexed[name]
        require(bool(node["scope"]), "Missing theorem scope")
        for kind in ("source", "audit"):
            require(node[kind] in files, "Unpinned node artifact")
            check_hash((ROOT / node[kind]).read_bytes(), node[kind + "_sha256"], node[kind])
        if "audited_frozen_source" in node:
            frozen = node["audited_frozen_source"]
            require(frozen in files, "Unpinned original freeze")
            check_hash((ROOT / frozen).read_bytes(), node["audited_frozen_sha256"], frozen)
            require(node["audited_frozen_sha256"] in (ROOT / node["audit"]).read_text(),
                    "Audit does not identify original freeze")
        else:
            require(node["source_sha256"] in audit_text,
                    "No historical audit pins current text: " + name)
        for dep in node["depends_on"]:
            visit(dep)
        active.remove(name)
        done.add(name)

    for name in sorted(IDS):
        visit(name)
    for item in read_json(ROOT / "provenance.json"):
        require(item["path"] in files, "Unpinned provenance artifact")
        check_hash((ROOT / item["path"]).read_bytes(), item["sha256"], item["path"])
    return {"manifest_sha256": digest((ROOT / "manifest.json").read_bytes()),
            "pinned_files": len(files), "acyclic_scoped_nodes": len(done)}


def matchings(vertices):
    """Exhaustive recurrence: the least vertex has exactly one partner."""
    if not vertices:
        yield ()
        return
    p = vertices[0]
    for j, q in enumerate(vertices[1:], 1):
        for rest in matchings(vertices[1:j] + vertices[j + 1:]):
            yield ((p, q),) + rest


def normalize_matching(raw, n):
    require(isinstance(raw, list) and len(raw) == n // 2, "Wrong matching length")
    require(all(isinstance(e, list) and len(e) == 2 and
                all(type(v) is int and 0 <= v < n for v in e) and e[0] < e[1]
                for e in raw), "Invalid edge")
    result = tuple(sorted(tuple(e) for e in raw))
    require(sorted(v for e in result for v in e) == list(range(n)), "Not a perfect matching")
    return result


def matching_cover(certificate):
    require(certificate["n"] == 8, "Wrong terminal order")
    all_pm = tuple(matchings(tuple(range(8))))
    require(len(all_pm) == len(set(all_pm)) == 105, "Incomplete perfect-matching enumeration")
    red = tuple((p, p + 1) for p in range(0, 8, 2))
    require(normalize_matching(certificate["red"], 8) == red, "Wrong fixed red matching")
    pm_sets = {p: frozenset(p) for p in all_pm}
    blue_candidates = [p for p in all_pm if not pm_sets[p] & pm_sets[red]]
    expected = {(b, g) for b in blue_candidates for g in blue_candidates
                if not pm_sets[b] & pm_sets[g]}
    seen = set()
    for case in certificate["cases"]:
        b, g, witness = (normalize_matching(case[k], 8) for k in ("blue", "green", "witness"))
        key = (b, g)
        require(key in expected and key not in seen, "Invalid or repeated color pair")
        seen.add(key)
        colored = (red, b, g)
        edge_color = {e: h for h, p in enumerate(colored) for e in p}
        require(witness not in colored and set(witness) <= edge_color.keys(), "Invalid extra matching")
        word = [-1] * 8
        for u, v in witness:
            word[u] = word[v] = edge_color[u, v]
        require(len(set(word)) > 1, "Witness word is pure")
        # Independently inspect EVERY matching, not just the supplied witness.
        compatible = [p for p in all_pm if all(e in edge_color and
                      word[e[0]] == word[e[1]] == edge_color[e] for e in p)]
        require(compatible == [witness], "The mixed coefficient is not a unique nonzero monomial")
    require(seen == expected, "Matching certificate misses normalized color pairs")
    require(bool(seen), "Empty coverage")
    # The analogous claim is FALSE at the allowed four-site boundary.
    small = tuple(matchings(tuple(range(4))))
    require(len(small) == 3 and len(set().union(*(set(p) for p in small))) == 6,
            "Four-site exception broken")
    return {"perfect_matchings": len(all_pm), "normalized_ordered_color_pairs": len(seen),
            "unique_mixed_witnesses": len(seen), "four_site_exception_preserved": True}


def load_checker(name, replacement=None):
    path = ROOT / "checks" / name
    source = path.read_text()
    if replacement is not None:
        before, after = replacement
        require(source.count(before) == 1, "Ambiguous mutation")
        source = source.replace(before, after)
    namespace = {"__name__": "frozen_replay", "__file__": str(path)}
    # Historical, byte-preserved scripts contain asserts. Explicit optimize=0
    # retains them EVEN when this wrapper is launched with python -O or -OO.
    exec(compile(source, str(path), "exec", optimize=0), namespace)
    return namespace


def historical_replays():
    foundation = load_checker("foundation.py")
    f = {key: foundation[function]() for key, function in (
        ("reflection", "reflection_checks"), ("covariance", "covariance_checks"),
        ("matrix_expansion", "matrix_checks"), ("boundary_controls", "boundary_controls"))}
    require(f["reflection"]["tested_contractions"] == 58, "Reflection coverage drift")
    require(f["covariance"]["homogeneous_checks"] == 54, "Covariance coverage drift")
    rotations = f["covariance"]["rational_rotations"]
    require(len(rotations) == 6 and all(r["pairing"] != "0" for r in rotations),
            "Vacuous rotation check")
    require(f["matrix_expansion"]["off_diagonal_checks"] == 882 and
            f["matrix_expansion"]["diagonal_checks"] == 162, "Matrix coverage drift")
    triangle = load_checker("triangle.py")
    counts = {str(n): triangle["check_two_cubic"](n) + triangle["check_two_cubic"](n, True)
              + triangle["check_three_cubic"](n) for n in (6, 8, 10, 12)}
    require(sum(counts.values()) == 132, "Triangle coverage drift")
    boundary = load_checker("boundary.py")
    output = io.StringIO()
    saved = sys.argv
    try:
        sys.argv = ["boundary.py"]
        with redirect_stdout(output):
            boundary["main"]()
    finally:
        sys.argv = saved
    b = json.loads(output.getvalue())
    require(b["scalar_cofactor_inverse_entries_checked"] == 100 and
            b["crown_plus_edge_scalar_hafnian"] == 15, "Scalar scope control drift")
    return {"foundation": f, "triangle_identity_counts": counts, "component_boundary": b}


def retained_vacuum_checks():
    """Direct coefficient extraction challenges RV's three pairing coefficients."""
    f = load_checker("foundation.py")
    total = nonzero = 0
    for n in (2, 4, 6):
        covariance, rows = f["input_data"](n, 926000 + n)
        rows.append({key: (value * 3 + rows[0][key]) for key, value in rows[2].items()})
        zero = f["MatchingMoments"](covariance, {})
        for selected in (rows, [rows[0]] * 4):
            cache = {}

            def coefficient(indices, word):
                degree = len(indices)
                if degree > n:
                    return 0
                answer = 0
                for bits in product((0, 1), repeat=degree):
                    subset = tuple(indices[j] for j, bit in enumerate(bits) if bit)
                    if subset not in cache:
                        mean = {x: sum(selected[j][x] for j in subset) for x in rows[0]}
                        cache[subset] = f["MatchingMoments"](covariance, mean)
                    answer += (-1) ** (degree - sum(bits)) * cache[subset].moment(word)[0][degree]
                return answer

            for pairs in ([(0, 1)] * n, [(i % 3, (i + 1) % 3) for i in range(n)]):
                lhs = rhs = 0
                for sign, word, complement in f["words_for_pairs"](pairs):
                    lhs += sign * zero.moment(word)[0][0] * coefficient((0, 1, 2, 3), complement)
                    for first, second in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
                        rhs += sign * coefficient(first, word) * coefficient(second, complement)
                require(lhs == rhs, "Retained-vacuum four-row identity failed")
                total += 1
                nonzero += lhs != 0
    require(total == 12 and nonzero > 0, "Vacuous retained-vacuum controls")
    return {"identities": total, "nonzero_pairings": nonzero, "even_orders": [2, 4, 6]}


def expect_failure(function, label):
    try:
        function()
    except (ValueError, AssertionError):
        return label
    raise ValueError("Negative control was incorrectly accepted: " + label)


def negative_controls(certificate):
    missing = deepcopy(certificate)
    missing["cases"].pop()
    wrong = deepcopy(certificate)
    wrong["cases"][0]["witness"] = wrong["red"]
    labels = [expect_failure(lambda: matching_cover(missing), "missing matching case"),
              expect_failure(lambda: matching_cover(wrong), "pure witness substituted"),
              expect_failure(lambda: check_hash(b"altered", digest(b"original"), "control"),
                             "corrupt artifact hash")]
    mutated = load_checker("foundation.py", ("assert before == after", "assert before == after + 1"))
    labels.append(expect_failure(mutated["covariance_checks"],
                                 "incorrect rotation identity, including under -O"))
    return labels


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write a new JSON receipt (refuses overwrite)")
    args = parser.parse_args()
    integrity = check_manifest()
    certificate = read_json(ROOT / "matching8.json")
    cover = matching_cover(certificate)
    replays = historical_replays()
    vacuum = retained_vacuum_checks()
    negative = negative_controls(certificate)
    report = {"status": "PASS", "scope": "Integrity, finite matching lemma, and exact bounded controls; "
              "all-order mathematical certification uses the accompanying proofs and independent audits.",
              "integrity": integrity, "eight_site_terminal_lemma": cover,
              "exact_controls": replays, "retained_vacuum_controls": vacuum,
              "negative_controls_rejected": negative}
    encoded = json.dumps(report, indent=2) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
