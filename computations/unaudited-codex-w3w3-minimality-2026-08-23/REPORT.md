# W3 x W3 nine-source minimality result

This directory tests whether the public ten-source PyTheus construction of
the ancilla-free state `W3 x W3` can be reduced to at most nine nonzero
coloured source coordinates.

## Outcome

Ten coloured source coordinates are necessary and sufficient.

The exact occurrence screen requires only that all nine target words have a
perfect-matching occurrence.  Even without imposing any condition on the 55
forbidden words, the `<=9` instance is UNSAT.  This excludes all choices of
amplitudes and phases before cancellation is considered.  The public
ten-source graph has exactly one occurrence for each target word and none for
any forbidden word, so unit weights prove sharpness.

The mathematical statement and proof reduction are in `THEOREM.md`.

## Frozen artifacts

| artifact | size/count | SHA-256 |
|---|---:|---|
| `w3w3_target_cover9.cnf` | 654 variables; 1,509 clauses | `1fb5b7f9cc601b712fa570e033f9edeb90f815415471f5267cf680c7cff322b5` |
| `w3w3_target_cover9.drup` | 7,614 additions | `a44e69e40132f6c59789761a5279b5af3ed24ef6236bf349c69aae806b73b73b` |

Glucose 4.2 generated the deletion-free DRUP trace.  The combined verifier
rebuilds and byte-compares the CNF, audits the occurrence inventory, checks
the public and independently found ten-source witnesses, solves the 9/10
target-cover boundary with CaDiCaL 1.9.5, and replays every proof addition with
CaDiCaL 1.9.5.

## Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  computations/unaudited-codex-w3w3-minimality-2026-08-23/verify_w3w3_minimality.py
```

Expected final lines:

```text
PASS deletion-free DRUP: variables=654 cnf_clauses=1509 proof_additions=7614
PASS W3 x W3: no <=9-source target cover; exact 10-source support exists
```

## Upstream instance

The target and ten-coordinate witness were read from PyTheus commit
`845af31f7eb158afe544fe8a982a309f746a66e8`:

- `pytheus/graphs/HighlyEntangledStates/W3W3/config_W3W3.json`
- `pytheus/graphs/HighlyEntangledStates/W3W3/plot_W3W3_clean-10-9-0.1000_0.0000.json`

The resource being minimized is the number of nonzero coloured graph-edge
coordinates, which is PyTheus's edge-list count for this instance.  Identical
parallel coordinates can be combined into one effective complex weight, so
allowing duplicates cannot evade the lower bound.

Pinned upstream files:

- https://github.com/artificial-scientist-lab/PyTheus/blob/845af31f7eb158afe544fe8a982a309f746a66e8/pytheus/graphs/HighlyEntangledStates/W3W3/config_W3W3.json
- https://github.com/artificial-scientist-lab/PyTheus/blob/845af31f7eb158afe544fe8a982a309f746a66e8/pytheus/graphs/HighlyEntangledStates/W3W3/plot_W3W3_clean-10-9-0.1000_0.0000.json

## Novelty status

A targeted search of the PyTheus paper, repository, follow-up citations, and
exact-phrase web results found the ten-coordinate construction but no lower
bound or claim of optimality for this instance.  The certificate therefore
closes the public 9-versus-10 resource gap found in those sources.  A formal
publication claim should still include confirmation from the PyTheus authors
and a conventional scholarly literature search.
