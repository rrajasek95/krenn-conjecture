# Small tensor findings

Let `V` be the color space with basis `e_r`.  After combining parallel
sources having the same unordered vertex pair and the same ordered endpoint
colors, attach to every pair `ij` the completely arbitrary tensor

\[
A_{ij}=\sum_{a:N(a)=\{i,j\}}w(a)e_{k(a,i)}\otimes e_{k(a,j)}\in V_i\otimes V_j.
\]

The matching tensor on a vertex set `S` is

\[
H_S(A)=\sum_{M\in\operatorname{PM}(S)}\bigotimes_{ij\in M}A_{ij}.
\]

This aggregation retains endpoint order and all cancellation among parallel
sources.  In particular, an `A_ij` need not be symmetric or rank one.

### Self-contained diagonal partition-rank lemma

Here is a proof of the rank fact used below.  Let `X` be finite and let

\[
F_d(x_1,\ldots,x_d)=\sum_{a\in D}c_a
  \delta_a(x_1)\cdots\delta_a(x_d),\qquad c_a\ne0.              \tag{PR}
\]

Then the unrestricted partition rank of `F_d` is `|D|` over `C` (in fact,
over any field).  The displayed diagonal sum gives the upper bound.  For the
lower bound, induct on `d`, the case `d=2` being ordinary matrix rank.
Suppose, contrary to the claim, that

\[
F_d=\sum_{i=1}^r f_i(x_{S_i})g_i(x_{T_i}),\qquad r<|D|,          \tag{PR1}
\]

where `S_i,T_i` are nonempty complements.  Interchange the factors so that
`|S_i| <= d/2` for every `i`.

If no `S_i` is a singleton, sum (PR1) over an arbitrary coordinate, say
`x_1`.  On the left this gives the same diagonal tensor (PR) in `d-1`
variables.  On the right, every surviving summand still factors across a
nontrivial partition: if `1 in S_i`, then `S_i\{1}` is nonempty, and if
`1 in T_i`, then `T_i\{1}` is nonempty because `|T_i| >= d/2 >= 2`.
The induction hypothesis says `|D| <= r`, a contradiction.

Otherwise choose `j` for which some `S_i={j}`, and put
`U={i:S_i={j}}`, `u=|U|`.  In the vector space of functions `X -> C`, let

\[
W=\{v:\sum_{x\in X}v(x)f_i(x)=0\text{ for every }i\in U\}.
\]

Then `dim W >= |X|-u`.  Choose `v in W` with maximal support.  Necessarily
`|supp(v)| >= dim W`: otherwise the restriction map from `W` to the
coordinates in `supp(v)` has a nonzero kernel element `w`; this `w` vanishes
on `supp(v)`, so `v+w` has strictly larger support.  Consequently

\[
|D\cap\operatorname{supp}(v)|\ge |D|-u.                         \tag{PR2}
\]

Contract (PR1) in coordinate `j` against `v`.  The `u` terms indexed by `U`
vanish.  Every other surviving term still factors across a nontrivial
partition: its `S_i` factor retains a variable unless `S_i={j}` (the excluded
case), while its `T_i` factor retains a variable because `|T_i|>=2`.
Thus the contracted tensor has partition rank at most `r-u`.  But it is a
diagonal `(d-1)`-tensor with precisely
`|D cap supp(v)| >= |D|-u` nonzero diagonal entries.  Induction gives
`|D|-u <= r-u`, contradicting `r<|D|`.  This proves the lemma without any
positivity or genericity hypothesis.

## 1. A partition-rank bound, sharp at four sites

Fix `p in S`.  Expanding by the partner of `p` gives the exact identity

\[
H_S(A)=\sum_{j\in S\setminus\{p\}} A_{pj}\otimes
H_{S\setminus\{p,j\}}(A).                                      \tag{1}
\]

For `|S| >= 4`, every nonzero summand in (1) has partition rank one,
for the nontrivial bipartition `{p,j} | S\{p,j}`.  The partition rank of
the diagonal tensor

\[
\Delta_{S,q}=\sum_{r=1}^q e_r^{\otimes S}
\]

is exactly `q` over every field (the diagonal partition-rank lemma).  Hence

\[
q\le d_p:=\#\{j:A_{pj}\ne0\text{ and }
H_{S\setminus\{p,j\}}(A)\ne0\}\le |S|-1.                       \tag{2}
\]

Thus every site of a putative `q`-color realization has at least `q`
tensor-active partners.  For four sites, (2) proves `q <= 3` with no
positivity, same-color-endpoint, simplicity, or genericity assumption.  It
also explains why the same invariant stalls at `q <= 5` for six sites.

An ordinary fixed flattening cannot replace partition rank here.  For
example, if `A_13=A_24=I_q`, the single matching term
`A_13 tensor A_24` has rank `q^2` across the cut `12 | 34`, although it has
partition rank one across `13 | 24`.

### What simultaneous star expansions add

All star expansions can be combined exactly.  For arbitrary scalars
`alpha_v` satisfying `sum_v alpha_v=1`, every perfect matching uses each
vertex once, and hence

\[
H_S(A)=\sum_{i<j}(\alpha_i+\alpha_j)
 A_{ij}\otimes H_{S\setminus\{i,j\}}(A).                        \tag{8}
\]

Indeed, the coefficient acquired by a fixed matching `M` on the right is
`sum_{ij in M}(alpha_i+alpha_j)=sum_v alpha_v=1`.  If `G_*` is the graph of
tensor-active edges

\[
E(G_*)=\{ij:A_{ij}\ne0,\ H_{S\setminus\{i,j\}}(A)\ne0\},
\]

then the diagonal partition-rank lemma applied to (8) gives the simultaneous
necessary condition

\[
q\le \min_{\sum_v\alpha_v=1}
\#\{ij\in E(G_*):\alpha_i+\alpha_j\ne0\}.                       \tag{9}
\]

This is also the complete family of universal scalar combinations of the
edge-deletion terms.  Namely, suppose scalars `beta_ij` obey
`sum_{ij in M} beta_ij=1` for every perfect matching of the complete graph.
Comparing two matchings which agree off four vertices gives, for every four
distinct indices,

\[
\beta_{ij}+\beta_{k\ell}=\beta_{ik}+\beta_{j\ell}
=\beta_{i\ell}+\beta_{jk}.
\]

Over `C` these four-point relations imply
`beta_ij=alpha_i+alpha_j` (for instance define
`alpha_i=(beta_ij+beta_ik-beta_jk)/2`; the relation makes this independent
of the auxiliary distinct `j,k`).  The matching-sum condition then says
`sum_i alpha_i=1`.  Thus merely taking further scalar linear combinations
of star expansions cannot yield an invariant beyond (9).

Taking one `alpha_p=1` and all others zero recovers (2), so (9) can be
strictly stronger for a sparse active graph.  For example, every bipartite
connected component of `G_*` must be balanced.  Otherwise put opposite
constants on the two sides of that component and zero on all other
components.  Every active-edge coefficient is then zero but `sum alpha_v`
is nonzero, so normalization in (8) would give `H_S=0`.

However, (9) does not by itself improve the universal `q <= |S|-1`.  For a
complete active graph on `n>=4` vertices its minimum is exactly `n-1`.  To
see the lower bound, form the graph `Z` of pairs with
`alpha_i+alpha_j=0`.  If `Z` is disconnected it has at most
`binom(n-1,2)` edges.  If it is connected, it has no odd cycle (an odd cycle
would force every `alpha_i=0`), so it is bipartite; its two sides must have
unequal sizes because `sum alpha_i ne 0`, and their product is again at most
`binom(n-1,2)`.  Thus at least `n-1` pairs survive, while the one-vertex
choice attains `n-1`.  On six vertices, balanced `K_{3,3}` similarly makes
the right-hand side of (9) exactly `3`: the one-vertex choice gives three,
whereas seven zero edges would form a connected spanning zero-edge graph,
forcing opposite constants on the two equal sides and hence sum zero.
Consequently simultaneous star identities alone do not exclude the critical
`q=3` case.

## 2. Exact two-site contraction / exterior identity

Fix distinct sites `p,q`, put `R=S\{p,q}`, and take an arbitrary bilinear
covector `C in V_p^* tensor V_q^*`.  Define

\[
s_C=\langle C,A_{pq}\rangle
\]

and, for distinct `i,j in R`,

\[
B^C_{ij}=\operatorname{contr}_{p,q}^C
  (A_{pi}\otimes A_{qj}+A_{pj}\otimes A_{qi})\in V_i\otimes V_j, \tag{3}
\]

where tensors are canonically reordered before contraction.  Splitting a
perfect matching according as it contains `pq` or sends `p,q` to two
different vertices proves

\[
\operatorname{contr}_{p,q}^C H_S(A)
=s_C H_R(A)+D H_R(A)[B^C],                                      \tag{4}
\]

with the completely explicit directional derivative

\[
D H_R(A)[B]=\sum_{M\in\operatorname{PM}(R)}
 \sum_{ij\in M}B_{ij}\otimes
 \bigotimes_{e\in M\setminus\{ij\}}A_e.                       \tag{5}
\]

If `H_S(A)=Delta_{S,q}`, then (4) becomes

\[
s_C H_R(A)+D H_R(A)[B^C]
=\sum_{r=1}^q C(e_r,e_r)e_r^{\otimes R}.                        \tag{6}
\]

In particular every alternating `C in wedge^2 V^*` gives the exact exterior
constraint

\[
s_C H_R(A)+D H_R(A)[B^C]=0.                                    \tag{7}
\]

The derivative term in (4) is the precise obstruction to an induction that
simply caps two sites and claims to obtain a scalar multiple of the induced
matching tensor.  Also, `s_C` need not vanish for alternating `C`, because
endpoint-colored `A_pq` need not be symmetric.

## 3. Exact cancellation example defeating termwise-support lemmas

There is already a cancellation-rich realization of `Delta_{6,2}`.  Its
only nonzero aggregate edge tensors are

\[
\begin{array}{c|c}
12&(e_1+e_2)\otimes e_1\\
34,56,24&e_1\otimes e_1\\
13&-e_2\otimes e_1\\
16,23,45&e_2\otimes e_2.
\end{array}
\]

The underlying support graph has exactly three perfect matchings.  Their
tensors are, respectively,

\[
e_1^{\otimes6}+e_2\otimes e_1^{\otimes5},\qquad
-e_2\otimes e_1^{\otimes5},\qquad e_2^{\otimes6}.
\]

Their sum is exactly `Delta_{6,2}`.  Thus a nonconstant coefficient can have
two nonzero matching contributions which cancel, even with integer weights;
one cannot infer termwise vanishing or delete the bichromatic edges.

This example also witnesses nontrivial cancellation in (7).  Take
`p=1,q=3` and
`C=e_2^* tensor e_1^* - e_1^* tensor e_2^*`.  Then `s_C=-1`, while
`H_{\{2,4,5,6\}}=e_1^{\otimes4}`.  The matching `12,34,56` contributes
`+e_1^{\otimes4}` to the derivative term, exactly cancelling
`s_C H_R`; the all-2 matching contracts to zero.  Hence alternating
contraction does not force the antisymmetric part of an individual edge
tensor to vanish.

`computations/verify_cancellation_example.py` checks all 64 coefficients over
the integers and enumerates the three supported perfect matchings.
