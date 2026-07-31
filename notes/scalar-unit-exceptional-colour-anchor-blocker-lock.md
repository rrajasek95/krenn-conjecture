# Exceptional-colour filtration turns every new factor blocker into a nine-row lock

## 1. Outcome

Work at an intrinsic scalar-unit pair on \(2h\) residual sites,
\(h\geq3\), with

\[
 \alpha\delta_{ia}\delta_{ja}q^{[h]}
      +R_{ij}q^{[h-1]}=\delta_{ij}X_i,
 \qquad R_{ij}=p_i s_j,\qquad \alpha\ne0.               \tag{1}
\]

Suppose an exact replacement is compared inside the
maximum-mutual-anchor, then minimum-support stratum. The pure-\(a\)
projection of its exceptional row may force a nonzero all-\(a\) perfect
matching \(P\). This note gives a uniform continuation through the next
two ledgers.

1. **Anchor charge.** If the replacement preserves every old mutual
   anchor, then every edge of \(P\) which was not already an old anchor
   must be blocked at an \(a\)-coordinate. If \(m\) edges of \(P\) are
   new in this sense, the exact incidence charge is
   \[
      \sum_{\beta}\iota_P(\beta)\geq m,\qquad
      2N_{\rm int}+N_{\rm port}\geq m.                  \tag{2}
   \]
   Here an internal blocker has at most two \(a\)-incidences on \(P\),
   while a selected-star port has at most one. In the pure new-factor
   subcase \(U=P\) with no \(a\)-ports, at least
   \(\lceil h/2\rceil\) extra internal blockers are required. This is the
   configuration motivating the exact-cancellation repair, not a proved
   description of its entire branch. The conditional bound is sharp at
   every \(h\).
2. **Normalized one-star switch.** Let an internal blocker \(g\) meet a
   factor edge \(f\in P\) at the same residual \(a\)-coordinate. If the
   pure exceptional cofactor of \(f\) is nonzero, deleting \(g\) and
   rescaling \(f\) has a unique normalization which preserves the pure
   exceptional row. The change is supported on one physical star and
   therefore has square zero. It either preserves all nine rows, giving an
   exact support descent or anchor gain, or it has a nonzero, explicitly
   defined **blocker-lock class** in a higher exceptional colour grade or
   one of the other eight ordered rows.

At a lexicographically selected exact source, the first alternative is
impossible. Thus every cofactor-live blocker is detected by the blocker-lock
class. This is a positive kill-or-descent theorem, not merely a tangent
condition.

The exceptional Euler identity

\[
 \boxed{\sum_{e\ {\rm all}\text{-}a}q_e c_e
                 =(h-1)+\alpha Q_a}                    \tag{3}
\]

guarantees at least one live all-\(a\) cofactor unless
\(\alpha Q_a=-(h-1)\). Here

\[
 Q_a=[X_a]q^{[h]},\qquad
 c_e=[X_a]\,e\bigl(\alpha q^{[h-1]}
                         +R_{aa}q^{[h-2]}\bigr).        \tag{4}
\]

The resonance is absent in both branches motivating the construction:
\(Q_a=\alpha^{-1}\) when the response has no pure-\(a\) channel, and
\(Q_a=0\) on the complementary binary-top branch. Their Euler charges are
respectively \(h\) and \(h-1\).

What is not proved is that every required blocker shares a physical star
with a live factor cofactor, or that several individually locked switches
can be combined without nonlinear cross terms. A uniform all-\(a\) fan
below shows this is the sharp interface: it has a normalized exceptional
target, all \(h\) factor edges blocked, and every blocker active in the
pure response; nevertheless each normalized switch is a literal support
descent until an omitted nonexceptional/higher-grade row locks it.

The surviving problem is therefore an **integrable blocker-lock web**:
the full nine rows must supply compatible locks covering the anchor charge,
and those locks must remain independent after the nonlinear cross terms
between different residual stars are restored. No such web theorem is
proved here, and Krenn's conjecture remains open.

## 2. Exceptional colour grades

Grade a decorated quadratic cell by the number \(0,1,2\) of its residual
endpoint colours different from \(a\). Write

\[
 q=q_0+q_1+q_2,\qquad R_{aa}=R_0+R_1+R_2.              \tag{5}
\]

The exceptional equation is

\[
                         \alpha q^{[h]}+R_{aa}q^{[h-1]}=X_a. \tag{6}
\]

Its pure and one-defect parts are exactly

\[
 \boxed{\alpha q_0^{[h]}+R_0q_0^{[h-1]}=X_a,}          \tag{7}
\]

\[
 \boxed{(\alpha q_1+R_1)q_0^{[h-1]}
              +R_0q_1q_0^{[h-2]}=0.}                  \tag{8}
\]

No matching power has been cancelled. Equation (8) is the first mixed
colour constraint after the forced pure factor. It permits cancellation
between the internal one-defect cells, the selected response, and the
pure-response correction; it does not make any term vanish separately.

For later use, put

\[
 C=\alpha q^{[h-1]}+R_{aa}q^{[h-2]}.                   \tag{9}
\]

This is the exact finite difference cofactor for a one-star internal move.
Its one-defect part is

\[
 C_1=(\alpha q_1+R_1)q_0^{[h-2]}
                    +R_0q_1q_0^{[h-3]}.                \tag{10}
\]

Thus an all-\(a\) normalized switch \(d_0\) has first exceptional leakage
\(d_0C_1\). This is a genuinely lower colour-grade object than (8):
equation (8) says the old source is exact, whereas \(d_0C_1\) asks whether
the proposed support deletion stays exact.

## 3. Euler guarantees a live all-\(a\) cofactor

Let

\[
 S_a=[X_a]R_{aa}q^{[h-1]}.
\]

Taking the pure coefficient of (6) gives

\[
                              \alpha Q_a+S_a=1.         \tag{11}
\]

For every all-\(a\) decorated physical cell \(e\), let \(q_e\) be its
coefficient and define \(c_e\) by (4). Euler's identity in the \(q_e\)'s
gives

\[
 \begin{aligned}
 \sum_e q_ec_e
   &=\alpha h[X_a]q^{[h]}
          +(h-1)[X_a]R_{aa}q^{[h-1]}\\
   &=\alpha hQ_a+(h-1)S_a\\
   &=(h-1)+\alpha Q_a.
 \end{aligned}                                         \tag{12}
\]

This proves (3). If the right side is nonzero, at least one supported
all-\(a\) cell has \(c_e\ne0\). The statement is cancellation-aware: it
does not choose a term in (11) or assert that every factor edge is live.

In the exact-cancellation repair with no pure-\(a\) response,
\(S_a=0\) and \(Q_a=\alpha^{-1}\), so (12) equals \(h\). In the
binary-top normalization \(Q_a=0\) and \(S_a=1\), so it equals \(h-1\).
This common Euler charge is the precise point at which the two replacement
problems share a mechanism.

## 4. Anchor incidence charge

Consider an exact replacement \(A'\) which preserves every mutual
coordinate anchor of the selected source \(A\). Let \(P\) be a supported
all-\(a\) perfect matching in its internal quadratic. Let \(U\subseteq P\)
consist of those factor edges which were not mutual anchors of \(A\).

An **internal blocker** is a decorated internal cell outside \(P\) which
uses at least one residual \(a\)-coordinate lying on an edge of \(U\). A
**port blocker** is a nonzero component of one of the six selected
one-site forms \(p_i,s_j\) on such an \(a\)-coordinate. Define
\(\iota_P(\beta)\) as the number of distinct edges of \(U\) met by the
blocker at an \(a\)-coordinate.

If some \(e=uv\in U\) had no blocker, the \(aa\)-cell on \(uv\) would be
the only aggregate cell incident to either \((u,a)\) or \((v,a)\).
It would therefore be a mutual coordinate anchor of \(A'\). Since every
old anchor persists and \(e\) was not one of them, this would give
\(\nu(A')>\nu(A)\), contradicting maximum-anchor selection. Hence the
blockers cover \(U\), proving the first inequality in (2). An internal
cell has two endpoints and a port component one, proving the second.

If \(U=P\) and there are no \(a\)-ports, (2) gives
\(N_{\rm int}\geq\lceil h/2\rceil\). This is sharp. Number the factor
edges

\[
                          P=\{u_iv_i:0\leq i<h\}.        \tag{13}
\]

For even \(h\), add the \(\frac h2\) all-\(a\) cells

\[
                    u_0u_1,\ u_2u_3,\ldots,u_{h-2}u_{h-1}. \tag{14}
\]

For odd \(h\), use the same pairing through \(u_{h-2}\), then add
\(u_{h-1}u_0\). Every factor edge is blocked. Moreover the only perfect
matching in the resulting support is \(P\): using any blocker consumes
two \(u\)-vertices and strands their two \(v\)-partners. Thus the extra
cells do not change the pure top tensor. This construction proves sharpness
uniformly, but its blockers are top-inactive and need not survive support
minimality.

## 5. The normalized one-star switch

Let \({\bf f}\) be the unit decorated cell of a factor edge
\(f\in P\), with coefficient \(w\ne0\), and let \({\bf g}\) be an
internal blocker with coefficient \(\gamma\ne0\). Assume they meet at the
same physical site and the same residual \(a\)-coordinate there. Then
every cell in

\[
                         d=-\gamma{\bf g}+\delta{\bf f} \tag{15}
\]

meets that physical site, so \(d^{[2]}=0\).

Set

\[
 c_f=[X_a]{\bf f}C,\qquad c_g=[X_a]{\bf g}C.            \tag{16}
\]

If \(c_f\ne0\), there is a unique pure-row normalization

\[
                         \boxed{\delta=\gamma\,c_g/c_f.} \tag{17}
\]

Indeed,

\[
                  [X_a]\,dC=-\gamma c_g+\delta c_f=0.  \tag{18}
\]

Because \(d^{[2]}=0\), this is an exact finite statement, not a first-order
normalization.

Define the blocker-lock class

\[
 \boxed{
 {\cal L}(d)=
 \left(
   \Pi_{\geq1}(dC),\
   \bigl(R_{ij}d q^{[h-2]}\bigr)_{(i,j)\ne(a,a)}
 \right).}                                             \tag{19}
\]

Here \(\Pi_{\geq1}\) retains every exceptional word having at least one
non-\(a\) residual colour. The one-star divided-power identity gives

\[
 \begin{aligned}
 E_{aa}(q+d)-E_{aa}(q)&=dC,\\
 E_{ij}(q+d)-E_{ij}(q)&=R_{ij}d q^{[h-2]}
                                      &&((i,j)\ne(a,a)). \tag{20}
 \end{aligned}
\]

Equation (18) removes the pure coordinate. Consequently

\[
                           {\cal L}(d)=0                \tag{21}
\]

if and only if \(q\mapsto q+d\), with the direct block and all stars
fixed, preserves all nine tensor rows.

The move deletes \({\bf g}\) and only resizes the already supported
\({\bf f}\); it introduces no cell. Both \(f\) and \(g\) were nonanchors
because they shared the same \(a\)-coordinate. Removing either cannot
destroy an old anchor. Thus (21) gives an exact source with strictly lower
support, or with additional anchors if the removal exposes one. Either
outcome contradicts the lexicographic choice. We have proved:

> **Normalized-switch kill-or-descent lemma.** At a maximum-anchor,
> minimum-support exact source, every blocker/factor pair satisfying
> \(c_f\ne0\) has \({\cal L}(d)\ne0\).

For an all-\(a\) switch, the first possible exceptional component is
\(dC_1\) from (10). For a mixed blocker, the first possible component is
at its own defect grade. Thus (19) records precisely whether the next
colour grade or one of the eight restored rows prevents descent.

The lemma applies to replacements arising in both the exact-cancellation
and binary branches whenever its factor/blocker hypotheses hold. The
difference is where the Euler-live cofactors and the blockers occur.
Equation (12) does not prove that each blocker is incident to a live factor
edge; that incidence is the first surviving boundary.

## 6. A uniform response-active fan guard

The following physical packet shows that pure exactness, all colour grades,
anchor blocking, and response activity still do not produce the required
full-nine locks.

Use the sites in (13), put every displayed residual colour equal to \(a\),
and set

\[
 \begin{aligned}
 q={}&\sum_{i=0}^{h-1}e^a_{u_iv_i}
          +\sum_{j=1}^{h-1}e^a_{u_0u_j},\\
 p_a={}&x_{v_0}^a,\qquad
 s_a=\sum_{j=1}^{h-1}\rho_jx_{v_j}^a,\qquad
 R_{aa}=p_as_a,                                        \tag{22}\\
 \rho_j={}&1\quad(1\leq j<h-1),\qquad
 \rho_{h-1}=-(h-2).
 \end{aligned}
\]

Take \(\alpha=1\). The only internal perfect matching is \(P\), so
\(q^{[h]}=X_a\). For each \(j\), the response cell
\(e^a_{v_0v_j}\), blocker \(e^a_{u_0u_j}\), and the other \(h-2\)
factor edges give one copy \(\rho_jX_a\). Hence

\[
             R_{aa}q^{[h-1]}
                 =\left(\sum_{j=1}^{h-1}\rho_j\right)X_a=0,       \tag{23}
\]

and the exceptional row is exactly \(X_a\). Every mixed colour grade is
zero. Every factor edge is blocked at its \(u\)-endpoint; it is also
blocked at its \(v\)-endpoint by \(p_a\) or \(s_a\). Thus none of the
\(h\) factor edges is a mutual anchor.

Every blocker is nevertheless active in an individual pure response term.
For its normalized switch, take

\[
 d_j=-e^a_{u_0u_j}+\rho_j e^a_{u_0v_0}.                 \tag{24}
\]

The two cells share \(u_0\), so \(d_j^{[2]}=0\). Deleting the \(j\)-th
blocker removes \(\rho_jX_a\) from (23), while resizing the \(u_0v_0\)
factor adds the same \(\rho_jX_a\) to the direct top. Therefore

\[
 (q+d_j)^{[h]}+R_{aa}(q+d_j)^{[h-1]}=X_a               \tag{25}
\]

coefficientwise. The move lowers support and preserves every existing
anchor. This is exactly the descent side of the lemma.

The fan is not a ternary exact source: the complementary star rows are not
supplied. It proves the sharp logical boundary. To survive at a selected
full source, each \(d_j\) must be locked by a higher exceptional colour
grade or a nonexceptional row in (19). The collection of those locks must
also control combinations of different \(j\)'s, whose cross products no
longer vanish.

## 7. Residual invariant and scope

The uniform implication established here is

\[
 \boxed{
 \begin{gathered}
 \text{new all-}a\text{ factor}+\text{old-anchor persistence}\\
 \Longrightarrow\text{blocker incidence charge (2)},\\
 \text{cofactor-live blocker/factor pair}\\
 \Longrightarrow
 \text{exact support descent or }{\cal L}(d)\ne0.
 \end{gathered}}                                       \tag{26}
\]

The exact surviving invariant is the integrable blocker-lock web:

1. match the blocker cover forced by (2) to Euler-live factor cofactors;
2. identify the first nonzero component of every \({\cal L}(d)\);
3. use the shared nine-row provenance to rule out a compatible family of
   locks, including nonlinear cross terms between switches on different
   residual stars.

Step 1 is not automatic from the nonzero Euler sum (12), and individual
nonzero lock classes do not imply independence. The fan guard shows why
both qualifications are necessary. No support bound alone closes them.

This theorem supplies a conditional tool at the shared top-changing
difference-system interface of the exact-cancellation and binary
residual-target branches, but it does not prove that every replacement in
either branch satisfies \(U=P\) or has no \(a\)-ports. Neither branch
reduces to the other. It does not construct a Hamiltonization, a same-order
descendant, or an active clean cap.

The dependency-free checker
[verify_scalar_unit_exceptional_colour_anchor_blocker_lock.py](../computations/verify_scalar_unit_exceptional_colour_anchor_blocker_lock.py)
audits the defect-grade identities, Euler formula, sharp blocker cover,
fan response terms, anchors, and every normalized deletion for
\(3\leq h\leq8\). It uses exact rational arithmetic and explicit runtime
failures, and remains active under optimized Python.
