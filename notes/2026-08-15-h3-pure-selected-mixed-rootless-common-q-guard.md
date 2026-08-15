# The pure words and one mixed word do not force the generic rootless contradiction

## Verdict

In the literal (h=3), six-residual-site EqSystem, the three pure word
matrices and the first mixed word matrix do **not** generate the unit ideal,
even after imposing all of the following generic conditions:

- one common physical (q) and physical endpoint stars (p_i,s_j);
- (q^{[3]}) independent of the three pure target coordinates;
- full endpoint-star ranks ((3,3,6));
- the exact labelled GHZ quotient slices;
- the common direct matrix and the physical relation
  (K_*={\rm tr}(a)E_{01}-a_{01}I);
- activity on the selected line; and
- projective rootlessness of the clean-error cubics.

The checker gives an exact 20-cell rational packet satisfying all 36 scalar
rows at residual words

\[
  000000,\qquad111111,\qquad222222,\qquad010122.
\]

It is only a local guard, not a full exact source: 106 of the remaining 6525
scalar EqSystem rows fail.  The lexicographically first failure is already

\[
  (i,j;w)=(0,0;000011),\qquad {\rm LHS}- {\rm target}=1.
\]

Thus the next contradiction attempt must use at least one additional
mixed/deleted-word equation.  No certificate using only the displayed four
word matrices can be valid under the stated opens.

## The literal packet

All omitted cells are zero.  On residual sites (0,\ldots,5), set

\[
\begin{aligned}
q_{23}^{cc}=q_{45}^{cc}&=1 &&(c=0,1,2),\\
q_{01}^{01}=q_{23}^{01}&=1,\\
p_i(0,i)=s_i(1,i)&=1 &&(i=0,1,2),\\
p_0(2,0)=s_0(3,1)&=1,\\
p_0(4,0)=s_1(5,1)&=-1,\\
a_{00}=a_{01}&=-1.
\end{aligned}
\]

This consists of eight (q)-cells, five (p)-cells, five (s)-cells, and
two direct coefficients.  The three pure rows are immediate: (q^{[3]})
has no pure coordinate, while
(q_{23}^{cc}q_{45}^{cc}=1) and the endpoint cells at sites (0,1) give
the target entry (E_{cc}).  At (w=010122),

\[
 q^{[3]}(w)=1,\qquad C(w)=E_{00}+E_{01},\qquad
 a=-(E_{00}+E_{01}),
\]

so all nine mixed entries vanish exactly.

## Generic-branch and common-power checks

The endpoint stars have ranks ((3,3,6)).  The common cube (q^{[3]}) has
12 nonzero mixed coordinates, no pure coordinate, and

\[
 \operatorname{rank}\langle q^{[3]},X_0,X_1,X_2\rangle=4.
\]

Projection modulo (q^{[3]}) yields the three labelled matrices

\[
 E_{00},\qquad E_{11},\qquad E_{22}.
\]

Consequently every slice has rank one and their left and right factors each
span dimension three; this is the exact labelled GHZ criterion, not merely
coarse target-span containment.

The packet also passes the literal common-power realization audit inherited
from `cd2d0b2`: 1,215 Hessian coordinates, 10,935 first-derivative checks,
65,610 ordered Schreyer checks, and all 6,561 reconstructions of
(p_i s_jq^{[2]}).  Hence the counterguard is built from actual (p,s,q),
not from an independently declared nine-row tensor.

## Direct, activity, and rootlessness

The common direct matrix and its selected scalar-zero response are

\[
a=\begin{pmatrix}-1&-1&0\\0&0&0\\0&0&0\end{pmatrix},\qquad
K_*={\rm tr}(a)E_{01}-a_{01}I=I-E_{01}.
\]

Thus (det K_*=1) and (langle K_*,a\rangle=0).  For the line
(K_z=E_{01}+zI), the activity polynomial is

\[
 z^3(-1-z).
\]

The clean-coordinate family has affine gcd (1), rank four, and its full
degree-two projective Macaulay map has shape (6\times2187) and rank six.
More concretely, the checker selects six word/shift columns

\[
\begin{gathered}
(000001,0),(000001,1),(000001,2),\\
(000100,2),(000101,0),(010001,0),
\end{gathered}
\]

whose exact determinant is (-192).  This is an explicit rational
rootless certificate, rather than a numerical rank assertion.

Both last star cells are load-bearing for rootlessness in this displayed
ansatz: deleting either (p_0(4,0)) or (s_1(5,1)) changes the clean gcd to
(z(z+1)) and drops the projective Macaulay rank from six to four.  This is
not a claim of global 20-cell support minimality.

## Exact scope and next attack

The packet satisfies 6,455 of all 6,561 scalar rows, so it is not a finite
exact GHZ source and does not refute the conjecture.  It proves only that the
natural smallest subsystem—three pure words plus (010122)—survives every
generic, GHZ-slice, common-(q), direct, activity, and rootless condition
listed above.

The shortest next attack is therefore to append the first failed mixed row
((0,0;000011)), then continue by the defect orbit rather than adding more
latent compatibility interfaces.  A successful unit certificate must show
that this additional row (or a symmetry-equivalent deleted-word family)
cannot be repaired while preserving the six-column rootless minor.

## Reproduction

```text
python3 computations/verify_h3_pure_selected_mixed_rootless_common_q_guard.py
python3 -O computations/verify_h3_pure_selected_mixed_rootless_common_q_guard.py
python3 -I computations/verify_h3_pure_selected_mixed_rootless_common_q_guard.py
python3 -S computations/verify_h3_pure_selected_mixed_rootless_common_q_guard.py
python3 -I -S computations/verify_h3_pure_selected_mixed_rootless_common_q_guard.py
python3 -m py_compile computations/verify_h3_pure_selected_mixed_rootless_common_q_guard.py
```

Expected content hash:

```text
d920aad5e4430ddf2e0be7964e7a9e23a3583bf3c8165ef14891dacb052d9666
```
