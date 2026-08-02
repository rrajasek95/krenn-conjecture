# A rank-\(55\) \(1I+5Z\) guard survives the generic kernel and selected R2

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and exact scope

There is an exact selected level-two packet with endpoint-matrix ranks

\[
                              (2,0,0,0,0,0),                    \tag{1}
\]

all endpoint potentials zero, and

\[
                              \operatorname{rank}d\Psi_M=55.   \tag{2}
\]

It satisfies all \(60\) scalar generic-kernel identities, all \(64\)
selected level-two rows, and the six literal residual R2 rows for the
selected binary colour pair. At the sole invertible root, R2 uses two
distinct internal pure-column witnesses. At the five zero-star roots, the
selected pair is preserved.

Thus generic-kernel plus these selected residual R2 rows cannot close the
\(1I+5Z\) endpoint-rank pattern. Any exclusion of this component must use
additional information, such as L0/L1, an overlapping level-two block, or
R2 for further colour pairs. This packet is a guard, not a full eight-site
solution, not a conjecture counterexample, and not evidence that it extends
to the omitted equations.

The subsequent
[linear-L0 obstruction](level-two-one-invertible-five-zero-l0-obstruction.md)
shows that this exact residual packet does not extend: neither physical pure
target lies in its differential image. The guard retains its stated force
against generic kernel plus selected R2, but is not a survivor of L0.

## The zero-potential component leaves \(M\) arbitrary

For a selected level-two block, write

\[
 P_x=\binom{A_{px}[c,a]}{A_{px}[c,b]},\qquad
 Q_x=\binom{A_{qx}[c,a]}{A_{qx}[c,b]},\qquad
 X_x=[P_x\ Q_x],
\]

and let \(M\) be the residual binary packet on sites \(0,\ldots,5\). The
generic-kernel equation is

\[
 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv},\qquad
 J=\begin{pmatrix}0&1\\1&0\end{pmatrix}.                       \tag{3}
\]

Choose

\[
 X_0=I_2,\qquad X_1=\cdots=X_5=0,\qquad
 \nu_0=\cdots=\nu_5=0.                                       \tag{4}
\]

Every edge \(uv\) has at least one zero endpoint matrix, so the left side
of (3) vanishes. The right side also vanishes. Consequently (3) imposes no
condition at all on \(M\) on this zero-potential component. Since
\(z=-\sum_x\nu_x=0\), the exact selected level-two equation

\[
 z\Psi(M)+d\Psi_M(N)=0,\qquad
 N_{uv}=P_uQ_v^{\mathsf T}+Q_uP_v^{\mathsf T},                  \tag{5}
\]

is also automatic: in (4), no edge has two nonzero endpoint matrices, so
\(N=0\).

This is the sharply stated residual freedom behind the guard. It is not a
dimension heuristic: both sides of every scalar equation in (3) and (5)
are literally zero.

## An integral maximal-rank residual packet

Use pure \(E_{00}\) blocks on the one-factor

\[
                              01\mid23\mid45
\]

and pure \(E_{11}\) blocks on

\[
                              02\mid14\mid35.                   \tag{6}
\]

Give these six cells the nonzero integer weights specified by the checker,
and put deterministic positive integer \(2\times2\) blocks on the other
nine edges. This is the same useful residual design as the earlier
[one-sided rank-\(55\) guard](level-two-one-sided-rank55-guard.md), but with
a different endpoint-star assignment: here only \(X_0\) is nonzero, and it
is invertible.

The \(64\times60\) integer matrix \(d\Psi_M\) has rank exactly \(55\):

1. the five trace-zero vertex scalings
   \[
   K^\mu_{uv}=(\mu_u+\mu_v)M_{uv},\qquad \sum_u\mu_u=0,
   \]
   are independent integral kernel vectors, giving rank at most \(55\);
2. row reduction modulo \(101\) gives rank \(55\), so an integer
   \(55\times55\) minor is nonzero and the rational rank is at least \(55\).

The checker also constructs all \(60\) columns as literal finite
differences of the matching tensor. Hence the rank computation audits the
actual differential, not a support surrogate. Its \(64\) base matching
values are all nonzero, although that stronger property is not needed.

## Literal selected residual R2 rows

Take the physical selected stars

\[
 P_0=e_0,\qquad Q_0=e_1,\qquad
 P_x=Q_x=0\quad(1\le x\le5).                                  \tag{7}
\]

Thus \(X_0=I_2\), as required by (4). At residual root \(0\), the two rare
endpoint edges contain the outside output colour \(c\), so preservation of
the pair \(\{a,b\}\) fails. The two internal blocks

\[
                              M_{01}\sim E_{00},\qquad
                              M_{02}\sim E_{11}                  \tag{8}
\]

are nonzero, supported only in the physical output columns \(a\) and \(b\),
and lie on distinct neighbor labels. Their complementary four-site
cofactors are nonzero. They are therefore the two literal pure-column R2
witnesses at the sole invertible root.

At each root \(1,\ldots,5\), both selected endpoint stars vanish. All
residual blocks use only the binary output columns \(a,b\), so every
incident selected pair of rows is supported in those two columns. These
five roots satisfy the preservation alternative of R2. No pure-column
witness is inferred from a change of basis: (7)--(8) are audited directly
in the physical selected coordinates.

For an independent check of the value equation, the audit builds the
literal eight-site packet with the two rare endpoints fixed to colour \(c\)
and sums every perfect matching in all \(64\) selected rows. Every sum is
zero. This remains only a selected-block calculation; unlisted cells and
unselected equations are not assigned or claimed.

## Consequence for the endpoint-rank map

The at-most-one-invertible frontier cannot be attacked by extending the
generic-kernel/R2 support census alone. Already its \(1I+5Z\)
zero-potential component contains an arbitrary residual \(M\), including a
generic-kernel point of rank \(55\) with the selected R2 alternatives
realized exactly. The next obstruction must see data beyond this one block.

This does not classify the other \(1I+kR+(5-k)Z\) patterns, nor the
nonzero-potential boundary within \(1I+5Z\). It isolates one maximal-rank
component that every stratum-wide proof must remove by overlap or lower-level
equations.

## Exact audit

The standard-library checker
[verify_level_two_one_invertible_five_zero_r2_guard.py](../computations/verify_level_two_one_invertible_five_zero_r2_guard.py)

* verifies endpoint ranks \((2,0,0,0,0,0)\) and all \(60\)
  generic-kernel scalar identities;
* constructs the exact \(64\times60\) differential by finite differences,
  proves its rank is \(55\), and checks the five independent gauges;
* checks all \(64\) differential rows and independently all \(64\) literal
  eight-site selected matching sums; and
* audits the two physical pure-column witnesses at root \(0\), their active
  complementary cofactors, and the preservation alternative at roots
  \(1,\ldots,5\).

It passes normal, optimized, and isolated Python.
