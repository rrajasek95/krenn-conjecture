# The exact six-site binary point cannot be pair-suspended

## 1. Statement

Let

\[
T_m=e_0^{\otimes m}+e_1^{\otimes m}+(e_0+e_1)^{\otimes m}.
\]

Fix on six vertices the exact algebraic source `A` constructed in
[`binary-rank3-projection-counterexample.md`](binary-rank3-projection-counterexample.md),
so that `H_6(A)=T_6`.  Add two vertices `x,y`, retain all fifteen internal
matrices `A_uv`, and allow completely arbitrary binary matrices on `xy` and
on both new stars.

**Theorem 1.1.**  No such eight-site source has matching tensor `T_8`.

Thus the known finite six-site point does not extend by the most general
two-vertex pair suspension.  The theorem imposes no rank, support,
symmetry, or reality condition on the new matrices.  It does not exclude an
eight-site source whose internal six-site restriction is a different
quadratic.

## 2. Every pair-suspension slice lies in one Hessian image

Write `L_A` for the derivative of the six-site matching map at `A`:

\[
 L_A(Z)=\sum_{u<v} Z_{uv}\otimes H_{V\setminus\{u,v\}}(A).
 \tag{1}
\]

Fix external colors `i` at `x` and `j` at `y`.  Denote the corresponding
rows of the two new stars by

\[
 p_u(a)=A_{xu}(i,a),\qquad s_u(a)=A_{yu}(j,a).
\]

Expanding an eight-site perfect matching according to whether it uses
`xy` gives

\[
 H_8(A)_{ij,*}=A_{xy}(i,j)H_6(A)+L_A(Z^{ij}),              \tag{2}
\]

where

\[
 Z^{ij}_{uv}(a,b)=p_u(a)s_v(b)+s_u(a)p_v(b).               \tag{3}
\]

Euler's identity for the cubic map `H_6` says

\[
                         L_A(A)=3H_6(A).                    \tag{4}
\]

Consequently every slice in (2), including the direct-edge contribution,
lies in `im L_A`.

For the desired target, however, the `(i,j)=(0,1)` slice is

\[
                         (T_8)_{01,*}=(e_0+e_1)^{\otimes6}. \tag{5}
\]

It remains to prove that the all-ones coefficient vector in (5) is not in
`im L_A`.

## 3. Exact rank separation

The source field is

\[
 K=\mathbb Q(i,\sqrt3,\sqrt[3]2).
\]

The `64 by 60` matrix of `L_A` has rank exactly `54` over `K`, while
adjoining the vector in (5) raises the rank to `55`.  Here is a short exact
certificate.

There are five universal independent kernel directions.  For vertex
potentials `(r_v)` with `sum_v r_v=0`, put

\[
                         Z_{uv}=(r_u+r_v)A_{uv}.             \tag{6}
\]

Every perfect matching uses every vertex once, so (6) is killed term by
term by `L_A`.

There is a sixth direction from the exact two-parameter family used to
derive `A`.  In the notation of equations (10)--(11) of the six-site note,

\[
 A_{02}=\begin{pmatrix}a&a-c\\c&a\end{pmatrix},\qquad
 A_{13}=\begin{pmatrix}d&d-e\\e&d\end{pmatrix},\qquad
 ad=\kappa,\quad ce=\lambda.                               \tag{7}
\]

Differentiate this exact family with respect to `log a` at `a=c=1` and
generate all edge orbits by the same `C_3` rule.  Since every point of (7)
has output `T_6`, its tangent also lies in `ker L_A`.  These six directions
give

\[
                              \operatorname{rank}_K L_A\le54. \tag{8}
\]

For the reverse inequality and the augmented rank, specialize at the good
prime `109` by

\[
                   i\mapsto33,\qquad \sqrt3\mapsto49,
                   \qquad \sqrt[3]2\mapsto57.              \tag{9}
\]

Indeed `33^2=-1`, `49^2=3`, and `57^3=2` in `F_109`; every denominator in
the displayed six-site source remains invertible.  Exact row reduction gives

\[
 \operatorname{rank}_{\mathbb F_{109}}L_A=54,
 \qquad
 \operatorname{rank}_{\mathbb F_{109}}[L_A\mid\mathbf1]=55,\tag{10}
\]

and the six specialized kernel vectors are independent.  A nonzero minor
after a valid specialization is a nonzero minor over `K`.  Thus the first
rank in (10), together with (8), proves `rank_K L_A=54`; the second proves
that `mathbf1` is outside its image.  Equations (2)--(5) now prove Theorem
1.1. `QED`

## 4. Audit

Run

```text
.venv/bin/python computations/verify_binary_rank3_n6_pair_suspension_obstruction.py
```

The checker reconstructs the exact source after (9), verifies all 64
coefficients of `T_6`, constructs the full `64 by 60` Hessian, checks the
six independent kernel vectors, obtains both ranks in (10), and verifies
Euler's identity (4).  It uses only integer arithmetic modulo `109`.

