# General colorwise witnesses at an invertible `K_8` pair

## 1. Outcome

Fix an invertible deleted block `A_pq` and the six outside sites `R`.  Put

\[
 C_{u,r}=A_{pu}K_rA_{qu}^T,
 \qquad
 W_u=\{r:C_{u,r}=0\}.                                    \tag{1}
\]

The one-hole identities, the strict three-hole obstruction, and the
hard-annihilator two-hole obstruction imply

\[
 \#\{u:r\in W_u\}\ge2\quad(r=0,1,2),
 \qquad
 \#\{u:W_u\ne\varnothing\}\ge5.                         \tag{2}
\]

The three-site equality case is excluded in
[`n8-minimal-witness-union-obstruction.md`](n8-minimal-witness-union-obstruction.md).
The four-site equality case is excluded in
[`n8-hard-annihilator-union-four.md`](n8-hard-annihilator-union-four.md):
arbitrary common annihilators leave twelve hard-capacity patterns, of which
nine violate a two-hole determinant and three violate an anchor rectangle
or independent annihilator monomials.

This note classifies the incidence information in (2) and determines what
it gives to the target-apex method of
[`common-annihilator-plane-obstruction.md`](common-annihilator-plane-obstruction.md).

* The weaker colorwise counts together with union size at least three have
  228 six-site incidence orbits.  Six lie on the impossible three-site
  stratum and 23 on the impossible four-site stratum, so the strict bound
  (2) leaves 199.
* Every pattern contains a subincidence with exactly two witnesses per
  color; there are seven orbits of those selected cores.  If the **full**
  pattern itself has exactly two witnesses per color, only two remain
  after the strict union bound.
* The former equality candidate was the three-cycle of witness sets
  `{0,1}`, `{0,2}`, `{1,2}`.  Reversing the two star assignments in the
  three-hole identity gives the same nonzero residual-vector coordinate in
  a unique off-diagonal word, a contradiction.
* An exact two-color witness site has a fixed one-dimensional common
  annihilator, namely the missing coordinate line.  A singleton witness can
  have no fixed common annihilator.  Even a triple witness can have none if
  one of its two star blocks is zero and the other is invertible.

Consequently, the surviving colorwise witness incidence alone does not
reproduce the four
two-dimensional fixed planes needed by the pure-`K_4` target-apex proof.
Several five- and six-site minimal patterns can be realized with no
incidence-forced fixed annihilator at four or more sites.  Extending the
obstruction therefore requires a new identity for moving cross-product
lines or extra block information beyond the sets `W_u`.

## 2. The seven incidence-minimal cores

Encode a witness subset by its binary mask:

\[
\begin{array}{c|cccccccc}
\text{mask}&0&1&2&3&4&5&6&7\\ \hline
W&\varnothing&0&1&01&2&02&12&012.
\end{array}                                               \tag{3}
\]

Sites are interchangeable, and `S_3` permutes the three bits.  First impose
the three color-degree bounds and only the older union bound three.
Enumerating the nondecreasing six-tuples gives 228 raw orbits.  By the size
of the full witness union, they split as

\[
\begin{array}{c|rrrr}
\#\bigcup_rS_r&3&4&5&6\\ \hline
\text{number of orbits}&6&23&61&138.
\end{array}                                               \tag{4}
\]

The strict bound (2) deletes the first two columns, leaving

\[
                              61+138=199                 \tag{4a}
\]

incidence orbits in the general branch.

Choose exactly two witnesses for each color from any pattern satisfying
(2), discarding its other incidences.  The resulting degree vector is
`(2,2,2)`.  Up to the same symmetries, its mask multiset is one of exactly
seven rows:

\[
\begin{array}{c|c|c|c}
&\text{six masks}&\#\text{ witness sites}&
  \#\text{ exact-double sites}\\ \hline
A&(0,0,0,1,6,7)&3&1\\
B&(0,0,0,3,5,6)&3&3\\
C&(0,0,1,1,6,6)&4&2\\
D&(0,0,1,2,4,7)&4&0\\
E&(0,0,1,2,5,6)&4&2\\
F&(0,1,1,2,4,6)&5&1\\
G&(1,1,2,2,4,4)&6&0
\end{array}                                               \tag{5}
\]

Here “exact-double” refers to the displayed core.  Further incidences in
the original pattern can of course upgrade one of those sites.

If the **full** witness union had size three, Theorem 6.3 of
[`two-vertex-annihilation-identities.md`](two-vertex-annihilation-identities.md)
applies.  It gives permutations `sigma,tau` differing by a three-cycle and

\[
 A_{pu}=a_ue_{\sigma(u)}^T,qquad
 A_{qu}=b_ue_{\tau(u)}^T.                                \tag{6}
\]

At site `u`, the cross matrix is nonzero only in the third color.  Thus the
three witness masks are exactly `3,5,6`, in some order.  Row B was the
unique candidate after this normal form; row A and the other four raw
three-site orbits were already excluded.

The reverse-star argument in
[`n8-minimal-witness-union-obstruction.md`](n8-minimal-witness-union-obstruction.md)
eliminates row B as well.  Briefly, over the domain
`C[alpha,beta]/(alpha^T A_pq beta)`, the constant color-`r` word has one
ordered star source and a nonzero residual-vector coordinate.  Reversing
the two distinct star partners uses that same coordinate in an
off-diagonal word with a unique source.  Its coefficient must be both
nonzero and zero.  Hence the full witness union cannot have size three.

The seven rows in (5) remain the possible **selected subcores** of a larger
pattern: a union-at-least-five pattern can contain A--E after other
incidences are discarded.  If the full pattern itself has degree exactly
`(2,2,2)`, however, the strict bound excludes A--E and precisely F--G
remain.

## 3. What a witness subset says about the two row spaces

Put

\[
 P=A_{pu},\qquad Q=A_{qu},\qquad
 U=\operatorname{row}P,quad V=\operatorname{row}Q.       \tag{7}
\]

The entries of `PK_rQ^T` are the `r` coordinates of `x cross y` for
`x in U,y in V`.  This gives a complete elementary classification for
sites with at least two witnesses.

**Lemma 3.1 (local row-space classification).**

1. If all three colors are witnesses, then either `P=0`, `Q=0`, or the two
   nonzero row spaces are the same line.
2. Suppose exactly two colors are witnesses and `t` is the missing color.
   Then
   \[
                    U,V\subset e_t^\perp,
                    \qquad U+V=e_t^\perp.                \tag{8}
   \]
   In particular the fixed common annihilator is exactly `C e_t`.
3. Suppose `r` is a witness.  Let `pi_r` delete coordinate `r`.  If both
   `pi_r(U)` and `pi_r(V)` are nonzero, they lie on one common line in the
   remaining coordinate plane.  Hence `U+V` lies in a two-plane containing
   `e_r` and has a fixed annihilator line.  The exceptional alternative is
   that one projected row space is zero.  If the other projected row space
   has dimension two, `U+V=C^3` and there is no fixed common annihilator.

**Proof.**  The first statement is the triple-zero classification: every
`x in U` is parallel to every `y in V`.

For the second, every cross product lies in `C e_t`.  Since the witness set
is exact, choose `x,y` with `x cross y!=0`; their span is the coordinate
plane `e_t^perp`.  For any `x' in U`, the relation
`x' cross y in C e_t` puts `x'` in the same plane; the argument for `V` is
identical.  The chosen nonparallel pair makes the sum equal that plane.

For the last statement, `(x cross y)_r=0` says precisely that the two
coordinate projections `pi_r(x),pi_r(y)` have zero determinant.  If both
projected spaces are nonzero, every vector in one is parallel to every
vector in the other, so their sum is one-dimensional.  If one is zero, the
condition places no restriction on the other, giving the stated
exception. `QED`

The exceptional singleton case is not artificial.  For example,

\[
                  P=e_0e_r^T,qquad Q=I_3                \tag{9}
\]

has witness set exactly `{r}` and `U+V=C^3`.  Likewise `P=0,Q=I_3` has
all three witness colors but no nonzero fixed common annihilator.  On the
other hand, for distinct `r,s`,

\[
                  P=e_0e_r^T,qquad Q=e_1e_s^T           \tag{10}
\]

has exactly the two witnesses `{r,s}` and fixed annihilator equal to the
third coordinate line.  These examples show that every assertion above is
sharp at the level of the two stars.

## 4. Boundary of the target-apex extension

The closed all-triple-zero branch used more than the vanishing of the cross
matrices.  Arbitrary one-hole contractions forced six sites into coordinate
common-row-line classes

\[
 U_0\sqcup U_1\sqcup U_2,qquad |U_r|=2,                 \tag{11}
\]

and gave a fixed two-plane `L_u=e_r^perp` at every `u in U_r`.  Deleting
`U_r` then produced a nonzero pure matching tensor on four
two-dimensional spaces.  Its target-aligned apex drove the zero-cofactor
propagation.

No surviving full minimal pattern in (5) supplies this input:

* C and E give only two fixed coordinate lines;
* F gives one;
* G consists entirely of singleton witnesses, for which (9) shows that no
  fixed annihilator is forced;
* the triple site in D can be the one-sided example `P=0,Q=I_3`, so even it
  does not force a plane.

Rows A and B can still occur as a selected subcore inside a larger pattern,
but their additional witness sites—not the subcore—would have to supply any
fixed planes.

Thus the target-apex lemma remains valid wherever a nonzero pure projected
`K_4` can be constructed, but the general incidence data do not construct
one.  A viable extension would have to establish at least one of the
following genuinely new statements:

1. a moving-annihilator analogue of the pure-`K_4` apex lemma, allowing the
   one-dimensional line `C gamma_u(alpha,beta)` to vary with the incidence
   point;
2. a globalization theorem upgrading singleton or one-sided triple
   witnesses to fixed row-space planes; or
3. compatibility across several invertible deleted pairs, so that a site
   lacking a fixed plane for `pq` acquires one from another pair.

The existing common-annihilator proof does not justify any of these
upgrades by itself.

## 5. Exact checker

Run

```text
.venv/bin/python computations/verify_general_witness_incidence.py
```

It verifies the raw 228-orbit count and its `6+23+61+138` union-size split,
the strict 199 count, the seven selected cores (5), the two surviving full
minimal patterns F--G, and sharp exact `3 by 3` block models for witness
multiplicities zero through three.  The separate checker
`verify_n8_minimal_witness_union.py` audits the reversed-star word
incidence that removes the former three-site candidate, while
`verify_n8_hard_witness_union_four.py` audits the four-site elimination.
