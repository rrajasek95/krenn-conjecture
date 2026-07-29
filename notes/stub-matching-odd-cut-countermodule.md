# Stub-matching rewrites can force a bridge on the minimum face

## Outcome

Odd-cut parity does not orient the global selected-triple rewrite.  A state
is naturally a perfect matching of the `3n` vertex--colour stubs, and a
mixed transversal replacement preserves the selected stub at every vertex.
For every odd shore, the cut size stays odd, but its slack can increase or
decrease.

There is a sharp six-site countermodule over `Q`.  All `3^6=729`
homogeneous coefficient fibres vanish exactly, the three chosen constant
matching monomials are individually equal to one, and all supported cells
can be put at the same nonarchimedean valuation.  Its selected state is the
bridgeless triangular prism.  Rewriting one mixed transversal has three
cancellation mates, and **every one** produces a connected cubic occurrence
state with a bridge.  The exact state relation is

\[
                              1-3+1+1=0.                 \tag{1}
\]

Thus global valuation minimality, all leading coefficient equations,
cut parity, and freedom to choose a mate do not imply bridgelessness.  The
module has zero output rather than the inhomogeneous GHZ target, so the
remaining possible input is precisely a higher valuation layer carrying
the three target normalizations.

## 1. States are matchings of colour stubs

Let

\[
                         \Omega=B\times\{0,1,2\}.         \tag{2}
\]

An occurrence `(uv;a,b)` is an edge between the stubs `(u,a)` and `(v,b)`.
A locally rainbow cubic occurrence network `G` is exactly a perfect
matching of `Omega`: after forgetting the colour labels, every site has
degree three, and its three incident occurrences use its three different
stubs.

A **site transversal** `R` in `G` is a set of occurrences which covers each
site once.  It is therefore a perfect matching of `B`, and its chosen stubs
have the form

\[
                         \tau_R=\{(v,c_v):v\in B\}.       \tag{3}
\]

Every matching `N` in the same colouring fibre is another perfect matching
of the same stub set `tau_R`.  Hence

\[
                         G_N=(G\setminus R)\sqcup N       \tag{4}
\]

is again a perfect matching of all of `Omega`.  This is the global stub
version of the selected-triple rewrite; no local colour compatibility is
lost in (4).

## 2. Exact cut bookkeeping

For `S subset B`, let `b_S(G)` be the number of occurrences of `G` crossing
the site cut `delta(S)`.  If `|S|` is odd, the cubic handshake identity gives

\[
             3|S|=2|E_G(S)|+b_S(G),\qquad b_S(G)\equiv1\pmod2.           \tag{5}
\]

Both site perfect matchings `R` and `N` also cross every odd cut an odd
number of times.  Consequently

\[
                  b_S(G_N)=b_S(G)-b_S(R)+b_S(N),          \tag{6}
\]

and, for the odd-cut slack

\[
                         \sigma_S(G)={b_S(G)-1\over2},    \tag{7}
\]

one has the exact change

\[
              \sigma_S(G_N)-\sigma_S(G)
                    ={b_S(N)-b_S(R)\over2}.              \tag{8}
\]

Equation (5) is invariant but (8) has no sign.  For a connected cubic
multigraph, a bridge cuts off an odd shore, so bridgelessness is equivalent
to `b_S(G)>=3` for every odd proper shore.  A replacement with
`b_S(R)=3,b_S(N)=1` therefore creates a bridge in one step.

There is also no hidden orientation from valuation minimality.  If `G` has
minimum valuation among all supported stub states and contains a mixed
transversal `R`, then every supported replacement (4) has valuation at
least that of `G`.  Thus `z(R)` is a minimum term in its colouring fibre.
The ultrametric inequality applied to the exact zero coefficient supplies
another term of the same valuation, but says nothing about its value of
`b_S`.  The following module makes every such mate have smaller slack.

## 3. An exact all-fibre prism kernel

On `B={0,...,5}`, take the three one-factors

\[
\begin{aligned}
 P_0&=04\mid12\mid35,\\
 P_1&=05\mid14\mid23,\\
 P_2&=03\mid15\mid24.                                  \tag{9}
\end{aligned}
\]

Their union `E` is the triangular prism.  Put a full nonzero `3 by 3`
block on every edge of `E`, and no cell off `E`.  Define underlying edge
scalars

\[
                  h_{12}=-3,\qquad h_e=1\quad(e\ne12),   \tag{10}
\]

and endpoint gauges

\[
                 \lambda_{0,0}=-\frac13,
                 \qquad\lambda_{v,a}=1\quad((v,a)\ne(0,0)).             \tag{11}
\]

Every supported aggregate cell is

\[
                         A_{uv}(a,b)=h_{uv}
                             \lambda_{u,a}\lambda_{v,b}. \tag{12}
\]

The prism has exactly four underlying perfect matchings: the three in (9)
and

\[
                              R=04\mid15\mid23.           \tag{13}
\]

Their `h`-products are respectively

\[
                              -3,1,1,1.                  \tag{14}
\]

For an arbitrary vertex colouring `c`, every matching term has the common
endpoint factor

\[
                              \Lambda_c=\prod_v\lambda_{v,c_v}.          \tag{15}
\]

Therefore its complete coefficient is

\[
             F_c(A)=\Lambda_c(-3+1+1+1)=0.               \tag{16}
\]

This proves all 729 equations at once, over characteristic zero and with no
genericity or dimension argument.  The gauge (11) also normalizes the three
selected constant monomials:

\[
                  z(P_0^{00})=z(P_1^{11})=z(P_2^{22})=1. \tag{17}
\]

Let `U` be the union of these three decorated matchings.  It is a perfect
matching of all eighteen stubs, has weight one, and its occurrence graph is
the bridgeless prism.

If desired, work over `Q((t))` and multiply every cell in (12) by `t^{-1}`.
Every matching term then has valuation `-3` and every stub state has
valuation `-9`.  Thus `U` is globally valuation-minimal, as are all of its
replacement states.  Equation (16) remains exact.

## 4. Every mate is bridged

Decorate (13) using the occurrences already present in `U`.  Its colouring
is

\[
                              c=(0,2,1,1,0,2),            \tag{18}
\]

so it is mixed.  Put `Q=U\setminus R`.  For the odd shore

\[
                              S=\{0,3,5\},                \tag{19}
\]

the six occurrences of `Q` are precisely the two internal triangles on
`S` and its complement.  In particular

\[
                         b_S(U)=b_S(R)=3,qquad b_S(Q)=0. \tag{20}
\]

The complete `c`-fibre consists of the decorated versions of
`R,P_0,P_1,P_2`.  Besides `R`, call these three matchings `N_0,N_1,N_2`.
They cross (19) exactly once, on `04`, `23`, and `15`, respectively.  Hence

\[
                         b_S(Q\sqcup N_i)=1               \tag{21}
\]

for every `i`.  Each replacement is connected, so its sole crossing
occurrence is a literal bridge.  There is no good cancellation mate hidden
among the other terms.

The numerical state weights make the same conclusion exact algebraically.
From (12),

\[
 z(R)=-\frac13,qquad z(N_0)=1,qquad
 z(N_1)=z(N_2)=-\frac13,qquad W(Q)=-3.                  \tag{22}
\]

Multiplying the fibre equation by `W(Q)` gives

\[
       W(U)+W(Q\sqcup N_0)+W(Q\sqcup N_1)+W(Q\sqcup N_2)
                         =1-3+1+1=0.                     \tag{23}
\]

All four terms have the same `t`-valuation `-9`.  Replacing any `N_i` by
`R` literally restores `U`, so the move is reversible as well as
bridge-forcing in the forward rewrite.

## 5. Consequence and exact boundary

The module rules out each of the following proposed inputs, separately and
together, as an orientation of selected-triple rewrites:

1. parity of every odd cut;
2. nonnegative odd-cut slack;
3. bridgelessness of the selected state;
4. global minimum valuation; and
5. all homogeneous coefficient equations on the minimum layer.

The missing hypothesis is genuinely inhomogeneous.  The source (12) has
`H(A)=0`, whereas a Krenn source must have its three constant coefficients
equal to one.  In a nonarchimedean argument, (12) is an exact possible
homogeneous initial module below the target valuation, but this note does
not prove that it lifts through the later layers of a full exact source.
Thus a valid global theorem must use those later normalization equations
or another liftability constraint; cut parity and the initial rewrite
module cannot supply it.

[`verify_stub_matching_odd_cut_countermodule.py`](../computations/verify_stub_matching_odd_cut_countermodule.py)
enumerates the four prism matchings and all 729 colourings over `Q`, checks
(16)--(17), verifies the eighteen-stub matching condition, computes every
bridge and cut size in (20)--(21), audits (5)--(6) on every odd shore for
all three replacements, and checks the exact weighted rewrite (23).
