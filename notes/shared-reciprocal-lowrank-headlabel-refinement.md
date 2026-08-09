# Shared reciprocal low-rank packets after head-label propagation

This note continues the 16 coordinate-plane omission orbits from
[`shared-reciprocal-fourcover-overlap.md`](shared-reciprocal-fourcover-overlap.md).
It incorporates the literal reciprocal head labels, the exact ranks of the
four deleted endpoint stars, the opposite-chord diagonal clauses, and the
flat-wedge rank theorem.

The outcome is a complete finite refinement, not an unconditional closure of
the reciprocal branch.  No omission orbit by itself forces curvature or an
adjacent cubic pair.  Curvature is forced on an explicit subset of the
endpoint-rank/chord branches; every other case is now a finite residual
packet.  The sole zero-mismatch omission orbit is isolated completely.

## 1. Reciprocal head labels

For shared reciprocal pairs `pq,pr`, write

\[
 A_{pq}=\lambda E_{ba},\qquad A_{pr}=\mu E_{dc}.             \tag{1}
\]

The outgoing witnesses from `p` have distinct target colours, so

\[
                              a\ne c.                        \tag{2}
\]

The endpoint lines at the shared site `p` are `e_b,e_d`.  Combining the 99
labelled omission-contingency states with the 54 choices
`(a,c,b,d)`, and quotienting simultaneous target-colour permutation and
exchange `q<->r`, gives exactly

\[
                         \boxed{477}                         \tag{3}
\]

head-labelled low-rank packets.

For a packet let

\[
 i=\alpha(r),\qquad j=\beta(q)
\]

be the exceptional omitted colours.  The exact star-routing clauses are

\[
 (a=b=j)\ \lor\ A_{qr}[j,j]\ne0,
 \qquad
 (c=d=i)\ \lor\ A_{qr}[i,i]\ne0.                            \tag{4}
\]

Among the 477 packets, the number of distinct opposite-chord diagonal
colours forced by (4) is

\[
       0:\ 9,\qquad 1:\ 214,\qquad 2:\ 254.                 \tag{5}
\]

Two live diagonal cells are recorded as support information only; without
minor information they do not force matrix rank two.

## 2. Exact shared-endpoint rank fork

The full aggregate endpoint star at `p` has rank three.  If `b=d`, deleting
either reciprocal block leaves the other copy of the same line, so both
deleted stars at `p` still have rank three:

\[
 b=d\quad\Longrightarrow\quad
 (\operatorname{rk}S_p^{\setminus pq},
  \operatorname{rk}S_p^{\setminus pr})=(3,3).                \tag{6}
\]

There are 159 such head-labelled packets.  If `b!=d`, all four rank patterns
in `{2,3}^2` are possible.  The checker constructs seven coordinate endpoint
lines realizing each pattern exactly, so no stronger rank conclusion follows
from the two reciprocal lines and target flattening alone.

At an outer endpoint the omission plane sharpens this.  For example the five
common-core blocks at `q` span the coordinate plane omitting `j`.  If (4)
forces `A_qr[j,j]`, the chord is transverse to that plane and deletion of
`pq` has rank three.  If the direct block `A_pq` supplies the missing
diagonal instead, the chord may lie inside or outside the plane, so deletion
rank two or three is realizable.  The statement at `r` is symmetric.

Thus forced chord diagonals also force the corresponding outer goodness.
Nevertheless none of the 16 omission orbits alone supplies the three
essential incidences needed for a cubic site.  In particular, **no adjacent
cubic packet is forced by the four-cover, omission, and head-label data
alone**.

## 3. The exact curvature branches

When all four deleted endpoint stars have rank three, `pq` and `pr` are
adjacent rank-one good arms.  The pinned flat-wedge normal forms then give:

- if `b=d`, the shared factors are proportional, and flatness requires
  `rank(A_qr)>=2`;
- if `b!=d`, the shared factors are independent, and flatness requires
  `rank(A_qr)=3`.

Therefore

\[
 \boxed{
 \begin{array}{ll}
 b=d, \operatorname{rk}A_{qr}\le1 &\Longrightarrow
       \text{curved rank-one overlap},\\
 b\ne d, \operatorname{rk}A_{qr}\le2 &\Longrightarrow
       \text{curved rank-one overlap},
 \end{array}}                                                \tag{7}
\]

provided both arms are good at their outer endpoints as well.  The checker
branches every permitted shared/outer deletion rank and chord-rank class,
including the transverse-chord goodness just proved.  Across the 477
canonical head-labelled packets this produces 5,223 replay rows: 804 land
in the forced-curvature condition (7), while 4,419 remain
finite residual rows.  These row counts are an exhaustive replay ledger, not
additional symmetry-orbit counts.

The residual rows have one of three explicit guards:

1. a rank-two deleted star, hence a named essential reciprocal incidence;
2. a proportional good wedge with opposite chord rank at least two; or
3. an independent good wedge with invertible opposite chord.

Thus “finite residual packet” here has concrete rank data; it is not a
generic nonlinear ideal.

## 4. The sole zero-mismatch omission orbit

At the omission level there is exactly one orbit with no common-core
purification.  After head labels it splits into 15 packets.  Normalize its
common exceptional omitted colour to `i`.  Then:

- the five common coordinate planes agree site by site, with omission
  multiplicities `(1,2,2)`;
- `A_qr[i,i]` is forced in every packet, because `a!=c` prevents both shared
  reciprocal blocks from being diagonal in colour `i`;
- five of the 15 packets have `b=d`, so both shared-site deletions are rank
  three by (6);
- three packets have exactly one of `A_pq,A_pr` diagonal in colour `i`;
  the other twelve have neither one diagonal in colour `i`.

This is the sharp aligned residual family:

\[
 \boxed{\text{common planes aligned},\quad A_{qr}[i,i]\ne0,
        \quad 15\text{ endpoint-label packets}.}             \tag{8}

It has no purified common-core site, so further progress must use the live
chord cell, endpoint-star rank flags, or a coefficient identity.  Repeating
the four-cover count cannot refine it.

## 5. Scope

This closes the requested propagation through all 16 low-rank omission
orbits.  It deliberately makes no new claim about the residual full-span
branch: an incident space of dimension three can be assembled by several
rank-one blocks, and no clean finite implication to curvature was found.

The next exact coefficient targets are now bounded:

- close the 15 aligned packets (8), beginning with the five proportional
  shared-line cases;
- on mismatched packets, combine the purified K5 core line with the named
  essential incidence or high-rank chord in the residual-row guard; and
- use a three-essential completion only when it is actually present, rather
  than inferring cubicity from selected degree.

## Reproduction

```sh
python3 computations/verify_shared_reciprocal_lowrank_headlabel_refinement.py
python3 -O computations/verify_shared_reciprocal_lowrank_headlabel_refinement.py
```

The checker pins the four-cover overlap and flat-wedge normal forms,
constructs every permitted endpoint-rank pattern, and freezes the complete
head-label/chord/rank ledger.
