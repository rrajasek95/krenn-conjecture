# A good clique has curvature or is an induced zero shore

## 1. Outcome

Two existing uniform statements combine without any Hessian-chart
classification.

Let endpoint-ordered aggregate blocks on an even set \(B\), \(|B|=N\),
satisfy

\[
                         H_B(A)=\Delta_{B,3}.                      \tag{1}
\]

Let \(C\subseteq B\), \(|C|=h\ge4\), be a clique of doubly
aggregate-injective pairs.  Then at least one of the following conclusions
is available as a proof alternative.

1. Some canonical transition on a three-neighbour fan inside \(C\) is
   nonzero.  It gives a literal nonzero \(2\times2\) source-block minor,
   an inverse two-flag selector, and a generically active affine cap line.
2. Every aggregate block internal to \(C\) is zero:

   \[
                              A_{uv}=0\qquad(u\ne v\in C).          \tag{2}
   \]

In the second branch, put \(D=B\setminus C\), \(N=2m\), and assume
\(h\le m\).  If \(q\) is the quadratic formed by the blocks internal to
\(D\), and \(p_c^{(j)}\) is the colour-\(c\) row from \(x_j\in C\) into
\(D\), then

\[
 \boxed{\quad
 \left(\prod_{j=1}^{h}p_{c_j}^{(j)}\right)q^{[m-h]}
   =
   \begin{cases}
      X_c^D,&c_1=\cdots=c_h=c,\\
      0,&\text{otherwise}.
   \end{cases}
 \quad}                                                         \tag{3}
\]

Every one of the \(h\) three-row star maps into \(D\) is injective.  If
\(h>m\), the zero-shore branch is impossible by matching capacity.

The bad-pair graph is \(4\)-degenerate, so the good-pair graph contains a
clique of order at least \(\lceil N/5\rceil\).  Consequently every exact
ternary source at every even \(N\ge16\) has the uniform alternative

\[
\boxed{
\begin{array}{c}
\text{a physical nonzero curvature minor and a generically active cap line;}
\\[2mm]\text{or}\\[1mm]
\text{an induced aggregate-zero shore of order }
h=\lceil N/5\rceil\ge4\text{ satisfying (3).}
\end{array}}                                                     \tag{4}
\]

This improves the
[former induced-zero-shore export](good-pair-fan-induced-zero-four-cut-reduction.md)
in one direction and weakens it in another.  It starts at \(N=16\), has no
E1/E2 escape list, and makes the zero shore grow linearly.  Its star rows
are arbitrary, however; it does not inherit the former two-site support
bound.  Thus (4) does not yet prove the conjecture.  It isolates two
natural, nonenumerative targets: a common-root theorem on the active cap
lines, or an arbitrary-frame obstruction to the large zero-shore identity
(3).

## 2. Clique flatness forces literal zero blocks

Fix \(p\in C\) and put

\[
                              F_p=C\setminus\{p\}.
\]

Since \(h\ge4\), the fan \(F_p\) has at least three members.  Every
\(\{p,q\}\), \(q\in F_p\), is good by the clique hypothesis.  For centre
colour \(a\), direct row \(d_q^a\), and the physical \(q\)-star \(S_q\),
the canonical transition is

\[
 D_{qr}^a(\beta,\gamma)
  =d_q^a(\beta)S_r(\gamma)|_{B\setminus\{p,q,r\}}
   -d_r^a(\gamma)S_q(\beta)|_{B\setminus\{p,q,r\}}.                \tag{5}
\]

The
[canonical transition-pencil theorem](canonical-transition-pencil-fan-dichotomy.md)
proves that if (5) vanishes for all \(a,\beta,\gamma,q,r\in F_p\), then

\[
                              A_{pq}=0\qquad(q\in F_p).             \tag{6}
\]

Suppose no transition centred at any \(p\in C\) is nonzero.  Applying
(6) for every centre proves (2).  Conversely, if one transition is
nonzero, Sections 6--7 of the cited theorem give the source minor,
two-flag inverse, and active cap line in the first branch.  No
annihilator representative or Hessian gauge is used.

The two displayed outcomes need not be mutually exclusive as properties
of arbitrary source data: a source could have a zero clique and curvature
elsewhere.  The assertion is the proof alternative obtained by inspecting
the transitions inside the chosen clique.

## 3. Exact zero-shore expansion

Assume (2), enumerate \(C=\{x_1,\ldots,x_h\}\), and orient every block from
the named site into \(D\).  In the site-square-zero algebra the aggregate
quadratic is exactly

\[
               A=q+\sum_{j=1}^{h}\sum_{c=0}^2
                       e_c^{(x_j)}p_c^{(j)}.                       \tag{7}
\]

There is no term using two sites of \(C\).  Hence every perfect matching
must send the \(h\) named sites injectively to \(h\) distinct sites of
\(D\).  If \(h>|D|=N-h\), no matching exists, contradicting (1).  This is
the capacity assertion \(h\le m\).

When \(h\le m\), extract colours \(c_1,\ldots,c_h\) at the named slots of
\(A^{[m]}\).  Each named-star summand in (7) is used once, and the remaining
\(N-2h\) sites of \(D\) are matched by \(q\).  Divided powers cancel the
multinomial coefficient, giving

\[
                   \left(\prod_{j=1}^{h}p_{c_j}^{(j)}\right)
                              q^{[m-h]}.                            \tag{8}
\]

The same contraction of the target in (1) is zero for a nonconstant colour
tuple and is \(X_c^D\) for the constant tuple \(c^h\).  This proves all
\(3^h\) equations in (3) coefficientwise.  It neither selects a matching
term from a cancelling sum nor assumes equal endpoint colours.

At a named site \(x_j\), all blocks to the other named sites vanish.
Therefore its star into \(D\) is its complete aggregate star.  The
mode-\(x_j\) flattening of (1) has image \(V_{x_j}\), so that complete star
map is injective.  This proves the final assertion attached to (3).

## 4. Uniform clique size

The
[target-flattening essential-star theorem](target-flattening-essential-star-pair-bound.md)
proves that the graph of pairs which are not doubly
aggregate-injective is \(4\)-degenerate.  It is therefore \(5\)-colourable.
A largest colour class is an independent set in the bad graph, hence a
clique in the good graph, of order at least

\[
                               \left\lceil {N\over5}\right\rceil.  \tag{9}
\]

For even \(N\ge16\), the right side is at least four and at most \(N/2\).
Choose exactly that many vertices from the good clique and apply Sections
2--3.  This proves (4) uniformly.

No new executable is needed.  The only inputs are the already audited
bad-graph degeneracy theorem and the coefficientwise canonical-transition
theorem; (7)--(8) are the standard zero-shore matching expansion.  This
note changes their composition, not either local calculation.
