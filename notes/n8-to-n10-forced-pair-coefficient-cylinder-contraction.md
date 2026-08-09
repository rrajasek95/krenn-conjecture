# An exact N=8 to N=10 contraction for coefficient-cylinder obstructions

## Outcome

The coefficient-cylinder obstruction is not intrinsically N=8.  There is an
explicit matched-pair lift of the anchored source to N=10 and a local
controlled contraction which preserves the full residual, every labelled
old-hole cofactor column, and explicit nonzero affine and bilinear row
functionals.

The lift is deliberately bounded: it adjoins an isolated diagonal matched
pair.  It does not prove that an arbitrary N=10 source contracts to N=8.
Cross-edges incident to the two new vertices remain the precise obstruction
to an induction.

## 1. The pure-anchor-preserving lift

Adjoin vertices 8 and 9 and put only the diagonal source

\[
        g_{89}=E_{89;00}+E_{89;11}+E_{89;22}              \tag{1}
\]

on the new pair.  There are no sources joining either new vertex to an old
vertex.  Every perfect matching is therefore forced to use edge 89, and for
any old source tensor \(X\),

\[
                         X^{+}=X\otimes g.                \tag{2}
\]

In particular, the three pure coefficients of the lifted anchored source
remain \((1,1,1)\).  The lift generally has additional mixed output terms,
so it is a structural test of the cylinder obstruction, not an N=10 Krenn
realization.

Choose a retained old vertex \(a\).  Define the controlled diagonal
contraction

\[
 P_a\bigl(
 e_{i_0}\otimes\cdots\otimes e_{i_{N-1}}
 \otimes e_j\otimes e_k
 \bigr)
 =
 \delta_{j,k}\delta_{j,i_a}
 e_{i_0}\otimes\cdots\otimes e_{i_{N-1}}.                \tag{3}
\]

For every old tensor \(X\), exactly one of the three diagonal summands in
\(g\) agrees with the colour at \(a\).  Hence

\[
                 P_a(X\otimes g)=X,
                 \qquad P_a(\Delta_{N+2,3})=\Delta_{N,3}. \tag{4}
\]

The second identity is what an ordinary fixed-colour contraction lacks.  It
is also why the diagonal lift can retain all three pure anchors while still
contracting the target exactly.

## 2. Contraction of a cut cylinder

For the checked cut \(z=2\),

\[
 C=\{2,6,7\},\quad
 U_8=(0,1,3,4,5),\quad
 U_{10}=U_8\cup\{8,9\},
\]

and the checker uses the retained selector \(a=0\).  Let
\(c^{(N)}_{h,i}\) denote the labelled insertion column with hole \(h\) and
inserted colour \(i\).  Literal matching factorization gives

\[
\begin{aligned}
 P_0(c^{(10)}_{h,i})&=c^{(8)}_{h,i},
      &&h\in U_8,\\
 c^{(10)}_{8,i}=c^{(10)}_{9,i}&=0. &&
\end{aligned}                                             \tag{5}
\]

If \(r_b^{(N)}\) is the full residual row on boundary word \(b\), then (4)
gives

\[
                         P_0(r_b^{(10)})=r_b^{(8)}.        \tag{6}
\]

Equations (5)--(6) hold coefficient by coefficient for affine and bilinear
source parameters.  Thus

\[
 P_0({\cal U}^{(10)}_z)\subseteq{\cal U}^{(8)}_z.          \tag{7}
\]

Every quotient functional \(\ell_8\) annihilating the N=8 coefficient
cylinder therefore lifts to

\[
                         \ell_{10}=\ell_8\circ P_0,        \tag{8}
\]

with exactly the same residual coefficient polynomial.

The same definition works for any old cut: choose any old vertex on its
insertion shore as the controller.  It also iterates when further isolated
diagonal pairs are adjoined.

## 3. An explicit affine functional

Use the rank-one family

\[
                  A+E_{01;01}+tE_{14;01}.                \tag{9}
\]

On cut \(z=2\), boundary row \(b=000\), order the old shore coordinates as
\((0,1,3,4,5)\).  The exact N=8 coefficient-cylinder rank is 17, and the
quotient functional is the two-coordinate difference

\[
                   \ell_8(x)=x_{01000}-x_{00000}.         \tag{10}
\]

It annihilates every constant and linear coefficient slice of all fifteen
labelled insertion columns, while its residual coefficients are

\[
              \bigl(\ell_8(r_{000,0}),
                    \ell_8(r_{000,1})\bigr)=(1,0).        \tag{11}
\]

The lifted functional has the equally local form

\[
             \ell_{10}(x)=x_{0100000}-x_{0000000},        \tag{12}
\]

because both old words in (10) have controller colour zero.  The checker
reconstructs the N=10 source at \(t=0,1,2\), verifies (5)--(6), and obtains
the same nonzero pair \((1,0)\).

## 4. An explicit bilinear functional

For the rank-zero family

\[
                  A+tE_{24;20}+sE_{26;01},               \tag{13}
\]

take boundary row \(b=211\) on the same cut.  The N=8 universal bilinear
coefficient cylinder has rank 14.  The one-coordinate functional

\[
                         \ell_8(x)=x_{00101}              \tag{14}
\]

annihilates all four coefficient slices of all fifteen columns and evaluates
on the residual slices as

\[
                  (1,t,s,ts)\text{-coefficients}
                  =(0,1,0,0).                            \tag{15}
\]

Thus complete cylinder membership forces \(t=0\).  Its lift is simply

\[
                         \ell_{10}(x)=x_{0010100},         \tag{16}
\]

and gives the same coefficient tuple.  The checker verifies all four corners
\((0,0),(1,0),(0,1),(1,1)\) and the extra point \((2,3)\), so (15) is an
exact bilinear identity rather than a parameter sample.

## 5. What this does and does not stabilize

This proves exact stability on a nontrivial N to N+2 tower:

* the lifted source keeps all three pure anchors;
* matching tensors and target residuals contract exactly;
* old-hole coefficient cylinders contract and new-hole columns vanish; and
* explicit affine and bilinear nonzero quotient rows survive unchanged.

The identity is local and order-independent.  Replacing N=8 by any even N in
(1)--(8) changes none of the reasoning.

It is not yet an induction for the conjecture.  A general N+2 source can have
edges from the new pair to old vertices.  Then edge 89 is no longer forced,
the new-hole columns need not vanish, and the image in (7) may acquire terms
outside the old coefficient cylinder.  The next structural question is
therefore sharply defined: prove that the four simultaneous cut conditions
eliminate those cross-edge terms modulo the old cylinder, or exhibit a
cross-edge source for which they survive.

## Reproduction

    python3 computations/verify_n8_to_n10_forced_pair_coefficient_cylinder_contraction.py
    python3 -O computations/verify_n8_to_n10_forced_pair_coefficient_cylinder_contraction.py
    python3 -I computations/verify_n8_to_n10_forced_pair_coefficient_cylinder_contraction.py
    python3 -S computations/verify_n8_to_n10_forced_pair_coefficient_cylinder_contraction.py

The checker uses only exact rational arithmetic and the literal perfect
matching expansion.
