# The collision splitter needs a spectator-Hasse module, not bare tensoring

## Outcome

The fixed-tail part of the proposed collision construction is already
uniform.  For every perfect-matching tail `M`, the four collision stars

```text
D*s1, p0*q01, D*s0, p1*q01
```

retain their two parent-labelled repairs `A/B` or `A/C`, and restriction of
a common tail edge commutes exactly with repair and reinsertion.  Thus the
`h=3` parent anti-diagonal of `58376f7` tensors formally with any fixed
tail.

That statement is strictly weaker than an all-order physical PP/AugP2
splitter.  Two new obligations appear already at `h=4`.

1. The product differential adds twelve faces `(de)*C`, one for each of the
   twelve `h=3` collision occurrences.  They are absent from the static
   tensor of the old boundary.
2. Keeping the old four tail sites paired internally covers only three of
   the fifteen perfect matchings of the six-site `h=4` tail.  Relabelling
   the `h=3` window covers all fifteen, but every matching is then presented
   three times, so the resulting cells require an overlap/descent homotopy.

Consequently a literal `h=3` cylinder does **not** suffice.  A single
`h=3` *schema* suffices only if “schema” already includes a strong dg-module
action of the complete spectator matching/Hasse species, coherent
restriction and reinsertion, overlap descent, and physical covariance of
the PP-to-AugP2 map and all protected rows.  Those clauses are precisely
the new all-`h` theorem; they do not follow from checking the `h=3` cell.

Exact checker:
[`verify_uniform_hyperbolic_collision_pp_augp2_spectator_naturality_gate.py`](../computations/verify_uniform_hyperbolic_collision_pp_augp2_spectator_naturality_gate.py).

## 1. The all-order parent-split family

Let `R` be the residual tail set, with

\[
                 |R|=2(h-1),\qquad n=h-1,
\]

and let `PM(R)` be its set of perfect matchings.  Then

\[
                         |PM(R)|=(2h-3)!! .             \tag{1}
\]

For each of the four collision types `f` and each `M in PM(R)`, write
`C_f(M)` for the collision occurrence and `P_f^+(M),P_f^-(M)` for its two
squarefree parents.  The collection map in that block is

\[
  \mathbb Q\{P_f^+(M),P_f^-(M)\}
       \longrightarrow \mathbb Q\{C_f(M)\},\qquad (x,y)\mapsto x+y. \tag{2}
\]

Its kernel is the parent anti-diagonal `(1,-1)`.  Different `f,M` retain
their root, missing/doubled, and tail labels, so (2) is block diagonal.
Hence the exact all-order counts are

\[
\begin{aligned}
 \#\{C_f(M)\}&=4(2h-3)!!,\\
 \#\{P_f^\pm(M)\}&=8(2h-3)!!,\\
 \dim\ker(\text{collection})&=4(2h-3)!! .             \tag{3}
\end{aligned}
\]

The matching theorem of `58376f7` is already enough to prove that, for
every fixed `M`, the two repairs are exactly

```text
A*M and B*M for D*s1 and p0*q01,
A*M and C*M for D*s0 and p1*q01.
```

No repair enters the tail fan.  If `e` is an edge of `M`, deleting it before
repair gives the same two parents as repairing first and deleting `e`.
Reinserting `e` reverses that equality.  Thus the matching placement and
the parent anti-diagonal are genuinely natural for every tail size; this is
the formal positive part of the uniformization.

The checker enumerates the exact family through `h=7`:

| `h` | tail matchings | four collision occurrences | parent-kernel dimension |
|---:|---:|---:|---:|
| 3 | 3 | 12 | 12 |
| 4 | 15 | 60 | 60 |
| 5 | 105 | 420 | 420 |
| 6 | 945 | 3780 | 3780 |
| 7 | 10395 | 41580 | 41580 |

The proof of (1)--(3) is the usual first-partner recursion for perfect
matchings and the block decomposition (2), so it is independent of the
finite audit range.

## 2. Formal tensoring versus the new faces

Suppose, conditionally, that `c_f` is a physical collision PP/AugP2 cell.
For one fixed tail `M`, static multiplication gives

\[
                         (dc_f)M.                       \tag{4}
\]

This does preserve the local information:

* the parent anti-diagonal and its `A/B` or `A/C` squarefree return;
* the two local-arm PP faces;
* every already constructed local response-to-AugP2 comparison face; and
* additive word, fine, repeated-edge, and operation-tail grades.

It does not give the differential of the product.  The chain rule is

\[
 d\mu(c_f,M)=\mu(dc_f,M)+(-1)^{|c_f|}\mu(c_f,\partial M), \tag{5}
\]

where, after orienting the `n` edges of `M`,

\[
              \partial M=\sum_{j=1}^{n}(-1)^{j-1}M\setminus e_j. \tag{6}
\]

The first term of (5) is formal tensoring.  The second is the new
Leibniz/restriction packet.  Each collision occurrence has exactly

```text
2 local-arm first-PP flags,
n=h-1 tail-edge first-PP flags.
```

Across the full four-family object this gives

\[
  8(2h-3)!!\quad\hbox{local-arm flags},\qquad
  4(h-1)(2h-3)!!\quad\hbox{tail-edge flags}.           \tag{7}
\]

At `h=3`, (7) is the known split `24+24`.  If instead one takes the twelve
fixed-window `h=3` collision cells and adds just one new spectator edge,
the second term in (5) gives twelve new faces at `h=4`.  More generally,
`r=h-3` added edges give `r` new first faces and `2^r-1` nonempty Boolean/
cobar tail faces for every `h=3` collision occurrence and every added-tail
matching.

The oriented formulas are internally consistent:

\[
                         \partial^2=0,
\]

and, if `I_e` inserts a new oriented edge first,

\[
                   \partial I_e+I_e\partial=\mathrm{id}.       \tag{8}

Together with the Koszul sign in (5), these identities imply `d^2=0` for
the tensor totalization.  The checker verifies (5)--(8) for both carrier
parities and tails through five edges.  What is missing is not the abstract
sign convention; it is its realization by physical labelled cells.

The new tail-edge faces retain the collision carrier on `M\e`.  At `h=3`
their topology is the familiar `P3+K2`; at higher `h` it is its spectator
extension.  For the forward roots it still has local operation type `DSQ`,
which has no committed `DS` lower idempotent.  For the reverse roots it is
`PQQ`, which has only the coarse `P2` topology and still lacks the
response-to-cap word/fine cylinder.  Tensoring does not repair either
physical typing failure from `b40cebc`.

## 3. Why a fixed `h=3` window is not exhaustive

Fix the old residual sites `2345` and require them to be internally
matched.  The three possible matchings on those sites can be multiplied by
a matching on the extra `2(h-3)` sites.  This reaches

\[
                         3(2h-7)!!                     \tag{9}
\]

tails, versus the full count `(2h-3)!!` in (1).  The difference consists
of tails with edges crossing the chosen old/new partition.  The first
counts are

| `h` | full tails | fixed-window tensors | omitted cross-partition tails |
|---:|---:|---:|---:|
| 3 | 3 | 3 | 0 |
| 4 | 15 | 3 | 12 |
| 5 | 105 | 9 | 96 |
| 6 | 945 | 45 | 900 |

This does not force an outside fan in the local repair: for any one full
tail, repair still stays on the operation four-cycle.  It says that a fixed
choice of spectator factor does not enumerate the intrinsic higher-order
source.

Relabelling the `h=3` window removes the support gap but creates a descent
problem.  Every full tail `M` has `n=h-1` edges, and choosing any two of
them as the four-site `h=3` subtail presents `M` as

```text
(two-edge h3 window) * (n-2 edge spectator tail).
```

Therefore every `M` has exactly

\[
                           \binom{h-1}{2}               \tag{10}
\]

such presentations.  A sum over windows multiplies every occurrence by
(10).  Over a characteristic-zero field one may divide by (10), but the
cell still needs coherent identifications on all overlaps; in an integral
or occurrence-labelled presentation one instead needs the corresponding
coequalizer/homotopies.  Neither normalization nor overlap coherence is
contained in one fixed `h=3` cylinder.

## 4. Minimal uniform hypotheses

Let `H` denote the oriented spectator matching Hasse/cobar species.  The
following four hypotheses are sufficient, and each answers a distinct
failure above or in the pinned physical audits.

**U1 — four-family source seed.**  There are physical parent-split
collision carriers for all four root-order families, with the complete
local PP/AugP2 boundary and the root/chart overlap square.  This is exactly
the local object still missing in `b40cebc`; two forward coefficient faces
alone are not an order-natural square.

**U2 — spectator dg-module.**  The physical source complexes carry a strong
symmetric-monoidal action

\[
                         \mu:\mathcal C\otimes H\to\mathcal C
\]

satisfying (5), the shuffle signs, and associativity/unitality.  This
supplies all `(dM)c_f` faces and makes their total differential square to
zero.

**U3 — restriction/reinsertion and overlap descent.**  The edge-labelled
restriction and insertion maps realize (8), satisfy Beck--Chevalley for
disjoint edges, and identify the `(10)` relabelled-window presentations.
This makes the construction independent of a distinguished spectator
partition and compatible with recursive reinsertion.

**U4 — physical covariance and exhaustivity.**  The PP-to-AugP2
word/fine/repeated comparison, reduced Eq, target, physical `q`, anchor,
`W`, ordinary residue, and shifted ridge are `H`-linear.  Normalized
window induction must land in the complete source and terminal/Macaulay
block, not merely the sector divisible by one fixed spectator tail.  This
clause includes the full-GHZ target compatibility which bare independent
spectator colours fail.

Under U1--U4, set

\[
                         C_f(M)=\mu(c_f,M).             \tag{11}

U2 gives every local and spectator face of (11) and proves `d^2=0`; U3
makes restriction/reinsertion and window presentation coherent; U4
transports the physical AugP2 and protected rows and descends to the full
order-`h` source.  Thus (11) is the required four-family collision
PP/AugP2 splitter at every `h`.

Conversely, the four failures isolate the roles of the hypotheses:

```text
without U1: the h3 collision/DSQ/PQQ cell is already absent;
without U2: twelve (de)*C faces survive at h4;
without U3: the three h4 window presentations need not agree;
without U4: the result stays in a fixed word/tail sector and lacks the
            physical AugP2/target/ridge landing.
```

This is the requested all-`h` naturality theorem.  It is conditional, not a
construction of U1--U4.

## 5. Does one `h=3` schema suffice?

There are three distinct meanings, and only one is positive.

1. A single fixed-window `h=3` cell multiplied by disjoint tails: **no**.
   It misses both the Leibniz term and cross-partition matchings.
2. All site relabellings of that cell, summed or averaged: **still no by
   itself**.  It covers the tops, but introduces the overlap multiplicity
   (10) and does not totalize the spectator faces or physical readouts.
3. One `h=3` generator declared inside a structure satisfying U1--U4:
   **yes**.  The dg-module and descent axioms then force the all-order
   formula (11).  Those axioms are substantive new uniform data, so this is
   a compact presentation of the required theorem, not a deduction from an
   isolated `h=3` verification.

The shortest positive test is therefore the first structure map at `h=4`:
construct `mu(c_f,e)` for one spectator edge, with its twelve `(de)*C`
faces and the homotopy identifying the three relabelled-window
presentations, while retaining the four parent labels and the forward
`DSQ`/reverse `PQQ` physical AugP2 types.  A successful cell of that form is
the first nonformal datum in U2--U4; the oriented Hasse identities then give
the exact recursion which must be continued at higher order.

## Verification

Run

```text
python3 computations/verify_uniform_hyperbolic_collision_pp_augp2_spectator_naturality_gate.py
python3 -O computations/verify_uniform_hyperbolic_collision_pp_augp2_spectator_naturality_gate.py
python3 -I -S computations/verify_uniform_hyperbolic_collision_pp_augp2_spectator_naturality_gate.py
```

The checker pins `b40cebc` and `58376f7` and the established spectator
guards, enumerates the exact parent-split and PP/restriction families
through `h=7`, verifies the fixed-window and relabelled-window counts, and
checks the oriented Leibniz/reinsertion totalization for both parities.

Frozen ledger digest:

```text
49c1833414dfafa6fcc145133b5eebcd27472e6b66985d5a36876eac91ed2c8e
```
