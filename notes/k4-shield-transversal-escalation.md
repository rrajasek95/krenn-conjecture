# `K_4` shields escalate from a coarse transversal to a pivot cofactor

The first rational shield module in
`notes/three-family-k4-shield-countermodule.md` has the feasible cover

\[
 (S\cup\{4,6\})\mathbin{\dot\cup}\{5,7\}
                         \mathbin{\dot\cup}\varnothing. \tag{1}
\]

It is natural to conjecture that a shielded minimal four-core always has a
feasible cofactor containing all of `S` and one vertex from each outside
class.  This note gives the smallest exact countermodule to that statement
and isolates the valid deterministic-pivot replacement.

## 1. A valid global pivot lemma

For a recurrence family `F_r`, define its full deletion graph

\[
 D_r=\{uv:\{u,v\}\in F_r,\ V\setminus\{u,v\}\in F_r\}.                 \tag{2}
\]

**Lemma 1 (private pivot).**  If `F_0,F_1,F_2` have no proper disjoint
feasible cover, then

\[
                         D_r\cap E(F_s)=\varnothing
                         \qquad(r\ne s).                 \tag{3}
\]

Moreover every vertex has a neighbor in every `D_r`.

**Proof.**  An edge `uv in D_r cap E(F_s)` gives the proper two-color cover

\[
             V=(V\setminus\{u,v\})\mathbin{\dot\cup}\{u,v\}
                                      \mathbin{\dot\cup}\varnothing     \tag{4}
\]

in colors `r,s,t`.  This proves (3).  Expanding the nonzero full recurrence
at an arbitrary pivot supplies an incident edge in (2). `QED`

Thus a deterministic pivot does yield a cover exactly when one of its
nonzero cofactor edges is supported in another color.  The missing global
step is to force such an overlap; recurrence in one color only proves that
`D_r` is spanning.

## 2. Killing every coarse transversal

Retain the blocks

\[
 S=\{0,1,2,3\},\quad A=\{4,5\},\quad B=\{6,7\}.         \tag{5}
\]

Colors one and two are exactly the two rational shield matrices from the
preceding note.  In particular their full hafnians are both `30`,
`h_1(A)=h_2(B)=1`, and

\[
 h_1(A\cup e)=h_2(B\cup e)=0
                         \qquad(e\in\tbinom S2).         \tag{6}
\]

For color zero, give `S` the weights

\[
 a_{01}=-2,qquad a_{02}=a_{03}=a_{12}=a_{13}=a_{23}=1, \tag{7}
\]

put every edge inside `A union B` equal to zero, and give each outside
vertex `4,5,6,7` the same column to `S`,

\[
                              z=(1,1,2,5/2).             \tag{8}
\]

As before, `h_0(S)=-2+1+1=0`.  More strongly, for every two-set
`C subset A union B`,

\[
                              h_0(S\cup C)=0.            \tag{9}
\]

Indeed the two outside vertices must both cross into `S`; after factoring
the two orders, the remaining scalar is

\[
\begin{aligned}
 &-2z_2z_3+z_1z_3+z_1z_2+z_0z_3+z_0z_2+z_0z_1\\
 &\hspace{35mm}=-10+5/2+2+5/2+2+1=0.                  \tag{10}
\end{aligned}
\]

Every full perfect matching must match the four outside vertices
bijectively to `S`.  Hence

\[
                h_0(V)=4!z_0z_1z_2z_3=120\ne0.         \tag{11}
\]

The three full values are therefore `(120,30,30)`, while (6), (7), and (9)
retain all pair shields and kill every proposed cofactor of the form (1).

## 3. The next layer and the deterministic pivot

The module still has a cover, as it must at order eight.  Delete the cross
edge `37`.  Directly,

\[
 h_0(V\setminus\{3,7\})
      =3!z_0z_1z_2=12,                                  \tag{12}
\]

while the color-one shield matrix has `a^1_37=1`.  Thus

\[
 V=\{0,1,2,4,5,6\}\mathbin{\dot\cup}\{3,7\}
                                      \mathbin{\dot\cup}\varnothing    \tag{13}
\]

is feasible in colors `0,1,2`, with hafnians `(12,1,1)`.

This is a genuine full-pivot cofactor: `37 in D_0 cap E(F_1)`.  It contains
three vertices of `S` and three outside vertices, rather than the whole
core plus an outside pair.  Exact enumeration finds 924 proper feasible
colorings.

Consequently the coarse-transversal theorem is false.  The correct global
target is now precise:

> under the shield hypotheses and no-cover assumption, prove that some
> full deletion graph `D_r` must meet another color's edge support.

Lemma 1 would then finish immediately.  The present construction shows why
one must use all three private deletion graphs simultaneously: neither the
minimal core, all six pair shields, nor the vanishing of every
`S`-containing six-set forces the overlap separately.

The exact audit is
`computations/verify_k4_shield_transversal_escalation.py`.
