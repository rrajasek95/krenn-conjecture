# An order-five lower-face correction repairs the residual-(q) commutator

The covariance--curvature symbol from `52d5baa` is not merely a formal
four-corner pattern.  It admits an exact generator-level completion by
linear-coefficient order-five operators.

## The two source generators

Let

\[
 A_0=H_{11111111},\qquad A_1=H_{11211211}
\]

be the two complete direct-free rows, each with 90 matching monomials.  Let
(D_4) be the signed fourth operator with corner coefficients
((-1,1,1,-1)).  The previous theorem gives

\[
                         D_4A_0=D_4A_1=0,              \tag{1}
\]

and identifies its first surviving Hasse face with (-delta).  But (D_4)
does not preserve the pair-generator relations by itself:

\[
\begin{array}{c|ccc}
G&A_0^2&A_0A_1&A_1^2\\\hline
|\operatorname {supp}D_4G|&60&96&60.
\end{array}                                             \tag{2}
\]

## Complete order-five system

Consider every operator

\[
                         x\,\partial_T,\qquad |T|=5,   \tag{3}
\]

where (x) is linear and (3) has total site-degree shift (-1^8).  Across
the three pair generators there are exactly

```text
40 ring variables,
31,008 distinct operator columns,
1,080 literal output coordinates,
12 complete source-word blocks.
```

The exact rational rank is 706, and adjoining the negative of (2) leaves the
rank 706.  A deterministic echelon choice gives a rational correction
(D_5) with 248 nonzero terms.  It uses no source-ideal quotient columns:
the cancellation is literal.  Exactly,

\[
 \boxed{
 (D_4+D_5)(A_0^2)=
 (D_4+D_5)(A_0A_1)=
 (D_4+D_5)(A_1^2)=0.}                                  \tag{4}
\]

Every fifth derivative kills the quartics (A_0,A_1), so (1) remains true
for (D=D_4+D_5).  In particular, the order-five repair does not alter the
proved (-delta) fourth symbol.

The fine grading is exact as well.  The 248 terms split as

```text
pure-tail commutator shift:   111,
mixed-tail commutator shift:  137,
all other shifts:               0.
```

Thus solvability does not come from leaking into unrelated colour grades.

## The remaining terminal is genuinely relative

Every cell used by the repair has colours 1 or 2; none has colour zero.
Moreover, no cell incident with the marked (p/x) sites uses colour 2.
Consequently the natural action of the five colour-zero stabilizers
(eta_z) on this source repair is zero, as is the relevant
(sigma_{p,2}-sigma_{x,2}) response.

This separates the remaining issue cleanly.  The source homotopy is now
constructed, while the desired terminal values are formally carried by the
(t-u_v) eta primitive and the (-q_{pq}^{22}) sigma face.  What remains is
one **relative fiber-product comparison** placing those terminal corrections
on this source lift in the same physical repeated grade.  They cannot be
read off from the source operator's ordinary stabilizer character.

## Meaning for the proof

Equation (4) is precisely the pair-generator compatibility required by the
(R)-linear Hasse convention: the differential acts on the free source
generators, not on arbitrary polynomial coefficients.  It proves that the
literal private-boundary obstruction is not an impossibility at this level;
the signed commutator has a complete lower-face repair.

This is not yet the physical cell (M_v).  Three interfaces remain:

1. identify the 248-term correction with a chain in the labelled repeated
   (P_3\sqcup K_2) physical relative source complex;
2. glue that chain to the known eta and sigma terminal corrections through
   a physically typed relative comparison; and
3. separately prove transverse rank landing after the conditional endpoint
   holonomy theorem.

Nor does (4) assert the stronger coefficient-prolonging condition
(D(I^2)\subset I) for arbitrary multipliers.  That ideal-level condition
contains additional Leibniz layers and is not needed by the pinned
(R)-linear generator totalization.

Verification:

```text
python3 computations/verify_h3_residual_q_order5_generator_repair.py
python3 -O computations/verify_h3_residual_q_order5_generator_repair.py
python3 -I -S computations/verify_h3_residual_q_order5_generator_repair.py
```

Frozen ledger SHA-256:

```text
b6a24e76e44d18ab2135b1e1198b3473a24759b215a37f7186331d0455ef647b
```
