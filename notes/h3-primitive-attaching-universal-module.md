# The primitive attaches in the Hasse prolongation but not in the physical module

## Outcome

This is the smallest literal module calculation that combines the
denominator-marked four-cube of `ed60e2c`, the full split-cap target and
ordinary-residue columns, and the committed curvature/lower-face candidates.
It gives a split verdict.

Let (I={u,t,e,f}) be the four labelled directions of the selected
four-cube and let (r_0[U],r_m[U]), (U\subseteq I), be the squarefree
Hasse prolongations of the pure and mixed full-nine rows.  In this prolonged
source-labelled module the 17-term chain

\[
 s_I=\sum_{S\subseteq I}(\partial_S H_m)r_0[I\setminus S]
       -(H_0-u)r_m[I]
\]

is closed.  The literal four-polar from `ed60e2c` is
(\partial_IH_m=1), so the only target-carrying term is the genuine source
face (r_0[\varnothing]), with coefficient one.  Therefore

\[
 \boxed{n_A=\kappa(s_I-T)},\qquad
 (d,\operatorname{tgt},\operatorname{ores})(n_A)
   =(\kappa Yw,0,0).                                  \tag{1}
\]

The checker constructs (1) as a linear combination of the 16 labelled
(r_0)-faces, the top (r_m)-face, and the already existing cap column
(T).  There is no declared `n_A` generator.  With the committed bridge
([\mathcal K]=\alpha[A]), (A=16Q_3+\sum m_S), and the cap normalization
(\mathcal K=\kappa Yw), (1) is exactly the requested formal attaching
class.

It does **not** descend to the committed underived physical source module.
That failure has a four-coordinate integral certificate, not merely a
failure of a candidate search.

## The integral physical cokernel

After setting every labelled edge to zero, retain the coordinates

\[
 (E,W,T,R)=( [u e_{\rm Eq}], [Yw],\operatorname{tgt},[Y\operatorname{ores}]).
\]

The complete physical row/cap basis has columns

\[
\begin{array}{c|rrrr}
 &E&W&T&R\\ \hline
 r_0&-1&0&1&0\\
 r_m&0&0&0&0\\
 T&0&-1&1&0\\
 Y\rho&0&1&0&1.
\end{array}                                             \tag{2}
\]

All 60 labelled denominator faces (15 columns times four internal faces)
and their curvature response corrections are literal scalar multiples of
combinations of the columns in (2).  The checker enumerates all of them;
12 are nonzero, with the exact (5,3,3,1) Hasse ladder.  The primitive
integral covector

\[
                 \boxed{\lambda(E,W,T,R)=E+W+T-R}      \tag{3}
\]

kills (2), every one of those 60 lower faces, the diagonal top
(r_0-T=(-1,1,0,0)), and the curvature response
(r_0-T-Y\rho=(-1,0,0,-1)).  It evaluates to one on the desired invisible
boundary

\[
                         K=(0,1,0,0).                  \tag{4}
\]

The three nonzero columns in (2) have rank three and gcd of maximal minors
one.  Adding (4) gives rank four and determinant (\pm1).  Thus (3) is the
primitive free integral cokernel, and no polynomial combination of any
available underived candidate can be (n_A).

The lower Hasse faces in (1) cancel the (E=-1) defect without adding
ordinary residue, so (1) violates (3).  This is precisely why it exists in
the prolonged module and precisely why the diagonal projection is not a
physical comparison: its commutator is ((H_0-u)e_{\rm Eq}).  This agrees
with the all-column descent lock of `6c35854`.

## Scope

Proved here:

- exact module membership for (n_A) in the squarefree four-Hasse
  prolongation, reconstructed from 17 source-labelled face terms;
- exact integral nonmembership in the committed underived physical module,
  including every labelled denominator/lower-face and split-cap candidate;
- compatibility with the already proved bridge
  ([\mathcal K]=\alpha[A]).

Not proved here: a target- and ordinary-residue-preserving comparison from
the prolonged module to a larger, not-yet-constructed physical source
resolution.  Declaring such a comparison would assume the missing theorem.

Run:

```text
.venv/bin/python computations/verify_h3_primitive_attaching_universal_module.py
```
