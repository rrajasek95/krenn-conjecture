# The normalized local-GL3 bar homotopy leaves the target/residue endpoint class

## Outcome

The standard normalized bar/principal-parts construction does provide a
canonical word-changing homotopy, but its boundary is

\[
             d h_{\rm EZ}=L^{\otimes k}-D^{\otimes k}, \tag{1}
\]

not (L^{\otimes k}) alone.  Here (L) is output-colour change and (D)
is the contragredient source derivation from local (GL_3) covariance.  The
Eilenberg--Zilber shuffle signs are compatible, and every shuffle path gives
the same endpoint difference (1).

For the four residual face changes, both endpoints have zero physical
target: the face words `2112`, `1112`, `1212`, `1212`, and `1211` contain
both nonzero colours, so the all-(L) operator kills (Delta), while every
term containing (D) kills it because (Delta) is source-variable
independent.  The obstruction is the normalized degree-zero class.  The bar
augmentation has

\[
                   \epsilon(L)=\epsilon(D)=1,          \tag{2}
\]

so it annihilates every boundary but evaluates to one on either endpoint.
Under the committed denominator-to-split-cap landing, this is exactly the
ordinary-residue class (h_vY_0).  Therefore the canonical homotopy relates
the desired output-lowered face to the all-derivation companion; it does not
make either one an invisible boundary.

The endpoint-only (22\to00) three-operator comparison has an additional
target problem on the two faces with (m_v=2): all three local operators
are (E_{0,2}), and their action on the pure-2 summand of (Delta_8) is
nonzero.  On the three (m_v=1) faces it vanishes because the input labels
are mixed.  Extending to the complete seven-site word change kills this
target action on all five faces, but it does not kill the normalized bar
class (2).

Thus a standard normalized shuffle homotopy does not cancel the physical
((H_0-u)e_{\rm Eq}) defect with both target and ordinary residue zero.
Cancelling the Eq defect leaves a pure target class; cancelling that target
with the old cap target also cancels the desired cap boundary.  Equivalently,
using the old target-zero landing leaves ordinary residue.  A successful
comparison needs a new **reduced relative augmentation** or a physical chain
whose residue correction is independent of the bar augmentation.  Declaring
that reduced endpoint to vanish would be precisely the missing attaching
generator (n_A).

This is an exact obstruction to the standard normalized bar/EZ construction,
not to every possible enlarged source resolution and not a Krenn
counterexample.

## 1. The normalized covariance interval

At one site, local covariance gives

\[
                         DT=L T,                        \tag{3}
\]

where (T) is the universal matching tensor.  The normalized comparison
interval has degree-zero endpoints (D,L), one degree-one edge (E), and

\[
                         dE=L-D.                       \tag{4}
\]

Both endpoints have augmentation one.  Tensor (k) copies.  For a
permutation (pi) of the (k) directions, let (h_pi) be the monotone
path which changes the coordinates from (D) to (L) in order (pi).
The tensor differential telescopes:

\[
                         dh_pi=L^k-D^k.               \tag{5}
\]

The normalized EZ average

\[
                    h_{\rm EZ}={1\over k!}\sum_pi h_pi
\]

has the same boundary.  The checker verifies every one of the (4!=24)
and (7!=5040) paths exactly.

The degree-zero cube has (2^k) vertices and its edge-incidence rank is
(2^k-1).  Hence its (H_0) is one-dimensional, detected by

\[
             \epsilon(c_DD^k+c_LL^k+\cdots)=
                       c_D+c_L+\cdots .                \tag{6}
\]

Equation (5) has augmentation zero.  The desired single endpoint (L^k)
has augmentation one and cannot be a boundary in the normalized complex.
This is independent of the shuffle order or signs.

## 2. Target action

For a subset of sites with input labels (a_x), the product of local output
matrix units acts on

\[
                         \Delta_n=\sum_{c=0}^2e_c^{\otimes n}
\]

only when all (a_x) are the same colour.  If they are, the corresponding
pure summand survives with zero at the acted sites; if the inputs contain
both 1 and 2, the result is zero.

For every four-site deletion face, the input word contains both 1 and 2.
Thus the all-(L) endpoint of (5) has zero target.  Every other cube vertex
contains at least one source derivation (D), and source derivations act
trivially on (Delta).  The entire four-cube is therefore target-zero.

For the endpoint-only bridge the input triple is

\[
                         (m_v,2,2).                    \tag{7}
\]

It is mixed when (m_v=1), but is ((2,2,2)) at the two positions where
(m_v=2).  Those two all-(L) endpoints have a nonzero target word.  The
complete seven-site word change uses the inputs

\[
                         (1,2,1,1,2,2,2),              \tag{8}
\]

so its all-(L) target is zero.  Adding the residual-face homotopy therefore
removes the endpoint target issue, but moves the problem back to the
degree-zero augmentation (6).

## 3. Ordinary residue and the five independent face classes

On a face (F_v), every (L/D) corner of the local covariance cube has
the same polynomial value

\[
                         h_vY_0.                        \tag{9}
\]

This is the exact coefficientwise covariance identity, not a choice of
homotopy.  Under the old split-cap landing, the normalized augmentation (2)
is ordinary residue.  Therefore (5) has zero ordinary residue, but either
endpoint in isolation has residue (h_vY_0).

The five (h_v) have disjoint labelled matching supports, so these residual
(H_0) classes have rank five.  No constant cross-face shuffle cancels the
all-(D) companions while retaining the all-(L) endpoints.  A different
physical ordinary-residue map on a genuinely new chain remains possible,
but the automatic covariance/bar construction does not define one.

## 4. The physical Eq/target/cap quotient

The same obstruction appears in the smallest exact physical quotient with
coordinates

\[
        (u e_{\rm Eq},w,\operatorname {tgt},
                              \operatorname {ores}).    \tag{10}
\]

For a nonzero cap scalar (Y), the old physical columns are

\[
\begin{array}{c|rrrr}
 &u e_{\rm Eq}&w&\operatorname {tgt}&\operatorname {ores}\\ \hline
 C_{\rm tgt}&-1&0&1&0\\
 T&0&-Y&1&0\\
 \rho&0&1&0&1.
\end{array}                                             \tag{11}
\]

The projected (q)-zero Hasse top is

\[
                         C_{\rm tgt}-T=(-1,Y,0,0),      \tag{12}
\]

which displays the defect (-(H_0-u)e_{\rm Eq}).  Subtracting
(C_{\rm tgt}) cancels that Eq coordinate but leaves

\[
                         (0,Y,-1,0).                   \tag{13}
\]

Adding (T) cancels the target and simultaneously cancels the desired
(w)-boundary.  Using `rho` instead introduces ordinary residue.

The integral covector

\[
                         \Lambda=(Y,1,Y,-1)             \tag{14}
\]

annihilates all three columns in (11) but evaluates to (Y\ne0) on the
desired invisible face ((0,Y,0,0)).  Thus the old augmented rank is three
and the desired face raises it to four.  This is the exact target/residue
class left by the normalized bar homotopy after the physical projection.

## 5. Scope and verification

The calculation proves that the canonical normalized local-(GL_3)
bar/principal-parts homotopy does not furnish (n_A).  It does not exclude
a non-normalized comparison with a new augmentation-zero source generator,
a specialization-created relative Tor class, or a higher Bianchi/Spencer
cell with its own physical ordinary-residue correction.

The dependency-free checker
[`verify_h3_gl3_normalized_bar_word_change_obstruction.py`](../computations/verify_h3_gl3_normalized_bar_word_change_obstruction.py)
verifies the normalized tensor differential, every 4- and 7-direction
shuffle path, the cubical incidence ranks, all five target ledgers, the two
endpoint-only target survivors, the five independent face supports, and the
four-coordinate augmented rank/covector at three rational values of (Y).
It uses runtime failures and runs unchanged under normal, optimized,
isolated, and optimized-isolated Python.
