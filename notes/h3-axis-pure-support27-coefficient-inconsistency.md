# The first axis-pure support-27 stratum is coefficient-inconsistent

## Result

The `F0 + K2,2 + K2,4` support isolated by `dbee33d` admits no solution of
the complete coefficient equations.  The strongest contradiction is already
internal to three off-target coefficients on `K2,4`; it needs no target
normalization.

For the canonical representative,

```text
F0 = 01|23|45,
q:11 = K2,2 with bipartition {2,3}|{4,5},
p1,s1 shores = {0,1}.
```

Write the `K2,4` edges as `y_ij=qij:22`, with `i in {0,1}` and
`j in {2,3,4,5}`.  Three actual off-target `q³` equations are nonzero
support multiples of

\[
\begin{aligned}
F_{23}&=y_{02}y_{13}+y_{03}y_{12},\\
F_{24}&=y_{02}y_{14}+y_{04}y_{12},\\
F_{34}&=y_{03}y_{14}+y_{04}y_{13}.
\end{aligned}                                                    \tag{1}
\]

All `y_ij` are nonzero.  The ratios `r_j=y_0j/y_1j` would obey
`r_i=-r_j` for every pair, which any three indices contradict in
characteristic zero.  Equivalently,

\[
y_{14}F_{23}-y_{13}F_{24}+y_{12}F_{34}
                 =2y_{03}y_{12}y_{14}\ne0.             \tag{2}
\]

The literal coefficient equations are

```text
e23=q45:00*F23,  e24=q35:11*F24,  e34=q25:11*F34.
```

Multiplying (2) through gives the denominator-free certificate

\[
\begin{aligned}
&q_{35}^{11}q_{25}^{11}y_{14}e_{23}
-q_{45}^{00}q_{25}^{11}y_{13}e_{24}
+q_{45}^{00}q_{35}^{11}y_{12}e_{34}\\
&\qquad=2q_{45}^{00}q_{35}^{11}q_{25}^{11}
               y_{03}y_{12}y_{14}\ne0.                \tag{3}
\end{aligned}
\]

There is also an independent target-aware certificate.  Put

\[
 Q_1=q_{24}^{11}q_{35}^{11}+q_{25}^{11}q_{34}^{11},
 \qquad
 E_1=p_{1,0}s_{1,1}+p_{1,1}s_{1,0}.                  \tag{4}
\]

The off-target and target equations are

\[
 f_q=q_{01}^{00}Q_1=0,
 \qquad f_t=E_1Q_1-X_1=0,
\]

and satisfy

\[
 \boxed{q_{01}^{00}f_t-E_1f_q=-q_{01}^{00}X_1\ne0}.              \tag{5}
\]

Thus the first support stratum is empty at the coefficient level, and the
axis-pure support lower bound improves to

\[
                         |\operatorname{supp}|\ge 28.            \tag{6}
\]

Checker:

```text
computations/verify_h3_axis_pure_support27_coefficient_inconsistency.py
```

Frozen ledger digest:

```text
7f07fd0b9cfe7deec07920b0078ba6e9dc34573246df3e440dfb977716e2363c
```

## Audit of the complete active system

On the displayed 27-coordinate support, the checker constructs all `3,645`
axis-pure matching monomials in all `849` output fibres.  Exactly `41`
fibres are active:

```text
38 off-target equations, each with two monomials,
3 target equations, with 1, 4, and 24 monomials.
```

It verifies (1)--(5) by sparse polynomial arithmetic.  A further redundant
off-target factorization is

\[
 G_{11}[110000]=q_{23}^{00}q_{45}^{00}E_1=0,           \tag{7}
\]

which separately forces the endpoint permanent to vanish.  The decisive
point is that the target coefficient factors as `E1*Q1`: it uses the same
K2,2 hafnian already killed by the off-target `q³` equation.  This is an
exact consequence of the support geometry, not a generic rank test or a
no-singleton approximation.

## Why one representative suffices

The pinned support theorem proves that the twelve labelled support-27
closures form two site orbits and that the two orbit types exchange under
the bright-colour swap `1<->2`.  Formula (3) is natural under site
permutations.  Bright-colour swap replaces the displayed colour-1 equation
by its colour-2 copy.  Hence every support-27 closure is inconsistent.

This eliminates the need to normalize the literal `F0` coloop at the first
stratum: there is no exact source point to land.  It does not eliminate the
arbitrary-coloop theorem for supports at least 28, where extra coordinates
can break the shared-factor obstruction or produce a larger coupled packet.

## Scope

This is exact for the canonical `h=3` axis-purified five-tensor equations
over a field.  It does not assert emptiness of larger supports or of the
unpurified source locus.

Run normally, optimized, and isolated/no-site.  Expected output:

```text
axis-pure support-27 complete coefficient system: INCONSISTENT
primary certificate: three K2,4 permanents force 2*unit=0
secondary certificate: q01*f_target-E1*f_q=-q01*X1
all 12 closures excluded by site/bright-colour covariance
exact axis-pure support lower bound: >=28
```
