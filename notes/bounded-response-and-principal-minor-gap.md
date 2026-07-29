# Bounded odd-shore responses and the principal-minor gap

## 1. Outcome

There is an exact, arbitrary-aggregate reduction to either eight or six
sites.  Let an odd shore `C` be separated from an odd exposed set `U` and
group the matching tensor by the number of crossing edges.  The
high-crossing separation criterion below is sufficient, but is no longer
the sharp criterion.  As proved in
[`one-crossing-kernel-collapse.md`](one-crossing-kernel-collapse.md), it is
already enough that the kernel of the total one-crossing flattening be
contained in the kernel of the target flattening.  This factors the desired
bounded target directly through the one-crossing response; the high sector
need not be killed.  Taking `|U|=7` gives an eight-site response and taking
`|U|=5` gives a six-site response.

The high-crossing Schmidt space is exactly the obstruction only if one
insists that the shore map both send the three constant tensors to the new
color basis and annihilate the high sector.  A one-vertex response itself
needs neither requirement separately; it needs only the direct
one-crossing factorization proved in the newer note.

A literal principal-cofactor version of the proposed reduction is false in
a field-uniform way already for binary equality.  On every even alternating
cycle, the full matching tensor is binary GHZ, while every proper induced
even-site cofactor is either zero or one pure tensor.  Thus preservation of
local subrank under deletion is not a rank-agnostic property of matching
powers.  Any theorem forcing an eight- or six-site ternary minor must use
the simultaneous three-color equations, or the response criterion below;
it cannot follow formally from `Q^m=GHZ_q` for arbitrary `q`.

Throughout, aggregate edge tensors are arbitrary elements
`A_uv in V_u tensor V_v`.  Hence parallel decorated sources, asymmetric
endpoint colors, and complex cancellation are already included.

## 2. Square-free matching powers and principal cofactors

Let

\[
 \mathscr S_B=\bigotimes_{v\in B}(\mathbb C\oplus V_v),
 \qquad V_vV_v=0,
\]

and put

\[
                       Q=\sum_{u<v}A_{uv}.                 \tag{1}
\]

If `|B|=2m`, then the full-support component of the matching exponential is

\[
        [\exp Q]_B={Q^m\over m!}
          =H_B(A)=\sum_{M\in\operatorname {PM}(B)}
                         \bigotimes_{uv\in M}A_{uv}.       \tag{2}
\]

For an even subset `S subseteq B`, restriction of `Q` to pairs inside `S`
will be denoted `Q_S`.  Its principal matching cofactor is

\[
                         H_S(A)={Q_S^{|S|/2}\over(|S|/2)!}.\tag{3}
\]

If `H_S(A)` has local subrank three, there are maps
`L_v:V_v -> C^3`, `v in S`, for which

\[
                  (\bigotimes_{v\in S}L_v)H_S(A)
                         =\Delta_{S,3}.                    \tag{4}
\]

Applying `L_u tensor L_v` to every aggregate block `A_uv`, `u,v in S`,
commutes with the matching sum.  Thus (4) is itself an ordinary
three-color realization on `S`.  Notice that when every `V_v=C^3`, all
the `L_v` in (4) must be invertible.  In that chart, local subrank three of
a cofactor is the very rigid assertion that the cofactor lies in the local
`GL(3)` orbit of ternary GHZ; full multilinear rank is not enough.

## 3. The general odd-shore decomposition

Write

\[
                         B=C\mathbin{\dot\cup}U,
 \qquad |C|\text{ odd},\quad |U|=2t-1\text{ odd}.         \tag{5}
\]

Every perfect matching crosses `C|U` an odd number of times.  Let `T_j`
be the sum of all matching terms which cross it exactly `j` times, and put

\[
                         T_{\rm hi}=\sum_{j\ge3\atop j\ {m odd}}T_j.
                                                                    \tag{6}
\]

For a tensor `T in V_C tensor V_U`, write

\[
 \operatorname {LS}_C(T)=
   \{(\operatorname{id}_{V_C}\otimes\beta)T:
                                  \beta\in V_U^*\}.        \tag{7}
\]

For the ternary target set

\[
 g_{C,r}=e_r^{\otimes C},\qquad
 \mathcal G_C=\operatorname {span}\{g_{C,0},g_{C,1},g_{C,2}\},
 \qquad
 \mathcal W_C=\operatorname {LS}_C(T_{\rm hi}).          \tag{8}
\]

The following statement is both a reduction and an exact audit of its
scope.

**Theorem 3.1 (odd-shore response criterion).**  Suppose

\[
                         H_B(A)=\Delta_{B,3}.              \tag{9}
\]

There is a linear map `Phi:V_C -> C^3` satisfying

\[
 (\Phi\otimes\operatorname{id}_{V_U})T_{\rm hi}=0,
 \qquad
 \Phi(g_{C,r})=e_r\quad(0\le r\le2)                      \tag{10}
\]

if and only if

\[
                         \boxed{\mathcal G_C\cap\mathcal W_C=0}. \tag{11}
\]

Whenever (11) holds, the one-crossing sector gives aggregate edge tensors
on the `2t` vertices `{star} union U` whose matching tensor is exactly
`Delta_(2t,3)`.

**Proof.**  The first equation in (10) is equivalent to
`W_C subseteq ker Phi`.  If (10) holds, a vector in the intersection in
(11) is sent both to zero and, by the second equation, to the same linear
combination of the independent vectors `e_0,e_1,e_2`.  Hence the
intersection is zero.

Conversely, (11) makes the three classes of `g_(C,r)` independent in
`V_C/W_C`.  Send those classes to `e_r`, extend linearly on the quotient,
and compose with the quotient map.  This constructs (10).

It remains to identify the response as an ordinary matching tensor.  For
`u in U`, define

\[
 K_u=\sum_{c\in C}\ \sum_{N\in\operatorname {PM}(C\setminus\{c\})}
       \left(\bigotimes_{xy\in N}A_{xy}\right)\otimes A_{cu}
       \in V_C\otimes V_u,                                \tag{12}
\]

with endpoint slots restored to their natural order, and put

\[
 Y_{\star u}=(\Phi\otimes\operatorname{id}_{V_u})K_u,
 \qquad Y_{uv}=A_{uv}\quad(u,v\in U).                    \tag{13}
\]

A matching crossing the cut once has a unique edge `cu`; after removing
it, the two shores are matched independently.  Expansion at `star`
therefore gives

\[
 H_{\{\star\}\cup U}(Y)
       =(\Phi\otimes\operatorname{id}_{V_U})T_1.          \tag{14}
\]

Equations (9)--(10), together with `H_B=T_1+T_hi`, turn the right side into

\[
 \sum_{r=0}^2\Phi(g_{C,r})\otimes e_r^{\otimes U}
                  =\Delta_{\{\star\}\cup U,3}.           \tag{15}
\]

Every `Y` in (13) is an arbitrary two-endpoint tensor, so (15) is a valid
aggregate realization.  No matching term was discarded individually.
`QED`

Two instances are the desired bounded responses.

**Corollary 3.2 (eight- and six-site alternatives).**

* If `|U|=7` and (11) holds, (9) yields an exact eight-site realization.
* If `|U|=5` and (11) holds, (9) yields an exact six-site realization.

Consequently, if the six-site obstruction is used, every hypothetical
larger realization must satisfy

\[
 \mathcal G_{B\setminus U}\cap
 \operatorname {LS}_{B\setminus U}(T_{\rm hi}^{(B\setminus U)|U})
 \ne0                                                     \tag{16}
\]

simultaneously for every five-set `U`.  If eight sites are also excluded,
the analogous condition holds simultaneously for every seven-set.

There is a cancellation-sensitive test which avoids constructing the left
Schmidt space explicitly.  Regard the three tensors as flattening maps

\[
 F_1,F_{\rm hi}:V_U^*\longrightarrow V_C,
 \qquad D:V_U^*\longrightarrow\mathcal G_C,               \tag{16a}
\]

for `T_1,T_hi,Delta`, respectively, and let
`pi:V_C -> V_C/G_C` be the quotient.  Exactness gives
`D=F_1+F_hi`, and hence

\[
 K_U:=\ker(\pi F_1)=\ker(\pi F_{\rm hi}),
 \qquad
 \mathcal G_C\cap\operatorname {im}F_{\rm hi}
                         =F_{\rm hi}(K_U).                 \tag{16b}
\]

Indeed, `F_hi(beta)` is diagonal exactly when its quotient is zero, which
by `pi D=0` is equivalent to `pi F_1(beta)=0`.  It follows that (11) is
equivalent to the single kernel condition

\[
                         (D-F_1)(K_U)=0.                   \tag{16c}
\]

This is often smaller than a termwise boundary audit and keeps every
cancellation in `T_hi`.  A consequence, originally used here only as a
necessary test, is

\[
                         \ker F_1\subseteq\ker D.          \tag{16d}
\]

Thus each of the three constant right rows of the target must lie in the
row space of the aggregate one-crossing sector.  In fact (16d) is itself
sufficient for an ordinary bounded response.  Let
`delta:V_U^* -> C^3` be the target flattening with
`delta(beta)=sum_r beta(e_r^tensor U)e_r`.  Since `ker D=ker delta`, the
rule `Phi(F_1(beta))=delta(beta)` is well defined on `im F_1`; extend it
linearly to `V_C`.  Then
`(Phi tensor id)T_1=Delta_({star} union U,3)`, and the response construction
(12)--(14) is already the desired matching tensor.  No action on `T_hi` is
required.  See `one-crossing-kernel-collapse.md` for the full proof, an
exact matching-realizable strictness example, and all-cut audits.

Theorem 3.1 includes tight-cut collapse: if every supported matching
crosses the odd cut once, then `T_hi=0` and (11) is automatic.  More
generally, it shows precisely what an algebraic one-vertex contraction has
to prove.  A conformal graph minor or an internal perfect matching in `C`
does not remove `W_C`; all matchings crossing three or more times remain as
response contamination.

## 4. Principal deletion does not preserve local subrank

The failure is already exact for binary equality and persists at every
even order.

Let `B=Z/(2m)` with `m>=2`, and let

\[
 P_0=01|23|\cdots|(2m-2,2m-1),\qquad
 P_1=12|34|\cdots|(2m-1,0).                               \tag{17}
\]

Put the rank-one tensor `e_0 tensor e_0` on every edge of `P_0`, the tensor
`e_1 tensor e_1` on every edge of `P_1`, and zero on all other pairs.  The
support is the alternating cycle and has exactly its two alternating
perfect matchings.  Hence

\[
                         H_B=e_0^{\otimes B}+e_1^{\otimes B}
                              =\Delta_{B,2}.               \tag{18}
\]

Now take any proper even subset `S subsetneq B`.  Its induced support is a
disjoint union of paths and isolated vertices.  A path has at most one
perfect matching, so the whole induced graph has at most one.  Therefore

\[
                         H_S=0
 \quad\hbox{or}\quad
                         H_S=\lambda\bigotimes_{v\in S}e_{c_v}           \tag{19}
\]

for a nonzero scalar `lambda` and a (possibly mixed) binary word `c`.
Thus every proper principal cofactor has tensor rank, and hence local
subrank, at most one, although the full tensor (18) has local subrank two.

This does not rule out a specially ternary contraction theorem.  It proves
that such a theorem cannot be a formal monotonicity principle for powers of
quadratics in the square-free site algebra.  It must exploit the third
constant component together with the vanishing of all mixed coefficients,
or verify the high-sector separation (11).

## 5. Exact boundary of a proposed matching-minor proof

A graph deletion keeps `Q_S` and hence the principal cofactor (3).  A
one-shore contraction keeps the one-crossing response (12)--(14).  Neither
operation accounts for `T_hi` automatically.  The exact possibilities are
therefore:

1. find a principal even subset whose cofactor already has local subrank
   three; this directly gives a smaller realization by (4), but is a very
   rigid GHZ-orbit condition;
2. find an odd shore satisfying (11); this gives a genuine eight- or
   six-site response while retaining every cancellation in the total high
   sector; or
3. use a richer boundary gadget which represents the high-crossing
   signature rather than calling it an ordinary matching minor.

Without one of these extra steps, local subrank three of the full incidence
tensor does not logically descend to a bounded principal matching minor.
