# One two-term colour component still has no common-power lift

## 1. Result

Let \(U\) be a six-set, and at every site \(u\) let \(V_u\) contain three
distinguished independent vectors

\[
 e_0^{(u)},e_1^{(u)},e_2^{(u)}.
\]

For a pair \(P\subset U\) and a colour \(i\), write

\[
 E_i(P)=\bigotimes_{u\notin P}e_i^{(u)},
 \qquad X_i=\bigotimes_{u\in U}e_i^{(u)}.
\]

Choose pairs \(A,B,C,D\), assuming initially only that \(A\ne B\), and
choose four nonzero complex numbers \(\alpha,\beta,\gamma,\delta\).  Thus
\(C,D\) may initially coincide with each other or with \(A,B\).  Put

\[
 F=\alpha E_0(A)+\beta E_0(B)+\gamma E_1(C)+\delta E_2(D).       \tag{1}
\]

The star rows

\[
 p_0,p_1,p_2,s_0,s_1,s_2\in\bigoplus_{u\in U}V_u
\]

are completely arbitrary: they can meet several sites, contain directions
outside the displayed three-dimensional spaces, vanish in some components,
and use arbitrary complex cancellation.  Retain all nine exact products

\[
                       p_i s_jF=\delta_{ij}X_i.          \tag{2}
\]

**Theorem 1.1 (one-multiterm obstruction).**  Under (1)--(2), there is no
six-site quadratic \(q\) for which

\[
                       q^{[2]}=F,\qquad q^{[3]}=0.       \tag{3}
\]

Here bracket powers are unordered matching sums.  The proof first shows by
hand that (2) forces all four missing pairs \(A,B,C,D\) to be distinct.  It
then becomes stronger than the stated theorem: for every four distinct
pairs, (1) and (3) alone are inconsistent.  This common-power assertion is
certified by 25 unsaturated affine unit ideals, one for each exact support
orbit.

The standalone checker
[`verify_one_multiterm_common_power_obstruction.py`](../computations/verify_one_multiterm_common_power_obstruction.py)
enumerates all \(16{,}380\) labelled supports, audits the complete linear
kernel of \(qF=0\), constructs every coefficient of \(q^{[2]}-F\), freezes
the generator ledgers, and obtains the unit basis \([1]\) over
\(\mathbb Q\) in all 25 cases.

## 2. Literal products force four distinct pairs

Work in the site-square-zero algebra

\[
 \mathcal R_U=\bigotimes_{u\in U}(\mathbb C\oplus V_u),
 \qquad V_uV_u=0.                                      \tag{4}
\]

For \(P=\{a,b\}\), multiplication of \(p_i s_j\) by \(E_k(P)\) retains
exactly the two endpoint orders

\[
 B_{ij}(P)=p_{i,a}\otimes s_{j,b}
             +s_{j,a}\otimes p_{i,b}\in V_a\otimes V_b. \tag{5}
\]

Thus no orientation of a physical pair has been selected or discarded.  Let

\[
 W_k(P)=\left(\bigotimes_{u\in P}V_u\right)
          \otimes\left(\bigotimes_{u\notin P}\mathbb C e_k^{(u)}\right)
\]

inside the full-support component of (4).  If \(k\ne l\), then

\[
                         W_k(P)\cap W_l(Q)=0            \tag{6}
\]

for any pairs \(P,Q\): at least two sites lie outside \(P\cup Q\), and at
each such site the two coordinate factors are distinct.  More precisely,
each \(W_k(P)\) is spanned by a set of coordinate words, and these word sets
are disjoint for distinct colours.  Hence the coordinate-word supports of
the entire colour-zero sum \(W_0(A)+W_0(B)\), the colour-one term
\(W_1(C)\), and the colour-two term \(W_2(D)\) are mutually disjoint; there
is no three-subspace cancellation hidden behind (6).  For two distinct
pairs of the same colour,

\[
 W_0(A)\cap W_0(B)=
 \begin{cases}
   \mathbb C X_0,&A\cap B=\varnothing,\\
   V_x\otimes\displaystyle\bigotimes_{u\ne x}\mathbb C e_0^{(u)},
      &A\cap B=\{x\}.
 \end{cases}                                           \tag{7}
\]

Apply (2) with \((i,j)=(1,1)\), and separate the three colour-support
spaces using (6).  The colour-one equation says

\[
 B_{11}(C)=\gamma^{-1}e_1^{(a)}\otimes e_1^{(b)}
 \quad(C=\{a,b\}),                                     \tag{8}
\]

whereas the colour-two response at \(D\) is zero.  If \(C=D\), the same
literal tensor \(B_{11}(C)\) is therefore both nonzero and zero, a
contradiction.

The colour-zero part of the same row is

\[
 \alpha\,\iota_A B_{11}(A)+\beta\,\iota_B B_{11}(B)=0, \tag{9}
\]

where \(\iota_P\) inserts the fixed colour-zero factors outside \(P\).
If \(C=A\), equation (9) puts \(\iota_A B_{11}(C)\) in the intersection
(7).  Because \(A\ne B\), there is a site of \(A\setminus B\); (7) forces
the factor there to lie on the \(e_0\)-axis, while (8) puts it on the
distinct \(e_1\)-axis.  This is impossible.  The case \(C=B\) is identical.
Applying the same argument to row \((2,2)\) proves that \(D\) differs from
\(A,B,C\).  Hence

\[
                         A,B,C,D\text{ are all distinct}. \tag{10}
\]

This argument used the full two-order response (5), arbitrary multi-site
rows, and all possible cancellation between the two colour-zero lifts.

## 3. Three-dimensional reduction and exact weight normalization

Choose at each site a linear projection

\[
 V_u\longrightarrow
 \langle e_0^{(u)},e_1^{(u)},e_2^{(u)}\rangle
\]

which fixes the three displayed axes.  Together with the identity on the
scalar summands, these maps induce an algebra homomorphism of (4).  A
solution of (3) in larger local spaces would project to a solution with
three-dimensional local spaces and the same target.  It is therefore
lossless to use exactly three local coordinates in the calculation.

The four nonzero weights can also be removed without changing the exact
right side of (2).  Scale each axis independently by

\[
                         e_i^{(u)}\longmapsto t_{i,u}e_i^{(u)},
 \qquad t_{i,u}\in\mathbb C^*,                         \tag{11}
\]

and require \(\prod_{u\in U}t_{i,u}=1\), so every \(X_i\) is fixed.  A
coefficient \(\lambda E_i(P)\) becomes

\[
 \lambda\prod_{u\notin P}t_{i,u}E_i(P)
       ={\lambda\over\prod_{u\in P}t_{i,u}}E_i(P).    \tag{12}
\]

For colours one and two, prescribe respectively

\[
 \prod_{u\in C}t_{1,u}=\gamma,\qquad
 \prod_{u\in D}t_{2,u}=\delta,
\]

then use any site outside the relevant pair to make the total product one.
For colour zero prescribe

\[
 \prod_{u\in A}t_{0,u}=\alpha,\qquad
 \prod_{u\in B}t_{0,u}=\beta.                         \tag{13}
\]

If \(A,B\) meet, assign the two unique endpoints the values
\(\alpha,\beta\); if they are disjoint, assign one endpoint in each pair
those values.  In either case at least one remaining site can correct the
total product to one.  Thus (11) is a target-preserving algebra
automorphism taking all four coefficients in (1) to one.  It carries
\(p_i,s_j,q\) with it, preserves (2), and commutes with bracket powers.
No root extraction or generic coefficient assumption is involved.

From now on all four target coefficients equal one.

## 4. The complete linear consequence of the third power

For unordered matching powers,

\[
                         q q^{[2]}=3q^{[3]},             \tag{14}
\]

because every three-edge matching has three choices of distinguished edge.
Equations (3) therefore imply

\[
                              qF=0.                     \tag{15}
\]

Only \(q_P\) can multiply \(E_i(P)\) without repeating a site.  Separation
of the colour-one and colour-two response spaces gives

\[
                              q_C=q_D=0.                \tag{16}
\]

The two colour-zero terms can cancel, but (7) gives their full kernel.  If
\(A\cap B=\varnothing\), then for one scalar \(z\),

\[
 q_A=z\,e_0^{\otimes A},\qquad
 q_B=-z\,e_0^{\otimes B}.                             \tag{17}
\]

If \(A\cap B=\{x\}\), write \(A=\{x,a\}\) and
\(B=\{x,b\}\).  For one arbitrary \(v\in V_x\),

\[
 q_A=v\otimes e_0^{(a)},\qquad
 q_B=-v\otimes e_0^{(b)},                              \tag{18}
\]

with the factors reordered into their named sites.  Every other edge block
of \(q\) is free.  Consequently the kernel of (15) has dimension \(100\)
in the disjoint case and \(102\) in the adjacent case, out of the 135 edge
coordinates.  The checker independently constructs the full coefficient
matrix of \(qF\), obtains ranks \(35\) and \(33\), and verifies that
(17)--(18) are bases of the respective kernels.  The subsequent ideals
therefore omit no solution of the third-power equation.

## 5. Exhaustive support and affine-ideal certificate

There are 15 pairs on six labelled sites.  Treat \(A,B\) as an unordered
pair of same-colour summands, and retain the order of \(C,D\) until the
final symmetry which simultaneously swaps colours one and two.  Equation
(10) leaves exactly

\[
                         \binom{15}{2}\,13\,12=16{,}380 \tag{19}
\]

labelled supports.  Quotienting by \(S_6\), by \(A\leftrightarrow B\), and
by the simultaneous \(C\leftrightarrow D,\ 1\leftrightarrow2\) symmetry
gives the following 25 disjoint orbits.  An edge \(\{a,b\}\) is abbreviated
to \(ab\).

| no. | \((A,B;C,D)\) | orbit size | variables | equations |
|---:|---|---:|---:|---:|
| 1 | `(01,02;03,04)` | 360 | 102 | 1035 |
| 2 | `(01,02;03,12)` | 360 | 102 | 1107 |
| 3 | `(01,02;03,13)` | 720 | 102 | 1053 |
| 4 | `(01,02;03,14)` | 1440 | 102 | 1179 |
| 5 | `(01,02;03,34)` | 720 | 102 | 1179 |
| 6 | `(01,02;03,45)` | 360 | 102 | 1180 |
| 7 | `(01,02;12,13)` | 720 | 102 | 1089 |
| 8 | `(01,02;12,34)` | 360 | 102 | 1108 |
| 9 | `(01,02;13,14)` | 720 | 102 | 1161 |
| 10 | `(01,02;13,23)` | 360 | 102 | 1215 |
| 11 | `(01,02;13,24)` | 720 | 102 | 1215 |
| 12 | `(01,02;13,34)` | 1440 | 102 | 1215 |
| 13 | `(01,02;13,45)` | 720 | 102 | 1215 |
| 14 | `(01,02;34,35)` | 360 | 102 | 1215 |
| 15 | `(01,23;02,03)` | 360 | 100 | 991 |
| 16 | `(01,23;02,04)` | 1440 | 100 | 1143 |
| 17 | `(01,23;02,13)` | 180 | 100 | 1215 |
| 18 | `(01,23;02,14)` | 1440 | 100 | 1215 |
| 19 | `(01,23;02,45)` | 360 | 100 | 1215 |
| 20 | `(01,23;04,05)` | 360 | 100 | 1143 |
| 21 | `(01,23;04,14)` | 360 | 100 | 999 |
| 22 | `(01,23;04,15)` | 360 | 100 | 1215 |
| 23 | `(01,23;04,24)` | 720 | 100 | 1215 |
| 24 | `(01,23;04,25)` | 720 | 100 | 1215 |
| 25 | `(01,23;04,45)` | 720 | 100 | 1215 |

The orbit sizes sum to \(16{,}380\).  The ordered representative-and-size
ledger has SHA-256

```text
32415c6354cbfeb6626f2a3692e90c935ce8ebc4a3a3cd5e913e2c110658e7a5
```

For each representative, substitute the complete kernel (16)--(18).  For
every four-set \(S=\{u_0,u_1,u_2,u_3\}\) and every ordered local colour word
\(c\in\{0,1,2\}^S\), the checker inserts the literal coefficient

\[
\begin{aligned}
 &(q_{u_0u_1})_{c_0c_1}(q_{u_2u_3})_{c_2c_3}
 +(q_{u_0u_2})_{c_0c_2}(q_{u_1u_3})_{c_1c_3}\\
 &\hspace{35mm}
 +(q_{u_0u_3})_{c_0c_3}(q_{u_1u_2})_{c_1c_2}
 -[F]_{S,c}.                                           \tag{20}
\end{aligned}
\]

Endpoint order is retained by the convention
\((q_{vu})_{ba}=(q_{uv})_{ab}\).  Formula (20) is every coefficient of
\(q^{[2]}-F\), not a selected projection.  The resulting ideals are the
full affine ideals in 100 or 102 variables over \(\mathbb Q\).  They use no
saturation, no auxiliary inverse, no nonzero declaration, and no division
by an unknown.  Singular returns the unit basis \([1]\) in all 25
cases.  Hence their complex zero sets are empty, including all degenerate
and cancellation strata.

The 25 individual ordered-generator hashes are frozen in the checker.  The
hash of the ordered orbit/support/hash ledger is

```text
5dee107cd6f6d278c54b796b8e3a70025a8916a057e5a448e051f34cf0904a11
```

Running with `--certificate --orbit N` additionally asks Singular for an
explicit lift of \(1\) through the original generator list and prints every
used labelled coefficient equation.  Thus the unit conclusions can be
expanded into direct polynomial identities without changing the ideals.
Together with Sections 2--4, the 25 unit certificates prove Theorem 1.1.

## 6. Exact scope and next enlargement

This theorem permits arbitrary complex nonzero coefficients, arbitrary
multi-site star rows, arbitrary endpoint order, arbitrary local dimensions,
and arbitrary cancellation.  Its restrictive hypothesis is the exact
four-term shape (1): one colour has exactly two distinct pure four-site
monomials, and each of the other two colours has exactly one.

It does not cover a third colour-zero monomial, two simultaneous
multi-monomial colour components, non-pure four-site tensors, or a general
cyclic/diagonal direct-block solution.  It is therefore not a global proof
of the six-site descent or of Krenn's conjecture.  The next bounded support
frontiers are the multiplicity profiles \((3,1,1)\) and \((2,2,1)\).  In
those profiles, (15) no longer has only the two-pair kernels (17)--(18): its
single-transverse equations become a genuine signed incidence system among
all same-colour missing pairs, and that incidence kernel should be solved
before any second-power ideals are formed.
