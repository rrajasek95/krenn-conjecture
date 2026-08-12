# A non-Euler diagonal GHZ-stabilizer jet realizes the marked polar with zero ordinary residue

Positive physical first- and second-jet theorem, with one remaining
source-descent gate. This note constructs, on the marked-cell open, a
non-Euler pair in the complete source/target/ordinary-residue tangent kernel
whose marked mixed Hessian is \(h_v\) with coefficient one. It does not prove
that projection to that marked sector is zero-indeterminate, so it does not
yet construct the terminal pentagon column \(P(e_v)\).

## The diagonal stabilizer theorem

Let \(A\) be an exact ternary source on eight sites:

\[
                         A^{[4]}=\Delta_{8,3}.
\]

For colour-diagonal site weights \(\lambda_{i,c}\), define the physical
edge-coordinate vector field

\[
 X_\lambda(a_{ij}^{ab})
   =(\lambda_{i,a}+\lambda_{j,b})a_{ij}^{ab}.           \tag{1}
\]

On the output coefficient with word \(w\), covariance gives

\[
                   J_A X_\lambda\big|_w
      =\Lambda(w)H_w(A),\qquad
 \Lambda(w)=\sum_i\lambda_{i,w_i}.                     \tag{2}
\]

Assume

\[
                         \sum_i\lambda_{i,c}=0
                 \qquad(c=0,1,2).                     \tag{3}
\]

For a pure word, (3) kills the right side of (2). For a mixed word,
\(H_w(A)=0\) because the exact target is GHZ. Therefore

\[
                             J_AX_\lambda=0.            \tag{4}
\]

This is a physical tangent at every exact source, not a universal
presentation difference.

For two such weights \(\lambda,\mu\), put

\[
 Z_{\lambda,\mu}(a_{ij}^{ab})
 =(\lambda_{i,a}+\lambda_{j,b})
  (\mu_{i,a}+\mu_{j,b})a_{ij}^{ab}.                    \tag{5}
\]

Termwise on a perfect matching, the mixed Hessian plus (5) factors as

\[
\begin{aligned}
 &(J_AZ_{\lambda,\mu}
       +H_A(X_\lambda,X_\mu))\big|_w\\
 &\hspace{30mm}=\Lambda(w)M(w)H_w(A)=0.                \tag{6}
\end{aligned}
\]

Equations (4)--(6) are the complete physical source Hasse equations.

## The marked non-Euler pair

Fix a deleted odd site \(v\), set
\(F_v=D\setminus\{v\}\), and choose \(z_v\in F_v\). Let

\[
 u_v=a_{xv}^{00},\qquad t=a_{pq}^{00}.
\]

Choose the only nonzero weights

\[
\lambda_{x,0}=1,\quad\lambda_{z_v,0}=-1,\qquad
\mu_{p,0}=1,\quad\mu_{z_v,0}=-1.                       \tag{7}
\]

They satisfy (3). On \(u_vt\ne0\), normalize

\[
                 \xi_v={X_\lambda\over u_v},\qquad
                 \eta_v={X_\mu\over t}.                \tag{8}
\]

Then

\[
 (\xi_v)_{u_v}=1,\quad(\eta_v)_t=1,\qquad
 (\xi_v)_t=(\eta_v)_{u_v}=0.                           \tag{9}
\]

The class of each direction modulo site-Euler gauge is nonzero. Indeed,
site-Euler gauge adds the same weight to all three colours at one site,
whereas

\[
 \lambda_{x,0}-\lambda_{x,1}=1,\qquad
 \mu_{p,0}-\mu_{p,1}=1                                \tag{10}
\]

are quotient invariants.

The exact ordinary-residue companions are the fifteen matching monomials
\(q_{v,N}\) on \(F_v\), decorated by the selected colours
\(m_i\in\{1,2\}\). The weights (7) are supported only in colour zero, so

\[
 \xi_v(q_{v,N})=\eta_v(q_{v,N})
   =Z_{\lambda,\mu}(q_{v,N})=0                         \tag{11}
\]

for every \(v,N\). Thus both first jets and their mixed correction have
zero ordinary residue.

For the selected mixed word \(c_v\), every marked matching is

\[
                         u_v\,t\,q_{v,N}.
\]

Equations (8)--(9) give

\[
 H_A(\xi_v,\eta_v)\big|_{\text{marked sector}}
             =\sum_N q_{v,N}=h_v,                     \tag{12}
\]

with coefficient one. The correction (5) has no marked \(u_v\)- or
\(t\)-component. Hence the desired three-term polar survives exactly.

## The remaining descent gate

The full corrected mixed coefficient is nevertheless zero, as it must be
for an integrable target-stabilizer orbit. On the selected mixed word,
\(\Lambda(c_v)=M(c_v)=1\), so (6) reads

\[
 J_AZ_{\lambda,\mu}+H_A(\xi_v,\eta_v)
                         =H_{c_v}(A)=0.                \tag{13}
\]

The three marked matchings in (12) are completed by the other 87
direct-free matchings in (13). Therefore (12) is a genuine physical sector
of a complete source/target/residue-zero Hasse jet, but selecting that sector
is still a relative operation.

The exact remaining theorem is:

> Construct a source-labelled terminal map on the corrected jet (8), (5)
> which sends the marked sector (12) to the pentagon ridge generator,
> kills the other completion terms in (13), and annihilates every change of
> Hasse lift in the augmented Jacobian kernel.

The last condition is the zero-indeterminacy requirement. If it holds, this
single jet constructs one physical \(P(e_v)\), and symmetry constructs all
five. If it fails, its separating covector is the desired non-Euler no-go.

This result strictly escapes the site-Euler conservation theorem. The
site-Euler family has anchor equal to ordinary residue; the colour-diagonal
pair (7) has zero ordinary residue while retaining marked polar coefficient
one. What remains is descent of that physical marked sector, not discovery
of further tangent directions.

## Verification

Run

    python3 computations/verify_h3_rootless_non_euler_diagonal_stabilizer_jet.py
    python3 -O computations/verify_h3_rootless_non_euler_diagonal_stabilizer_jet.py
    python3 -I -S computations/verify_h3_rootless_non_euler_diagonal_stabilizer_jet.py

The checker verifies the colourwise GHZ stabilizer equations, nontriviality
modulo site-Euler gauge, all fifteen matching-labelled ordinary-residue
companions, the three marked polar terms, and the complete 90-term physical
Hasse correction for every deleted face.
