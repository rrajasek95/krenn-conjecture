# The first normalized Buchberger cell is a universal star-minor identity

## 1. Exact identity

Let \(B\) be even, let \(v\ne u\) be vertices, and fix a colour word
\(d:B\setminus\{v\}\to\{0,1,2\}\).  Choose two distinct colours \(a,b\)
at \(v\), and write \(d^a,d^b\) for the two resulting words on \(B\).
Use \(X_{vw}(r,s)\) for the aggregate edge coordinate whose colour at
\(v\) is \(r\) and whose colour at \(w\) is \(s\), with the endpoint order
converted to the repository convention when \(w<v\).  Put

\[
 \alpha=X_{vu}(a,d_u),\qquad \beta=X_{vu}(b,d_u).
\]

Laplace expansion of a hafnian coefficient at \(v\) gives the polynomial
identity

\[
\boxed{
 \beta H_{d^a}-\alpha H_{d^b}
  =\sum_{w\ne u,v}
   \bigl(\beta X_{vw}(a,d_w)-\alpha X_{vw}(b,d_w)\bigr)
   H_{d|_{B\setminus\{v,w\}}}.}                         \tag{1}
\]

Indeed, the summand in which \(v\) is paired with \(u\) is
\(\beta\alpha H_{d|B\setminus\{u,v\}}\) in the first product and
\(\alpha\beta H_{d|B\setminus\{u,v\}}\) in the second, so it cancels.
For every other partner \(w\), the remaining matching sum is exactly the
smaller hafnian coefficient displayed on the right.  No division,
genericity, sign choice, or equality of endpoint colours is used.

The bracket in (1) is the \(2\)-by-\(2\) minor of the two colour rows on the
\(v\)-star, using columns \(u,w\), with the colours at the opposite
endpoints prescribed by \(d\).  Thus (1) is a source-provenant relation
between a mixed-word pair and smaller cofactors.

## 2. The exact chart-26 degree-five cell

In normalized chart 26, take the two Hamming-one words with codes \(1,2\).
Their leading monomials are

```text
0948c6f4 = (02:00)(13:00)(45:00)(67:01),
0948c6f5 = (02:00)(13:00)(45:00)(67:02).
```

They share the first three variables, so their Buchberger lcm has degree
five.  Formula (1), with \(v=7\), \(u=6\), \(a=1\), and \(b=2\), is exactly
that S-polynomial.  Direct normalized expansion has 180 terms:

\[
             120\text{ in degree }5,qquad
              48\text{ in degree }4,qquad
              12\text{ in degree }3,
\]

with 90 coefficients \(+1\) and 90 coefficients \(-1\).  None of its terms
is divisible by an original degree-four leading monomial.  Its new leading
monomial is

```text
0948cfebf5 = (02:00)(13:00)(46:00)(57:01)(67:02),
```

which is again squarefree and contains no homogenizing variable \(t\).
This proves that the original 6,558 normalized generators are not a
Groebner basis, while keeping open a squarefree Groebner completion.

The numerical census in this section is to be frozen by the dedicated
checker; identity (1) is independent of that computation.

There is a second universal degree-five cell.  Suppose two words agree away
from vertices \(u,v\), and use colour pairs \((a,b)\) and \((a',b')\) at
\((v,u)\).  Abbreviate the common outside word by \(d\).  Cancelling the
matching term which uses \(uv\) gives

\[
\begin{aligned}
 &X_{vu}(a',b')H_{d^{a,b}}
       -X_{vu}(a,b)H_{d^{a',b'}}\\
 &=\sum_{\substack{w,z\notin\{u,v\}\\w\ne z}}
 \bigl[
   X_{vu}(a',b')X_{vw}(a,d_w)X_{uz}(b,d_z)\\
 &\hspace{43mm}
  -X_{vu}(a,b)X_{vw}(a',d_w)X_{uz}(b',d_z)
 \bigr]
 H_{d|_{B\setminus\{u,v,w,z\}}}.                 \tag{2a}
\end{aligned}
\]

Every matching avoiding \(uv\) has unique partners \(w\) of \(v\) and
\(z\) of \(u\), which proves (2a).  This is the direct-double companion of
the one-end star transport (1).  At eight sites both have total degree five,
and every raw monomial on their right sides is squarefree: the displayed
three edges are distinct and the remaining matching avoids all four of
their exposed vertices.

## 3. Why this is the relevant recursive cell

The new basis element is not an opaque high-degree S-pair.  It performs one
legal elimination of a chosen support partner \(u\) and replaces it by the
other possible partners \(w\), with an explicit star minor recording the
transport.  Iterating Buchberger completion therefore generates alternating
partner paths rather than arbitrary monomials.  A viable well-founded order
is lexicographic in the eliminated partner, refined by the support-distance
of the replacement edge.

On a mixed common zero, whenever both words \(d^a,d^b\) are mixed, (1)
becomes a literal relation among the smaller cofactors

\[
 \sum_{w\ne u,v}
   \det\!\begin{pmatrix}
    X_{vu}(b,d_u)&X_{vw}(b,d_w)\\
    X_{vu}(a,d_u)&X_{vw}(a,d_w)
   \end{pmatrix}
   H_{d|_{B\setminus\{v,w\}}}=0.                         \tag{2}
\]

If the displayed star-minor rows span the relevant cofactor space, (2)
isolates the smaller hafnian coefficients and gives a source-valid descent.
If they do not, their rank defect is an explicit low-rank star boundary.
This is exactly the dichotomy needed by the uniform clean-pair program, but
(1) alone does not prove the spanning alternative and does not yet close
that program.

## 4. Its same-star critical pairs have exact Pluecker reductions

The first layer of the proposed straightening law is already formal.  Write

\[
 A_w=X_{vw}(a,d_w),\quad B_w=X_{vw}(b,d_w),\quad
 h_w=H_{d|_{B\setminus\{v,w\}}},
\]

and put

\[
 H_a=\sum_w A_wh_w,\qquad H_b=\sum_w B_wh_w,
 \qquad \Delta_{uw}=B_uA_w-A_uB_w.
\]

The cell based at partner \(u\) is

\[
                  R_u=B_uH_a-A_uH_b=\sum_w\Delta_{uw}h_w. \tag{3}
\]

For any two partners \(u,z\), the ordinary \(2\)-by-\(m\) Pluecker
identities give

\[
 \boxed{
   A_zR_u-A_uR_z=\Delta_{uz}H_a,
   \qquad
   B_zR_u-B_uR_z=\Delta_{uz}H_b.}                         \tag{4}
\]

For example,
\(A_z\Delta_{uw}-A_u\Delta_{zw}=\Delta_{uz}A_w\), and
summing against \(h_w\) proves the first identity; the second is identical.
Thus critical pairs between two transports for the same vertex, word, and
colour pair reduce back to the two original hafnian generators.  This is
the determinantal mechanism which can keep their diagonal leading terms
squarefree.  Critical pairs that change the word, the selected vertex, or
the colour pair are the genuinely new compatibility audit.

There is also an exact three-colour Koszul relation.  For a third colour
row \(C\), define \(R_u^{AB}=B_uH_A-A_uH_B\), and cyclically.  Then

\[
             C_uR_u^{AB}-B_uR_u^{AC}+A_uR_u^{BC}=0.       \tag{5}
\]

Indeed every product \(A_uB_uH_C\), \(A_uC_uH_B\), and
\(B_uC_uH_A\) cancels twice with opposite signs.  More conceptually, for
fixed \(v,d\), form the three-row matrix whose partner columns are
\((A_u,B_u,C_u)^{\mathsf T}\) and whose last column is
\((H_A,H_B,H_C)^{\mathsf T}\).  The transports are its two-by-two minors
using the last column.  Equations (4)--(5) are the first
Eagon--Northcott/Pluecker syzygies.  Determinantal ideals have squarefree
diagonal degenerations; the remaining issue is compatibility of these
local determinantal systems when their cofactor words and selected vertices
overlap.

## 5. Next exact audit

The chart computation should adjoin the complete support-stabilizer orbit of
(1), then examine only non-product critical pairs involving those new cells.
At every stage record whether the new *minimal* leading monomial remains
squarefree.  A finite squarefree completion proves radicality of the
normalized ideal; a first repeated-variable leading monomial identifies the
precise nonreduced Bockstein cell which must be controlled separately.
