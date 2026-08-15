# Pure escape normalization does not descend the marked parent selector

## Result

The structural pure escape and the local `PAComp` route meet at the same
parent anti-diagonal, but normalization does not remove it.

In the exact nine-cell escape packet, write the already weighted occurrence
coordinates as

```text
M0 = long C6 cap parent, contribution  2
M1 = short C4 cap parent, contribution -2
N  = cap-avoiding escape, contribution  1.
```

The physical mixed and pure covectors are

\[
 m=(1,1,0),\qquad p=(1,1,1).                         \tag{1}
\]

Thus normalization makes the escape covector absolute:

\[
 e_N=p-m=(0,0,1),\qquad e_N(2,-2,1)=1.              \tag{2}
\]

But the parent selector and shortest-tail restriction are

\[
 e_{M_1}=(0,1,0),\qquad e_{01}=(0,1,1).             \tag{3}
\]

Both raise the rank of the physical row span from two to three.  The parent
anti-diagonal

\[
 \delta=(1,-1,0)                                    \tag{4}
\]

is killed by `m` and `p` but read as `-1` by both covectors in (3).  Pure
normalization changes the right-hand side of (1); it does not enlarge the
row span.  Therefore it proves that an escape is nonzero, but does not choose
the cap parent with which that escape has the shortest alternating cycle or
common tail.

The exact checker is
[`verify_escape_parent_selector_marked_carrier_comparison.py`](../computations/verify_escape_parent_selector_marked_carrier_comparison.py).

## 1. The marked/unmarked obstruction

The same calculation can be stated without the nine-cell coefficients.
Let two marked cap lifts be the basis of `Q{M0,M1}`.  Forgetting the parent
mark is the augmentation

\[
                         A=(1,1).                    \tag{5}
\]

The marked projector onto `M1` has readout `(0,1)`.  Descent to the unmarked
one-dimensional module would require a scalar `lambda` satisfying

\[
                  \lambda(1,1)=(0,1),               \tag{6}
\]

which is impossible.  Its obstruction is exactly
`ker(A)=Q{(1,-1)}`.  The canonical swap-invariant section
`1 -> (M0+M1)/2` exists, but it is the symmetric average, not an occurrence
selector.

Tensoring (5) with the normalized escape scalar `N=1` leaves (5), its rank,
and its kernel unchanged.  Equivalently, multiplying a relative marked
projector by a unit does not turn it into an unmarked idempotent.  The unit
is useful only after a parent-resolving landing has already been constructed:
then it certifies that the selected tail channel is live.

## 2. Comparison with `c3f6231`

Commit `c3f6231` constructs exactly the **combinatorial kind** of datum that
the structural recurrence asks for:

* the collision branch retains its literal parent, missing site, fine
  matching, and reinsertion label;
* the divided-root square commutes on all 540 parent branches;
* all 1,080 marked `P3+K2` deletion faces are coefficient-one termwise; and
* the omitted-root restrictions give a monic pointed occurrence section.

This is a genuine positive match, but only in the canonical marked-derived
operation

```text
response word 11110000  ->  cap word 01211222,
P2 cuts q23:21 and q45:12.
```

The structural selector in (3) lives in the diagonal coefficient operation
`111111`, with cap `34` and common tail `01`.  A site permutation matches the
bare matching geometry, but it does not change the response operation into
that coefficient operation or supply its complete companion rows.  Hence
`c3f6231` supplies the parent-labelled marked carrier, not its underived
physical transport to the structural escape packet.

Its first protected landing makes the same failure visible:

```text
derived readout     (delta_plus, delta_plus)
required output     (delta_plus, 0).
```

The primitive anti-diagonal reads zero on the tied vector and nonzero on the
required one; the committed integral normalization reads `3`.

## 3. Comparison with `9bbff79`

Commit `9bbff79` constructs the source side of the desired operation change.
For every literal response parent it has the trigger-labelled replacement

\[
 T_{i\mid j}=I_jD_i,\qquad T_{i\mid j}(M)=x_j(M/x_i), \tag{7}
\]

and deletion of `x_j` followed by reinsertion of `x_i` recovers the parent.
The ordered-pair readout covers all 159 coordinates, while collision
triangles and the common Euler carrier

\[
                         dG_0=H-u                     \tag{8}
\]

complete the response-side chain object
`TrigEulerSpencer_rep`.

What (7)--(8) do not do is change the operation idempotent.  Every current
trigger replacement remains in `End(response)`.  Consequently the missing
map is still

\[
 \mathrm{TrigEulerSpencer}_{rep}\longrightarrow C_{AugP2}, \tag{9}
\]

sending trigger deletion/reinsertion to the selected marked cap face and
`G0` to `r0/E`.  Equation (2) cannot define (9); it only gives a scalar
normalization after such a map exists.

## 4. Comparison with `d97bf7a`

Commit `d97bf7a` makes the parent-kernel diagnosis literal.  With the
missing-site/fine mark retained, the collision-to-cap square is Cartesian
and the derived cap totalization resolves the same 90-parent module as the
response complex.  Forgetting the mark collapses 1,080 marked cap flags to
380 unmarked cofactors, each with two or three lifts.  The unmarked square is
not Cartesian.

At the protected underived descent its primitive coordinates are

```text
dN      = (1,0)
dr0     = (0,1)
omega   = (1,-1).
```

They have rank two.  This is the two-coordinate analogue of (1)--(4): the
unmarked/common-parent comparison cannot see the anti-diagonal needed by the
physical protected readout.

The normalized-cone guard is decisive.  A relative cell

\[
                         dK=tE                         \tag{10}
\]

becomes `dK=0` after the normalization `t=H0-u=0`, leaving one `H0` and one
new `H1` class.  Only an absolute `dK=E` kills both.  Thus the structural
normalization `N=1` cannot be used as a new argument that normalization makes
the marked occurrence projector absolute; that is precisely the inference
already ruled out by the normalized-cone calculation.

## 5. Unified frontier

The two routes now share a precise division of labour.

1. The structural terminal-ear route constructs an escape and, by (2), an
   absolute nonzero scalar.  Alternating-cycle surgery supplies a candidate
   shorter common tail.
2. `c3f6231` and `d97bf7a` show that retaining the parent/fine/reinsertion
   mark is sufficient to make the candidate occurrence section monic in the
   derived collision species.
3. `9bbff79` supplies a uniform parent-labelled response carrier and its
   Euler/triangle proper faces.
4. The still missing datum is a pointed **augmented operation-changing**
   linearization carrying those marks and all protected readouts, together
   with an absolute decorated `Eq` contraction—or an exact conservative
   theorem on the physical solution locus which kills the same class.

Under item 4, pure escape normalization becomes genuinely useful: it proves
the landed common-tail channel is nonzero, after which the permanent-triangle
or smaller-core recurrence can run.  Without item 4, normalization certifies
only the total escape and the parent anti-diagonal (4) survives.

This conclusion is sharper than saying that an “occurrence projector is
missing”: the marked projector already exists in the derived species.  What
is absent is its augmented operation-changing descent to the physical source
grade of the structural escape.

## Verification

```text
python3 computations/verify_escape_parent_selector_marked_carrier_comparison.py --mode structural
python3 -O computations/verify_escape_parent_selector_marked_carrier_comparison.py --mode full
python3 -I -S computations/verify_escape_parent_selector_marked_carrier_comparison.py --mode exhaustive
```

All modes have frozen ledger SHA-256
`807dd5cfc370808568bcf52a19442f7dd8c146a33fa8231f53680ebb02c2d86e`.
