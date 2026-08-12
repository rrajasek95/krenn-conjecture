# Site-Euler corrected marked jets conserve anchor and ordinary residue

Exact coefficient-ring split and positive physical first-jet construction.
This note answers the first question left by the presentation-jet
obstruction. It does not construct the ordinary-residue-compatible terminal
column \(P(e_v)\).

## Outcome

Fix one selected mixed word \(c_v\) and the marked variables

\[
                 u_v=a_{xv}^{00},\qquad t=a_{pq}^{00}.
\]

Over the constant span of physical coordinate directions, neither marked
Jacobian column can be corrected. In the selected row there are 252 labelled
coordinate columns, 27 nonzero columns, and 360 residual-matching features.
Every feature has exactly one coordinate owner. Thus one monomial of
\(\partial_{u_v}H_{c_v}\), and similarly one monomial of
\(\partial_tH_{c_v}\), is a primitive integral separator:

\[
 \ell_v(\partial_{u_v}H_{c_v})=1,\qquad
 \ell_v(\partial_eH_{c_v})=0\quad(e\ne u_v).            \tag{1}
\]

This rules out a scalar marked-one correction. It does not survive passage
to the first localized polynomial coefficient module.

Let site weights satisfy \(\sum_i\lambda_i=0\), and put

\[
                  \Xi_\lambda(a_{ij}^{ab})
                    =(\lambda_i+\lambda_j)a_{ij}^{ab}. \tag{2}
\]

Every perfect matching uses every site once. Therefore, term by term in
every literal output word,

\[
                  J\Xi_\lambda
                   =\left(\sum_i\lambda_i\right)H=0.    \tag{3}
\]

Choose an auxiliary odd site \(z_v\ne v\). For the left marked direction take

\[
 \lambda_x=1,\quad\lambda_{z_v}=-1,\quad\lambda_i=0
 \text{ otherwise}.
\]

Since \(v\ne z_v\), the \(u_v\)-component of (2) is \(u_v\), while its
\(t\)-component is zero. On the open
\(u_v\ne0\),

\[
 \xi_v={\Xi_\lambda\over u_v},\qquad (\xi_v)_{u_v}=1,
 \qquad J\xi_v=0.                                      \tag{4}
\]

For the right marked direction take

\[
 \mu_p=1,\quad\mu_{z_v}=-1,\quad\mu_i=0
 \text{ otherwise}.
\]

Its \(t\)-component is \(t\), while its \(u_v\)-component is zero. Thus on
\(t\ne0\),

\[
 \eta={\Xi_\mu\over t},\qquad \eta_t=1,\qquad J\eta=0. \tag{5}
\]

Equations (4)--(5) are physical source-coordinate tangents, not differences
of row presentations. They hold on all \(3^8\) literal output rows after
the direct-free specialization, and hence have zero physical target.

## The complete mixed Hasse correction

The two site scalings commute. Write

\[
 w_{ij}={\lambda_i+\lambda_j\over u_v},\qquad
 z_{ij}={\mu_i+\mu_j\over t}.
\]

The mixed term in their two-parameter action is the physical coordinate
vector

\[
                  (\zeta_v)_{ij}^{ab}
                       =w_{ij}z_{ij}a_{ij}^{ab}.        \tag{6}
\]

On a matching \(M\), the Jacobian correction and mixed Hessian are

\[
\begin{aligned}
 (J\zeta_v)_M&=\sum_{e\in M}w_ez_e,\\
 H(\xi_v,\eta)_M&=\sum_{\substack{e,f\in M\\e\ne f}}w_ez_f.
\end{aligned}
\]

Their sum factors:

\[
 (J\zeta_v+H(\xi_v,\eta))_M
   =\left(\sum_{e\in M}w_e\right)
      \left(\sum_{f\in M}z_f\right)=0.                 \tag{7}
\]

Thus (4)--(7) satisfy the complete physical source Hasse equations

\[
 J\xi_v=J\eta=0,\qquad J\zeta_v+H(\xi_v,\eta)=0.        \tag{8}
\]

The marked edges \(xv\) and \(pq\) are disjoint, and the opposite marked
components were arranged to vanish. Hence the coefficient of the
desired mixed polar
\(\partial_t\partial_{u_v}H_{c_v}\) inside (7) is exactly
\((\xi_v)_{u_v}\eta_t=1\). The remaining mixed-Hessian terms are the literal
physical correction required by source provenance.

The construction is fine-homogeneous after localization. Every component
of \(\xi_v\) has the coordinate degree shifted by
\(-\deg u_v\), every component of \(\eta\) by \(-\deg t\), and (6) has the
sum of those two shifts. Thus the earlier endpoint-grade mismatch is not the
first obstruction.

## Exact anchor--ordinary-residue conservation

The preceding choice isolates the ordered marked polar, but it does not have
zero ordinary residue. The exact five-ridge response companions are the
matching monomials \(q_{v,N}\) on \(F_v=D\setminus\{v\}\). For general
site-Euler weights put

\[
 a=\lambda_x+\lambda_v=1,\quad
 b=\lambda_p+\lambda_q,\quad
 c=\mu_x+\mu_v,\quad
 d=\mu_p+\mu_q=1.                                      \tag{9}
\]

Since both total site-weight sums vanish,

\[
 \sum_{i\in F_v}\lambda_i=-(1+b),\qquad
 \sum_{i\in F_v}\mu_i=-(1+c).                         \tag{10}
\]

After the common \(u_vt\)-normalization, the first ordinary-residue actions
on every \(q_{v,N}\) have coefficients \(-(1+b)\) and \(-(1+c)\).
The marked Hessian contribution on
\(u_vtq_{v,N}\) is \(1+bc\), including both ordered crosses, while the
\(u_v,t\) part of \(J\zeta_v\) is \(b+c\). Hence

\[
\boxed{
 \operatorname{anchor}_{v}
  =(1+bc)+(b+c)
  =(1+b)(1+c)
  =\operatorname{ores}_{v}.}                           \tag{11}
\]

This is the exact anchor--ordinary-residue conservation law for the whole
site-Euler family. If both first jets have zero ordinary residue, (10)
forces

\[
                         b=c=-1,
\]

and (11) gives zero corrected anchor.

There are two useful normal forms.

* The auxiliary-site choice in (4)--(5) has \(b=c=0\). It gives endpoint
  anchor \(1\), but its four-site response companion and ordinary residue
  are also \(1\).
* The residue-zero choice

  \[
    \lambda_x=1,\ \lambda_p=-1,\qquad
    \mu_p=1,\ \mu_x=-1
  \]

  acts trivially on all fifteen \(q_{v,N}\). But it has \(b=c=-1\):
  the marked Hessian coefficient is \(2\), and the endpoint part of
  \(J\zeta_v\) is \(-2\). The corrected anchor is zero.

The site-Euler jet fixes the complete source output tensor and therefore its
physical target. On each matching term its full corrected physical class is
zero. In the residue-zero normal form the coefficient ledger is

\[
\begin{array}{c|c}
\text{piece}&\text{coefficient}\\ \hline
\text{two ordered marked Hessian crosses}&+2\\
\text{endpoint part of }J\zeta_v&-2\\
\text{four-site ordinary residue}&0.
\end{array}                                             \tag{12}
\]

Thus the local three-term polar can survive in a chart-sector projection,
but zero ordinary residue makes the full gauge correction cancel its
terminal aggregate coefficientwise. Its class in the source+target cokernel
is zero, and its primitive relative-anchor incidence is also zero.

A torus orbit also supplies no primitive relative-anchor incidence. To use
this zero cokernel class as one of the formal pentagon columns, a new
source-labelled relative map would have to retain the marked sector while
killing the other entries in (12). That is precisely the missing provenance
operation, not a consequence of tangency.

The bounded verdict is therefore:

* constant physical coordinate corrections fail by the primitive separator
  (1);
* localized polynomial physical corrections succeed by (4)--(8), but give
  the zero gauge class after the complete correction; and
* within the entire site-Euler family, zero ordinary residue forces zero
  terminal anchor by (11), so no column \(P(e_v)\) is constructed.

If a future non-Euler physical jet has \(H=-J\zeta\) with zero ordinary
residue and a primitive relative-anchor label, the Fredholm alternative
immediately enters its generator branch. Equation (11) proves that the
site-Euler torus cannot be that jet.

The localization is load-bearing. If \(u_v=0\) or \(t=0\), this normalized
marked-one construction is unavailable; no claim is made for that boundary.

## Reproducibility

Run

    python3 computations/verify_h3_rootless_marked_first_jet_site_euler_correction.py
    python3 -O computations/verify_h3_rootless_marked_first_jet_site_euler_correction.py
    python3 -I -S computations/verify_h3_rootless_marked_first_jet_site_euler_correction.py

The checker exhausts the 252 coordinate columns in each of the five selected
rows, produces ten primitive separators, checks the two site-Euler identities
and their mixed Hasse correction on all 90 direct-free matching types, and
uses word-independence to cover all 6561 literal output rows.
