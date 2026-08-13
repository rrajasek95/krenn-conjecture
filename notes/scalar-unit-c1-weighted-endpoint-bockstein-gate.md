# The first weighted carrier is canonical upstairs and obstructed by one vertical residue downstairs

## Outcome

The first weighted Hilbert--Cauchy carrier

\[
 H_1=\int_0^1t(q+tr)^{[h-2]},dt
    =\sum_{\ell=0}^{h-2}{1\over\ell+2}
          q^{[h-2-\ell]}r^{[\ell]},                    \tag{1}
\]

is canonically constructed in the **top-suspended** literal response
module for every (h\geq3).  It is not canonically desuspended by applying
(beta)- or Hasse differentiation to the unweighted physical (H_0) lift.

The exact positive top identity is as follows.  For the literal response
path

\[
 S_{jk}(t)=R_{jk}(q+tr)^{[h-1]},                        \tag{2}
\]

Segre factorization and divided-power differentiation give

\[
 S'_{jk}(t)=R_{ja}R_{ak}(q+tr)^{[h-2]}.                \tag{3}
\]

Therefore

\[
 \boxed{
 R_{ja}R_{ak}H_1
   =\int_0^1tS'_{jk}(t)\,dt
   =S_{jk}(1)-\int_0^1S_{jk}(t)\,dt.}                  \tag{4}
\]

This is a literal source-polynomial identity with the four ordered star
roles retained.  No intermediate (q+tr) is asserted to solve the source
equations.

To reach the physical first carrier relation

\[
                         c_1=(r-2q)H_1=0,               \tag{5}
\]

one must desuspend the four star roles through the same common augmented
carrier comparison used for

\[
                         c_0=(r-2q)H_0=0.               \tag{6}
\]

The first unavoidable obstruction is already one-dimensional in the path
direction.  A based loop

\[
                         \eta(t)=t(1-t)                 \tag{7}
\]

fixes both endpoints and the unweighted lift because

\[
 \eta(0)=\eta(1)=0,
 \qquad \int_0^1d\eta=0,                               \tag{8}
\]

but changes the first weighted lift by

\[
                         \int_0^1t\,d\eta=-{1\over6}.   \tag{9}
\]

Hasse differentiation does not remove this ambiguity:

\[
                         D_t\eta=1-2t\ne0.              \tag{10}
\]

Thus two horizontal lifts may have identical endpoints, top response
path, and (H_0) class while differing in (H_1).  The exact missing
physical row is a nullhomotopy of the resulting vertical residue.

## 1. Theorem-shaped first-moment gate

Let (widetilde C^{(4)}_{jk}) be an ordered four-star physical carrier
complex, let

\[
 \pi_{jk}:\widetilde C^{(4)}_{jk}\longrightarrow A_{jk} \tag{11}
\]

be literal star-weighted reinsertion into the top response module, and let

\[
 \chi_{jk}:\widetilde C^{(4)}_{jk}\longrightarrow Q_{h-2} \tag{12}
\]

be a common-carrier desuspension into the physical augmented module.  The
module (Q) includes its protected target, anchor, terminal, and physical
(q)-cocycle rows and permits legal multiplication by (q,r).

> **First weighted endpoint theorem.**  Suppose the (c_0) common-carrier
> comparison is constructed and a polynomial horizontal lift of (3) exists.
> Then the induced (c_1) class is independent of the choice of horizontal
> lift if and only if
>
> \[
> \boxed{
> (r-2q)H(\chi_{jk})\bigl(\ker H(\pi_{jk})\bigr)=0
>                       \quad\text{in }H(Q).}            \tag{13}
> \]
>
> Under (13), weighted integration produces a canonical physical class
> (c_1).  If its source row vanishes, (5) holds.  If (13) fails, the
> failing class has a finite augmented cokernel dual.

Indeed, change a lift by (z,d\eta), with (z) a vertical cycle and
(pi_{jk}(z)=0).  Its first-moment change after desuspension is exactly

\[
 \boxed{
 \mathfrak o_1(z)=-{1\over6}
      \big[(r-2q)\chi_{jk}(z)\big]\in H(Q).}            \tag{14}
\]

Characteristic zero makes (-1/6) a unit, so (14) vanishes for every
allowed (z) exactly when (13) holds.  This proves both directions.

The hypothesis that the (c_0) comparison is already constructed is
load-bearing.  Without it, (chi_{jk}) is not a map into one common
carrier module, multiplication by (r-2q) is not typed, and (14) is only a
formal expression.  Thus the dependency order is

\[
 \boxed{
 \text{primitive/common }H_0\text{ lift}
 \ \Longrightarrow\ c_0\text{ gate}
 \ \Longrightarrow\ \mathfrak o_1\text{ is typed}
 \ \Longrightarrow\ c_1\text{ gate}.}                 \tag{15}
\]

## 2. Exact (h=3) calculation

For (h=3), in the divided-power basis ordered by increasing (r)-degree,

\[
 H_0=q+{1\over2}r,
 \qquad
 H_1={1\over2}q+{1\over3}r,                            \tag{16}
\]

and ordinary multiplication gives

\[
 c_1=(r-2q)H_1
     =-2q^{[2]}-{1\over6}qr+{2\over3}r^{[2]}.          \tag{17}
\]

The first based-loop space is (t(1-t)mathbb K), one-dimensional for
each vertical class (z).  Its residue map is multiplication by (-1/6):

\[
 d(t(1-t))\otimes[z]
       \longmapsto-{1\over6}[(r-2q)\chi(z)].            \tag{18}
\]

Thus there is no smaller path ambiguity to eliminate.  Either the single
class (18) is a physical boundary for every (z), or a primitive dual
survives.

The necessity of this row is also algebraically exact.  With

\[
 u=qr^{[2]}+r^{[3]},
 \qquad x=q^{[3]}+rq^{[2]},                             \tag{19}
\]

one has

\[
 x={7\over20}u+{43\over60}qc_0-{7\over60}rc_0
                              -{8\over5}qc_1,           \tag{20}
\]

whereas

\[
                  x\notin\operatorname {span}
                        \{u,qc_0,rc_0\}.                \tag{21}
\]

So even a successful (c_0) common-carrier lift does not close the
(h=3) moment argument.  The first weighted row (5) is exactly the
additional scalar relation required.

## 3. Uniform loop formula

The same based loop controls the first ambiguity in every order.  For all
(s\geq1),

\[
 \int_0^1t^s\,d(t(1-t))
              =-{s\over(s+1)(s+2)}.                    \tag{22}
\]

In particular, the (c_1) residue remains (-1/6), independently of
(h).  The response degree changes (H_1) through (1), but not the first
vertical path coefficient.

Formula (4) is also uniform in (h).  Therefore the source frontier is not
construction of another target-side moment polynomial; that is already
done.  It is the source-specific vanishing (13), together with the physical
row asserting that the canonical class produced after (13) is zero.

For later moments, higher based Rodrigues loops give a triangular residue
matrix.  None is needed to state the first gate.  At (h=3,4), (H_1) is
the last new moment after (H_0); hence (13) is the only new lift-
indeterminacy theorem needed for those two scalar Hilbert--Cauchy
calculations.

## 4. Finite augmented membership and cokernel criterion

Let

\[
 D_Q:B_Q\longrightarrow Z_Q                              \tag{23}
\]

be the complete physical boundary map in the degree-((h-1)) carrier
grade.  Let (V) be a finite cycle basis for (ker H(pi_{jk})), and let

\[
 L_1=(r-2q)\chi_{jk}|_V:V\longrightarrow Z_Q.           \tag{24}
\]

Then (13) is exactly the finite rank condition

\[
 \boxed{
               \operatorname {rank}D_Q
        =\operatorname {rank}[D_Q\mid L_1].}            \tag{25}
\]

This is the first exact physical obstruction.  If (25) fails, there are
(z\in V) and (lambda\in Z_Q^*) such that

\[
 \lambda D_Q=0,
 \qquad
 \lambda L_1z\ne0.                                     \tag{26}
\]

The covector (lambda) is a physical terminal/Fredholm separator only
when (23) literally contains every protected, anchor, terminal, and
physical-(q) row.  Before that augmentation it is merely the carrier-lift
cokernel dual.  Conversely, when those rows are present, failure of (25)
can be fed directly into the existing generator/separator alternative.

The positive version of (25) can be established in either of two ways:

1. construct explicit physical nullhomotopy columns for every column of
   (L_1); or
2. construct an augmented filtered contraction of the primitive-cap family.
   The homological perturbation formula then gives a canonical transferred
   second differential
   (beta[x]=[D_2x]), and its corrected augmentation guarantees terminal
   zero indeterminacy.

The abstract contraction theorem proves canonicity once the contraction
and physical augmentation exist.  It does not construct them in the
hafnian/endpoint source complex.

## 5. Endpoint-projector interpretation

The centered endpoint projector supplies a coefficient-level occurrence
projector and isolates one missing primitive cap cell whose unweighted
augmentation is the (H_0) base class.  If that cell is enriched to the
common-carrier family required by (15), its first weighted horizontal face
should be represented by (4).

This expectation is not presently a construction.  The committed endpoint
projector is a fixed finite incidence/Čech operator.  It has no affine path
parameter (t), no horizontal density (dt), and no source-proved
contraction killing (14).  Formally differentiating its unweighted output
cannot recover data lost under the based loop (7)--(9).

The smallest positive endpoint theorem is therefore:

> Enrich the primitive cap lift to a polynomial horizontal family whose
> unweighted face is the common (H_0) carrier, whose first weighted face
> has top image (4), and whose vertical residue map (L_1) satisfies
> (25), with the complete physical augmentation.

That one theorem provides (c_0) and types the (c_1) obstruction in the
same family.  A separate source row or filtered contraction is still needed
to make the resulting (c_1) class zero.

## Verification

Run

```text
python3 computations/verify_scalar_unit_c1_weighted_endpoint_bockstein_gate.py
python3 -O computations/verify_scalar_unit_c1_weighted_endpoint_bockstein_gate.py
python3 -I -S computations/verify_scalar_unit_c1_weighted_endpoint_bockstein_gate.py
```

The checker pins the Hermite first-moment obstruction, augmented HPL
Bockstein lemma, (c_0) common-carrier gate, centered endpoint primitive
cap gate, and the independent (h=3) endpoint-projector moment-dependency
audit.  It verifies (1)--(4) for (3\leq h\leq24), the (h=3) constants
(16)--(18), the all-(s) residue (22), and the finite membership/dual
criterion (25)--(26).
