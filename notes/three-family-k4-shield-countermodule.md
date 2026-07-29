# Three-family shields do not eliminate a minimal `K_4` cancellation core

The one-family dense cancellation core in
`notes/minimal-recurrence-cancellation-core.md` does acquire strong extra
constraints inside a hypothetical three-family no-cover system.  This note
proves the exact constraint and gives the smallest simultaneous rational
countermodule to turning it directly into an induction.

## 1. The forced shield law

Let `F_0,F_1,F_2` be even-set families with `emptyset,V` feasible and with
no proper disjoint feasible cover.  Suppose

\[
 V=S\mathbin{\dot\cup}A\mathbin{\dot\cup}B,
 \qquad |S|=4,                                           \tag{1}
\]

where every pair in `S` belongs to `F_0`, while

\[
                     S\notin F_0,qquad A\in F_1,qquad B\in F_2.         \tag{2}
\]

Thus `S` is the smallest possible matchable cancellation core in a failed
matching cover.

**Lemma 1 (pair-extension shields).**  For every pair `e subset S`,

\[
                         A\cup e\notin F_1,
             \qquad     B\cup e\notin F_2.              \tag{3}
\]

If additionally `e in F_1`, then the supported graph on `A union e` has at
least two perfect matchings, and similarly with colors one and two
interchanged.

**Proof.**  Let `f=S\setminus e`, which is another pair and hence belongs
to `F_0`.  Feasibility of `A union e` would make

\[
                         V=f\mathbin{\dot\cup}(A\cup e)
                              \mathbin{\dot\cup}B         \tag{4}
\]

a proper feasible cover in colors `0,1,2`.  This proves the first
nonmembership in (3); swapping `A,F_1` with `B,F_2` proves the second.  If
`e in F_1`, a perfect matching of `A` together with `e` makes `A union e`
matchable.  The unfolding lemma says that a matchable infeasible set cannot
have a unique perfect matching, proving the last assertion. `QED`

The extra matching is the simultaneous *shield*: cancellation must protect
every attempt to move one core pair into either complementary color class.

## 2. An order-eight rational countermodule

The shield law by itself is not contradictory.  Let

\[
 S=\{0,1,2,3\},\qquad A=\{4,5\},\qquad B=\{6,7\}.       \tag{5}
\]

We give three symmetric zero-diagonal rational matrices.  Unlisted entries
are zero, and every displayed four-vector lists the entries from vertices
`0,1,2,3` to the named outside vertex.

All three matrices have the same restriction to `S`:

\[
 a_{01}=-2,qquad a_{02}=a_{03}=a_{12}=a_{13}=a_{23}=1, \tag{6}
\]

and all have `a_45=a_67=1`.  Put

\[
 x=(1,1,0,-1/2),\quad y=(1,0,1,1),
\quad p=(1,2,1/2,1/2),\quad q=(0,2,-1,-1).              \tag{7}
\]

For color zero, the columns to `4,5` are both `x`, the columns to `6,7`
are both `y`, and all four `A--B` entries vanish.

For color one, the columns to `4,5` are `p,q`, the columns to `6,7` are
both `y`, and all four `A--B` entries are one.  Color two is obtained by
swapping the roles of `A` and `B`: its columns to `6,7` are `p,q`, its
columns to `4,5` are both `y`, and again all `A--B` entries are one.

Let `F_r` be the nonzero principal-hafnian support of the color-`r` matrix.
These are genuine characteristic-zero recurrence families.  Exact
expansion gives

\[
 \bigl(h_0(V),h_1(V),h_2(V)\bigr)=(2,30,30),            \tag{8}
\]

so every full set is feasible, while for every color

\[
 h_r(S)=h_r(S\cup A)=h_r(S\cup B)=0.                   \tag{9}
\]

Also `h_1(A)=h_2(B)=1`, and, for every pair `e subset S`,

\[
                         h_1(A\cup e)=h_2(B\cup e)=0.   \tag{10}
\]

To see the first equality in (10) directly, if `e={i,j}` then

\[
 h_1(A\cup e)=a_{ij}+p_iq_j+q_ip_j=0;                  \tag{11}
\]

the six off-diagonal entries of `pq^T+qp^T` are precisely the negatives of
the six entries (6).  The other equality is identical.

Equations (9)--(10) kill every proper coloring which is constant on each of
the three blocks `S,A,B`, as well as every direct repair which leaves one
core pair in color zero and moves the complementary pair into `A` or `B`.
Thus all consequences used in the most direct `K_4`-core contraction are
satisfied simultaneously.

The module is deliberately not a global no-cover model.  For example,

\[
 \{0,1,2,3,4,6\}\in F_0,qquad \{5,7\}\in F_1,qquad
 \varnothing\in F_2,                                   \tag{12}
\]

with respective hafnians `11/2,1,1`.  This repair takes one vertex from
each shield pair.  It is invisible to (3), (9), and (10).  Exact enumeration
finds 955 proper feasible colorings, all supplied by such finer crossing
data rather than by the canceled coarse block states.

## 3. Induction boundary

The example is order-minimal for a simultaneous nonempty shield:
`|S|>=4` and two nonempty even complementary classes require at least
`4+2+2=8` vertices.  It proves that cross-color coupling does **not** defeat
the one-color `K_4` core using only pair-extension cancellations, full-set
accessibility, or coarse block contractions.

A successful induction must control the transversal cofactors typified by
(12).  Equivalently, after (3) forces the zero- and two-cross layers, one
must use the next crossing layer across both shields.  This is a genuinely
three-family condition; Gallai--Edmonds structure of the core and the two
separate shield cycles do not contain it.

The dependency-free exact audit is
`computations/verify_three_family_k4_shield_countermodule.py`.
