# Inactive roots at the first \(8\to6\) boundary: a conditional matrix-cap problem

## 1. Outcome

Fix \(h=3\), hence the first \(8\to6\) pair boundary, and assume a canonical
line with the displayed diagonal unary and scalar-zero clean endpoints.
Then the complete unary root, the complete scalar-zero complementary root,
and every transverse two-site coefficient can be written in one lossless
four-site system. The system is displayed in Section 3. Its two residual
columns are exactly the two Omega tensors, not proxies for them.

The useful structural conclusion is that the two-chart problem is **not**
a scalar four-cut problem. All nine pair covectors form one matrix-valued
cap connection. The unary effective quadratic is its \(00\)-entry, the
scalar-zero response is the trace of its \(11,22\) entries, the six
off-diagonal rows are its Koszul cycle, and the three diagonal target rows
are its fixed anchors. Section 4 gives the source-level connection before
any common power is multiplied in.

For two overlapping charts already satisfying the additional hypotheses
listed in Section 6, this identifies the following focused bounded target:

> **Conditional anchored matrix-cap exclusion.** On two overlapping
> diagonal full-nine \(h=3\) charts with their displayed simultaneous clean
> endpoints and a nonzero selected \(0000\) curvature minor, two bad Omega
> maps cannot coexist: at least one chart has a kernel vector with both
> pencil coordinates nonzero.

The exact direct formulation is (23). It is an open conditional implication,
not an output of the present selection theorem. A separate, stronger
intersection lemma could also address a compatible common-coloop corner,
but only after that corner, its scalar-zero contraction, and a visible label
with \(K_{cc}\ne0\) are added as hypotheses; Section 7 keeps this distinction
explicit.

The audited inputs do **not** prove (23), do not supply its hypotheses from
an arbitrary curved line, and do not extract this \(h=3\) packet uniformly
from higher order. In particular,
two transported anchors align two axes but leave a relative torus, a
crossed target-zero row is invariant under that torus, and the four-index
row \((r,r;s,s)\) is not the endpoint cell \(E_{rs}\). The ordinary
four-cut multiplication map also mixes exterior curvature with symmetric
matching squares. Consequently no proof of the full transverse
two-chart exclusion is claimed here. What is proved below is the exact
one-chart \(h=3\) algebra, the literal source-provenant connection, and the
precise conditional target still needed. No conjecture-level or uniform
reduction is claimed.

The inputs used are the audited
[two-root polarization](curved-two-root-polarization-and-four-cut-square.md),
[complementary-row frontier](curved-complementary-row-coupling-frontier.md),
[two-chart guard pair](curved-two-chart-offdiagonal-anchor-complementarity.md),
[two-anchor correction](selector-hall-and-one-anchor-threshold-independent-audit.md),
[common-coloop quotient](common-coloop-full-nine-residual-coupling.md),
and its [flat odd-residue transport](common-coloop-odd-residue-and-flat-overlap.md).

## 2. The conditional one-chart \(h=3\) packet

Work on six residual sites \(W\) in the site-square-zero algebra

\[
 {\cal R}_W=\bigotimes_{x\in W}(\mathbb C\oplus V_x),
 \qquad V_xV_x=0.
\]

Let \(q\in({\cal R}_W)_2\) be the internal quadratic. This section assumes,
rather than derives, a canonical diagonal binary line with a clean unary
point \(K_0\) and a clean scalar-zero complementary point \(K_1\), with
\(\sigma\ne0\) and

\[
 \begin{array}{c|ccc}
       &s&F&T\\ \hline
 K_0&\sigma&F=\sigma q+P_0S_0&X_0\\
 K_1&0&R=-(P_1S_1+P_2S_2)&-(X_1+X_2).
 \end{array}                                                   \tag{1}
\]

The complete physical and clean equations are

\[
 \begin{aligned}
 Fq^{[2]}-2\sigma q^{[3]}&=X_0,
 &F^{[3]}&=\sigma^2X_0,\\
 Rq^{[2]}&=-(X_1+X_2),
 &R^{[3]}&=0.                                                  \tag{2}
 \end{aligned}
\]

At \(h=3\), the two-root polarization theorem gives

\[
 {\cal E}(\lambda K_0+\mu K_1)
   =\lambda\mu(\lambda\Omega _0+\mu\Omega _1),                \tag{3}
\]

where, using the physical complementary row,

\[
 \boxed{
 \Omega _0=R\bigl(F^{[2]}-\sigma^2q^{[2]}\bigr),
 \qquad
 \Omega _1=R^{[2]}F.}                                        \tag{4}
\]

Activity on this line is exactly \(\lambda\mu\ne0\). Hence the line has no
active clean point precisely when

* \(\Omega _0,\Omega _1\) are independent; or
* exactly one of \(\Omega _0,\Omega _1\) is zero.

Nonzero dependence, or two zero columns, gives an active clean point.
Thus all of the inactive-root geometry is the kernel geometry of the map

\[
 \Phi:\mathbb C^2\longrightarrow({\cal R}_W)_6,
 \qquad (\lambda,\mu)\longmapsto
                  \lambda\Omega _0+\mu\Omega _1.              \tag{5}
\]

The bad condition is the coordinate-free statement

\[
                 \ker\Phi\cap(\mathbb C^*)^2=\varnothing.     \tag{6}
\]

This formulation is useful because diagonal changes of the two anchored
axes rescale rows and columns but do not change (6).

## 3. Lossless transverse two-cut formulas at \(h=3\)

Choose two residual sites \(r,s\in W\), fix their physical colours
\(c,d\), and put \(D=W\setminus\{r,s\}\). In the selected coefficient
write

\[
\begin{aligned}
q&=z+e_{r,c}t+e_{s,d}v+e_{r,c}e_{s,d}U+\cdots,\\
F&=f+e_{r,c}L+e_{s,d}H+e_{r,c}e_{s,d}M+\cdots,\\
R&=\rho+e_{r,c}\alpha+e_{s,d}\beta
       +e_{r,c}e_{s,d}\gamma+\cdots .                        \tag{7}
\end{aligned}
\]

Here \(z,f,\rho\) are quadratics on \(D\),
\(t,v,L,H,\alpha,\beta\) are linear forms on \(D\), and
\(U,M,\gamma\) are scalars. Direct divided-power expansion gives the two
linear-in-\(R\) polars

\[
\begin{aligned}
 {\sf B}_q(R)&=
   \gamma z^{[2]}+(\alpha v+\beta t+\rho U)z+\rho tv,\\
 {\sf B}_F(R)&=
   \gamma f^{[2]}+(\alpha H+\beta L+\rho M)f+\rho LH,          \tag{8}
\end{aligned}
\]

and the two quadratic-in-\(R\) polars

\[
\begin{aligned}
 {\sf C}(R)&=\gamma\rho^{[2]}+\alpha\beta\rho,\\
 {\sf Q}_F(R)&=
   M\rho^{[2]}+(L\beta+H\alpha+f\gamma)\rho+f\alpha\beta.
                                                                    \tag{9}
\end{aligned}
\]

These are not definitions chosen to resemble the top rows. They are
literally the \((r,c),(s,d)\)-coefficients of, respectively,

\[
 Rq^{[2]},\qquad RF^{[2]},\qquad R^{[3]},\qquad R^{[2]}F.       \tag{10}
\]

Therefore (2) is equivalent, on this cut, to

\[
\boxed{\begin{aligned}
{\sf B}_q(R)
 &=-\delta_{c1}\delta_{d1}X_1^D
   -\delta_{c2}\delta_{d2}X_2^D,\\
{\sf C}(R)&=0,\\
Mz^{[2]}+(Lv+Ht+fU)z+ftv
 -2\sigma\bigl(Uz^{[2]}+tvz\bigr)
 &=\delta_{c0}\delta_{d0}X_0^D,\\
Mf^{[2]}+LHf&=\sigma^2\delta_{c0}\delta_{d0}X_0^D.
                                                               \tag{11}
\end{aligned}}\]

Most importantly, the two Omega columns have the exact transverse
coefficients

\[
 \boxed{
  \omega _0={\sf B}_F(R)-\sigma^2{\sf B}_q(R),
  \qquad
  \omega _1={\sf Q}_F(R).}                                   \tag{12}
\]

Collecting (12) for all \(c,d\) is an injective coefficient encoding of
each top tensor. Thus no Omega information is discarded in passing to
(11)--(12). Conversely, (11) shows why the binary target row alone does
not determine the Omega columns: it fixes \({\sf B}_q(R)\), while the
uncontrolled second polars are \({\sf B}_F(R)\) and \({\sf Q}_F(R)\).
The deconcentrated complementary packet is exactly a witness to this
distinction.

In particular, the two endpoint-degenerate alternatives have the
coefficientwise forms

\[
\begin{aligned}
 \Omega_0=0
 &\Longleftrightarrow
 {\sf B}_F(R)=\sigma^2{\sf B}_q(R)
       \quad\text{on every transverse cut},\\
 \Omega_1=0
 &\Longleftrightarrow
 {\sf Q}_F(R)=0
       \quad\text{on every transverse cut}.                  \tag{12a}
\end{aligned}
\]

The first is equality of two literal mixed polars; the second is a
consecutive-power annihilator condition. Neither is implied by
\(R^{[3]}=0\).

## 4. The source-faithful matrix-cap connection

Now expose four source sites \(p,q,r,s\) and put
\(D=B\setminus\{p,q,r,s\}\). Retain all row labels. Write the six direct
blocks, in endpoint order, as

\[
\begin{array}{lll}
A_{ij}=A_{pq}(i,j),&B_{ik}=A_{pr}(i,k),&C_{jk}=A_{qr}(j,k),\\
E_{i\ell}=A_{ps}(i,\ell),&F_{j\ell}=A_{qs}(j,\ell),
   &U_{k\ell}=A_{rs}(k,\ell),
\end{array}                                                    \tag{13}
\]

and let \(x_i,y_j,t_k,v_\ell\) be the corresponding star rows into
\(D\). The \(pq\)-cap attached to the matrix unit \(E_{ij}\) has

\[
\begin{aligned}
 f_{ij}&=A_{ij}z+x_i y_j,\\
 L_{ij;k}&=A_{ij}t_k+B_{ik}y_j+C_{jk}x_i,\\
 H_{ij;\ell}&=A_{ij}v_\ell+E_{i\ell}y_j+F_{j\ell}x_i,\\
 M_{ij;k\ell}&=A_{ij}U_{k\ell}
          +B_{ik}F_{j\ell}+E_{i\ell}C_{jk}.                  \tag{14}
\end{aligned}
\]

The \(pr\)-cap attached to \(E_{ik}\) has

\[
\begin{aligned}
 g_{ik}&=B_{ik}z+x_i t_k,\\
 L_{ij;k}&=B_{ik}y_j+A_{ij}t_k+C_{jk}x_i,\\
 N_{ik;\ell}&=B_{ik}v_\ell+E_{i\ell}t_k+U_{k\ell}x_i,\\
 M_{ij;k\ell}&=B_{ik}F_{j\ell}
          +A_{ij}U_{k\ell}+E_{i\ell}C_{jk}.                  \tag{15}
\end{aligned}
\]

The common \(L\) and \(M\) are literal. Direct expansion gives, for
every \(i,j,k,\ell\),

\[
\boxed{\begin{aligned}
 f_{ij}t_k-g_{ik}y_j
   &=(A_{ij}t_k-B_{ik}y_j)z,\\
 U_{k\ell}f_{ij}+t_kH_{ij;\ell}
   -F_{j\ell}g_{ik}-y_jN_{ik;\ell}
   &=(A_{ij}t_k-B_{ik}y_j)v_\ell
      +(A_{ij}U_{k\ell}-B_{ik}F_{j\ell})z.                  \tag{16}
\end{aligned}}\]

Equation (16) is the source-faithful matrix connection on which a comparison
map could be built. It holds before a top common power, before traces are
taken, and before endpoint colours are conflated. For the conditional
two-chart target below, impose the additional selected-colour hypothesis

\[
             \kappa=A_{00}U_{00}-B_{00}F_{00}\ne0.            \tag{17}
\]

The uniform curvature-selection theorem only supplies some nonzero minor
\(A_{ab}U_{cd}-B_{ac}F_{bd}\). It does not supply (17): the pure targets tie
the colour labels across sites, so independent relabelling cannot in general
move that minor to \(0000\). Nor does curvature selection supply simultaneous
diagonal unary and complementary clean endpoints on both overlapping charts.
Those are separate hypotheses throughout Sections 6--7.

On the full \(pq\)-residual put

\[
 {\mathfrak f}_{ij}=A_{ij}q+P_iS_j,
\]

whose selected cut data are (14). The unary effective quadratic is
\({\mathfrak f}_{00}\). If \(A_{11}+A_{22}=0\), the complementary
response is the negative trace

\[
              R_{pq}=-({\mathfrak f}_{11}+{\mathfrak f}_{22}).
                                                                    \tag{18}
\]

The scalar terms cancel in (18), leaving exactly
\(-(P_1S_1+P_2S_2)\); every cut jet is therefore the negative trace of
the corresponding entries in (14). Similarly put
\({\mathfrak g}_{ik}=B_{ik}q'+P'_iT_k\) on the full \(pr\)-residual.
If \(B_{11}+B_{22}=0\), then

\[
              R_{pr}=-({\mathfrak g}_{11}+{\mathfrak g}_{22}).
                                                                    \tag{19}
\]

Thus the unary and complementary packets are not separate decorations of
the overlap. They are the \(00\)-entry and the complementary diagonal
trace of the same matrix connection. The six off-diagonal entries supply
the primitive \(K_{3,3}\setminus\{00,11,22\}\) Koszul cycle, while the
three diagonal physical rows anchor its flags. This is the shared
structure which the diagonal-only and off-diagonal-only guards separate.

## 5. Why the scalar four-cut cannot be the comparison lemma

Tracing (16) over \(11,22\) does not produce a scalar connection of the
same form. The two diagonal terms have different multipliers
\(t_1,y_1\) and \(t_2,y_2\). The off-diagonal rows are exactly what can
couple those two connections. Dropping them leaves the audited
diagonal-row guard; dropping the diagonal anchors leaves the independent
and exactly-one-zero off-diagonal guards.

There are three further obstructions to a shorter scalar argument.

1. The inverse of \(\kappa\) is exterior-square data, whereas a two-star
   matching response contains same-channel symmetric squares. Hence
   inverting (17) does not project (18) onto a physical matching row.
2. Two diagonal anchors fix two axes but retain the action

   \[
       G=\operatorname {diag}(g_r,g_s,1),\qquad
       H=\operatorname {diag}(g_r^{-1},g_s^{-1},1).            \tag{20}
   \]

   It fixes \(E_{rr},E_{ss}\) and scales \(E_{rs}\) by \(g_s/g_r\).
   A crossed target-zero row remains zero under this action and therefore
   cannot determine the relative scale.
3. The coefficient-dark four-index row \((r,r;s,s)\) is a diagonal
   endpoint cell evaluated on another cut colour. It is not \(E_{rs}\).
   Its conditional coefficient-dark contradiction remains valid, but it
   cannot be substituted for the missing overlap character.

The matrix connection (16) avoids all three mistakes. It retains endpoint
order and row labels, and it is covariant under (20); no arbitrary relative
normalization is required.

## 6. Exact conditional bad-locus formulation on two \(h=3\) charts

For \(\chi\in\{pq,pr\}\), let

\[
 \Phi_\chi=(\Omega_{\chi0}\ \ \Omega_{\chi1}):
       \mathbb C^2\longrightarrow({\cal R}_{W_\chi})_6.       \tag{21}
\]

Let \({\sf Cut}_\chi\Phi_\chi\) be the collection of (12) over all
two-site cuts and all physical colours. Coefficient decomposition gives

\[
 \ker({\sf Cut}_\chi\Phi_\chi)=\ker\Phi_\chi,
 \qquad
 \operatorname {rank}({\sf Cut}_\chi\Phi_\chi)
       =\operatorname {rank}\Phi_\chi.                        \tag{22}
\]

Now add all of the following hypotheses explicitly:

1. \(h=3\), so both residuals have six sites and their mixed endpoint
   cleanliness has exactly the two Omega columns in (21);
2. the \(pq\)- and \(pr\)-charts come from the same literal full-nine source;
3. both charts have the simultaneous diagonal unary and diagonal binary
   scalar-zero clean physical endpoints displayed in Sections 2 and 4;
4. the selected \(0000\) minor (17) is nonzero; and
5. the endpoint-star maps needed to form the displayed charts are good.

These are assumptions of the bounded problem, not consequences of the
currently proved curvature selection. Under them, the requested full
transverse two-chart statement is exactly

\[
 \boxed{
 \kappa\ne0\quad\Longrightarrow\quad
 \ker\Phi_{pq}\cap(\mathbb C^*)^2\ne\varnothing
 \quad\text{or}\quad
 \ker\Phi_{pr}\cap(\mathbb C^*)^2\ne\varnothing .}             \tag{23}
\]

There is no hidden activity condition in (23): the two coordinates are
the unary and scalar-zero endpoints, so both nonzero is precisely active.
By (22), proving (23) from (11), the full-nine coefficient cuts, and the
matrix connection (16) would exclude simultaneous independent or
exactly-one-zero Omega pairs in this conditional \(h=3\) configuration.
Equation (23) remains open.

The bounded algebra entering (23) consists of

\[
 \boxed{
 \text{matrix connection (16)}
 +\text{ diagonal target anchors}
 +\text{ off-diagonal Koszul cycle}
 +\text{ second polars (8)--(9)}.}                             \tag{24}
\]

No support classification is present in (24). Conversely, no result in this
note routes an arbitrary curvature line, selector circuit, or higher-order
packet into these hypotheses.

## 7. A separate common-coloop quotient and a conditioned bridge

The common-coloop ledger is distinct from the diagonal binary inactive-root
packet of Sections 2--6. To compare them, one must separately assume a
compatible literal \(h=3\) source with a common-coloop site \(x\) and the
common-coloop Taylor data. Write

\[
 q=q_0+\varrho,\qquad A=q_0^{[2]},\qquad
 I=\operatorname {im}(z\mapsto zA).                           \tag{25}
\]

After the literal full-nine Taylor splitting and reduction modulo
\(V_x\otimes I\), the response correction is

\[
 \overline\Gamma_{ij}
   =\delta_{ij}e_i^{(x)}\otimes\overline Y_i.                  \tag{26}
\]

If the two rank-two shore kernels are disjoint singletons \(r,s\), and
\(t\) is the third label, the entire non-descending quotient is the one
corner

\[
 \begin{array}{c|cc}
      &\bar S_r&\bar S_t\\ \hline
 \bar P_s&0&0\\
 \bar P_t&0&C_t
 \end{array},
 \qquad
 C_t=e_t^{(x)}\otimes\overline Y_t\ne0.                       \tag{27}
\]

For a scalar-zero contraction \(K\), the corner is weighted by its diagonal
coefficient \(K_{tt}\), not universally by one common scalar. The crossed
zero row is another entry of (27) and does not remove it.

There is now a canonical way to transport this corner without choosing a
relative label gauge. On the odd set \(K=W\setminus\{x\}\), put

\[
 A=q_0^{[2]},\qquad B=q_0,\qquad
 C_{q_0}=({\cal R}_K)_5/({\cal R}_K)_1A,
\]

and, for a quadratic \(Z\) and linear form \(T\), define

\[
       \operatorname {res}_{q_0}(Z;T)=[TZB]\in C_{q_0}.
                                                                    \tag{28}
\]

This odd residue kills every genuine vertex-gauge quadratic. More
importantly, let

\[
 {\cal P}_{pq}^{ij}=3P_iS_j+A_{ij}q
\]

be the canonical unnormalized cap. It is related to the raw effective cap
of Section 4 by
\({\cal P}_{pq}^{ij}=3{\mathfrak f}_{ij}-2A_{ij}q\); the added
\(q\)-term has zero odd residue. After exposing \(x\), write

\[
 q=q_0+\sum_c e_c^{(x)}t_c,\qquad
 {\cal P}_{pq}^{ij}
   =P_{pq}^{ij}+\sum_c e_c^{(x)}L_c^{ij}.
\]

The complete physical row and the power-free connection give the exact
identities

\[
\begin{aligned}
 \operatorname {res}_{q_0}(P_{pq}^{ij};t_c)
   &=3\delta_{ij}\delta_{ic}\,\overline Y_i,\\
 \operatorname {res}_{q_0}(P_{pq}^{ij};t_c)
   &=\operatorname {res}_{q_0}(P_{px}^{ic};y_j).              \tag{29}
\end{aligned}
\]

Thus the linear matrix-cap connection transports the constant-word
residue **unchanged**. It does not kill it. For a general scalar-zero
contraction \(K\), its off-\(x\) response satisfies

\[
 \boxed{\quad
 \operatorname {res}_{q_0}(\overline R_K;t_c)
       =K_{cc}\,\overline Y_c.
 \quad}                                                        \tag{30}
\]

In particular, for \(K_*=\tau E_{ab}-\alpha I\),
\[
 K_{*,cc}=\tau\delta_{a,c}\delta_{b,c}-\alpha.
\]
When \(a\ne b\), the off-diagonal common-coloop contraction sees every
label with coefficient \(-\alpha\). It is not the diagonal binary endpoint
used to derive (3)--(6). At the diagonal binary point \(E_{00}-I\), the
\(c=0\) residue vanishes while the \(c=1,2\) residues have coefficient
\(-1\). Thus the two ledgers cannot be identified without a compatibility
argument, and a surviving colour-zero corner is invisible to that binary
endpoint.

In the singleton-corner branch, if its label \(t\) satisfies
\(K_{tt}\ne0\), then (30) is precisely the nonzero class \(C_t\) of (27)
with its local \(e_t^{(x)}\)-factor removed. The physical diagonal target
row restores that factor and the deleted pair, so the corner line maps
canonically to the global line \(\mathbb C X_t^B\). Under this explicit
visibility hypothesis,

\[
          \kappa\,
          \operatorname {res}_{q_0}(\overline R_K;t_t)
       =\kappa K_{tt}\,\overline Y_t\ne0.                      \tag{31}
\]

is a literal torus-invariant coefficient. Equation (29) shows, however,
that (16) and (31) alone can never yield a contradiction: the flat
connection carries the nonzero class faithfully.

The genuinely new arrow would have to come from the nonlinear polars
(8)--(12). It is important not to conflate that possible bridge with the
direct inactive-root target (23). One well-posed but strictly stronger
intersection lemma would be:

> **Conditioned residue--Omega incidence.** Let one literal \(h=3\)
> full-nine source satisfy every two-chart hypothesis listed in Section 6.
> Assume in addition that the same source has the specified common-coloop
> singleton corner (25)--(27), that a scalar-zero Omega endpoint \(K\)
> defines the off-site response \(\overline R_K\), and that the surviving
> label \(c\) obeys both \(\overline Y_c\ne0\) and \(K_{cc}\ne0\). If both
> Omega maps obey the bad condition (6), then
> \[
>       \operatorname {res}_{q_0}(\overline R_K;t_c)=0.
> \]

Equation (30) contradicts the conclusion immediately. Equivalently, it is
enough to prove that the relevant off-site scalar-zero response becomes a
vertex-gauge quadratic, since the residue kills those gauges. In the
language of Sections 3--4, this is exactly the assertion that the
matrix-cap connection is faithful on the **nonlinear second-polar**
module, not merely on its flat first connection.

This intersection lemma has not been proved, and no result here routes
either remaining ledger into all of its simultaneous hypotheses. In
particular, the off-diagonal common-coloop contraction cannot simply be
substituted for the diagonal binary Omega endpoint; a comparison theorem
would be required. The formal full-nine
corner guard shows that the nine response products without one literal
consecutive-power representative do not prove it. The literal
consecutive-power curvature guard shows that consecutive powers without
the diagonal anchors do not prove it. The exactly-one-zero Omega guard
shows that the unary anchor and all six off-diagonal rows still do not
prove it without the complementary diagonal targets. These guards motivate
the conditioned target but do not make it a common exhaustive lemma.

## 8. What the four-site flag circuit actually supplies

The corrected minimal selector-union reduction gives a local linear
trichotomy on a complete six-site packet. It does not route that packet
into the chart hypotheses of (23). Consider its four-site flag circuit
\(A\subset W\), with

\[
 |A|=4,\qquad
 \rho_P(A)=1,\qquad \rho_S(A)=2,
 \qquad W\setminus A=\{u,v\}.                                 \tag{32}
\]

The transposed rank pair is identical after exchanging the endpoints. Put

\[
 U_P=\sum_{x\in A}L_x^P\subset{\mathsf C}^*,
 \qquad
 U_S=\sum_{x\in A}L_x^S\subset{\mathsf D}^*,
 \qquad
 \dim U_P=1,\quad\dim U_S=2.                                 \tag{33}
\]

Every selector base for the rank-one endpoint must use both \(u\) and
\(v\): the four-site core contributes rank only one and a base has rank
three. There is then a short exact linear routing.

* If one of the aggregate endpoint maps off \(u\) or off \(v\) has rank
  at most two, the packet is already in a shore residual.
* Otherwise, for each \(x\in\{u,v\}\), the local \(P\)-row space
  surjects onto the two-dimensional quotient
  \({\mathsf C}^*/U_P\), while the local \(S\)-row space maps nontrivially
  onto the one-dimensional quotient \({\mathsf D}^*/U_S\).

Indeed, for \(x=u\), full rank of the map off \(v\) says
\(U_P+L_u^P={\mathsf C}^*\) and
\(U_S+L_u^S={\mathsf D}^*\); the assertion for \(v\) is the same with the
two sites exchanged. Thus the combined local quotient map

\[
 \theta_x:V_x^*\longrightarrow
       ({\mathsf C}^*/U_P)\oplus({\mathsf D}^*/U_S)            \tag{34}
\]

has rank two or three. If it has rank two, its nonzero kernel is a
core-valued physical probe: both endpoint evaluations land back in
\(U_P,U_S\). If it has rank three, it is an isomorphism onto the full
three-dimensional transverse quotient. This is only a full-rank local
quotient probe at \(x\), not a source chart. Consequently the flag circuit
has the structural trichotomy

\[
 \boxed{\text{shore residual}\quad\text{or}\quad
        \text{core-valued probe}\quad\text{or}\quad
        \text{two full-rank local quotient maps}.}             \tag{35}
\]

This is pure linear algebra and uses no matching-support census. It does
not close the shore or core-probe alternatives. More importantly, the last
alternative supplies none of the second source pair, direct cap blocks,
selected \(0000\) curvature, simultaneous clean endpoints, Omega equations,
fixed-label compatibility, or common-coloop residue required in Sections
6--7. A new source-provenance lifting theorem would be needed to obtain
those objects.

This flag statement is also confined to the complete six-site selector
packet on which the two Rado matroids have rank three. Selecting six sites
from a larger residual does not preserve the off-site ranks or the remaining
common power. Therefore (32)--(35) is neither a uniform extraction theorem
nor an exhaustive route to (23).

## 9. Uniform-order limitation

The two-column Omega map is special to \(h=3\). For a residual of size
\(2h\), two clean endpoints instead give

\[
 {\cal E}(\lambda K_0+\mu K_1)
   =\lambda\mu\sum_{j=1}^{h-1}
      \lambda^{h-1-j}\mu^{j-1}E_j.
                                                               \tag{36}
\]

For \(h>3\), the factor remaining after \(\lambda\mu\) is a
degree-\((h-2)\) vector polynomial, not the linear map (5). Consequently
the bad locus is not characterized by the rank or kernel of two columns,
and (6), (21), and (23) are not uniform statements.

The odd common-coloop quotient has a separate uniform notation using
\(A=q_0^{[h-1]}\) and \(B=q_0^{[h-2]}\), but Sections 7--8 use only
\(A=q_0^{[2]}\), \(B=q_0\), and a complete six-site packet. No theorem in
this note extracts those data from a higher-order packet while preserving
the same source, remaining common power, fixed labels, clean endpoints,
and selected curvature. The order-\(h\) extraction problem remains open.

## 10. Exact status

The verified content is deliberately bounded:

1. conditional on the displayed diagonal \(h=3\) endpoints, (3)--(12)
   give the exact one-chart Omega and transverse two-cut algebra;
2. (14)--(16) give the exact source-level matrix-cap connection;
3. conditional on all five extra hypotheses in Section 6, (23) is the
   exact direct two-chart implication still to prove;
4. conditional on separate compatible common-coloop data, (29)--(31)
   give the residue transport and the necessary visibility factor
   \(K_{cc}\); and
5. the flag circuit yields only the local quotient alternatives in (35).

Neither (23) nor the conditioned residue--Omega intersection statement is
proved. The latter is not equivalent to (23), and neither is established
as an exhaustive conjecture-level bottleneck. The note therefore records
verified \(h=3\) algebra and two precise conditional research targets; it
does not close, uniformly reduce, or exhaust the inactive-root,
common-coloop, selector, or full conjecture ledgers.
