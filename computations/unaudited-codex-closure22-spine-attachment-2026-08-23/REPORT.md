# Terminal closure22 separator versus the X5/triangle proof spine

Status: **UNAUDITED exact attachment theorem and negative holonomy guard.**
The terminal characteristic-zero separator proves that `closure22` needs a
new word type, but it is immediately killed by mandatory literal `X5`.  It
does not select the rank-at-most-two holonomy boundary, and it closes none of
the 560 blocked-triangle branches.

## 1. Terminal closure22 theorem

The authoritative upstream object is now the completed joint-semigroup CEGAR
result
[`results_closure22_joint_cegar.json`](../unaudited-codex-rootless-fine-macaulay-2026-08-22/results_closure22_joint_cegar.json),
not the preliminary 16-column first-layer dual.  Starting from the 124,368
independent target-touching rows, 24 exact exchange rounds add 533 independent
translations of the existing 22 words.  Exhaustive convolution at the
terminal stage gives

```text
terminal integer-dual support                         100
max absolute coefficient                               4
abstract degree-nine translations of the 22 words
  having nonzero integer pairing                       0
target pairing                                         1.
```

Thus `closure22` alone is genuinely insufficient in the full joint
28-edge/9-ordered-colour semigroup at degree 13.  Some new mixed word type is
mathematically necessary.

## 2. Exact X5 attachment

Let `pi` denote the joint-semigroup map and `lambda_22` the terminal
100-column integer functional.  For the original canonical rootless word

```text
w = 01211222
```

take the literal degree-nine source multiplier

```text
m = A_07[00] A_17[00] A_27[00] A_36[00]^3
    A_45[10] A_45[11]^2.
```

The independent source replay verifies

```text
lambda_22(pi(m F_01211222)) = -3.                    (1)
```

There are five terminal-separator crossings for this word, with pairings
`{-3,-1,1,1,1}`.  The word is not in `closure22`, but it is a mandatory
literal mixed-amplitude equation in full `X5`.  Consequently

```text
lambda_22 in (I_closure22,13)^perp,
lambda_22 notin (I_X5,13)^perp.                       (2)
```

Equation (2), interpreted only in the audited joint semigroup, is the exact
theorem-shaped attachment.  A nonzero pairing invalidates this dual; it does
not prove that the holonomy target belongs to the enlarged ideal.

There is also a smaller source-symmetry family.  The full `7+1` word orbit has
48 members.  For the fixed canonical separator, seven new members cross:

```text
00010000  00001000  00000100  00000010
00020000  00002000  00000200.
```

For example, `00000010` has six crossings with pairings `{-1,-1,-1,1,1,1}`.
Transporting the carrier, target and separator together transports this
literal witness; if a source-symmetric packet is wanted, adjoining the whole
48-word `7+1` orbit is sufficient to ensure that every transported separator
has such a row.  Full `X5` already contains that orbit, so this is not an
additional hypothesis.

## 3. Why triangle membership does not create this row

The answer to the requested derivation question has two distinct levels.

1. From the authoritative proof-spine hypothesis, no derivation is needed:
   `X5` is all 6,558 mixed equations, so both (1) and the entire `7+1` orbit
   are already present.
2. From triangle membership plus the existing five-set identities alone,
   no source-labelled derivation is frozen.  The strongest exact five-set
   statement remains

   ```text
   ell_c in rowspan [L_triangle ; R_xy],               (3)
   ```

   and its literal expansion retains the six terms on the omitted triangle
   edge.  The hostile source in
   [`triangle-five-set-annihilator`](../unaudited-codex-triangle-five-set-annihilator-2026-08-22/REPORT.md)
   shows that those terms cannot be formally discarded.  A blocker
   membership is an incidence condition on `ker L_triangle`; it is not the
   degree-nine polynomial multiplier (1).

Therefore the 560 blocked-triangle clauses do not explain the separator
crossing.  They are separate incidence data to be used only after the new
literal `X5` packet has been admitted.

## 4. Rank-at-most-two is not the separator boundary

The terminal separator already fails on a mandatory `X5` row before any
holonomy localization or blocker choice.  Hence it cannot imply `H=0`, and
it cannot be used to route a no-cap point to the rank-at-most-two stratum.
That stratum remains the independent determinantal boundary of the exact
triangle comparison ladder

```text
19 -> 26 -> 27,
```

whose final factor is the `3x3` cofactor holonomy determinant.  The sound
diagram is

```text
full 22-word exchange closure -- separated by lambda_22
             |
             | add a mandatory new X5 word (one witness is 01211222)
             v
full X5 degree-13 block ------ lambda_22 is no longer a dual witness
             |
             +-- 560 blocked triangles: separate incidence conditions
             +-- H != 0 / H = 0: still an unresolved determinantal split.
```

The next exact calculation, if this route is continued, is therefore a new
CEGAR closure after adjoining either the canonical rootless word and its
needed transports or the 48-word `7+1` orbit, followed by the triangle
incidence rows.  Reusing `lambda_22` as a proof-spine obstruction is retired.

## 5. Replay and scope

The terminal attachment checker is
[`audit_terminal_separator_spine_attachment.py`](audit_terminal_separator_spine_attachment.py),
with frozen result
[`results_terminal_separator_spine_attachment.json`](results_terminal_separator_spine_attachment.json).
It reconstructs every displayed pairing over `Z` and explicitly lifts every
joint translation to a decorated degree-nine source monomial.

```sh
python3 computations/unaudited-codex-closure22-spine-attachment-2026-08-23/audit_terminal_separator_spine_attachment.py --check-results
python3 -O computations/unaudited-codex-closure22-spine-attachment-2026-08-23/audit_terminal_separator_spine_attachment.py --check-results
python3 -I -S computations/unaudited-codex-closure22-spine-attachment-2026-08-23/audit_terminal_separator_spine_attachment.py --check-results
```

Pinned terminal-CEGAR SHA-256:
`69f19e71df27d55cbe76a1e101fe2daad68d6b5a4a23d8d98e3f6e9a78d6bd75`.
Logical attachment SHA-256:
`b77fd6eb39eb8b6d1e4119569aa5afdd6449424be2da8557ebce945c61287c1d`.

The older 16-column checker/result in this directory is retained only as a
first-layer diagnostic and is superseded for proof-spine attachment by the
terminal 100-column package above.
