# The Interface-II survivor is an occurrence-normalization problem

## Exact verdict

At a unary-compatible trapped source, let

\[
 f=p_1[0,1]s_1[1,1]q_{23}[0,0]q_{45}[0,0]\ne0
\]

be the marked occurrence in response coefficient `11:110000`, and let
\(H=d_{p,q}f\) with the right endpoint row `s_1` fixed, as in `dac1248`.
The mixed target coefficient is zero, so its literal physical equation is

\[
 R_{11,110000}=f+G=0,                                  \tag{1}
\]

where `G` is the sum of the other 89 endpoint/matching occurrences.

Homogeneity, target normalization, and the physical diagonal Euler/Hasse
action do **not** exclude

\[
 \Lambda\in\operatorname {row}(A),\qquad
 H\notin\operatorname {row}(A).                       \tag{2}
\]

They expose the first missing datum sharply: either prove infinitesimal
occurrence rigidity \(df(T_xS)=0\) on the actual fixed-right source fibre,
or add a genuinely occurrence-labelled, target-corrected relative cell.

Checker:
[`verify_h3_trapped_carrier_occurrence_euler_source_gate.py`](../computations/verify_h3_trapped_carrier_occurrence_euler_source_gate.py).

## 1. Why physical Euler cannot select the occurrence

The coefficient `R_11,110000` contains exactly

```text
6 choices of the p site * 5 choices of the s site * 3 residual matchings
= 90 literal occurrences.
```

Every one covers every residual site exactly once, with colour prescribed
by the same output word `110000`.  Therefore all 90 monomials have the same
site/colour incidence vector.  For a colour-diagonal target stabilizer
\(\lambda=(\lambda_{u,a})\),

\[
 \sum_u\lambda_{u,a}=0\quad(a=0,1,2),                 \tag{3}
\]

the induced Euler field satisfies the polynomial identity

\[
 L_\lambda R_{11,110000}
   =\left(\sum_u\lambda_{u,w_u}\right)R_{11,110000}.  \tag{4}
\]

Every iterated diagonal Euler/Hasse operator has the same property.  It
acts on the aggregate coefficient, not on one endpoint/matching summand.
At the actual source, (4) is zero because (1) is zero.

The ordinary fixed-`s` homogeneity identity is equally rigid.  Every term
has one moving `p` factor and two moving `q` factors, so

\[
                         E_{p,q}R=3R.                 \tag{5}
\]

At the mixed target this again gives zero.  It does not give `H`.

## 2. The tempting coefficient projector is not source-valid

Let

\[
 D_f=(p_1[0,1]\partial_{p_1[0,1]})
     (q_{23}[0,0]\partial_{q_{23}[0,0]})
     (q_{45}[0,0]\partial_{q_{45}[0,0]}).             \tag{6}
\]

Because `s_1` is fixed and every response occurrence is squarefree, literal
enumeration gives

\[
                             D_fR=f.                  \tag{7}
\]

The two `q` projectors alone retain exactly two endpoint orientations; the
displayed `p` projector reduces the support to the single marked term.
Thus (7) is the fastest formal route to `H=d_{p,q}f`.

It is also exactly where source validity fails.  At the actual trapped
source,

\[
                 R(x)=0,\qquad (D_fR)(x)=f(x)\ne0.    \tag{8}
\]

Hence `D_f` does not preserve the physical response equation.  Declaring
`d(D_fR)=H` to be a higher tangent/Hasse row would impose a new prolonged
constraint; it is not a consequence of the old Jacobian `A`.  Unary
compatibility does not repair this: the unary equation contains no `p`
factor, so the operator (6) kills it rather than supplying the missing
scalar correction.

This is the endpoint-response analogue of the previously pinned tangent
Euler splitter warning: a raw logarithmic coefficient projector is not a
GHZ-source tangent merely because it isolates a squarefree occurrence.

## 3. Minimum support does not remove the first defect

Equation (1) and `f(x) != 0` force `G(x)=-f(x) != 0`.  Thus a mate packet is
required by target normalization; minimum support cannot delete it using
only the fact that the marked term is active.

The smallest literal quotient retains the marked occurrence and one
aggregate mate:

\[
                   R=f+g,qquad (f,g)=(1,-1).          \tag{9}
\]

The tangent `(1,-1)` kills `dR` but is read as `1` by `df`.  Taking
`Lambda=dR` realizes `Lambda in row(A)` in this quotient while the marked
polar survives.  This is not asserted to extend to a full trapped source;
it is a quotient of the actual 90-term response polynomial proving that
homogeneity, active support, and the mixed target equation alone cannot
give the desired contradiction.  Any positive proof must use another
complete source equation to kill this cancellation direction.

## 4. The smallest positive theorem or cell

Let `S` be the actual fixed-right unary-plus-four-response fibre.  The
needed positive theorem has the intrinsic form

\[
                    df(T_xS)=0.                       \tag{10}
\]

Since `A` is the full evaluated Jacobian on the `p,q` domain, (10) is
equivalent by exact Fredholm duality to `H in row(A)`.  A useful proof of
(10) must show, from another literal word/head equation or a complete
source comparison, that `dG=0` in (1).  Euler identities only show
`d(f+G)=0`.

If (10) is false, the minimal extension is an occurrence-normalization
coordinate `u_f` with a source-valid equation

\[
                            f-u_f=0.                  \tag{11}
\]

Its tangent row is `H-du_f`; a physical target/relative face must absorb
`du_f`.  Equivalently, a relative Spencer cell realizing the raw projector
must carry scalar zero-face `-f(x)`.  A target-zero occurrence projector is
impossible by (8).  This target/augmentation correction is the first
primitive boundary, not an optional terminal decoration.

Finally, under the survivor hypothesis `Lambda in row(A)`, adding a
multiple of `Lambda` to a candidate correction does not alter its conormal
class modulo `row(A)`.  The six-term row therefore cannot supply the
missing occurrence-normalization face in this branch.

## 5. The formal-arc route needs an obstruction comparison

There is a natural alternate plan: `H notin row(A)` gives a tangent
\(\xi\in\ker A\) with \(H(\xi)\ne0\); prolong it to a formal source arc and
contradict maximum-anchor/minimum-support.  For the literal polynomial map
\(F=(q^{[3]}-X_0,\,p_i s_jq^{[2]}-\delta_{ij}X_i)\), however, its first
extension equation is

\[
          A\xi_2=-D^2F_x(\xi,\xi).                    \tag{12}
\]

The obstruction is the class of the right side in the **output** cokernel
`coker(A)`.  By contrast, `Lambda` in `row(A)` is a covector in the
**source cotangent** and says only

\[
                         \Lambda(\xi)=0.               \tag{13}
\]

Thus `Lambda in row(A)` does not make (12) soluble.  To prove that all
higher arc obstructions are the six-term class one first needs a physically
typed comparison map

\[
          \kappa_2:\operatorname {coker}(A)\longrightarrow
                    \mathbf Q[\Lambda]                \tag{14}
\]

carrying the Hessian obstruction, together with coherent higher maps for
the cubic source equations.  Constructing (14) is precisely a
Hasse/Spencer comparison theorem, not a consequence of the row-space
survivor.  Once it exists, the proposed prolongation dichotomy may be very
short; without it, the arc argument crosses domain/codomain complexes.

## Scope

This is a structural counterguard at every actual unary-compatible trapped
source carrying the displayed active occurrence.  It rules out the raw
homogeneity/Euler and uncorrected coefficient-Hasse shortcuts and identifies
the minimal remaining theorem/cell.  It also pins the first comparison map
needed by a formal-arc proof.  It does not prove that a full trapped
source has the two-coordinate tangent (9), prove `H` independent of
`row(A)`, or construct the target-corrected occurrence cell (11).

Run:

```text
python3 computations/verify_h3_trapped_carrier_occurrence_euler_source_gate.py
python3 -O computations/verify_h3_trapped_carrier_occurrence_euler_source_gate.py
python3 -I -S computations/verify_h3_trapped_carrier_occurrence_euler_source_gate.py
```

Frozen ledger SHA-256:

```text
7394dc51c712cc04191433944d87d72afd8833bc75701644a22c026bf0729feb
```
