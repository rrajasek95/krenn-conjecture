# Trigger reinsertion gives the edge-Euler carrier, not physical `r0`

## Verdict

For an ordered site-0 star branch \(i\mid j\), the trigger-labelled operator

\[
                       T_{i\mid j}=I_{x_{0i}}D_{x_{0j}}                 \tag{1}
\]

is an exact split inverse on every missing-\(i\), doubled-\(j\) collision
monomial:

\[
 T_{i\mid j}\bigl(x_{0j}(M/x_{0i})\bigr)=M.            \tag{2}
\]

At carrier level it gives

\[
 T_{i\mid j}\bigl(x_{0j}\iota_{0i}(e)\bigr)
                   =x_{0i}\iota_{0i}(e).              \tag{3}
\]

The normalized full-star average is therefore

\[
 {1\over6}\sum_{i<j,\text{ ordered branches}}T_{i\mid j}
       =\sum_{i=1}^7x_{0i}\iota_{0i}                  \tag{4}
\]

on the carrier.  Its boundary is \(H\), not \(H-u\).  The missing term is
the independent homogenizer carrier \(u\iota_u(e)\).

More decisively, every operator in (1) is response-internal.  Even after
formally identifying its matching shadow with the cap-private coordinate
`B`, the comparison is

```text
                         B  Eq  target  e_C A e_R
trigger Euler shadow     1   0     0        0
physical r0              1   1     1        1
```

These two rows have rank two.  The trigger construction gives a new response
Euler copy, not the existing tied physical `r0`.

Exact checker:
[`verify_h3_full_star_trigger_reinsertion_r0_gate.py`](../computations/verify_h3_full_star_trigger_reinsertion_r0_gate.py).

## 1. Minimal parent-labelled Taylor deletion

Fix the first pair \(a=x_{01}^{11}\), \(b=x_{07}^{11}\).  There are 12
direct-free matching parents containing \(a\) and 12 containing \(b\).  A
Taylor cell must retain the ordered parent labels \((M,N)\).  Put

\[
 L_{M,N}=\operatorname{lcm}(M,N)=M\cup N.              \tag{5}
\]

For the ordered branch \(a\mid b\), the unique minimal deletion is

\[
 L_{M,N}\longmapsto b(M/a),qquad
 E_{M\mid N}=L_{M,N}\setminus b(M/a).                 \tag{6}
\]

The opposite branch is obtained by interchanging \((M,a)\) and \((N,b)\).
Deletion followed by reinsertion of \(E_{M\mid N}\) recovers the labelled
lcm exactly.

The complete census is

| lcm degree | deletion depth | labelled cells |
|---:|---:|---:|
| 6 | 2 | 12 |
| 7 | 3 | 42 |
| 8 | 4 | 90 |

Thus (6) is the smallest possible deletion on each labelled cell.  Every
one of the 12 left collision branches has 12 opposite parents, and likewise
on the right.  The normalized map is the \(1/12\) average over those opposite
parent labels.

## 2. Why lcm collection loses canonicity

The 144 labelled Taylor cells collect to only 135 distinct lcms:

```text
lcm presentation multiplicity 1       126 lcms
lcm presentation multiplicity 2         9 lcms
```

All nine ambiguous lcms have degree eight.  For each one, its two parent
presentations give two distinct left branches and two distinct right
branches.  Therefore there is no well-defined map

\[
 \{\text{unlabelled lcm monomials}\}longrightarrow
 \{\text{collision branches}\}.                      \tag{7}
\]

The parent indices are load-bearing operation labels, not bookkeeping that
may be forgotten after Taylor minimization.  This is the first exact reason
the deletion must use the full Taylor presentation rather than only its lcm
poset or Scarf-style collection.

## 3. Restriction/insertion naturality

On a parent-labelled cell, restriction commutes with (6) for every factor
kept in the four-cell branch.  There are

```text
one ordered side:     576 commuting kept-factor flags
both ordered sides: 1,152 commuting kept-factor flags.
```

It fails on every factor in the deletion set.  If \(q\in E_{M\mid N}\),
then source restriction by \(q\), followed by deletion of the remaining
factors, still produces \(b(M/a)\).  But restriction of the target branch by
the same \(q\) is zero because the target no longer contains \(q\).  The
exact debts are

```text
one ordered side:     510 deleted-factor faces
both ordered sides: 1,020 deleted-factor faces.
```

Hence minimal deletion is split and canonical on labelled objects, but it is
not a strict map of the full restriction cube.  A mapping-cylinder/Hasse
component is required for every deleted-factor direction.  The selected
factor \(a\), which is absent from every \(a\mid b\) branch, is already one
such unavoidable face.

## 4. Full-star trigger reconstruction

Apply (1) directly to every branch of all 21 site-0 pairs.  There are 540
branch instances per root and 1,080 over the separately labelled `AB` and
`AC` roots.  Every direct-free cap matching occurs exactly six times.  Thus
(4) is termwise exact, and its differential commutes with trigger
reinsertion on the matching component:

\[
 d\,T_{i\mid j}(x_{0j}\iota_{0i}e)
 =x_{0i}\partial_{0i}H
 =T_{i\mid j}\,d(x_{0j}\iota_{0i}e).                  \tag{8}
\]

Restrictions along the three non-trigger factors of each branch commute
with (1), giving 1,620 remote-factor squares over the full star.  The 540
trigger-changing faces are part of the transvection itself rather than
ordinary same-label restriction squares.

The crucial Euler distinction is

\[
 d\left(\sum_i x_{0i}\iota_{0i}e\right)=H,            \tag{9}
\]

whereas the homogenized source equation requires

\[
 d\left(\sum_i x_{0i}\iota_{0i}e+u\iota_ue\right)
                                      =H-u.            \tag{10}
\]

No pair collision or site-edge trigger supplies the last summand in (10).
This corrects the tempting statement that the seven-edge star alone produces
the complete homogenized Euler carrier.

## 5. Comparison with the existing cap generator

The old cap theorem constructs a specific generator with

\[
 dr_0=(H_0-u)e_{\rm Eq},\qquad \operatorname{target}(r_0)=1,            \tag{11}
\]

and its literal private full-nine boundary is tied: `B=Eq`.

The trigger operator has none of those cap incidences source-validly:

1. it lives in `EqSystem/response -> response`, so \(e_CAe_R=0\);
2. its star average has boundary \(H\), omitting the \(-u e_{\rm Eq}\) face;
3. it has no normalized target value;
4. its output is a bare matching occurrence.  Private full-nine insertion is
   split monic as a 180-term readout, but it is not an operation-changing
   physical map.

Thus the first categorical failure is the operation idempotent.  After a
formal cap retag, the first boundary failure is the homogenizer/central-Eq
face, and the first protected failure is target normalization.

The ordinary occurrence restriction theorem supplies one further warning.
On a centered carrier, \(\sum_eI_eD_e=2\operatorname{id}\) reconstructs the
top, but the two marked cuts retain lower centered classes.  Trigger
reinsertion does not totalize those intermediate faces merely because its
top coefficient is correct.

## Shortest positive completion

The exact remaining object is now smaller than a new coefficient orbit:

> Construct a parent-labelled Taylor-to-Spencer deletion cylinder for the
> 1,020 deleted-factor faces, together with one root-natural mixed
> divided-Hasse map carrying the complete edge-plus-homogenizer Euler carrier
> to the already existing tied `r0`.

The map must retain the private insertion square and the `AB/AC` root labels.
If it exists, the previous 7-dimensional termwise theorem makes its
normalized `B=Eq` landing unique.  Without it, calling (4) `r0` simply adds a
new off-diagonal operation by declaration.

## Scope

The Taylor, deletion, ambiguity, restriction-flag, trigger, star-average,
and rank statements are exact over \(\mathbb Q\) for the canonical
direct-free `h=3` packet.  The physical comparison is against the pinned
constructed `r0`.  No untracked common-augmentation artifact is used.
