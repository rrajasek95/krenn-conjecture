# The one-bad response fibre need not contain a literal coordinate port

## Outcome

The fixed-port cap theorem in `7ccff7c` cannot yet be applied to the arbitrary
one-bad packet by a response-only affine concentration.  For fixed internal
(q) and fixed opposite star rows, the exact replacement problem is an
affine joint-kernel problem.  Its solution fibre can be nonempty while
missing every literal target-coordinate line.

This is the exact obstruction, not anchor preservation.  After the
anchor-safe reduction in `30df1dd`, a newly constructed one-bad source does
not need to preserve the old anchor count.  It only needs to retain


\[
q^{[3]}=X_0,
\qquad
p_i s_jq^{[2]}=\delta_{ij}X_i
\quad(i,j\in\{1,2\}).                                  \tag{1}
\]

The missing theorem must use all five tensors in (1).  The four response
identities considered only as aggregate affine equations do not force the
needed coordinate points.

The exact checker is
`computations/verify_n8_one_bad_affine_coordinate_concentration_guard.py`.

## The affine joint-kernel gate

Put (F=q^{[2]}), fix (s_1,s_2), and define


\[
L_s(v)=(vs_1F,vs_2F).
\]

The two left response rows lie in the affine fibres


\[
\begin{aligned}
\mathcal A_1&=\{v:L_s(v)=(X_1,0)\}
              =p_1+\ker L_s,\\
\mathcal A_2&=\{v:L_s(v)=(0,X_2)\}
              =p_2+\ker L_s.
\end{aligned}                                           \tag{2}
\]

Thus replacing (p_i) while keeping (q,s_1,s_2) fixed is exact if and
only if the difference belongs to the joint kernel.  A literal target port
for row (i) exists precisely when


\[
\mathcal A_i\cap
\bigcup_{u=0}^{5}\mathbb C^*e_i^{(u)}\ne\varnothing.    \tag{3}
\]

After choosing the two left ports, the two right rows obey the analogous
fibres for


\[
M_p(w)=(p_1wF,p_2wF).                                   \tag{4}
\]

Finally, the four candidate-site sets must admit a system of distinct
representatives.  This Hall condition is exactly the “four distinct ports”
input used by the permanent-null cap.

Equations (1) prove only that the four affine fibres are nonempty: the
original multisite rows inhabit them.  Nonempty affine subspaces do not in
general meet a prescribed finite union of coordinate lines.  The physical
guard below shows this failure inside a genuine (F=q^{[2]}), not merely
for an artificial linear map.

## A five-cell physical common-square guard

On residual sites `0,...,5`, take


```text
q = 13:11 + 24:11 + 12:10 - 02:10 + 34:00,
s = e1@5,
p = e1@0 + e1@1.
```

There is no three-edge matching because no (q)-cell meets site 5, so
(q^{[3]}=0).  The two components of (p) give


\[
\begin{aligned}
(e_1^{(0)})s q^{[2]}&=X_1+Y,\\
(e_1^{(1)})s q^{[2]}&=-Y,
\end{aligned}                                           \tag{5}
\]

where


\[
Y=e_1^{(0)}e_1^{(1)}e_0^{(2)}e_0^{(3)}e_0^{(4)}e_1^{(5)}.
\]

The provenance is literal:

- `13:11 * 24:11` gives the (X_1) cofactor with holes `05`;
- `12:10 * 34:00` gives (+Y) with holes `05`;
- `-02:10 * 34:00` gives (-Y) with holes `15`.

Consequently


\[
                         psq^{[2]}=X_1.                 \tag{6}
\]

No individual target-coordinate port has the same response.  The complete
linear map from all eighteen coordinate components of (p) has eleven
nonzero output-word rows and rank nine.  Its augmented target matrix also
has rank nine, so (6) is solvable.  Exactly nine coordinate columns are
zero.  The other nine columns are independent, and none is a nonzero scalar
multiple of (X_1).  Hence the affine fibre has dimension nine, but its
only freedom is along response-zero coordinate columns; the coefficients
of `e1@0` and `e1@1` are both forced to one.  In particular (3) is empty.

This is a cancellation of two different missing-pair contributions to one
physical response tensor.  Deleting either star component exposes the mixed
word (Y), so the proposed specialization is not an exact source
modification.

## Exact scope

The guard is not a one-bad source or a Krenn counterexample.  It has
(q^{[3]}=0), not (X_0), and it includes only one diagonal response colour.
It proves the narrower and load-bearing negative statement:

> common-square provenance plus an exact aggregate pure response does not
> imply that its affine response fibre contains a literal port.

Therefore a theorem completing the concentration route must use the unary
top, the second diagonal response, and both ordered cross-zero responses to
exclude every circuit of the form (5).  If it does so, it must then prove the
four candidate-site sets satisfy Hall.  Neither step follows from anchor
maximality, which is no longer relevant after `30df1dd` anyway.

A simultaneous nonlinear change of all four star rows is not excluded by
this one-sided affine guard.  Such a construction would amount to proving
that the complete fixed-(q) response variety intersects one of the
four-distinct coordinate-port strata, a stronger statement than translating
one row inside a joint kernel.

## Relation to the curvature alternative

For arbitrary multisite rows, the permanent-null matrix still makes the
first insertion (R_Kq^{[2]}=X_1+X_2), but (R_K^{[2]}q) need not vanish.
The guard identifies its source: the same multi-hole cancellation invisible
to the aggregate first response.  This higher term is naturally a second
fundamental form of (q\mapsto q^{[3]}).

The one-bad packet alone does not yet supply the hypotheses of the curved
doubly-good OO gate.  It supplies one physical selected pair and two active
binary responses, but the curved gate also needs a second physical good pair
and a nonzero overlap curvature minor.  Thus “route the defect to curvature”
is a valid alternative target, not an automatic consequence of (1).

## Verification

Run


```bash
uv run python computations/verify_n8_one_bad_affine_coordinate_concentration_guard.py
uv run python -O computations/verify_n8_one_bad_affine_coordinate_concentration_guard.py
```

The frozen ledger digest is


```text
742dfea9c22dfee03112d9b89f8922a144a28eb7e9d39edce7c24041e2093ae0
```
