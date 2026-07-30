# Independent audit: flat degree four is an exactly mergeable cubic split

## 1. Verdict and terminology

The algebraic claims in
[`flat-degree-four-essential-purity-nullity-export.md`](flat-degree-four-essential-purity-nullity-export.md)
are correct over \(\mathbb C\), with the global-flat hypothesis inherited
from
[`flat-good-fan-degeneracy-degree-four-collapse.md`](flat-good-fan-degeneracy-degree-four-collapse.md).
In fact the essential-edge lemma proves slightly more cleanly than its use
there requires: every bad pair has both a nonzero aggregate block and a
nonzero monochromatic pure complementary matching tensor.

Two pieces of terminology are now explicit in the primary note and are
retained here.  Write

\[
 N_A(p):=\{j\in B\setminus\{p\}:A_{pj}\ne0\}
\]

is the **aggregate support neighbourhood**.  Thus a nonneighbour of \(p\)
means a site \(q\) with \(A_{pq}=0\); it need not mean that the original
decorated multigraph had no sources on the physical pair \(pq\), because
parallel sources may have cancelled in aggregation.  Also, an
**aggregate-active** pair means \(A_{uv}\ne0\), whereas a
**cofactor-active** pair means
\(H_{B\setminus\{u,v\}}(A)\ne0\).  The essential-edge argument below
forces both.  This resolves the potentially ambiguous word ``active'' in
the primary note.

No mathematical repair to the primary result is needed.  The reuse
qualifications collected in Section 7 delimit its scope.

## 2. Essentiality forces a pure nonzero cofactor

Let

\[
 L_{u\leftarrow x}:=
 \operatorname{im}\bigl(V_x^*\longrightarrow V_u\bigr),
 \qquad
 S_u^{(v)}:=\sum_{x\notin\{u,v\}}L_{u\leftarrow x}.
\]

The target mode flattening gives
\(\sum_{x\ne u}L_{u\leftarrow x}=V_u\).  Say that \(uv\) is essential
at \(u\) when \(S_u^{(v)}\subsetneq V_u\).  Choose
\(0\ne\lambda\in\operatorname{Ann}S_u^{(v)}\), and contract the exact
star expansion at \(u\).  Every summand except the one using \(uv\)
vanishes, so

\[
 \sum_{c=0}^2\lambda(e_c)e_c^{\otimes(B\setminus\{u\})}
 =\bigl((\lambda\otimes\operatorname{id})A_{uv}\bigr)^{(v)}
   \otimes H_{B\setminus\{u,v\}}(A).                 \tag{A1}
\]

The left side is nonzero.  Across the flattening with \(V_v\) on one
side, its rank is exactly the number of nonzero coordinates of
\(\lambda\); the right side is a nonzero simple tensor and has rank one.
Consequently every nonzero element of
\(\operatorname{Ann}S_u^{(v)}\) is supported on one coordinate
covector.  This annihilator cannot have dimension at least two, because
the sum of two independent coordinate-supported vectors has two nonzero
coordinates.  Hence, for a unique colour \(c\),

\[
 \operatorname{Ann}S_u^{(v)}=\mathbb C e_c^*,
 \qquad S_u^{(v)}=\ker e_c^*.
\]

Taking \(\lambda=e_c^*\) in (A1) and using uniqueness of the factors of a
nonzero simple tensor gives nonzero \(\alpha,\beta\) with

\[
 (e_c^*\otimes\operatorname{id})A_{uv}=\alpha e_c,
 \qquad
 H_{B\setminus\{u,v\}}(A)
   =\beta e_c^{\otimes(B\setminus\{u,v\})},
 \qquad \alpha\beta=1.                                \tag{A2}
\]

This proof permits asymmetric endpoint colours, parallel sources after
aggregation, zero entries elsewhere, and arbitrary complex cancellation.

A pair is bad precisely when it is essential at at least one endpoint.
If \(A_{uv}=0\), deleting \(v\) from the \(u\)-star removes no support,
so \(S_u^{(v)}=V_u\); the same is true with \(u,v\) reversed.  Thus a
bad pair cannot have zero aggregate block.  Applying (A2) at a deficient
endpoint proves the exact global corollary

\[
 \boxed{\text{every bad pair is aggregate-active and cofactor-active,
 and its complementary cofactor is monochromatic pure.}}       \tag{A3}
\]

In particular, ``essential at one endpoint'' is enough; no symmetry of
the two deleted endpoint stars is being assumed.

## 3. The pure-port partition

Fix a centre \(p\) for which every aggregate-active incident pair is bad,
and write \(J=N_A(p)\).  By (A3), for every \(j\in J\) there are a colour
\(\kappa(j)\) and \(\beta_j\ne0\) such that

\[
 C_j:=H_{B\setminus\{p,j\}}(A)
   =\beta_j e_{\kappa(j)}^{\otimes(B\setminus\{p,j\})}. \tag{A4}
\]

Put \(M_j=\beta_jA_{pj}\).  Expansion at \(p\) gives

\[
 \Delta_{B,3}=\sum_{j\in J}M_j^{(p,j)}\otimes
 e_{\kappa(j)}^{\otimes(B\setminus\{p,j\})}.           \tag{A5}
\]

Fix \(j\), put \(c=\kappa(j)\), and inspect a word that has a colour
different from \(c\) at \(j\) and colour \(c\) at every site outside
\(\{p,j\}\).  A same-fibre summand centred elsewhere fixes the \(j\)
slot to \(c\), while a different-fibre summand is separated at a third
site.  The target coefficient vanishes.  Varying the \(p\)-colour and
the non-\(c\) colour at \(j\) proves

\[
                       M_j=v_j^{(p)}\otimes e_c^{(j)}       \tag{A6}
\]

for a nonzero \(v_j\in V_p\).  Inspecting words which are colour \(c\)
at every site outside \(p\) then gives

\[
                     \sum_{\kappa(j)=c}v_j=e_c
                     \qquad(c=0,1,2).                     \tag{A7}
\]

Each fibre of \(\kappa\) is therefore nonempty.  Equations (A4), (A6),
and (A7) are the asserted pure-port partition, and their proof does not
use \(|J|=4\).  When \(|J|=4\), the fibre sizes are \(2,1,1\).  The two
singletons are already diagonal coordinate cells, and if \(b,b'\) form
the repeated colour-\(k\) fibre then

\[
                              v_b+v_{b'}=e_k.              \tag{A8}
\]

This establishes the degree-four conclusion in both branches of the
earlier pure-versus-essential-direction dichotomy: in the dependent
branch the fourth edge is essential at \(p\), and in the independent
branch it is essential at the opposite endpoint.  Equation (A2) is
endpoint-independent once the pure complementary cofactor is obtained.

## 4. Exact port-merging surgery and entry-minimal strengthening

For each colour \(c\), choose one representative
\(a_c\in\kappa^{-1}(c)\).  Leave all blocks not incident with \(p\)
unchanged, and set

\[
 A'_{pa_c}=\beta_{a_c}^{-1}e_c^{(p)}\otimes e_c^{(a_c)},
 \qquad
 A'_{pj}=0\quad
 (j\in\kappa^{-1}(c)\setminus\{a_c\}).                 \tag{A9}
\]

Every retained cofactor \(C_{a_c}\) deletes \(p\), so none of the
changes in (A9) affects it.  Consequently expansion of the new matching
tensor at \(p\) gives

\[
 H_B(A')=\sum_{c=0}^2
   \beta_{a_c}^{-1}e_c^{(p)}\otimes e_c^{(a_c)}\otimes C_{a_c}
 =\sum_{c=0}^2e_c^{\otimes B}=\Delta_{B,3}.              \tag{A10}
\]

This is exact source surgery, not a limiting argument.  An aggregate
scalar cell is realizable by one degree-two decorated source of that
complex weight.  The surgery keeps all three target colours present and
allows arbitrary original endpoint order.  It may insert a diagonal cell
that was previously zero, which is harmless: a fibre containing \(t\)
ports had at least \(t\) nonzero scalar entries and is replaced by one.
Thus any surplus port strictly decreases the total aggregate-entry
support.

It follows that if the hypothetical ternary exact source is chosen with
minimum aggregate-entry support among **all** ternary exact sources, every
bad-only star is already cubic.  The local irredundancy proof gives the
same conclusion directly.  Indeed, for a nonzero coordinate \(v_j(d)\)
in a colour-\(c\) fibre, the corresponding derivative atom is a nonzero
multiple of

\[
                 e_d^{(p)}\otimes e_c^{\otimes(B\setminus\{p\})}.
                                                                    \tag{A11}
\]

Star irredundancy permits at most one nonzero such coordinate for each
ordered pair \((d,c)\).  Taking coordinates in (A7), an off-diagonal
pair \(d\ne c\) has sum zero and hence no nonzero term, while the
diagonal pair has sum one and hence exactly one term.  Since every port
is nonzero, each colour fibre is a singleton and its block is the
corresponding diagonal coordinate cell.

## 5. Ordered flat centres

Choose a \(4\)-degeneracy ordering \(p_1,\ldots,p_N\) of the bad graph,
so \(p_i\) has at most four later bad neighbours.  Its total bad degree
is at most

\[
                              \deg_{\mathcal B}(p_i)\le i+3. \tag{A12}
\]

For \(i\le N-7\), it therefore has at least three good neighbours.  In
the **globally flat branch**, meaning that every canonical transition on
every such good fan vanishes, the flat-fan theorem kills every good block
at \(p_i\).  Hence

\[
 N_A(p_i)\subseteq N_{\mathcal B}(p_i),
 \qquad 3\le |N_A(p_i)|\le i+3,                         \tag{A13}
\]

and Section 3 supplies a pure-port partition at each of these centres in
the original source.  These conclusions hold simultaneously.  Port
surgeries need only be applied at one selected centre and are not claimed
to commute.  If the source is entry-minimal, Section 4 instead shows
simultaneously, without surgery, that every centre in (A13) is cubic.
In particular \(p_1\) is cubic for every even \(N\ge8\); for \(N\ge10\)
the first three ordered centres are all cubic.

Thus the global-flat branch reduces to the existing cubic branch, rather
than leaving degree four, five, or six as separate terminal strata.

## 6. The two overlapping nullity webs

Retain a degree-four star before surgery.  Let \(a_c,a_d\) be its
singleton ports and let \(b,b'\) be the repeated colour-\(k\) ports.
For any aggregate-support nonneighbour

\[
 q\notin\{p,a_c,a_d,b,b'\},
\]

put \(W=B\setminus\{p,q\}\).  There are exactly \(N-5\) choices.  For
an anchor \(a\), put \(K_a=W\setminus\{a\}\), and let

\[
 \Phi_{q,a}(z)=\sum_{v\in K_a}z_v^{(v)}\otimes
 H_{K_a\setminus\{v\}}(A).                              \tag{A14}
\]

If \(s_i\) is the complete colour-\(i\) row of the \(q\)-star into
\(W\), expansion of the pure cofactor (A4) at \(q\) gives

\[
 \Phi_{q,a}(\pi_as_i)
   =\delta_{i,\kappa(a)}\beta_a
      e_{\kappa(a)}^{\otimes K_a}.                       \tag{A15}
\]

The proof of the cubic leave-one-anchor nullity theorem uses only the
three equations (A15) for three distinct anchors, one of each colour,
and their nonzero diagonal right sides.  It does not require that the
centre producing those identities was already cubic.  Applying it first
to \((a_c,a_d,b)\) and then to \((a_c,a_d,b')\), and writing
\(\nu_a=\dim\ker\Phi_{q,a}\), yields

\[
 \begin{gathered}
 \nu_{a_c},\nu_{a_d},\nu_b,\nu_{b'}\ge1,\\
 \#\{a\in\{a_c,a_d,b\}:\nu_a\ge2\}\ge2,\\
 \#\{a\in\{a_c,a_d,b'\}:\nu_a\ge2\}\ge2.             \tag{A16}
 \end{gathered}
\]

For completeness, the mechanism is cancellation-safe: for a fixed
anchor, its two wrong-colour rows lie in the kernel; the nonzero diagonal
equations prevent them from being both zero or nonzero proportional.  If
two anchor maps had nullity one, their uniquely supported wrong rows and
the shared lower cofactor would force that cofactor to be both zero and
nonzero, or pure in two distinct colours.  Thus at most one map in each
three-colour triple has nullity one, which is exactly (A16).

After (A9) merges, say, \(b'\) into \(b\), the site \(b'\) becomes an
aggregate-support nonneighbour of the new cubic centre.  The standard
cubic nullity web therefore applies there as well as at the original
\(N-5\) nonneighbours.  This last assertion concerns the surgically
modified exact source; (A16) concerns the original degree-four source.

## 7. Editorial qualifications for reuse

The primary note is mathematically sound and now makes the key terminology
explicit.  Later citations should retain the following points.

1. ``Neighbour'' means membership in \(N_A(p)\), not existence of an
   uncancelled or cancelled underlying decorated source on that pair.
2. In the every-bad-pair corollary, ``active'' should be split into the
   two proved facts \(A_{uv}\ne0\) and
   \(H_{B\setminus\{u,v\}}(A)\ne0\).
3. The normalization \(\alpha\beta=1\) in the essential-edge lemma is
   obtained by taking \(\lambda=e_c^*\) after identifying the unique
   coordinate \(c\).
4. The ordered-centre statement assumes global fan flatness.  Its pure
   partitions coexist in the original source, whereas surgeries at
   different centres are not asserted to coexist.  Entry-minimality is
   what makes all those centres cubic simultaneously.
5. The support-minimal surgery uses minimality among all exact aggregate
   ternary sources, not minimality within a fixed graph or fixed support.

With these readings, the degree-four foothold introduces no new flat
endpoint: it is an exact one-colour splitting of the cubic endpoint, and
the only remaining flat obstruction is the already registered cubic
nullity-web closure problem.
