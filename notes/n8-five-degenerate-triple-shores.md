# Five row-degenerate triple shores around every invertible `K_8` pair

## 1. Outcome

Fix an invertible edge `A_pq` in a hypothetical eight-vertex realization.
For an outside vertex `x`, let

\[
 S_r(p,q)=\{x:A_{px}K_rA_{qx}^T=0\},                    \tag{1}
\]

and call `x` row-degenerate when, for the triple shore
`C_x={p,q,x}`, at least one constant one-cross row lies in the mixed-row
span:

\[
 D_{pq}=\{x:\ell_{r^{C_x}}\in M_{B\setminus C_x}
                    \text{ for some }r\}.               \tag{2}
\]

Two independently proved facts combine without loss:

1. every staircase site lies in none of the three sets `S_r`, so
   `S_r subset D_pq` for every color;
2. the hard-annihilator theorem gives
   `|S_0 union S_1 union S_2|>=5` on `K_8`.

Therefore

\[
                         \boxed{|D_{pq}|\ge5.}            \tag{3}
\]

Thus at most one of the six triples through an invertible pair can be in
the nondegenerate cyclic-staircase chart.  Some fixed target color is a
degenerate one-cross row color on at least two of the six triples.

Equivalently, at least five triples carry **pure three-cross selectors**:
there are colors `r_x` and covectors `Theta_x` on `{p,q,x}` such that

\[
 (\Theta_x\otimes\operatorname{id})T_1^{C_x|U_x}=0,
 \qquad
 (\Theta_x\otimes\operatorname{id})T_3^{C_x|U_x}
                         =e_{r_x}^{\otimes U_x}.          \tag{3a}
\]

Two of these selectors have the same target color.  This selector family,
not merely the colors `r_x`, is the remaining overlap datum.

This does not yet force an all-triple-zero pair or exclude invertible edges.
At the level of all presently combined incidence, hard-capacity, and local
staircase data, the bound is sharp: there is a five-site witness union with
one exact double witness, four singleton witnesses, one staircase site, and
no triple-zero site.  An exact local block model below realizes that
pattern.  Hence the next argument must couple the actual quotient rows for
different triple shores; counting degeneracy labels cannot suffice.

## 2. The combined theorem

**Theorem 2.1 (five degenerate triple shores).**  Suppose

\[
                         H_B(A)=\Delta_{B,3},\qquad |B|=8, \tag{4}
\]

and `A_pq` is invertible.  Then

\[
 S_r(p,q)\subseteq D_{pq}\quad(0\le r\le2),
 \qquad |D_{pq}|\ge5.                                   \tag{5}
\]

More precisely, exactly one of the following holds.

1. `D_pq` is all six outside sites.  Every triple through `pq` has a named
   constant-row degeneracy.
2. `D_pq` has five sites.  The remaining site is in the cyclic staircase
   chart, has all three cross matrices nonzero, and
   \[
             D_{pq}=S_0(p,q)\cup S_1(p,q)\cup S_2(p,q).  \tag{6}
   \]
   In this case either one of the five sites is triple-zero, or some site is
   an exact double witness.  For an exact double witness with missing color
   `c`,
   \[
     \operatorname{row}A_{px},\operatorname{row}A_{qx}
           \subset e_c^\perp,
     \qquad
     \operatorname{row}A_{px}+\operatorname{row}A_{qx}=e_c^\perp. \tag{7}
   \]

For each color `r`, at least two sites in `D_pq` are also `r`-zero
witnesses.  Independently, after choosing one degeneracy color at each site
of `D_pq`, one color is chosen at least twice.

For every chosen degeneracy color there is a selector (3a).

**Proof.**  The staircase--witness incompatibility in
`notes/staircase-overlap-fixed-pair.md` proves the first inclusion in (5):
outside `D_pq`, all three one-cross residues survive; invertibility of the
shared edge forces the cyclic staircase, and its three cross matrices are
all nonzero.  Theorem 1 of `notes/n8-hard-annihilator-union-four.md` gives

\[
                 |S_0\cup S_1\cup S_2|\ge5,              \tag{8}
\]

which proves (3)--(5).

There are only six outside sites.  If `|D_pq|=5`, its complement is a
staircase site and belongs to no `S_r`; (8) then forces (6).  The one-hole
identity gives `|S_r|>=2` for all three colors, so the five sites in (6)
carry at least six witness incidences.  If none is triple-zero, some site
has exactly two witness colors.  The exact-double row-space classification
gives (7).  If `|D_pq|=6`, the first alternative holds.  The last two
assertions follow respectively from `|S_r|>=2` and the pigeonhole principle
on five or six chosen degeneracy colors.  Corollary 2.3 of
`notes/five-set-contamination-normal-form.md` turns each row membership into
(3a). `QED`

The degeneracy color at a site in (2) need not be one of its zero-cross
colors.  This mismatch is why (5) does not upgrade to a colorwise inclusion
between row-degeneracy labels and the sets `S_r`.

## 3. Exact overlap equations for two equal-color selectors

Let `s,t in D_pq` have the same chosen degeneracy color `r`, and choose the
selectors `Theta_s,Theta_t` from (3a).  Put

\[
                         W=R\setminus\{s,t\},\qquad |W|=4. \tag{8a}
\]

The following formulas separate exactly the two cases requested by the
three-cross combinatorics: the other selected site is either one of the
three cross partners, or it lies on the unique residual internal edge.

For a three-set `S subset U_s`, define its capped cross permanent

\[
 P_s(S)=(\Theta_s\otimes\operatorname{id}_S)
     \sum_{\pi:C_s\mathbin{\simto}S}
          \bigotimes_{c\in C_s}A_{c,\pi(c)}.              \tag{8b}
\]

The selector equation before contracting `t` is

\[
 e_r^{\otimes U_s}
   =\sum_{\{a,b\}\subset U_s}
        A_{ab}\otimes P_s(U_s\setminus\{a,b\}).          \tag{8c}
\]

Indeed, `{a,b}` is precisely the residual internal edge in `U_s`, and the
other three sites are the distinct cross partners of `p,q,s`.

Let

\[
 d_{tw}=(e_r^{*(t)}\otimes\operatorname{id}_{V_w})A_{tw},
 \qquad
 R^{s\to t}_{ab}=(e_r^{*(t)}\otimes\operatorname{id}_{V_a\otimes V_b})
                         P_s(\{t,a,b\})                  \tag{8d}
\]

for `w,a,b in W`.  For an edge family `R` on the four sites `W`, use the
standard first derivative

\[
 DH_W(A)[R]=\sum_{\{a,b\}\subset W}
           R_{ab}\otimes H_{W\setminus\{a,b\}}(A).       \tag{8e}
\]

Contracting (8c) at `t` by `e_r^*` gives

\[
 \boxed{
 e_r^{\otimes W}=DH_W(A)[R^{s\to t}]+Y^{s\to t},
 \qquad
 Y^{s\to t}=\sum_{w\in W}d_{tw}\otimes P_s(W\setminus\{w\}).} \tag{8f}
\]

The derivative term is the case where `t` is a cross partner: the residual
internal edge is contained in `W`.  The slice sum `Y` is the case where the
residual edge is `tw`, leaving all three other sites of `W` as cross
partners.  No matching occurs in both cases.

The killed one-cross sector gives a second, independent first-jet identity.
Define

\[
 L_u^s=\Theta_s\mathbin{\lrcorner}
    (A_{pq}\otimes A_{su}+A_{ps}\otimes A_{qu}
                              +A_{qs}\otimes A_{pu})\in V_u. \tag{8g}
\]

Grouping a one-cross matching by its unique cross partner says exactly

\[
                    0=\sum_{u\in U_s}L_u^s\otimes
                                      H_{U_s\setminus\{u\}}(A). \tag{8h}
\]

Put `lambda_(s->t)=e_r^{*(t)}(L_t^s)` and, for `{a,b} subset W`,

\[
 Z^{s\to t}_{ab}=L_a^s\otimes d_{tb}+d_{ta}\otimes L_b^s. \tag{8i}
\]

Expanding the four-site cofactor in (8h) at `t` yields

\[
 \boxed{
       \lambda_{s\to t}H_W(A)+DH_W(A)[Z^{s\to t}]=0.}    \tag{8j}
\]

All tensors in (8d), (8f), and (8i) have their endpoint slots restored to
the named vertices.

Exchange `s,t` and use `Theta_t` to obtain the analogous four equations.
Because both pure responses have the same color, subtraction gives the
exact overlap syzygies

\[
\begin{aligned}
 DH_W(A)[R^{s\to t}-R^{t\to s}]
       +Y^{s\to t}-Y^{t\to s}&=0,\\
 DH_W(A)[\lambda_{t\to s}Z^{s\to t}
       -\lambda_{s\to t}Z^{t\to s}]&=0.                 \tag{8k}
\end{aligned}
\]

Equivalently, the cross-shaped four-site covector

\[
 \Omega_{st}=\Theta_s\otimes e_r^{*(t)}
                  -\Theta_t\otimes e_r^{*(s)}            \tag{8l}
\]

annihilates the full matching tensor on the common four-site complement
`W`.  Across the split `{p,q}|{s,t}`, its `s,t` support lies only in the
row or column of color `r`, so its Schmidt rank is at most five.  Its
four-cross boundary component is `Y^{s->t}-Y^{t->s}`.  The one-cross
selector identities split its remaining boundary into a zero-cross term
`(lambda_(s->t)-lambda_(t->s))H_W` and a two-cross first-jet term; (8j)
is exactly their cancellation.  The `T_3` part supplies the other
two-cross term in the first line of (8k).  Thus no crossing sector has been
discarded separately.

Equations (8f), (8j), and (8k) are a genuine common four-site response,
not an incidence relaxation.  The augmented first-jet map

\[
 \mathcal J_W:(\lambda,Z)\longmapsto
                    \lambda H_W(A)+DH_W(A)[Z]             \tag{8m}
\]

is never literally injective: vertex rescaling gives the unavoidable gauge
kernel

\[
 \lambda=-\sum_{w\in W}c_w,qquad
                 Z_{ab}=(c_a+c_b)A_{ab}.                 \tag{8n}
\]

Suppose instead that the internal four-site quadratic is **gauge-rigid** in
the sense of `notes/nonclean-pair-catalecticant-bridge.md`, so (8n) is the
whole kernel of (8m).  Then (8j) forces scalars `c_w` for which

\[
 \lambda_{s\to t}=-\sum_wc_w,qquad
 L_a^s\otimes d_{tb}+d_{ta}\otimes L_b^s
                         =(c_a+c_b)A_{ab}.                \tag{8o}
\]

This is a concrete pair-cap catalecticant alternative.  Every edge with
`c_a+c_b!=0` has rank at most two.  Hence an invertible internal edge
`A_ab` forces `c_a+c_b=0` and

\[
                  L_a^s\otimes d_{tb}+d_{ta}\otimes L_b^s=0
                                                               \tag{8p}
\]

on that pair.  If the invertible-edge graph on `W` contains a spanning
connected nonbipartite subgraph, the relations `c_a=-c_b` force every
`c_w=0`; hence `Z^(s->t)=0` on all six pairs.  If moreover every `d_tw` is
nonzero, the equations

\[
                  L_a^s\otimes d_{tb}+d_{ta}\otimes L_b^s=0
                  \qquad(a\ne b)                         \tag{8q}
\]

force `L_w^s=0` for every `w in W`: nonzero rank-one equality makes
`L_w^s` proportional to `d_tw`, and the signs around any triangle in `W`
then force all proportionality constants to vanish.

Thus the overlap is localized to three explicit branches: an excess
catalecticant kernel beyond gauge, a bipartite/singular internal
invertible-edge pattern, or a zero coordinate star row `d_tw=0`.  No claim
that these branches are impossible is made here.

## 4. Sharp incidence pattern without a triple-zero site

Label the six outside sites `0,1,2,3,4,5` and take

\[
 S_0=\{0,1\},\qquad S_1=\{2,3\},\qquad S_2=\{0,4\}.       \tag{9}
\]

The union has size five, each color has its required two witnesses, site
zero is an exact double witness, sites `1,2,3,4` are exact singleton
witnesses, and site `5` has no zero cross color.  There is no triple-zero
site.

This pattern satisfies the hard-capacity requirements exactly.  A
non-triple site with one or two zero-cross colors has precisely those hard
colors.  Thus the hard witness counts are two in every color.  At site zero,
whose missing color is one, the two row lines below span `e_1^perp`, as
required by (7).

There is also an exact fixed-pair block realization of (9).  Use

\[
 A_{pq}=\begin{pmatrix}-1&-2&-1\\0&-1&0\\0&-1&1\end{pmatrix},
 \qquad \det A_{pq}=1.                                  \tag{10}
\]

At site zero take rank-one blocks whose row spaces are `C e_2` and
`C e_0`; their cross product is `e_1`, giving zero set `{0,2}`.  At a
singleton site of color `r`, take rank-one blocks with row vectors

\[
 a=(1,1,1),\qquad
 b_0=(2,1,1),\quad b_1=(1,2,1),\quad b_2=(1,1,2).        \tag{11}
\]

The cross products are

\[
             a\mathbin\times b_0=(0,1,-1),\quad
             a\mathbin\times b_1=(-1,0,1),\quad
             a\mathbin\times b_2=(1,-1,0),              \tag{12}
\]

so they have exactly the desired singleton zero colors.  At site five use
the cyclic staircase blocks

\[
\begin{aligned}
 A_{q5}&=E_{00}+e_1u^T+\mathbf1e_2^T,\\
 A_{p5}&=E_{11}-e_0u^T+\mathbf1e_2^T,
 \qquad u=(1,1,0)^T.                                    \tag{13}
\end{aligned}
\]

Together with (10), these satisfy the exact three-slice identity

\[
 e_0^{(p)}\otimes A_{q5}+e_1^{(q)}\otimes A_{p5}
       +e_2^{(5)}\otimes A_{pq}=\Delta_{\{p,q,5\},3},   \tag{14}
\]

and all three matrices `A_p5 K_r A_q5^T` are nonzero.

Equations (9)--(14) are a local relaxation, not a matching-tensor
realization: the five declarations that the corresponding triple-shore
rows are degenerate have not been produced from one common set of external
cofactors.  That is exactly the point.  The witness incidence, hard
capacities, and staircase overlap are mutually consistent without a
triple-zero site.  A contradiction must therefore compare the actual five
quotient memberships in (2), or combine them with pair-cap/two-hole
cofactor equations; it cannot follow from their colors and supports alone.

## 5. Exact audit

Run

```text
.venv/bin/python computations/verify_n8_five_degenerate_triple_shores.py
```

The checker verifies (10)--(14), the exact witness sets (9), the absence of
a triple-zero site, all hard-capacity counts, the double-witness plane in
(7), and the fact that site five has three nonzero cross matrices.

The independent checker

```text
.venv/bin/python computations/verify_equal_color_selector_overlap.py
```

uses arbitrary deterministic integer edge matrices and an arbitrary
three-site covector.  It enumerates all perfect matchings and verifies the
cross-partner/residual-edge split (8f) and the contracted one-cross
first-jet formula underlying (8j), coefficient by coefficient on the common
four-site complement.
