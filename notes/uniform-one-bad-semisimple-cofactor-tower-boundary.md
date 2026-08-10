# Semisimplicity does not close the carrier-rich one-bad branch

## Outcome

Put

\[
 P=\langle p_1,p_2\rangle,\qquad S=\langle s_1,s_2\rangle,
 \qquad F=q^{[h-1]}.
\]

The four one-bad rows say that multiplication by $F$ is the bilinear map

\[
 B:P\times S\longrightarrow
 A=\mathbb C X_1\oplus\mathbb C X_2,
 \qquad B(p_i,s_j)=\delta_{ij}X_i.                    \tag{1}
\]

Thus $A$ is the semisimple algebra consisting of two copies of the complex
numbers, and (1) is a perfect $A$-valued pairing.  This has a sharp but
negative consequence:

\[
 P\cap N_S=0,\qquad S\cap N_P=0,                     \tag{2}
\]

where

\[
 N_S=\{\ell:\ell S F=0\},\qquad
 N_P=\{\ell:P\ell F=0\}.                             \tag{3}
\]

Semisimplicity makes the two whole star planes dual.  It does not put an
individual physical-site component of a star into either ambient kernel in
(3).  Such a component is exactly what a source-preserving deletion or
concentration argument needs.  Therefore the two-summand semisimple
structure is a normal form for the remaining problem, not its solution.

The exact checker is
`computations/verify_uniform_one_bad_semisimple_cofactor_tower_boundary.py`.

## 1. The genuine $h=3$ cofactor recurrence

On six labelled residual sites let $q_{xy}$ be the universal scalar
quadratic.  Retain every source edge label.  For disjoint physical edges put

\[
\begin{aligned}
 H_e&=\operatorname{Haf}(q|_{U\setminus e}),\\
 G_{e,f}&=\operatorname{Haf}(q|_{U\setminus(e\cup f)}),\\
 J_{e,f,g}&=1\quad(e\sqcup f\sqcup g=U).
\end{aligned}                                         \tag{4}
\]

There are respectively 15, 45, and 15 such source-labelled objects.  Direct
perfect-matching expansion gives every recurrence

\[
\begin{aligned}
 G_{e,f}&=\sum_{g\cap(e\cup f)=\varnothing}q_gJ_{e,f,g},\\
 2H_e&=\sum_{f\cap e=\varnothing}q_fG_{e,f},\\
 3q^{[3]}&=\sum_eq_eH_e.                              \tag{5}
\end{aligned}
\]

At $h=3$, the first line has a unique complementary edge.  Thus imposing
genuine third cofactors does not add a freely adjustable curvature row: it
sets $G$ equal to the literal complementary $q$-cell, and the next line
sets $H$ equal to the three literal two-edge matchings.  Contracting (5)
with $p_i,s_j$ recovers (1); it does not produce a one-sided kernel beyond
(2).

## 2. Exact site-component cokernel

The independent-target minimum-response packet has the component columns

\[
\begin{array}{c|cc}
 &\text{first site}&\text{second site}\\ \hline
 p_1&X_1+Y&-Y\\
 p_2&X_2+Z&-Z.
\end{array}                                           \tag{6}
\]

Their matrix on coordinates $X_1,Y,X_2,Z$ is unimodular.  Neither site
column is in the joint kernel, although each pair sums to the desired
primitive target.  This is the smallest exact cokernel to a deletion
argument: (1) determines the sums, while the cancellation tails $Y,Z$
remain independent.  In that packet $p_1^{[2]},p_2^{[2]}\ne0$.  Its
essential scope guard remains load-bearing: $F$ is formal rather than
$q^{[2]}$ for a common $q$.

## 3. The complementary genuine-tower guard

The converse scope is also sharp.  In the scalar six-site site-square-zero
algebra take

\[
 q=e_{01}+e_{23}+e_{45},\qquad q^{[3]}=\mathrm{TOP}.   \tag{7}
\]

Its entire tower (4)-(5) is genuine.  Choose

\[
\begin{aligned}
 p_1&=e_0+e_2,&p_2&=e_1+e_4,\\
 s_1&=e_1+e_0-e_5,&s_2&=e_1-e_3+e_0.
\end{aligned}                                         \tag{8}
\]

Exact multiplication gives

\[
 p_i s_jq^{[2]}=\delta_{ij}\mathrm{TOP},              \tag{9}
\]

while all four self-squares in (8) are nonzero.  For the standard
permanent-null response

\[
 R=p_1s_1+p_1s_2-p_2s_1+p_2s_2
\]

the higher tail is

\[
 qR^{[2]}=-4\mathrm{TOP},\qquad
 R^{[3]}=-4\mathrm{TOP},\qquad
 qR^{[2]}+R^{[3]}=-8\mathrm{TOP}.                     \tag{10}
\]

So a genuine top, all genuine cofactors, and an abstract perfect diagonal
pairing do not force square-zero rows or make this standard permanent-null
cap clean.  The precise scope
guard is that both diagonal targets in (9) are the same scalar top word.
They are not the distinct endpoint-coloured words $X_1,X_2$.

Equations (6) and (7)-(10) are complementary sharp guards:

- distinct target words plus spread rows, but no common-$q$ provenance;
- genuine common $q$, top, and full cofactor tower, but collapsed target
  words.

The still-open theorem must use both inputs simultaneously.  It is exactly
an endpoint-coloured carrier-exchange statement: the shared cells which
make $q^{[h]}=X_0$ must force a nonzero site component into $N_S$ or
$N_P$, or force $R^{[2]}=0$ directly.  Another Euler recurrence or an
abstract semisimplicity argument cannot supply that step.

## Scope

This proves the universal $h=3$ source-labelled recurrence, the
coordinate-free duality/no-deletion theorem (2), and the two exact boundary
guards.  It does not construct an endpoint-coloured one-bad source, prove
the carrier-exchange theorem, or prove Krenn's conjecture.

Reproduce with

```text
.venv/bin/python computations/verify_uniform_one_bad_semisimple_cofactor_tower_boundary.py
python3 -O computations/verify_uniform_one_bad_semisimple_cofactor_tower_boundary.py
```
