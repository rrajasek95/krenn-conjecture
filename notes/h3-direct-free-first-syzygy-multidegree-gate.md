# The first reset syzygy exists in degree four, but the universal reset is not a chain map

Research reduction only.  This note does not construct the required relative
Rees generator, a nonzero filtered differential, a clean cap, or a proof of
Krenn's conjecture.

## 1. Outcome

The one-higher object isolated by the
[mixed-word reset audit](h3-mixed-word-reset-cross-quotient-chain-lift-no-go.md)
has a very small universal first test.  For the direct-free mixed coefficient,
write

\[
 m=01211222,
 \qquad 0=00000000,
\]

where the last two letters are the endpoint labels.  Let \(H_m,H_0\) be the
two universal eight-site hafnian polynomials, let \(r_m,r_0\) be their
EqSystem row generators, and homogenize the pure equation as \(H_0-u\).  The
fine site--colour grading proves:

1. no multiplier ansatz of edge degree \(0,1,2\), or \(3\) can compare these
   two rows;
2. the first possible degree is four; and
3. on the two-row support the primitive degree-four syzygy is the ordinary
   Koszul cell

\[
 \boxed{
 K_m=H_mr_0-(H_0-u)r_m
     =u r_m+H_mr_0-H_0r_m .}                              \tag{1}
\]

After dehomogenizing \(u=1\), the lowest target term of
\(\frac14K_m\) is exactly

\[
             \frac14 r_{22}^{012112},                    \tag{2}
\]

and applying the proposed word reset gives the associated symbol
\(\frac14{\sf P}_{12112}r_{22}\) requested in the preceding note.  This
uses the formal mixed EqSystem row, not its nonzero value on the rational
guard.

However, (1) does **not** yet instantiate the schematic cap homotopy

\[
 d_{\rm cap}{\sf H}_m+{\sf H}_m d_{\rm Eq}
       =-\kappa {\sf P}_m .                               \tag{3}
\]

Over a universal internal quadratic, the bare functional
\(\epsilon_{12112}\) fails to descend through
\({\cal R}_1q^{[2]}\) in five independent columns.  The failures are five
nonzero quadratic four-site hafnians.  The sparse rational guard makes all
five vanish, which explains why the packet-level reset descended, but the
direct-free condition \(A_{pr}=0\) does not impose any of these internal
quadratic equations.

There is no conflict with commit `befda3f`: its descent theorem is exactly on
the specialized rational guard quotient.  The five defects below concern the
universal internal-\(q\) quotient before that specialization.

Thus the first EqSystem syzygy is not the missing mathematics by itself.
Before (1) can become a typed source/cap homotopy, one must add five
denominator homotopies (or construct a corrected universal reset functional)
starting in internal degree two.  This is a smaller and earlier obligation
than another full degree-four EqSystem search.

## 2. Fine multidegree and the degree-four lower bound

Give a universal edge variable the fine degree

\[
 \deg w_{ab}^{ij}=e_{a,i}+e_{b,j}\in\mathbb N^{8\times3}.
                                                                    \tag{4}
\]

For a global word \(c\), every monomial of \(H_c\) has degree

\[
                       \mu(c)=\sum_{a=0}^7e_{a,c_a}.       \tag{5}
\]

The words \(m\) and \(0\) agree only at site zero.  Hence their componentwise
least common multiple has fifteen occupied slots, and its difference from
either row degree has seven slots.  A polynomial multiplier is a product of
edges, so its slot degree is even.  Seven is impossible.  The first possible
multiplier therefore has eight slots, or edge degree four.

The natural first common degree is

\[
                         \mu(m)+\mu(0).                   \tag{6}
\]

At site zero this contains the repeated common zero-colour slot; at each of
the other seven sites it contains both the mixed and the zero-colour slot.
The multiplier of \(r_0\) has degree \(\mu(m)\), while the multiplier of
\(r_m\) has degree \(\mu(0)\).  Treating \(u\) as a matching-degree-four
variable of fine degree \(\mu(0)\), (1) is homogeneous of (6).

There is also a useful two-row uniqueness statement.  The variables occurring
in \(H_0\) and \(H_m\) are disjoint: a shared edge variable would require two
sites at which the words both have colour zero, but site zero is their only
agreement.  Therefore \(H_0-u\) and \(H_m\) are coprime.  Over the universal
polynomial UFD, every two-row first syzygy is a multiple of (1).  In the first
possible degree the multiple is constant.  This uniqueness is only for the
support \(\{r_0,r_m\}\); it is not a computation of the full 6561-row syzygy
module.

## 3. The five universal denominator defects

Let \(D=\{1,2,3,4,5\}\) and write

\[
                 \bar m=(1,2,1,1,2).
\]

For each \(v\in D\), take the denominator generator
\(e_{\bar m_v}^{(v)}q^{[2]}\).  Coefficient extraction at \(\bar m\) gives

\[
 \epsilon_{\bar m}\!\left(e_{\bar m_v}^{(v)}q^{[2]}\right)
   =h_v,
 \qquad
 h_v=\operatorname {Haf}
       \left(q_{\bar m}\big|_{D\setminus\{v\}}\right).  \tag{7}
\]

Each \(h_v\) is the sum of the three perfect-matching monomials on four
sites, and hence is a nonzero universal quadratic.  For other colours at
site \(v\), the extracted coefficient is zero.  Consequently

\[
 {\sf P}_{12112}
   \left(e_{\bar m_v}^{(v)}q^{[2]}\right)=h_vY_0\ne0
 \quad(v=1,\ldots,5).                                    \tag{8}
\]

Equation (8) is exactly the failure of \({\sf P}_{12112}\) to be a map on
the universal quotient

\[
                {\cal R}_5(D)/{\cal R}_1(D)q^{[2]}.     \tag{9}
\]

It involves only internal \(q\)-variables.  Setting the `pr` direct block to
zero does not affect it.  By contrast, at the frozen direct-free guard and
the word `12112`, the only supported odd internal edges are `12` and `14`.
No four-site perfect matching is supported, so every \(h_v\) specializes to
zero.  The packet descent was therefore exact but nongeneric.

## 4. Target/residue evaluation and the remaining row type

Formally, the \(u r_m\) term in (1) has zero physical target and, after the
reset, odd response \(uY_0\).  Scaling by \(1/4=-\kappa_{\rm df}\) gives the
desired associated-grade pair

\[
                         (0,\tfrac14Y_0).                 \tag{10}
\]

The other two terms in (1) are the exact higher Koszul correction, and the
full EqSystem boundary of (1) is zero.  This is the correct formal sign and
normalization, and it does not divide by a guard residual.

But (10) is not a cap-chain value until (8) has been nullhomotoped.  The next
minimal source data are therefore the five typed denominator rows

\[
                  e_{\bar m_v}^{(v)}q^{[2]},
                  \qquad v=1,\ldots,5,                  \tag{11}
\]

together with degree-two internal homotopies whose boundaries cancel
\(h_vY_0\).  Equivalently, one may seek a polynomially corrected extraction
functional annihilating all fifteen denominator columns while retaining
coefficient one at `12112`.  No assertion is made here that such homotopies
or a corrected reset do not exist.

Zero indeterminacy is not yet reached: a functional which fails (9) has no
quotient readout whose independence can be tested.  The exact order of work
is now:

1. solve the five quadratic denominator defects (8);
2. insert the unique two-row degree-four EqSystem cell (1); and only then
3. test differences of the resulting physical lifts on the odd quotient.

This also explains why enlarging the EqSystem multiplier ansatz before fixing
the cap quotient would be inefficient.  The first EqSystem cell is already
present and exact; its proposed output is blocked one layer lower.

## 5. Exact verification and scope

The dependency-free checker
[`verify_h3_direct_free_first_syzygy_multidegree_gate.py`](../computations/verify_h3_direct_free_first_syzygy_multidegree_gate.py)
enumerates the 105 perfect matchings of eight sites, builds \(H_0,H_m\) as
sparse universal polynomials, verifies their disjoint variable sets and the
literal zero boundary of (1), checks the fine-degree parity bound, constructs
all five quadrics (7), and verifies that the guard support kills all of them.

The result is deliberately bounded.  It proves no multiplier of edge degree
at most three can compare the pure and selected mixed rows, and it identifies
the unique minimal cell on that two-row support.  It does not rule out
syzygies using other EqSystem rows, corrected reset functionals, denominator
homotopies, or higher-degree relative-Rees cells.  It also does not promote
the sparse guard to a source.  Finally, this is a statement over the universal
polynomial ring.  A non-flat specialization can create new invisible chains
through a \(\operatorname {Tor}_1\) kernel; the calculation neither excludes
nor constructs such a specialization-created source lift.
