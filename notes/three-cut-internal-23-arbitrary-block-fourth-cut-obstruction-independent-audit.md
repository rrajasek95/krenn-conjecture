# Independent audit: the arbitrary internal-$23$ block obstruction

## 1. Verdict and exact scope

The fixed-interior theorem in
[the primary note](three-cut-internal-23-arbitrary-block-fourth-cut-obstruction.md)
passes a clean-room exact reconstruction.  Retain the eight endpoint-ordered
internal cells

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
01&E_{00}&45&E_{00}&02&E_{11}\\
14&E_{11}&04&E_{22}&13&E_{22}\\
25&E_{00}&35&E_{10},
\end{array}
\]

and let $A_{23}$ be an arbitrary complex $3\times3$ matrix.  With two
arbitrary boundary stars and arbitrary $A_{67}$, the complete quotient
identities for cuts $2,3,4$ cannot also hold for cut $0$, $1$, or
$5$ while the three diagonal target fibres remain units.

The independent checker is
[verify_three_cut_internal_23_arbitrary_block_fourth_cut_obstruction_independent_audit.py](../computations/verify_three_cut_internal_23_arbitrary_block_fourth_cut_obstruction_independent_audit.py).
It imports no project module and, in particular, neither imports nor reads
results from the primary verifier or its full-support and cross-ratio helper
modules.  It freshly enumerates matchings, cylinders, projections, support
charts, shared-star equations, and all characteristic-zero ideals.  No flaw
was found.

This is still a local theorem about the displayed fixed six-site interior.
It does not allow a second internal block to vary, replace the fixed interior,
or by itself prove Krenn's conjecture.

## 2. Independent endpoint-ordered reconstruction

The checker generates perfect matchings by a vertex-bitmask recursion.  For
each matching, a cell $E_{ab}$ on an edge $ij$, $i<j$, assigns $a$ to
site $i$ and $b$ to site $j$.  Thus the nonsymmetric fixed cell
$35:E_{10}$, and every nonsymmetric entry of $A_{23}$, retain literal
endpoint order.

For a six-site coefficient vector $X$, the audit independently builds:

- the full matching tensor $H_S(X)$;
- all fifteen deleted-pair cofactors;
- the fifteen five-site insertion columns and their three cut-colour lifts,
  giving $45$ raw columns for every cylinder $C_z(X)$;
- the boundary-star atom list obtained by inserting every ordered endpoint
  colour into every cofactor.

Projected cylinder intersections are computed directly from column spaces.
The implementation intersects two spans through the coefficient kernel of
$[U\mid -V]$, using exact sparse rational elimination with greatest-word
pivots.  This is a different linear-algebra route from lifting cylinder
annihilators.

As a literal orientation check, all nine entries of $X$, all $108$
entries of the two boundary stars, and all nine entries of $A_{67}$ receive
distinct nonzero rational values.  Direct enumeration of the complete
eight-site matching tensor agrees on all nine boundary-colour slices with

\[
\begin{aligned}
 H_{ab}={}&r_{ab}H_S(X)+\beta_X(p^a,q^b),\\
 \beta_X(p,q)={}&\sum_{i<j}\sum_{c,d}
 \left(p_{i,c}q_{j,d}+p_{j,d}q_{i,c}\right)
 e_c^{(i)}e_d^{(j)}\otimes H_{S\setminus\{i,j\}}(X).
\end{aligned}                                                    \tag{A1}
\]

This simultaneously checks both endpoint attachments, reuse of the same
star entries in diagonal and ordered cross fibres, and the direct $67$
block.

## 3. The $480$ support masks and the torus charts

Order the nine entries of $X$ row-major and the four cells outside the old
five-cell locus as

\[
                         x_{10},x_{12},x_{20},x_{22}.       \tag{A2}
\]

Classifying a support by its first nonzero cell in (A2) gives, by exhaustive
bit enumeration,

\[
                           256+128+64+32=480.               \tag{A3}
\]

The independently reconstructed stabilizing torus has exponent rows, in
coordinates $(r_0,r_1,r_2,c_0,c_2)$,

\[
\begin{array}{c|ccc}
 &0&1&2\\ \hline
0&(1,0,0,1,0)&(2,0,0,0,0)&(1,0,0,0,1)\\
1&(0,1,0,1,0)&(1,1,0,0,0)&(0,1,0,0,1)\\
2&(0,0,1,1,0)&(1,0,1,0,0)&(0,0,1,0,1).
\end{array}                                                 \tag{A4}
\]

Every finite retained support below has full row rank.  An integer
full-row-rank monomial map is surjective on complex points because all
required roots exist in $\mathbb C^*$, so its retained nonzero coefficients
can be normalized to one.  Extending the torus to sites $6,7$ makes the
total exponent in each monochromatic target zero; boundary entries are only
rescaled by nonzero factors and remain arbitrary.

The four quotient charts are

\[
\begin{array}{c|c|c|c}
\text{first cell}&\text{earlier forced zeros}&\text{coordinate blocks retained}
 &\dim\overline N_{0,1,5}\\ \hline
x_{10}&-&10,11,21,22&2\\
x_{12}&10&12,11,21,22&1\\
x_{20}&10,12&10,20,11,21,22&2\\
x_{22}&10,12,20&10,12,20,11,21,22&1.
\end{array}                                                 \tag{A5}
\]

Retaining a forced-zero block preserves fixed cofactor equations; it does
not insert a variable term.  Optional presence of $x_{11},x_{21},x_{22}$
is recorded by

\[
d=2{\bf1}_{x_{11}\ne0}+4{\bf1}_{x_{22}\ne0},\qquad
b={\bf1}_{x_{21}\ne0}.                                    \tag{A6}
\]

This yields $8+7+8+4=27$ finite chart families.  The sole dependent
retained support is the $x_{12}$ rectangle

\[
                       \{x_{11},x_{12},x_{21},x_{22}\}.    \tag{A7}
\]

Its four weight rows have rank three and their primitive relation is

\[
 \operatorname{wt}(x_{12})+\operatorname{wt}(x_{21})
 =\operatorname{wt}(x_{11})+\operatorname{wt}(x_{22}).     \tag{A8}
\]

The three rows for $x_{12},x_{11},x_{22}$ are independent, so the gauge

\[
                 x_{12}=x_{11}=x_{22}=1,\qquad x_{21}=\lambda \tag{A9}
\]

is valid and $\lambda=x_{12}x_{21}/(x_{11}x_{22})$ is exactly the one
surviving invariant.  Sixteen of the $480$ masks lie in this rectangle
family; the other four bits are killed by its projection.

## 4. Nine disjoint coordinate blocks and safe projection

Only cofactors for deleted pairs $01,05,15,45$ can use edge $23$.  For
each cell $e=(a,b)$, the audit inserts all nine endpoint-colour choices
into the cell-dependent part of these four cofactors.  The resulting word
set $R_e$ satisfies

\[
 |R_e|=35,\qquad R_e\cap R_f=\varnothing\quad(e\ne f),\qquad
 \left|\bigcup_eR_e\right|=315.                            \tag{A10}
\]

It also reconstructs

\[
 [0^6]\in R_{00},\qquad[1^6]\in R_{11},\qquad[2^6]\in R_{22}, \tag{A11}
\]

with no pure target in any other block.

For each chart, the quotient kills $R_e$ for cells outside the retained
set in (A5).  The checker verifies coefficient by coefficient that adding
any killed cell changes only killed coordinates in:

- $H_S(X)$;
- every boundary-star atom;
- each of the $45$ raw columns of every one of the six cylinders.

Because edge $23$ occurs at most once in a matching, these differences are
linear in every killed coefficient.  The termwise calculation therefore
covers arbitrary complex values, rather than only the sampled zero/one
supports.

The checker additionally visits every one of the $480$ masks and compares
its projected tensor, atom dictionary, and all $270$ raw cylinder columns
with the representative of its chart family.  Every comparison is exact.

For an actual common normal

\[
 N_z=C_2\cap C_3\cap C_4\cap C_z,
\]

the proof uses only the universally valid relaxation

\[
 \pi N_z\subseteq
 \pi C_2\cap\pi C_3\cap\pi C_4\cap\pi C_z
 =:\overline N_z.                                         \tag{A12}
\]

No commutation of projection and intersection is assumed.  The right side
of (A12) is what the independent column-kernel calculation reconstructs.

## 5. Finite projected normals and the cross-ratio lock

For each of the $27$ finite families, the audit independently forms the
four projected cylinder spans.  For $z=0,1,5$, their intersections have
the dimensions shown in (A5), are equal as subspaces, and contain the
projected $H_S(X)$.  Thus every direct term $r_{ab}H_S(X)$, with
$r_{ab}$ arbitrary, is absorbed.  Both retained targets $[1^6]$ and
$[2^6]$ survive the quotient and lie outside the reconstructed normal.

The cross-ratio family is checked uniformly.  Since every cylinder column
is affine in $\lambda$, let $\widehat C_z$ be the span of its columns at
$\lambda=0$ and $\lambda=1$.  The audit also evaluates at $\lambda=2$
and verifies the affine interpolation term by term.  For each
$z=0,1,5$, an independent four-span intersection gives

\[
 \widehat C_2\cap\widehat C_3\cap\widehat C_4\cap\widehat C_z
 =P=\langle e,v\rangle,                                   \tag{A13}
\]

where

\[
\begin{aligned}
 e={}&[002100],\\
 v={}&[121200]+[001100]+[001200]+[002200]+[111110].
\end{aligned}                                              \tag{A14}
\]

For every one of the $45$ raw columns of $C_z(\lambda)$, $z=0,1,5$,
the independent checker verifies that the constant, linear, and quadratic
coefficients of

\[
 \bigl([002100]^*-\lambda[001100]^*\bigr)C_z(\lambda)       \tag{A15}
\]

all vanish.  If $w=\alpha e+\beta v$ belongs to the actual projected
four-cylinder intersection, (A15) gives $\alpha-\lambda\beta=0$.  Hence

\[
                       \pi N_z(\lambda)
                       \subseteq\langle v+\lambda e\rangle. \tag{A16}
\]

Direct matching enumeration gives
$\pi H_S(\lambda)=v+\lambda e$, so this is also precisely the line that
absorbs arbitrary $A_{67}$.  The argument includes every complex value of
$\lambda$, not merely generic values.

## 6. Shared-star fibre equations

The full system has $108$ star entries:
$p^a_{i,c}$ and $q^b_{i,c}$, with $a,b,c\in\{0,1,2\}$ and
$0\le i<6$.  Projecting a hypothetical solution and enlarging its normal
by (A12) gives the necessary equations

\[
 \pi\beta_X(p^a,q^b)-\delta_{ab}\pi[a^6]\in\overline N_z. \tag{A17}
\]

The contradiction retains the ordered packet

\[
                          (a,b)=(1,1),(1,2),(2,1),(2,2).    \tag{A18}
\]

These four fibres use the same $72$ variables
$p^1,p^2,q^1,q^2$: the two diagonal targets have coefficient one, and
both ordered off-diagonal targets are zero.  Any solution of the complete
nine-fibre, $108$-variable system restricts to (A18), so inconsistency of
this packet is sufficient.  No star monomial is freed independently.

## 7. Independent characteristic-zero certificates

For every finite chart family, the checker constructs the annihilator of
the exact projected normal and substitutes the four shared fibres (A18).
It then generates a fresh Singular program over $\mathbb Q$, using reversed
star-variable order.  The generator counts and reduced standard bases are

\[
\begin{array}{c|c|c}
\text{family}&(d,b)&\text{generator counts}\\ \hline
x_{10}&
(0,0),(0,1),(2,0),(2,1),(4,0),(4,1),(6,0),(6,1)&
328,432,412,516,440,544,524,628\\
x_{12}&
(0,0),(0,1),(2,0),(2,1),(4,0),(4,1),(6,0)&
332,436,416,520,444,548,528\\
x_{20}&
(0,0),(0,1),(2,0),(2,1),(4,0),(4,1),(6,0),(6,1)&
356,460,440,544,468,572,552,656\\
x_{22}&
(4,0),(4,1),(6,0),(6,1)&
384,488,468,572.
\end{array}                                                \tag{A19}
\]

All $27$ reduced standard bases are $[1]$.

For the rectangle (A9), the audit derives atom coefficients independently
from their values at $\lambda=0,1$, verifies the affine law at
$\lambda=2$, and imposes membership in the exact line (A16) by pivoting on
$[121200]$.  This produces $628$ generators in

\[
                   \mathbb Q[\lambda,p^1,p^2,q^1,q^2].     \tag{A20}
\]

Here $\lambda$ is an ordinary ring variable, not a generic coefficient or
an inverted parameter.  Its reduced standard basis is again $[1]$.  Thus
there is no exceptional complex cross-ratio value.  Extending scalars from
$\mathbb Q$ to $\mathbb C$ preserves every unit ideal.

## 8. Reproduction

From the repository root:

```text
.venv/bin/python computations/verify_three_cut_internal_23_arbitrary_block_fourth_cut_obstruction_independent_audit.py
```

The clean run on 2026-07-27 ended with

```text
independent arbitrary-A23 fixed-interior audit: PASS
480 masks partitioned 256+128+64+32; 27 finite charts + lambda: PASS
nine disjoint 35-coordinate blocks; killed terms vanish coefficientwise: PASS
projected cut-0/1/5 intersections and x12 Q[lambda] line lock: PASS
endpoint order, 108 shared-star entries, ordered four-fibre packet, A67: PASS
...
x12_crossratio_lambda: 628 generators, exact-Q[lambda] unit (41.372s): PASS
independent audit wall time: 137.989s
```

Python byte-compilation also passes.  The $28$ Singular jobs are run in a
bounded parallel pool; their individual timings therefore do not add to the
wall time.

## 9. Conclusion and scope boundary

The $480$ outside-locus masks are exhausted without assuming bounded
coefficients or generic parameters.  Combining this audit with the existing
independent five-cell audit covers all $512$ supports of an arbitrary
complex $3\times3$ block $A_{23}$, with the other eight internal cells
fixed as displayed.

The next local escape must change at least one additional internal block or
replace the fixed six-site interior.  This conclusion must not be promoted to
an unrestricted six-site obstruction, a dimension-drop theorem, or a proof of
the global conjecture without a separate argument.
