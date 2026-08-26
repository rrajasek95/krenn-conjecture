#!/usr/bin/env python3
"""UNAUDITED: before/after demonstration for the LEDGER-DISCIPLINE note.

Runs entirely in memory; writes nothing.  It reads
``computations/verify_h3_sl2_weyl_cartan_prism.py``, produces five textual
variants, executes each in a fresh namespace, and compares the frozen-ledger
digests.  Nothing in the repository is modified.

Variants (each with its self-pin disabled so the digest is reported rather
than compared):

  V0  as committed
  V1  V0 with `require` turned into a no-op -- i.e. every mathematical check
      in the file removed
  V2  V1 with the signed Weyl action mutated ((-1)**a -> (-1)**b), so the
      checker is now checking a FALSE statement with no checks left
  V3  V0 with a content-hashing ledger: a rolling sha256 of the actually
      computed Weyl images, their expected values and the Cartan homotopy
      images is added to the ledger
  V4  V3 with `require` neutered AND the same Weyl mutation

Claimed and verified here:

    digest(V1) == digest(V0)        the ledger contains no mathematical content
    digest(V2) == digest(V0)        wrong mathematics + no checks = same digest
    digest(V4) != digest(V3)        a content-hashing ledger catches it

That is the whole argument of the note, executable.
"""

from __future__ import annotations

import contextlib
from hashlib import sha256
import io
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TARGET = "computations/verify_h3_sl2_weyl_cartan_prism.py"
COMMITTED_PIN = (
    "bde6a55fb7061024ff741b38acd22f02d2299d7e77f704eebeb9298b7b5abbb2"
)
SOURCE_SHA256 = (
    "1024864418fea8f7f4ca6c77015972febd236f2a9822112daf20e1cf979bddaa"
)
EXPECTED_LEDGER_SHA256 = (
    "5fc65b4416593efbb07e3b125e9efc7b068141252f4b796a4e9bcca08d4d65e0"
)

NEUTER_REQUIRE = (
    "def require(condition, message):\n"
    "    if not condition:\n"
    "        raise RuntimeError(message)\n",
    "def require(condition, message):\n"
    "    return None\n",
)
MUTATE_WEYL = (
    "    coefficient = (-1) ** a\n",
    "    coefficient = (-1) ** b\n",
)
DISABLE_PIN = (
    'EXPECTED_LEDGER_SHA256 = (\n    "'
    "bde6a55fb7061024ff741b38acd22f02d2299d7e77f704eebeb9298b7b5abbb2"
    '"\n)\n',
    'EXPECTED_LEDGER_SHA256 = "TO_BE_PINNED"\n',
)
CONTENT_COUNTER = (
    "    states = 0\n",
    "    states = 0\n    content = sha256()\n",
)
CONTENT_UPDATE = (
    "                    require(weyl(vector) == signed_weyl_on_basis(basis),\n"
    '                            ("root factorization is not signed Weyl", basis))\n',
    "                    content.update(repr(sorted(\n"
    "                        weyl(vector).items())).encode())\n"
    "                    content.update(repr(sorted(\n"
    "                        signed_weyl_on_basis(basis).items())).encode())\n"
    "                    content.update(repr(sorted(\n"
    "                        weyl_homotopy(vector).items())).encode())\n"
    "                    require(weyl(vector) == signed_weyl_on_basis(basis),\n"
    '                            ("root factorization is not signed Weyl", basis))\n',
)
CONTENT_LEDGER = (
    '        "basis_states": states,\n',
    '        "basis_states": states,\n'
    '        "content_sha256": content.hexdigest(),\n',
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def substitute(text, pairs):
    for old, new in pairs:
        require(old in text, ("variant edit did not apply", old[:60]))
        text = text.replace(old, new, 1)
    return text


def run_variant(text, label):
    namespace = {"__name__": "sl2_variant_" + label, "__file__":
                 str(ROOT / TARGET)}
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        exec(compile(text, str(ROOT / TARGET), "exec"), namespace)
        namespace["audit"]()
    lines = [line for line in buffer.getvalue().splitlines()
             if line.startswith("ledger_sha256=")]
    require(len(lines) == 1, ("variant did not report a digest", label))
    return lines[0].split("=", 1)[1]


def main():
    source = (ROOT / TARGET).read_bytes()
    require(sha256(source).hexdigest() == SOURCE_SHA256,
            "the sl2 prism checker changed; re-pin this demonstration")
    text = source.decode()

    variants = {
        "V0_as_committed": [DISABLE_PIN],
        "V1_no_checks": [DISABLE_PIN, NEUTER_REQUIRE],
        "V2_no_checks_wrong_weyl": [DISABLE_PIN, NEUTER_REQUIRE, MUTATE_WEYL],
        "V3_content_hashed": [DISABLE_PIN, CONTENT_COUNTER, CONTENT_UPDATE,
                              CONTENT_LEDGER],
        "V4_content_hashed_no_checks_wrong_weyl":
            [DISABLE_PIN, CONTENT_COUNTER, CONTENT_UPDATE, CONTENT_LEDGER,
             NEUTER_REQUIRE, MUTATE_WEYL],
    }
    digests = {label: run_variant(substitute(text, pairs), label)
               for label, pairs in variants.items()}

    require(digests["V0_as_committed"] == COMMITTED_PIN,
            ("V0 no longer reproduces the committed pin",
             digests["V0_as_committed"]))
    require(digests["V1_no_checks"] == digests["V0_as_committed"],
            "deleting every mathematical require changed the digest")
    require(digests["V2_no_checks_wrong_weyl"] == digests["V0_as_committed"],
            "the wrong-mathematics-no-checks variant changed the digest")
    require(digests["V4_content_hashed_no_checks_wrong_weyl"]
            != digests["V3_content_hashed"],
            "the content-hashing ledger failed to notice wrong mathematics")

    ledger = {
        "demonstration": "frozen ledgers must hash mathematical content",
        "target": TARGET,
        "target_sha256": SOURCE_SHA256,
        "committed_pin": COMMITTED_PIN,
        "variant_digests": dict(sorted(digests.items())),
        "content_free_ledger_survives_deletion_of_every_require": True,
        "content_free_ledger_survives_wrong_weyl_action": True,
        "content_hashing_ledger_detects_wrong_weyl_action": True,
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger-discipline demonstration changed", digest))
    print("repair678 ledger-discipline demonstration: PASS")
    for label, value in sorted(digests.items()):
        print(f"  {label:42s} {value}")
    print("V1 == V0:", digests["V1_no_checks"] == digests["V0_as_committed"])
    print("V2 == V0:",
          digests["V2_no_checks_wrong_weyl"] == digests["V0_as_committed"])
    print("V4 != V3:", digests["V4_content_hashed_no_checks_wrong_weyl"]
          != digests["V3_content_hashed"])
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
