# Codex cap-packet lane — report

Status: **UNAUDITED**.  This lane changes no certified file.  “Exact” below
means exact arithmetic/raw polynomial reconstruction, not promotion into the
certified spine.

## Outcome

The literal six-site thirteen-exit packet does **not** lift to `N=8` as a
closed thirteen-exit object merely by adjoining a labelled common tail.
The raw degree-five chain

```text
a01^00 F_11100111 - 2 a01^11 F_00100111
```

and literal `a01^00` deletion has the signed complete **105-matching** row.
The tail-`67` sector contains the two parents and the familiar thirteen
exits, but there are another **90 crossing-tail fines**.  They split into 45
groups, each containing the two endpoint-ordered star pairings that make one
physical response term `R_ab`.  Thus “thirteen exits plus a spectator tail”
is not a raw `N=8` coefficient identity unless cut-cleanliness or an
equivalent response terminal has first been proved.

This is an exact scope correction, not a counterexample to the full
thirteen-exit lemma under its maximum-anchor/minimum-support exact-source
hypotheses.  No exact ternary source was constructed.

The more useful positive result is that W40's integral level-4 point has an
explicit active clean cap at pair `67`, with `K=I_3`.  In fact this persists
symbolically on W40's entire four-dimensional Laurent family.

## Exact four-torus cap

Write the W40 closed family using `s,t,a,b` in `(C*)^4`:

```text
lambda_21=s, lambda_65=t,
q04=a, q13=b, q26=-s*t, q57=-1/(a*b*s*t),
all other completion coordinates zero.
```

A raw Laurent reconstruction checks all 4,881 level-4 rows.  The only full
exactness defects are

```text
H_01110222 = 1/(s*a*b),
H_12221000 = s*b,
H_20002111 = -a.
```

For cap `67` and `K=I_3`,

```text
s_direct = 1,  (kappa_0,kappa_1,kappa_2)=(1,1,1),
s_direct*kappa_0*kappa_1*kappa_2 = 1.
```

The only nonzero response cells are

```text
R_05[0,2] = -1/(s*a*b),
R_15[0,1] = -1,
R_25[2,2] = 1/(a*b),
R_45[1,1] = 1.
```

They form a star centred at residual site `5`.  Consequently `r^2=0`, hence
`r^3=0`, and every one of the 729 coefficients of `E_67(I)` is identically
zero.  The raw cap-partition identity was checked independently on all 729
residual words; deletion of one response term is a must-fire negative
control.

At the integral point, exact Qbar Rabinowitsch decisions over all 17 live
pairs give seven active-cap pairs (`04,12,13,23,56,57,67`) and ten blocked
pairs.  Each positive pair has a stored rational cap; `67` is the uniform
one on the full torus.

## Assessment of the successor theorem

The high-value statement is now

> Every ternary `N=8` level-4 source with nonzero pure amplitudes has an
> active clean physical cap.

It would close general `N=8` immediately: an exact source is level-4, and
clean descent would produce a ternary `N=6` source, contradicting the
certified six-site theorem.

No named existing object refutes it:

* **W25-F8** is a genuine near-falsifier.  A fresh raw replay finds 78
  off-count-4 and 25 off-count-5 defects, so it is `X3` but not `X4`.
  This lane's independent cap encoder and exact saturation re-confirm all
  21 live pairs blocked, agreeing with W25.  The 78 level-4 rows are exactly
  what exclude it from the proposed theorem.
* **W37's `E_X4/E_X5` records are not source points.**  The scripts retain
  W25-F8's blocks and add selected nonzero `H_B` defect values inside the
  cap-error polynomial.  Even their exact 21/21 blockage does not construct
  an all-blocked `X4` source.
* **W40 is positive:** its whole four-dimensional `X4` torus has the cap
  above.

Therefore the bounded adversarial search verdict is only: **no all-blocked
`X4` falsifier occurs in the named W25/W37/W40 inputs**.  This is not
evidence for the universal theorem.

## Sharper finite attack

At `N=8`, the following elementary lemma replaces the cubic clean-error
system by a linear sufficient condition.

> **Response-star lemma.**  If a live pair `(p,q)` admits an active covector
> `K` for which all nonzero effective response edges `R_ab(K)` have matching
> number at most one (in particular, all lie in one residual star), then
> `E_pq(K)=0`.

Indeed

```text
E = s [r^2/2 exp(x)]_U + [r^3/6]_U,
```

and no two supported response edges are disjoint, so `r^2=r^3=0` in the
squarefree residual algebra.

For a fixed pair `(p,q)` and residual centre `v`, let `L_pqv(A)` be the
linear map in the nine entries of `K` whose rows are all cells of
`R_ab(K)` for edges `ab` not incident with `v`.  A response-star active cap
exists exactly when `ker L_pqv` is not contained in any of the four
hyperplanes

```text
K00=0, K11=0, K22=0, <K,A_pq>=0.
```

Over `C`, a vector space cannot be covered by finitely many proper linear
subspaces.  Hence the condition is equivalent to saying that none of those
four linear forms belongs to `rowspan L_pqv`.  Its negation is a finite
four-way row-span disjunction, expressible by minors in the original source
coordinates.

Recommended next attack:

1. Work on the actual level-4 scheme, not on packet folds.
2. For the 168 pair/centre choices, derive the row-span alternatives modulo
   maximum-anchor symmetry and the three exact binary restrictions.
3. Intersect the “all response stars blocked” alternatives with the raw
   level-4 equations.  Seek a source-ideal unit or a surviving explicit
   point.
4. Use W25-F8 as the outside-locus negative control: any proposed use of
   the level-4 equations must fail when its 78 off-count-4 rows are removed.
5. Use the W40 Laurent torus as the positive control: pair `67`, centre `5`,
   and `K=I` must survive every reduction.

The thirteen-exit packet should remain a local diagnostic after a
response/cut terminal is available; it is not currently the cleanest main
route at `N=8`.

## Files and replay

* `audit_cap_packet.py`: raw 105-term packet lift, W40 point replay, all-pair
  exact cap saturation, endpoint-order and mutation controls.
* `audit_w40_torus_cap.py`: standard-library Laurent reconstruction of the
  four-torus, all level-4 rows, cap partition, and clean error.
* `audit_successor_target.py`: adversarial W25/W37/W40 scope audit and fresh
  W25 all-pair saturation.
* `results_structural.json`, `results_all_caps.json`,
  `results_w40_torus_cap.json`, `results_successor_target.json`: frozen run
  records with executed-versus-declared control manifests.

Replay:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -I -S computations/unaudited-codex-cap-packet-2026-08-20/audit_cap_packet.py --pair all
PYTHONDONTWRITEBYTECODE=1 python3 -I -S computations/unaudited-codex-cap-packet-2026-08-20/audit_w40_torus_cap.py
PYTHONDONTWRITEBYTECODE=1 python3 -I -S computations/unaudited-codex-cap-packet-2026-08-20/audit_successor_target.py
```

