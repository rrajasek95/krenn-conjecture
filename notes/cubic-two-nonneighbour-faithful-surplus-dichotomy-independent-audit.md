# Independent audit: cubic two-nonneighbour faithful-surplus dichotomy

## Verdict

The dichotomy in
[cubic-two-nonneighbour-faithful-surplus-dichotomy.md](cubic-two-nonneighbour-faithful-surplus-dichotomy.md)
is correct over the intended field \(\mathbb C\), conditional on the cited
cubic nullity-web and local-port theorems.  It is an exact partition of the
three colours and retains zero cofactors, zero blocks, and cancellation in
the complete matching sums.

The rank conclusion is also correct, with one essential scope
qualification: every-invertible-block conclusion requires the
**entry-minimal exact-source** hypothesis.  The audited primary note now
states that qualifier explicitly; the conclusion is not asserted, and does
not follow, without entry-minimality.

## 1. Sets, parities, and the exhaustive colour split

A cubic support centre \(p\) has exactly the three neighbours
\(a_0,a_1,a_2\).  Hence

\[
 R=B\setminus\{p,a_0,a_1,a_2\}
\]

has size \(N-4\ge4\), so distinct \(q,q'\in R\) exist and both are
nonneighbours of \(p\).  For each colour \(c\),

\[
 L_c=B\setminus\{p,a_c,q,q'\}
\]

has the even size \(N-4\).  The domain sites of \(\Phi_{q,c}\) are
\(L_c\mathbin{\dot\cup}\{q'\}\), and those of \(\Phi_{q',c}\) are
\(L_c\mathbin{\dot\cup}\{q\}\), exactly as required by the two cited
cofactor-map theorems.

The nullity-web theorem gives

\[
 \nu_{q,c}\ge1,\qquad \nu_{q',c}\ge1,
 \qquad |E_q|\le1,\qquad |E_{q'}|\le1.
\]

Therefore the complement
\(C=\{0,1,2\}\setminus(E_q\cup E_{q'})\) is nonempty.  Exactly one of
the following statements holds:

1. some \(c\in C\) has \(P_c\ne0\); or
2. every \(c\in C\) has \(P_c=0\).

In the first case, \(c\notin E_q\cup E_{q'}\), together with integral
nullity at least one, implies that both nullities are at least two.  Since
\(P_c\ne0\), the local-port theorem makes restriction of both kernels to
the common \(L_c\)-star injective.  This is precisely the faithful-surplus
alternative.

In the second case,
\(\{c:P_c\ne0\}\subseteq E_q\cup E_{q'}\), and the union has size at
most two.  The exact gluing identity

\[
 A_{q\mid q'}(d,j)P_c+
 \Theta_c(s^q_{d,L_c},s^{q'}_{j,L_c})
 =\delta_{cd}\delta_{cj}\lambda_c^{-1}e_c^{\otimes L_c}
\]

then gives the displayed pure-crossing packet for every \(c\in C\): eight
complete Hessian responses vanish and the \((c,c)\)-response is the stated
nonzero decomposable tensor.  Because \(C\ne\varnothing\), at least one
such packet always exists.  This deduction sets the *complete* cofactor
\(P_c\) to zero; it makes no termwise noncancellation assumption.

## 2. Faithful-chart quotient

For \(P_c\ne0\), let

\[
 Z_{q,c}=\operatorname{res}_{L_c}(\ker\Phi_{q,c}).
\]

By definition restriction is surjective onto \(Z_{q,c}\), and the
local-port theorem makes it injective.  It is therefore an isomorphism
from the kernel onto its image, so every \(z\in Z_{q,c}\) has a unique
lift \((\eta_{q,c}(z),z)\).  Contracting the exact gluing formula at the
\(q'\)-port gives

\[
 \Theta_c(z,s^{q'}_{j,L_c})
 =-e_j^*(\eta_{q,c}(z))P_c.
\]

Thus all three responses land in \(\mathbb CP_c\); reversing \(q,q'\)
proves the symmetric statement.  Quotienting the nine physical equations
by this line kills the direct-block term and leaves only the \((c,c)\)
entry.  The claimed rank-at-most-one response is therefore valid (with
rank understood as the span/rank of the quotient response entries).  If
\([e_c^{\otimes L_c}]=0\), the quotient response simply has rank zero.
No intersection between the two defect spaces is claimed or needed.

## 3. Entry-minimality and the physical rank drop

The full cofactor complementary to the physical block \(qq'\) expands at
the cubic centre as

\[
 H_{B\setminus\{q,q'\}}(A)
 =\sum_{c=0}^2\lambda_c e_c^{(p)}\otimes
   e_c^{(a_c)}\otimes P_c.
\]

The three summands have independent \(p\)-factors.  Star irredundancy at
an entry-minimal exact source says that a nonzero entry of \(A_{qq'}\)
has nonzero complementary cofactor.  Consequently
\(A_{qq'}\ne0\) forces at least one \(P_c\ne0\), including when other
matching terms cancel.

On the concentrated branch, choose such an active colour \(c\).  It lies
in \(E_q\cup E_{q'}\).

* If \(c\in E_q\), the exact nullity-one classification supplies a wrong
  colour \(\rho_q(c)\ne c\) whose whole endpoint-\(q\) star row is
  supported only at \(a_c\).  Since \(q'\ne a_c\), contraction of the
  physical block \(A_{q\mid q'}\) by \(e_{\rho_q(c)}^*\) at \(q\) is
  zero.  Hence \(A_{q\mid q'}\) has a zero row.
* If \(c\in E_{q'}\), the same statement at the reversed endpoint gives a
  zero row of \(A_{q'\mid q}\).  Physical slot reversal transposes the
  displayed matrix, so this is a zero column of \(A_{q\mid q'}\).

Either condition forces \(\operatorname{rank}A_{qq'}\le2\).  Thus, at an
entry-minimal exact source, an invertible block between two nonneighbours
of the cubic centre cannot be on the concentrated branch and must be on
the faithful-surplus branch.

## 4. Audit artifacts

The primary note audited here had SHA-256

```text
b8c1094aa4fd0f799dc764d3e469c8880a342082f7b5648604a2792f44b2f491
```

The existing exact nullity-web checker passes its matching expansion,
shared-factorization cases, minimum profile \((1,2,2)\), and boundary
dimensions.  The local-port theorem and its independent audit already
verify both endpoint orientations of the nine-equation gluing identity.
The primary local-port checker was not rerun in this environment because
its optional `sympy` dependency is absent; no new computational claim is
introduced by the present dichotomy.
