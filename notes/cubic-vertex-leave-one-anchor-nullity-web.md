# A cubic vertex forces a threefold leave-one-anchor nullity web

## 1. Result

Let \(B\) have even cardinality \(N\geq8\), let every local target space
be \(V_v\cong\mathbb C^3\), and suppose hypothetically that

\[
                         H_B(A)=\Delta_{B,3}.             \tag{1}
\]

Assume that a support vertex \(p\) is cubic.  Cubic-vertex rigidity gives
three distinct neighbours \(a_0,a_1,a_2\) and nonzero scalars
\(\lambda_c\) such that

\[
 A_{p a_c}=\lambda_c e_c^{(p)}\otimes e_c^{(a_c)},
 \qquad
 H_{B\setminus\{p,a_c\}}(A)
   =\lambda_c^{-1}e_c^{\otimes(B\setminus\{p,a_c\})}.
                                                               \tag{2}
\]

Fix any nonneighbour \(q\) of \(p\).  There are exactly \(N-4\) choices
of \(q\).  Put \(W=B\setminus\{p,q\}\), let \(x\) be the quadratic
formed by the blocks internal to \(W\), and, for each \(c\), put

\[
                     K_c=W\setminus\{a_c\}.             \tag{3}
\]

Define the complete leave-one-anchor cofactor map

\[
 \begin{aligned}
 \Phi_{q,c}:\bigoplus_{v\in K_c}V_v
     &\longrightarrow \bigotimes_{v\in K_c}V_v,\\
 (z_v)_{v\in K_c}&\longmapsto
   \sum_{v\in K_c}z_v^{(v)}\otimes
       H_{K_c\setminus\{v\}}(x).
 \end{aligned}                                           \tag{4}
\]

All slots in (4) are restored to physical order.  Equivalently, if
\(N=2m\), (4) is the full-support component of

\[
                 \left(\sum_{v\in K_c}z_v\right)
                 {x^{m-2}\over(m-2)!}.                  \tag{5}
\]

**Theorem 1.1 (cubic nullity web).**  For every nonneighbour \(q\),

\[
 \boxed{
    \dim\ker\Phi_{q,c}\geq1\quad(c=0,1,2),
    \qquad
    \#\{c:\dim\ker\Phi_{q,c}\geq2\}\geq2.}           \tag{6}
\]

Thus all three maps are singular and their three nullities have sum at
least five.  In matrix language, each map has \(3(N-3)\) columns; all
three maximal-column minors vanish, and for at least two colours all
minors of size \(3(N-3)-1\) vanish as well.

This is an unconditional consequence of the exact mixed equations.  It
uses no genericity, positivity, entry minimality, supportwise
noncancellation, or symmetry of endpoint blocks.  Zero blocks and
arbitrary complex cancellation are retained.

## 2. The nine equations seen from a nonneighbour

Orient the blocks at \(q\) toward \(q\), and write their three complete
rows into \(W\) as

\[
 s_d=\sum_{v\in W}s_{d,v},\qquad
 s_{d,v}=(e_d^*\otimes\operatorname{id})A_{q\mid v}
          \in V_v.                                      \tag{7}
\]

Let \(\pi_c\) delete the component at \(a_c\):

\[
        \pi_c:\bigoplus_{v\in W}V_v
                  \longrightarrow\bigoplus_{v\in K_c}V_v. \tag{8}
\]

Expand the pure cofactor in (2) at its site \(q\), then contract the
\(q\)-slot by \(e_d^*\).  The result is the complete, cancellation-safe
identity

\[
 \boxed{
 \Phi_{q,c}(\pi_cs_d)
   =\delta_{cd}\lambda_c^{-1}
       e_c^{\otimes K_c}.}                               \tag{9}
\]

In particular, for fixed \(c\), both wrong-colour restrictions

\[
                  \pi_cs_d,\ \pi_cs_e\in\ker\Phi_{q,c},
        \qquad\{c,d,e\}=\{0,1,2\}.                     \tag{10}
\]

Both deleted endpoint stars of the zero-direct pair \(p,q\) are
aggregate-injective.  At \(p\) this is visible from the three distinct
cells in (2).  At \(q\), the target flattening spans all of \(V_q\), and
deleting the zero block \(A_{qp}\) removes no endpoint support.  Hence
the three global rows in (7) are linearly independent.  The proof below
in fact needs only the nonzero diagonal equations in (9).

## 3. Two wrong rows cannot collapse to one nonzero kernel line

We first record the exact shared-cofactor factorization behind (4).  For
distinct anchors \(a_c,a_b\), put

\[
                 T_{cb}=H_{W\setminus\{a_c,a_b\}}(x).  \tag{11}
\]

If \(z\) is supported only at \(a_b\), then

\[
                       \Phi_{q,c}(z)=z^{(a_b)}\otimes T_{cb}.
                                                               \tag{12}
\]

This is an identity of complete matching tensors, not a selected matching
term.

**Lemma 3.1.**  Fix \(c\), and let \(d,e\) be the other two colours.
The two kernel vectors in (10)

1. cannot both vanish; and
2. cannot be nonzero and proportional.

Consequently they are either linearly independent, or exactly one is
zero and the other is nonzero.

**Proof.**  Suppose first that both vanish.  Then \(s_d\) and \(s_e\)
are supported only at \(a_c\).  Apply the diagonal equation for colour
\(d\).  Since \(a_c\ne a_d\), equations (9) and (12) give

\[
 s_{d,a_c}^{(a_c)}\otimes T_{dc}
       =\lambda_d^{-1}e_d^{\otimes K_d}\ne0.            \tag{13}
\]

Thus both factors on the left are nonzero.  The off-diagonal equation for
row \(e\) in the same map gives

\[
                         s_{e,a_c}^{(a_c)}\otimes T_{dc}=0, \tag{14}
\]

so \(s_e=0\).  This contradicts its nonzero diagonal equation in (9).

Now suppose

\[
                         \pi_cs_e=t\,\pi_cs_d,
                         \qquad t\ne0.                  \tag{15}
\]

Then \(v=s_e-ts_d\) is supported only at \(a_c\).  Applying the maps
with diagonal colours \(d\) and \(e\) gives

\[
 \begin{aligned}
 \Phi_{q,d}(\pi_dv)&=-t\lambda_d^{-1}e_d^{\otimes K_d},\\
 \Phi_{q,e}(\pi_ev)&= \lambda_e^{-1}e_e^{\otimes K_e}.
 \end{aligned}                                          \tag{16}
\]

Both are nonzero.  In the first equality the factor at site \(a_c\) is
the single vector \(v_{a_c}\), so uniqueness of factors of a nonzero
decomposable tensor forces \(v_{a_c}\in\mathbb C^*e_d\).  The second
equality forces the same vector into \(\mathbb C^*e_e\), impossible for
\(d\ne e\).  This proves both assertions. \(\square\)

Lemma 3.1 immediately proves that every \(\Phi_{q,c}\) is singular.  It
also shows that if its nullity is one, there is a unique wrong colour
\(\rho(c)\ne c\) for which

\[
                         \pi_cs_{\rho(c)}=0.             \tag{17}
\]

Equivalently, the entire row \(s_{\rho(c)}\) is supported at the single
anchor \(a_c\).

## 4. Two nullity-one anchors are incompatible

**Lemma 4.1.**  For fixed \(q\), at most one of the three maps
\(\Phi_{q,c}\) has nullity one.

**Proof.**  Suppose two do, say the maps indexed by distinct colours
\(c,b\).  Let \(\rho(c),\rho(b)\) be supplied by (17).  These two colours
are distinct: otherwise the same nonzero global row would be supported in
both distinct direct summands \(V_{a_c}\) and \(V_{a_b}\).

Use the shared cofactor \(T_{cb}\) from (11).  The local row
\(s_{\rho(b)}\), supported at \(a_b\), gives under \(\Phi_{q,c}\)

\[
 \begin{cases}
 s_{c,a_b}\otimes T_{cb}
       =\lambda_c^{-1}e_c^{\otimes K_c}\ne0,
       &\rho(b)=c,\\
 s_{\rho(b),a_b}\otimes T_{cb}=0,
       &\rho(b)\ne c.
 \end{cases}                                             \tag{18}
\]

Since the displayed local row is nonzero, (18) says respectively that
\(T_{cb}\ne0\), with pure colour \(c\), or that \(T_{cb}=0\).  Reversing
\(b,c\) gives

\[
 \begin{cases}
 T_{cb}\ne0\text{ and has pure colour }b,&\rho(c)=b,\\
 T_{cb}=0,&\rho(c)\ne b.
 \end{cases}                                             \tag{19}
\]

There are only three colours.  Because
\(\rho(c)\ne c\), \(\rho(b)\ne b\), and
\(\rho(c)\ne\rho(b)\), either

* exactly one of \(\rho(b)=c\), \(\rho(c)=b\) holds; or
* both hold.

In the first case (18)--(19) make \(T_{cb}\) simultaneously zero and
nonzero.  In the second they make its nonzero tensor on
\(W\setminus\{a_c,a_b\}\) simultaneously a pure constant tensor of
colours \(c\) and \(b\).  This set has \(N-4\ge4\) sites, so the two
constant tensors are nonproportional.  Both cases are impossible.
\(\square\)

Lemmas 3.1 and 4.1 prove Theorem 1.1.

## 5. Consequences and remaining gate

For every cubic vertex, Theorem 1.1 produces the following uniform
determinantal ledger:

\[
 \begin{array}{c|c|c}
 \text{objects}&\text{forced singular}&\text{forced nullity at least two}\\ \hline
 \Phi_{q,c}&3(N-4)&2(N-4)
 \end{array}                                             \tag{20}
\]

The second count means that at least two maps for each fixed \(q\) have
the stronger nullity; the same map is not counted across different
\(q\)'s.  At \(N=8\), for example, each map is a
\(3^5\)-by-15 cofactor matrix.  All twelve maps are singular and at least
eight have rank at most thirteen.

This excludes a cubic vertex on the open chart where any one of the three
maps is injective, and also on the larger chart where two of them have
nullity at most one.  It upgrades the generic cubic survivor to an
overlapping high-corank locus for every one of its \(N-4\) zero-direct
pairs.

It is not yet an all-even descent.  Singular common-cofactor maps can
occur in active, nondiagonal cancellation sources, so the ranks in (20)
cannot simply be declared diagonal.  A continuation must use compatibility
of the actual kernel vectors as \(q\) and \(c\) vary.  Two concrete next
targets are:

1. show that one of the forced extra kernel directions lifts to a
   support-reducing variation of the \(q\)-star, modulo the unavoidable
   target torus; or
2. combine two nonneighbours \(q,q'\) and the common lower cofactors to
   force a clean two-vertex cap or a tight three-separator.

The exact checker
[verify_cubic_vertex_leave_one_anchor_nullity_web.py](../computations/verify_cubic_vertex_leave_one_anchor_nullity_web.py)
audits the matching expansion (9), the shared-cofactor identity (12), the
three-colour nullity-one incompatibility, and the rank/count ledger (20).
