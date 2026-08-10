# Independent audit: rank-one--rank-one clean quotient plane

## 1. Verdict

**PASS after one substantive scope correction and typesetting repairs.**
The four-dimensional double-annihilator space, response cancellation,
\(|B|\leq3\) square-zero argument, diagonal-functional classification,
bilinear scalar annihilator, and finite-hyperplane completion in
[the source note](rank-one-rank-one-shore-clean-quotient-plane.md) are
correct.

The source now distinguishes the maximal \(|B|=3\) branch from the
stronger auxiliary range \(|B|\leq3\).  The claim that the scalar gate
escapes the \(B\mid A\) rank-one flattening requires \(|B|=3\).  If
\(|B|\leq2\) and no coordinate gate occurs, the scalar gate is already
impossible.  This does not alter the intended maximal \(b=3\),
rank-\((1,1)\) result.

Malformed occurrences of \({\cal Q}\) and \({\cal E}\) were also
repaired, and “rank-five annihilator” was replaced by the unambiguous
“five-dimensional annihilator condition.”

The corrected source has SHA-256

    1543c767f6c6f541a675643b16380bd1e1890ca565412eb201be1ed9f21ffbb9

## 2. Assertion ledger

| Assertion | Verdict | Audit result |
|---|---|---|
| Rank-one shore factorization | **PASS** | Rank one gives \(p_i^A=\lambda_iU\) and \(s_j^A=\mu_jV\) with nonzero \(\lambda,\mu,U,V\). |
| Dimension and annihilator orientation of \({\cal Q}\) | **PASS** | \({\cal Q}=(\ker\lambda^{\mathsf T})\otimes(\ker\mu^{\mathsf T})\) under \(x\otimes y\mapsto xy^{\mathsf T}\), so \(\dim{\cal Q}=4\). |
| Response cancellation | **PASS** | The left and right radical equations kill the \(AA\), \(AB\), and \(BA\) response pieces exactly. |
| \(|B|\leq3\Rightarrow r^{[2]}=0\) | **PASS** | Two two-site supports inside a set of at most three sites must intersect. |
| Clean-error conclusion | **PASS** | Every error term contains \(r^{[j]}\) for \(j\ge2\). |
| Each diagonal functional | **PASS** | \(\kappa_i|_{\cal Q}=0\) exactly when \(\lambda\parallel e_i\) or \(\mu\parallel e_i\). |
| Scalar annihilator | **PASS** | Under the explicitly bilinear entrywise pairing, \({\cal Q}^{\perp}=\lambda\otimes\mathbb C^3+\mathbb C^3\otimes\mu\) with the stated matrix orientation. |
| Finite-hyperplane “if and only if” | **PASS** | Over \(\mathbb C\), four proper linear hyperplanes cannot cover the four-dimensional vector space \({\cal Q}\). |
| Remaining gates for maximal \(b=3\) | **PASS** | They are exact obstructions to activity inside this clean subspace, but are not themselves eliminated. |
| Scalar-gate scope for all \(|B|\le3\) | **PASS after correction** | The non-rank-one discussion is now restricted to \(|B|=3\); the source records the sharper \(|B|\le2\) conclusion. |

No algebraic **FAIL** remains after the correction.

## 3. Rank-one shore factorization and fixed labels: PASS

Let

\[
 P_A:\mathbb C^3\longrightarrow({\cal R}_A)_1,
 \qquad P_A(e_i)=p_i^A.                                    \tag{A1}
\]

If \(\operatorname{rank}P_A=1\), its nonzero image is a line
\(\mathbb C U\).  Hence there is a coordinate column
\(\lambda=(\lambda_i)\), unique up to inverse scaling of \(U\), such that

\[
                              p_i^A=\lambda_iU.              \tag{A2}
\]

The same reasoning gives \(s_j^A=\mu_jV\).  Rank one makes all four of
\(\lambda,\mu,U,V\) nonzero.  No change of the fixed physical basis
\(e_0,e_1,e_2\) is involved; the coordinates of \(\lambda\) and \(\mu\)
therefore retain their target-label meaning.

This is consistent with Section 6 of
[the endpoint-dark shore note](endpoint-dark-shore-consecutive-power-jet.md),
which writes

\[
 P|_A=\lambda\otimes U,\qquad S|_A=\mu\otimes V,\qquad
 r_A=(\lambda^{\mathsf T}K\mu)UV.                           \tag{A3}
\]

The present note selects matrices for which \(\lambda\) is a left
radical and \(\mu\) is a right radical.  That orientation is exactly the
one in (A3).

## 4. The four-dimensional matrix space: PASS

Put

\[
 X=\ker\lambda^{\mathsf T},\qquad
 Y=\ker\mu^{\mathsf T}.                                     \tag{A4}
\]

Both \(X\) and \(Y\) have dimension two.  For \(x\in X\) and \(y\in Y\),

\[
 \lambda^{\mathsf T}(xy^{\mathsf T})
   =(\lambda^{\mathsf T}x)y^{\mathsf T}=0,\qquad
 (xy^{\mathsf T})\mu=x(y^{\mathsf T}\mu)=0.                 \tag{A5}
\]

Thus the injective tensor-to-matrix map

\[
 X\otimes Y\longrightarrow\operatorname{Mat}_{3\times3}(\mathbb C),
 \qquad x\otimes y\longmapsto xy^{\mathsf T}                \tag{A6}
\]

lands in

\[
 {\cal Q}_{\lambda,\mu}
   =\{K:\lambda^{\mathsf T}K=0,\ K\mu=0\}.                  \tag{A7}
\]

Conversely, \(K\mu=0\) says that \(K\) factors through
\(\mathbb C^3/\mathbb C\mu\), while \(\lambda^{\mathsf T}K=0\) says its
image lies in \(X\).  Hence

\[
 {\cal Q}_{\lambda,\mu}
 \simeq\operatorname{Hom}(\mathbb C^3/\mathbb C\mu,X)
 \simeq X\otimes Y,                                        \tag{A8}
\]

where the last identification uses the fixed bilinear coordinate
pairing.  In particular,

\[
                         \dim{\cal Q}_{\lambda,\mu}=2\cdot2=4. \tag{A9}
\]

The six displayed scalar radical equations have one compatibility
relation,

\[
             (\lambda^{\mathsf T}K)\mu
                =\lambda^{\mathsf T}(K\mu),                 \tag{A10}
\]

so their total rank is five, another check of (A9).

## 5. Literal response cancellation: PASS

Write \(p_i=\lambda_iU+p_i^B\) and
\(s_j=\mu_jV+s_j^B\).  Direct expansion gives

\[
\begin{aligned}
 r(K)
 ={}&(\lambda^{\mathsf T}K\mu)UV\\
 &+U\sum_j(\lambda^{\mathsf T}K)_j s_j^B
   +V\sum_i(K\mu)_i p_i^B
   +\sum_{i,j}K_{ij}p_i^Bs_j^B.                            \tag{A11}
\end{aligned}
\]

For \(K\in{\cal Q}_{\lambda,\mu}\), the first term vanishes from either
radical equation, the \(AB\) term vanishes from
\(\lambda^{\mathsf T}K=0\), and the \(BA\) term vanishes from
\(K\mu=0\).  Therefore

\[
                   r(K)=\sum_{i,j}K_{ij}p_i^Bs_j^B
                        =p_B^{\mathsf T}Ks_B.                \tag{A12}
\]

This is coefficientwise cancellation in the original response, not a
quotient modulo an annihilator and not cancellation after multiplication
by a power of \(q\).

## 6. Three-site support and cleanliness: PASS

Every nonzero monomial in (A12) occupies two distinct sites of \(B\);
same-site products vanish in the site-square-zero algebra.  If
\(|B|\le3\), any two two-element subsets of \(B\) intersect.  Hence every
product of two response monomials repeats at least one site and

\[
                             r(K)^2=0,\qquad r(K)^{[2]}=0.   \tag{A13}
\]

The bound is sharp as a support statement: on four sites, two disjoint
response edges can have a nonzero product.

The exact homogeneous cap error from
[the clean-pair descent theorem](clean-pair-cap-exact-descent-target.md)
is

\[
 {\cal E}(K)=\sum_{j=2}^{h}
     \sigma(K)^{h-j}q^{[h-j]}r(K)^{[j]}.                   \tag{A14}
\]

Equation (A13) implies \(r(K)^{[j]}=0\) for all \(j\ge2\), so every
\(K\in{\cal Q}_{\lambda,\mu}\) is clean.  No divided-power factor is
missing: \(r^{[2]}=r^2/2!\), and it vanishes because the ordinary square
does.

The descent theorem separately requires activity,

\[
                     \sigma(K)K_{00}K_{11}K_{22}\ne0.       \tag{A15}
\]

Thus an inactive scalar-zero point is clean but does not by itself give a
descent, exactly as the source states.

## 7. Exact diagonal functionals: PASS

For a fixed target label \(i\), let \(f_i(x)=x_i\) and \(g_i(y)=y_i\).
On a spanning rank-one matrix \(xy^{\mathsf T}\in X\otimes Y\),

\[
                       \kappa_i(xy^{\mathsf T})=f_i(x)g_i(y). \tag{A16}
\]

The tensor-product functional \(f_i|_X\otimes g_i|_Y\) is zero exactly
when at least one factor is zero.  Moreover,

\[
\begin{aligned}
 f_i|_X=0
 &\Longleftrightarrow e_i^{\mathsf T}
       \in(\ker\lambda^{\mathsf T})^\perp
  \Longleftrightarrow\lambda\parallel e_i,\\
 g_i|_Y=0
 &\Longleftrightarrow e_i^{\mathsf T}
       \in(\ker\mu^{\mathsf T})^\perp
  \Longleftrightarrow\mu\parallel e_i.                     \tag{A17}
\end{aligned}
\]

Therefore

\[
 \boxed{\;
 \kappa_i|_{{\cal Q}_{\lambda,\mu}}=0
 \Longleftrightarrow
 \lambda\parallel e_i\ \text{or}\ \mu\parallel e_i .
 \;}                                                        \tag{A18}
\]

This is an identity in the original fixed coordinates.  A generic basis
change sending \(\lambda\) to \(e_i\) would also rotate the diagonal target
functionals and is neither used nor permitted.

The fixed-endpoint interpretation follows literally.  If
\(\lambda\parallel e_i\), then \(p_j^A=0\) for \(j\ne i\), so only fixed
row \(i\) of the first endpoint survives on \(A\).  If
\(\mu\parallel e_i\), only fixed column \(i\) of the second endpoint
survives there.

## 8. The bilinear scalar annihilator: PASS

The cap contraction uses the entrywise complex-bilinear pairing

\[
                 \langle a,K\rangle=\sum_{i,j}a_{ij}K_{ij}
                    =\operatorname{tr}(a^{\mathsf T}K),     \tag{A19}
\]

not a Hermitian pairing.  There are no complex conjugates.

For arbitrary \(z,w\in\mathbb C^3\) and \(K\in{\cal Q}_{\lambda,\mu}\),

\[
\begin{aligned}
 \langle\lambda z^{\mathsf T},K\rangle
     &=\lambda^{\mathsf T}Kz=0,\\
 \langle w\mu^{\mathsf T},K\rangle
     &=w^{\mathsf T}K\mu=0.                                \tag{A20}
\end{aligned}
\]

Thus

\[
 L:=(\mathbb C\lambda)\otimes\mathbb C^3
       +\mathbb C^3\otimes(\mathbb C\mu)
       \subseteq{\cal Q}_{\lambda,\mu}^{\perp}.             \tag{A21}
\]

The two three-dimensional summands meet exactly in
\(\mathbb C(\lambda\mu^{\mathsf T})\), so \(\dim L=3+3-1=5\).
Since the entrywise pairing on the nine-dimensional matrix space is
nondegenerate and \(\dim{\cal Q}=4\), its annihilator also has dimension
five.  Hence equality holds:

\[
 \boxed{\;
 {\cal Q}_{\lambda,\mu}^{\perp}
  =\{\lambda z^{\mathsf T}+w\mu^{\mathsf T}:z,w\in\mathbb C^3\}.
 \;}                                                        \tag{A22}
\]

Consequently

\[
 \boxed{\;
 \sigma|_{\cal Q}=0
 \Longleftrightarrow
 a=\lambda z^{\mathsf T}+w\mu^{\mathsf T}
 \text{ for some }z,w\in\mathbb C^3 .
 \;}                                                        \tag{A23}
\]

The order in (A22) is essential and correct: the first radical produces
\(\lambda z^{\mathsf T}\), while the second produces
\(w\mu^{\mathsf T}\).  Replacing these by transposed summands would in
general be false.

## 9. Finite-hyperplane completion: PASS

The scalar \(\sigma|_{\cal Q}\) and the three diagonal restrictions
\(\kappa_i|_{\cal Q}\) are four homogeneous linear functionals on the
four-dimensional vector space \({\cal Q}\).  If any one is identically
zero, no point of \({\cal Q}\) is active.  Conversely, if none is
identically zero, their four kernels are proper linear hyperplanes.
A finite union of proper linear subspaces cannot cover a vector space
over the infinite field \(\mathbb C\).  Hence there is a \(K\in{\cal Q}\)
outside their union, and

\[
                         \sigma(K)\prod_{i=0}^2K_{ii}\ne0.   \tag{A24}
\]

Combining (A18), (A23), and (A24) proves the exact equivalence

\[
\begin{aligned}
 {\cal Q}\text{ contains an active clean cap}
 \quad\Longleftrightarrow\quad&
 a\notin{\cal Q}^{\perp},\\
 &\lambda\not\parallel e_i,\quad
   \mu\not\parallel e_i\quad(0\le i\le2).                  \tag{A25}
\end{aligned}
\]

The infinite-field hypothesis is used only here and is satisfied by the
stated ground field.

## 10. Correct scope of the scalar and coordinate gates

The negation of (A25) gives the exact inactivity alternatives for this
clean subspace:

\[
 \boxed{
 \begin{array}{ll}
 \text{scalar gate:}&
 a=\lambda z^{\mathsf T}+w\mu^{\mathsf T};\\[1mm]
 \text{coordinate gate:}&
 \lambda\parallel e_i\text{ or }\mu\parallel e_i
 \text{ for some }i.
 \end{array}}                                               \tag{A26}
\]

These alternatives may overlap.  They are sufficient and necessary for
the absence of an active member of \({\cal Q}\); they are only necessary
conditions for the absence of every active clean cap in the full
nine-dimensional cap space.

On the scalar gate, contraction of the complete physical rows gives the
literal family

\[
 (p_B^{\mathsf T}Ks_B)q^{[h-1]}
       =\sum_iK_{ii}X_i\qquad(K\in{\cal Q}).                  \tag{A27}
\]

For the intended maximal deficient shore, \(|B|=3\).  An edge of
\(p_B^{\mathsf T}Ks_B\) occupies two complement sites, while the remaining
site can participate in \(q^{[h-1]}\).  Thus the left side need not be a
single decomposable tensor across \(B\mid A\), and the two-site Schmidt-rank
argument does not close this scalar gate.

For completeness, the broader hypothesis \(|B|\le3\) has a sharper
low-\(B\) boundary.  Assume the scalar gate and no coordinate gate.  The
three nonzero diagonal functionals have a common \(K\in{\cal Q}\) with
\(K_{00}K_{11}K_{22}\ne0\).

* If \(|B|\le1\), every quadratic supported on \(B\) is zero, so (A27)
  contradicts linear independence of \(X_0,X_1,X_2\).
* If \(|B|=2\), the response occupies both sites of \(B\), and collision
  leaves

  \[
  (p_B^{\mathsf T}Ks_B)\otimes q_A^{[h-1]}
   =\sum_iK_{ii}
       (e_i^{(u)}e_i^{(v)})\otimes Y_i^A.                  \tag{A28}
  \]

  The left side has Schmidt rank at most one and the right side rank
  three, a contradiction.

This is the scope correction made to the source.  It does not eliminate
the maximal \(|B|=3\) scalar gate, and it does not classify cases in which
a scalar gate overlaps one or more coordinate gates.

## 11. Exact remaining open target

For the maximal \(b=3\), rank-\((1,1)\) shore, the unresolved target is to
eliminate or descend within:

1. the scalar-annihilator family (A27), with
   \(a=\lambda z^{\mathsf T}+w\mu^{\mathsf T}\); or
2. a fixed-coordinate endpoint
   \(\lambda\parallel e_i\) or \(\mu\parallel e_i\).

At eight sites
[`n8-rank11-scalar-released-site-three-target-closure.md`](n8-rank11-scalar-released-site-three-target-closure.md)
shows that no one-site release can expose all three labels: the released
site is a common zero of the two multiplier rows, so a three-colour diagonal
response would force all three individual targets.  Its equality and
blocker-incidence arguments force a literal local coordinate plane on the
dark shore or physical complement.  The surviving first case is therefore
the transport of that plane through the four adjacent response-catalecticant
columns from Section 6 of the endpoint-dark shore note.  The second case
still requires additional
fixed-label rows; rotating the endpoint line to a convenient coordinate
axis is not allowed.

Neither gate is declared impossible by the clean-plane argument itself.
The result is therefore an exact generic reduction of the maximal
rank-\((1,1)\) shore, not a closure of its coordinate or scalar boundary.
