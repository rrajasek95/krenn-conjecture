# An evaluated unbalanced determinant enters the exact coloop/five-lock landing

## Result

The alternating `K3,3` debt of `62054c1` has a physical transverse
interpretation only after evaluation.  Let

\[
 B_S(A)=
 \left(A_{s_i t_j}^{z_{s_i}z_{t_j}}\right)_{1\leq i,j\leq3}
\]

be a decorated cross-cut block for the six-site word `z=001122`.  If the
cut is colour-unbalanced and

\[
                              \det B_S(A)\ne0,                       \tag{1}
\]

then some offdiagonal physical cell `e` has a nonzero signed `2 x 2`
Laplace cofactor.  In particular `e!=0`.  The complete target-augmented
private-site identity at `e` therefore supplies a nonzero physical
determinant--hafnian-cofactor fan with distinct centre heads.

If `e` is a simple selected anchor edge, the existing transverse landing
theorem is now exhaustive:

1. no nonzero pure-`c` matching avoids `e`, giving the anchor-contained
   pure-target-coloop `C6/C8` carrier;
2. an avoiding pure-`c` matching exists and an active fan mate escapes,
   giving a distinct-head four-good overlap;
3. the active web is anchor-contained, and the five-lock theorem gives an
   anchor-safe deletion, a complementary crossed four-good wedge, or the
   injective no-complementary-wedge residual.

Thus evaluated determinant nonvanishing bridges cleanly to the **existing**
landing theorem once its offdiagonal factor is placed on the marked simple
edge.  It does not close either residual by itself.  Balanced determinants
can be nonzero with purely diagonal support, and an unbalanced determinant
can be a single anchor-contained matching with two disjoint offdiagonal
cells.  These are sharp guards to an unconditional landing claim.

Checker:
[`verify_h3_evaluated_determinant_transverse_landing_reduction.py`](../computations/verify_h3_evaluated_determinant_transverse_landing_reduction.py).

## 1. The Laplace bridge is physical

An unbalanced `3|3` cut has colour multiplicities

\[
                         (2,1,0)\mid(0,1,2),                       \tag{2}
\]

up to exchanging shores and permuting colours.  Choose a site on the first
shore whose repeated colour is absent from the second shore.  Every entry in
that row of `B_S` is offdiagonal.  Laplace expansion along it gives

\[
       \det B_S=\sum_{j=1}^{3}B_{ij}\operatorname {Cof}_{ij}(B_S).
                                                                    \tag{3}
\]

Under (1), at least one product on the right is nonzero.  Its entry

\[
                           e=B_{ij}\ne0                            \tag{4}
\]

is a literal decorated physical edge cell with distinct endpoint colours,
and its signed two-edge cross-cut cofactor is nonzero.

The physical active cofactor is obtained from a different identity and must
not be conflated with this signed cofactor.  For
`e=A_{vu}^{ba}`, `a!=b`, the complete pure-`a` private-site equation is

\[
       \sum_{s\ne u,v}\Delta^v_{us}C^a_{vs}=-A_{vu}^{ba}.          \tag{5}
\]

Since the right side is nonzero, some literal product
`Delta^v_us C^a_vs` is nonzero.  This is the actual source-provenant active
fan: `Delta` gives distinct centre heads and `C` is the nonzero common
hafnian cofactor.  Transposing `u,v` gives the bidirectional fan.  Therefore
the determinant supplies the nonzero offdiagonal input, while (5) supplies
the physical active-minor/cofactor typing.

The checker exhausts all `3^9` matrices with entries in `{-1,0,1}` on each
of the six unbalanced cuts.  Every nonsingular matrix has a nonzero
offdiagonal Laplace product in the prescribed absent-colour row.  The proof
is (3); the finite audit freezes the colour and sign conventions.

## 2. Landing after simple-edge typing

Assume the edge `e=uv` in (4) occurs in exactly one selected pure anchor
matching, of colour `c`.  Both deleted endpoint-star quotients then miss the
same head `c`.  There is a literal dichotomy in the pure-`c` target
coefficient.

If every nonzero pure-`c` matching contains `e`, then `e` is a target
coloop.  The physical `E2` alternative reduces it to an alternate target or
an exchange carrier.  At six-site order the only non-recombining
anchor-contained carriers are the one `C6` and six `C8` types.  This is the
first named residual.

Otherwise choose a nonzero pure-`c` matching avoiding `e`.  Reselecting it
removes `e` from the three-anchor union and makes both deleted stars at `e`
rank three.  Apply (5) and its transpose.

* If a nonzero active mate escapes the reselected anchor union, the mate and
  `e` have all four deleted-star ranks three, distinct centre heads, and a
  nonzero physical cofactor.  They form the required four-good active pair.
* If every active mate is trapped, the same-star five-lock theorem is exact:
  a kernel gives an anchor-safe support deletion, complementary crossed
  components give the four-good wedge, and otherwise the lock is injective
  with no complementary off-anchor wedge.

No additional determinant case remains after the simple-edge hypothesis.
The determinant is an entry certificate for (5), not a replacement for the
coloop/five-lock analysis.

## 3. Why determinant nonvanishing alone is insufficient

There are two independent sharp guards.

### Balanced diagonal guard

Across `024|135`, both shores have colours `(0,1,2)`.  Set the cross-cut
block to the identity.  Then

\[
                         \det B_{024}=1,                            \tag{6}
\]

but its only nonzero matching is `01|23|45`, decorated by `00,11,22`.
There is no offdiagonal cell to which (5) applies.  Thus an arbitrary
evaluated alternating determinant is not automatically transverse.

### Unbalanced anchor-contained guard

Across `012|345`, use the permutation block with nonzero matching

\[
                              04\mid15\mid23.                       \tag{7}
\]

It has determinant of absolute value one.  Cells `04` and `15` are both
offdiagonal of colour type `02`, while `23` is diagonal of type `11`.  The
two offdiagonal cells are disjoint, so they do not form a shared-centre fan,
and the whole matching may lie in the selected anchor union.  Hence the
extra two factors of a determinant monomial do not force fan escape or close
the injective five-lock residual.

These are local physical-coordinate guards, not standalone GHZ source
counterexamples.  They prove that the missing implication is source
incidence—simplicity and anchor escape—not another determinant identity.

## 4. Rectangular rank-two is a different branch

For the rectangular alternative, a rank increase by two in the **complete
protected physical matrix** already gives a localized source unit.  In the
minimal packet

\[
 M=(0),\qquad g=(1),\qquad h=(1),qquad
 \det\begin{pmatrix}0&1\\1&0\end{pmatrix}=-1.                     \tag{8}
\]

This branch closes algebraically and need not manufacture a four-good pair.
If only the numerical rank pattern is retained while the complete physical
minor is forgotten, it has no support interpretation: the Cartan coordinate
could carry the diagonal `(c,c)` head on the selected edge.  This is the
visibility guard of `32f3bdc`, not a new landing theorem.

Accordingly the correct split is:

```text
complete protected rectangular rank +2  -> localized source unit;
evaluated unbalanced cross-cut minor     -> offdiagonal private-site entry;
abstract rank or occurrence pairing      -> no physical landing conclusion.
```

## 5. Shifted frontier

There is a separate typing issue on the rectangular lift-or-separator gate.
If the domain `X` of the complete source map really has one independent
coordinate for the chosen matching occurrence and

\[
                              h=e_s^* ,                              \tag{9}
\]

then the separator

\[
                         \lambda^TM=e_s^*                            \tag{10}
\]

is indeed a localized occurrence pivot and closes the branch as a source
unit.  The current common-tail theorem has not constructed that domain.

It produces a marked matching monomial **inside** a complete coefficient
row.  If one physical row generator expands to three occurrence terms, the
map from its physical one-dimensional domain to the free occurrence module
is schematically

\[
                 R(1)=e_{\mu_1}+e_{\mu_2}+e_{\mu_3}.                 \tag{11}
\]

Every occurrence selector has the same pullback:

\[
                   R^*e_{\mu_1}^*=R^*e_{\mu_2}^*
                    =R^*e_{\mu_3}^*=1.                              \tag{12}
\]

Hence an occurrence covector on the free presentation does not isolate a
term on the physical complete-row domain; the other matching terms are not
independent source columns.  Conversely the protected pure-anchor or
anchor-incidence functional used in the rectangular theorem is a genuine
covector on physical columns, but it need not equal the selector of one
matching occurrence.

Therefore (10) is conditionally a source unit exactly as the lift-gate note
states, but that condition is the missing marked occurrence-domain lift,
not data already provided by common-tail multiplication.  Treating `h` as
both the occurrence selector and the aggregate physical anchor would assume
the theorem being sought.

The determinant-to-cofactor bridge is now closed.  The remaining hypothesis
is incidence/source typing:

> Place a nonzero offdiagonal Laplace factor of the evaluated determinant on
> the marked simple selected edge, or show that failure of simplicity is
> already an effective Hall/reselection exit.

Once simplicity holds, the existing transverse theorem routes every branch
to a source unit, anchor-safe deletion, four-good pair, pure-coloop `C6/C8`,
or injective five-lock no-wedge.  The cross-cut determinant supplies no
further relation capable of eliminating the last two residuals.

## Verification

```text
python3 computations/verify_h3_evaluated_determinant_transverse_landing_reduction.py
python3 -O computations/verify_h3_evaluated_determinant_transverse_landing_reduction.py
python3 -I -S computations/verify_h3_evaluated_determinant_transverse_landing_reduction.py
```

Frozen ledger SHA-256:

```text
880bd758e4266538e5e9c9d2c96872e24e00ad78b11240b4026b6f18d7d86bec
```
