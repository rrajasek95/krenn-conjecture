#!/usr/bin/env python3
"""Select the exact smallest residual chart and derive its held p32003 source."""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

H = Path(__file__).resolve().parent
ROOT = H.parents[1]
PROD = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-design-2026-08-26"
REF = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-referee-2026-08-26"
PROD_MANIFEST_SHA = "2b220f91ffa21c28506f5112a3a3e7fe791c7e3c783c1e7a319186628743659e"
REF_MANIFEST_SHA = "20f24c8de6e7edb0818c30c11df4716e983fd5f8bf5778ee36d6d3bccf27d0ff"
SELECTED_Q_SHA = "13c204f73bb82e263267ec977c19a10dba045541921375c2e7568ba48d5baba0"
SELECTED_NAME = "rep5_k2_t1_gauge_yn11_yn21_t01_t20_Q_design.sing"
OUT = H / "rep5_k2_t1_gauge_yn11_yn21_t01_t20_p32003.sing"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_bytes(path: Path, data: bytes) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(data)
    os.replace(temporary, path)


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


class TermCounter:
    """Count fully distributed syntax-tree terms without materializing expansion."""
    def __init__(self, expression: str):
        self.tokens = re.findall(r"[A-Za-z_][A-Za-z_0-9]*|\d+|[()+*\-]", expression)
        self.position = 0

    def expression(self) -> int:
        count = self.term()
        while self.position < len(self.tokens) and self.tokens[self.position] in "+-":
            self.position += 1
            count += self.term()
        return count

    def term(self) -> int:
        count = self.factor()
        while self.position < len(self.tokens) and self.tokens[self.position] == "*":
            self.position += 1
            count *= self.factor()
        return count

    def factor(self) -> int:
        token = self.tokens[self.position]
        if token == "-":
            self.position += 1
            return self.factor()
        if token == "(":
            self.position += 1
            count = self.expression()
            assert self.tokens[self.position] == ")"
            self.position += 1
            return count
        self.position += 1
        return 1


def equations(text: str) -> list[str]:
    body = text.split("ideal I=", 1)[1].split(";\nprint", 1)[0]
    result = []
    depth = 0
    start = 0
    for position, character in enumerate(body):
        depth += character == "("
        depth -= character == ")"
        if character == "," and depth == 0:
            result.append(body[start:position].strip())
            start = position + 1
    result.append(body[start:].strip())
    assert depth == 0
    return result


assert sha(PROD / "MANIFEST.sha256") == PROD_MANIFEST_SHA
assert sha(REF / "MANIFEST.sha256") == REF_MANIFEST_SHA
ledger = []
for path in sorted((PROD / "sources").glob("*.sing")):
    text = path.read_text()
    term_count = 0
    parsed = equations(text)
    assert len(parsed) == 6561
    for equation in parsed:
        counter = TermCounter(equation)
        term_count += counter.expression()
        assert counter.position == len(counter.tokens)
    ledger.append({
        "path": str(path.relative_to(PROD)), "filename": path.name,
        "bytes": path.stat().st_size, "expanded_syntax_term_count": term_count,
        "sha256": sha(path), "variables": 73, "generators": 6561,
    })
assert len(ledger) == 16
ordered = sorted(ledger, key=lambda item: (item["bytes"], item["expanded_syntax_term_count"], item["sha256"]))
selected = ordered[0]
assert selected["filename"] == SELECTED_NAME and selected["sha256"] == SELECTED_Q_SHA
assert selected["bytes"] == 4416511 and selected["expanded_syntax_term_count"] == 5322351
q_path = PROD / selected["path"]
q_bytes = q_path.read_bytes()
assert q_bytes.count(b"ring r=0,(") == 1 and q_bytes.endswith(b"quit;\n")
strong = b'''ideal G=slimgb(I);\nprint("GROEBNER_SIZE="+string(size(G)));\npoly remainder=reduce(1,G);\nprint("UNIT_REMAINDER="+string(remainder));\nif (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\nquit;\n'''
modular = q_bytes.replace(b"ring r=0,(", b"ring r=32003,(", 1)[:-len(b"quit;\n")] + strong
assert modular.replace(b"ring r=32003,(", b"ring r=0,(", 1)[:-len(strong)] + b"quit;\n" == q_bytes
assert modular.count(b"ring r=32003,(") == 1 and b"ideal G=slimgb(I);" in modular
atomic_bytes(OUT, modular)
derivation = {
    "schema": "KRENN_X5_REP5_K2_T1_TORUS_COVER_SMALLEST_MODULAR_SOURCE_V1",
    "status": "PASS_DETERMINISTIC_SMALLEST_SOLE_RING_PLUS_EPILOGUE_ZERO_RUN",
    "selection_rule": ["source_bytes", "expanded_syntax_term_count", "lexicographic_sha256"],
    "term_count_definition": "sum over 6561 generators of fully distributed syntax-tree leaf terms; multiplication multiplies counts, addition sums counts; no expansion materialized",
    "candidate_count": 16, "all_candidates_tied_on_bytes_and_terms": len({(item['bytes'], item['expanded_syntax_term_count']) for item in ledger}) == 1,
    "selection_ledger": ordered, "selected": selected,
    "transformation": {"ring_replacements": 1, "old_field": "Q", "new_field": "F_32003", "strong_epilogue_appended": True, "inverse_byte_replay": True, "other_Q_body_bytes_identical": True},
    "modular": {"path": OUT.name, "sha256": sha(OUT), "bytes": OUT.stat().st_size, "variables": 73, "generators": 6561, "field": "F_32003"},
    "chart": {"assignment": {"yn1": 1, "yn2": 1, "t0": 1, "t2": 0}, "logical_scope": "one of 16 exact residual torus charts", "sufficient_for_all_16": False},
    "pins": {"torus_producer_manifest_sha256": PROD_MANIFEST_SHA, "torus_referee_manifest_sha256": REF_MANIFEST_SHA},
    "scope": {"solver_runs": 0, "attempts": 0, "launch_authorized": False, "exact_Q_authorized": False, "other_chart_authorized": False, "automatic_relaunch_authorized": False},
}
atomic_json(H / "source_derivation.json", derivation)
atomic_json(H / "selection_ledger.json", {"schema": "KRENN_X5_REP5_K2_T1_TORUS_16_SELECTION_LEDGER_V1", "selection_rule": derivation["selection_rule"], "term_count_definition": derivation["term_count_definition"], "candidates": ordered, "selected_sha256": selected["sha256"]})
print(json.dumps({"status": derivation["status"], "selected": selected["filename"], "Q_sha256": selected["sha256"], "p32003_sha256": sha(OUT), "solver_runs": 0}, sort_keys=True))
