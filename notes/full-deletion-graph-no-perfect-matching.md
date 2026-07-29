# A full deletion graph need not have a perfect matching

For a recurrence family `F` on an even ground set `V`, write

\[
 E(F)=\{uv:\{u,v\}\in F\},\qquad
 D(F)=\{uv:\{u,v\}\in F,\ V\setminus\{u,v\}\in F\}.
\]

Expanding the feasible full set at each pivot proves only that `D(F)` has
no isolated vertex.  It is tempting to choose a perfect matching of `D(F)`
and compare three such matchings.  The following minimal recurrence model
shows that this choice need not exist.

## Six-vertex model

Let

\[
 V=\{0,1,2,3,4,5\}
\]

and declare the following even sets feasible:

\[
 \varnothing,\quad V,\quad \binom V2,\quad
 V\setminus\{0,i\}\quad(1\leq i\leq5).
 \tag{1}
\]

All other four-sets are infeasible.  This satisfies the exact support
consequences of the diagonal recurrence:

* a two-set has its unique edge-to-empty summand and is feasible;
* at every pivot of every four-set, all three edge/remainder summands are
  supported, so either value (feasible or infeasible) is permitted;
* at the full set, the supported partners are precisely the neighbors of
  the pivot in the star with center `0`.  There are five terms at pivot `0`
  and one term at every other pivot, consistent with feasibility of `V`.

Here every pair is feasible, while its complementary four-set is feasible
exactly for the five pairs `0i`.  Consequently

\[
                         D(F)=K_{1,5}.                  \tag{2}
\]

This deletion graph is spanning and has minimum degree one, but it has no
perfect matching.

## A genuine rational hafnian module

The failure is not an artifact of discarding the values.  Split the same
six vertices into

\[
 L=\{0,1,2\},\qquad R=\{3,4,5\},
\]

and take the symmetric zero-diagonal matrix `A` with weights

\[
 a_{ij}=1\quad(ij\notin\tbinom R2),
 \qquad
 a_{ij}=-2\quad(ij\in\tbinom R2).                       \tag{3}
\]

For a cross edge `ij in L times R`, its complementary four-set has one
`L-L`/`R-R` matching and two all-cross matchings.  Therefore

\[
                    \operatorname{haf}A[V\setminus ij]
                         =(1)(-2)+1+1=0.                \tag{4}
\]

For an edge inside `L`, the complementary set has one `L` vertex and
three `R` vertices, giving cofactor `3(-2)=-6`.  For an edge inside `R`,
the analogous cofactor is `3`.  All edge weights are nonzero, so

\[
                         C(F)=D(F)=K_3\mathbin{\dot\cup}K_3,           \tag{5}
\]

where `F` is the exact nonzero principal-hafnian family of `A`.  In
particular this genuine deletion/cofactor graph has no perfect matching.

The full hafnian is nevertheless nonzero.  The six all-cross perfect
matchings contribute `6`, while the nine matchings with one cross edge
contribute `9(-2)=-18`; hence

\[
                         \operatorname{haf}A[V]=-12.    \tag{6}
\]

Equivalently, every nonzero full-recurrence edge term is `-6`.  Each pivot
sees the two edges in its own triangle, and their sum is `-12`.  This makes
the obstruction transparent: the recurrence gives a signed/complex
fractional perfect matching on `D(F)`, and odd components can support such
a fractional object without supporting an integral perfect matching.

## Minimality and consequence

Order six is minimal.  On four vertices, if an edge belongs to `D(F)`, its
complementary edge also belongs to `D(F)`; those two edges themselves form
a perfect matching.  Feasibility of the full set ensures that `D(F)` is
nonempty.

## Even the stronger private cofactor graphs need not have matchings

Define the larger cofactor graph

\[
 C_r=\{uv:V\setminus\{u,v\}\in F_r\}.
\]

The actual no-cover consequence is stronger than deletion-edge privacy:

\[
                         C_r\cap E(F_s)=\varnothing
                         \qquad(r\ne s).                 \tag{7}
\]

Indeed an edge in this intersection immediately gives an `(n-2,2,0)`
cover.  Nevertheless, even (3) does not restore the proposed matching
argument.  There is an exact eight-vertex recurrence model satisfying (3)
in which

\[
\begin{aligned}
C_0={}&\{04,13,24,35,67\},\\
C_1={}&\{02,06,16,17,23,46,56,57\},\\
C_2={}&\{07,14,27,36,45\}.
\end{aligned}                                           \tag{8}
\]

None has a perfect matching.  The first and third each have two odd
components already; deleting vertex `6` from the second leaves three odd
components.  Their deletion subgraphs are

\[
D_0=C_0,\qquad
D_1=C_1\setminus\{02,17\},\qquad
D_2=C_2.                                                   \tag{9}
\]

so all three `D_r` also lack perfect matchings.

The full feasible families are recorded as exact support bitsets in the
audit script.  Independent enumeration checks every recurrence pivot and
every cross-color cofactor-privacy condition.  The model has 97 proper
feasible covers, all of size type `(4,4,0)` or `(4,2,2)`; condition (3)
correctly eliminates every `(6,2,0)` cover.  Thus it is not a counterexample
to the desired covering theorem.  It instead shows precisely that even the
strong cofactor-graph conditions discard the middle-layer mechanism that
creates a cover.

Thus the recurrence axioms do **not** justify selecting even one
`D_r`-perfect matching, let alone three of them.  Any three-family argument
must retain more information than the unlabelled deletion graphs.  Two
possible replacements are:

1. work with the pivot-labelled choices (a supported deletion edge for
   each pivot), allowing many pivots to select the same hub; or
2. exploit cross-color privacy `C_r cap E(F_s)=empty` together with the
   middle ranks, rather than reducing to `C_r` or `D_r` alone.

The dependency-free exact audit is
`computations/verify_full_deletion_graph_no_perfect_matching.py`.
