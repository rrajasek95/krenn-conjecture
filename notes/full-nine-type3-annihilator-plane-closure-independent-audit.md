# Independent audit: full-nine type-3 annihilator-plane closure

## 1. Verdict

**PASS, with a valid all-order strengthening.**  I independently
reconstructed the argument in
[the primary note](full-nine-type3-annihilator-plane-closure.md) from the
six-site pair equations and found no row/column transpose, fixed-colour
normalization, exceptional-site contraction, square-zero factorization,
case-split, tensor-lemma, rank-zero, or injectivity gap.

Moreover, the proof of Theorem 1.1 is not intrinsically cubic.  With the
matching powers changed from \(q^{[3]},q^{[2]}\) to
\(q^{[h]},q^{[h-1]}\), it proves the same rank-at-least-two conclusion on
every even residual set of size \(2h\), for every \(h\ge1\).  Section 11
states and audits this stronger theorem.  Six sites are first genuinely
needed only in the downstream selector routing as the smallest case
\(h\ge3\) in which a response top power rules out a star supported on two
sites.

The conclusion is exactly as scoped.  For one endpoint, the complete nine
equations and injectivity of that endpoint alone imply that its restriction
away from any site has rank at least two.  Injectivity of the opposite
endpoint, a cap covector, invertibility of that covector, and
\(r(K)^{[3]}\ne0\) are not used in this theorem.  The nonnilpotence condition
is used only afterward to eliminate the distinct two-site-support alternative
and hence, with Hall--Rado, force a selector.

No mathematical correction is required.  In particular, the unary
contracted-row guard in
[the earlier sparse-shore note](rootless-sparse-star-propagation-and-rank-one-shore-guard.md)
does not contradict this result: that guard fails individual pair rows, while
the present proof uses literal columns of all nine equations.

The audited primary file had SHA-256 digest

```text
3c230b56c580aeb39007b3edc19234a666da1ec80f1607413c7720b8a6289065  notes/full-nine-type3-annihilator-plane-closure.md
```

## 2. Reconstruction of the exact pair system

On six residual sites, sort a perfect matching after deleting two named
physical endpoints according to its use of those endpoints.  It either uses
their direct edge, followed by a three-edge matching internal to the six
sites, or uses one endpoint-star edge from each named endpoint, followed by a
two-edge internal matching.  With divided powers, each matching is counted
once, giving exactly

\[
 a_{ij}Q+p_i s_jF=\delta_{ij}X_i,
 \qquad Q=q^{[3]},\quad F=q^{[2]}.                     \tag{A1}
\]

There is no factor of two in the second term.  Although the residual algebra
is commutative, the two star factors retain their named endpoint roles:
choosing the first star at residual site \(u\) and the second at \(v\) is the
term \(p_{i,u}s_{j,v}\), while the reverse assignment is the separate term
\(p_{i,v}s_{j,u}\).  Same-site assignments vanish.  This agrees with the
independent derivation of the full-nine equations in
[the curved-line audit](curved-no-root-macaulay-and-scalar-zero-packet-independent-audit.md).

The row convention in (A1) is also fixed: \(i\) labels \(p_i\) and the first
physical colour, while \(j\) labels \(s_j\) and the second physical colour.
Consequently, if \(c=\sum_i c_i f_i\), summing the equations in a fixed
column \(j\) gives

\[
 (c^{\mathsf T}a)_jQ+P(c)s_jF=c_jX_j.                 \tag{A2}
\]

Thus the \(c^{\mathsf T}a\), rather than \(ac\), in the primary equation
(14) is correct.

## 3. Exceptional-site factorization and contraction

Fix \(x\) and first suppose

\[
                         \operatorname{rank}P_{\bar x}=1.
\]

Then \(U=\ker P_{\bar x}\) is two-dimensional.  If \(c\in U\) and
\(P_x(c)=0\), both the \(x\)-component and the off-\(x\) component of \(P(c)\)
vanish.  Injectivity of \(P\) therefore makes

\[
                   P_x|_U:U\longrightarrow V_x               \tag{A3}
\]

injective.  Its image \(M\) is a physical two-plane.  The fact (A3) is the
sole consequence of endpoint injectivity used throughout the rank-one proof;
it is invoked both in the one-active-index case and in the final rectangle
contradiction.

Choose \(0\ne\lambda\in V_x^*\) with kernel \(M\).  Since degree six is top
degree in a six-site square-zero algebra,

\[
 ({\cal R}_W)_6=V_x\otimes\bigotimes_{y\ne x}V_y.
\]

Thus \(Q=q^{[3]}\) has a literal \(x\)-slot, and
\(T=(\lambda\otimes1)Q\) is well-defined.  No physical basis has been changed
in choosing \(\lambda\); it is generally an oblique covector at this point.

For \(c\in U\), \(P(c)=P_x(c)\) is supported only at \(x\).  Write

\[
 q_0=q|_{W\setminus\{x\}},\qquad
 h_j=(s_j|_{W\setminus\{x\}})q_0^{[2]}.
\]

Every summand of \(s_jq^{[2]}\) which uses site \(x\) is killed on
multiplication by \(P_x(c)\), because \(V_xV_x=0\).  The surviving summands
are precisely the restriction of \(s_jq^{[2]}\) to the other five sites.
Restriction is an algebra homomorphism and commutes with divided powers, so

\[
 P(c)s_jq^{[2]}=P_x(c)\otimes h_j.                    \tag{A4}
\]

This equality neither assumes that \(q\) is monomial nor selects individual
nonzero matching terms; arbitrary complex cancellation is retained in
\(h_j\).

Now use \(X_j=e_j^{(x)}\otimes X_j'\) in (A2), apply (A4), and contract the
\(x\)-slot by \(\lambda\).  Since \(P_x(c)\in\ker\lambda\), the result is

\[
 \boxed{(c^{\mathsf T}a)_jT
       =\epsilon_j(c)\lambda(e_j^{(x)})X_j'.}          \tag{A5}
\]

The two same-looking labels in the right side have different origins:
\(\epsilon_j\) is a fixed row-coordinate covector on \(C\), whereas
\(\lambda(e_j^{(x)})\) evaluates an independently derived physical covector
on a fixed colour axis.  Equation (A5) follows from the diagonal target; it
does not identify the row and physical spaces.

## 4. Exhaustion of the nonzero-slice case

Assume \(T\ne0\), and put

\[
 J=\{j:\lambda(e_j^{(x)})\epsilon_j|_U\ne0\}.
\]

For each \(j\in J\), equation (A5) makes the same nonzero \(T\) proportional
to \(X_j'\).  The three \(X_j'\) are distinct coordinate tensors and are
linearly independent, so \(|J|\le1\).  For \(j\notin J\), (A5) and \(T\ne0\)
give

\[
                     (c^{\mathsf T}a)_j=0\quad(c\in U). \tag{A6}
\]

This leaves exactly two cases.

### 4.1 \(J=\varnothing\)

Substituting (A6) into the uncontracted equation (A2) gives

\[
                    P_x(c)\otimes h_j=\epsilon_j(c)X_j
                    \quad(c\in U).                    \tag{A7}
\]

A two-plane in \(\mathbb C^3\) contains a vector with at least two nonzero
fixed coordinates.  For such a \(c\), two instances of (A7) have nonzero
right sides.  Uniqueness of the first factor of a nonzero pure tensor forces
the same nonzero \(P_x(c)\) to be proportional to two distinct physical
axes.  This is impossible.

### 4.2 \(J=\{k\}\)

Here \(\epsilon_k|_U\ne0\), so \(U\cap\ker\epsilon_k\) is a line.  A nonzero
vector on it cannot have both coordinates outside \(k\) nonzero, since the
two inactive columns would reproduce the preceding contradiction.  It is
therefore a nonzero multiple of one fixed basis vector \(f_d\), with \(d\ne k\).
After rescaling, (A7) in inactive column \(d\) gives

\[
                    P_x(f_d)\otimes h_d=X_d.           \tag{A8}
\]

Hence \(h_d\ne0\) and \(P_x(f_d)\parallel e_d^{(x)}\).  If \(c'\in U\) is
independent of \(f_d\), the same column gives

\[
             P_x(c')\otimes h_d=\epsilon_d(c')X_d.     \tag{A9}
\]

The left side is nonzero by (A3) and (A8).  Therefore
\(P_x(c')\parallel e_d^{(x)}\) as well, making the images of two independent
vectors dependent and contradicting (A3).

The \(J=\varnothing\) and \(|J|=1\) cases exhaust \(|J|\le1\).  Thus every
hypothetical rank-one solution must have \(T=0\).

## 5. The zero slice forces a fixed coordinate rectangle

With \(T=0\), (A5) says

\[
                  \epsilon_j(c)\lambda(e_j^{(x)})=0
                  \quad(c\in U).                      \tag{A10}
\]

Because \(\lambda\ne0\), choose \(d\) for which
\(\lambda(e_d^{(x)})\ne0\).  Then \(U\subseteq\ker\epsilon_d\), and equality
holds because both are planes.  A second nonzero coordinate of \(\lambda\)
would put the plane \(U\) inside the one-dimensional intersection of two
coordinate hyperplanes.  Hence, for the complementary indices \(u,v\),

\[
 \begin{aligned}
 U&=\operatorname{span}\{f_u,f_v\},
 &\lambda&\parallel(e_d^{(x)})^*,\\
 M&=P_x(U)=\ker\lambda,
 &M&=\operatorname{span}\{e_u^{(x)},e_v^{(x)}\}.       \tag{A11}
 \end{aligned}
\]

This coordinate flag is a consequence of the equations in the original
labels.  It is not produced by a permissible or impermissible basis change.
In particular, the literal rows \(p_u,p_v\) are supported at \(x\), their
local values \(\widehat p_u,\widehat p_v\) form a basis of \(M\), and the
literal physical axes \(e_u^{(x)},e_v^{(x)}\) form another basis of \(M\).

The kernel of

\[
 \lambda\otimes1:V_x\otimes Z\longrightarrow Z
\]

is exactly \(M\otimes Z\).  Thus \(T=0\) implies \(Q\in M\otimes Z\), not
merely that one coefficient of \(Q\) vanishes.  Restricting (A1) to the
literal rows and columns \(u,v\) yields the four equations

\[
 a_{ij}Q+\widehat p_i\otimes h_j
   =\delta_{ij}e_i^{(x)}\otimes X_i'
 \qquad(i,j\in\{u,v\}).                               \tag{A12}
\]

All spaces and bases needed by the two-row rectangle lemma are therefore
present without normalization.

## 6. Independent audit of the two-row rectangle lemma

Let \(p_u,p_v\) be a basis of a two-space \(L\), let \(e_u,e_v\) be another
basis, and let \(Y_u,Y_v\) be independent.  Consider

\[
 \beta_{ij}Q+p_i\otimes h_j
   =\delta_{ij}e_i\otimes Y_i.                         \tag{A13}
\]

The proof's cases are exhaustive and each is valid.

1. If \(Q=0\), the off-diagonal cells force \(h_u=h_v=0\), and the diagonal
   targets fail.
2. If \(Q\ne0\) and both off-diagonal scalars are nonzero, the two
   off-diagonal cells put \(Q\) in both \(p_u\otimes Z\) and
   \(p_v\otimes Z\).  Their intersection is zero because \(p_u,p_v\) are
   independent.
3. If exactly one is nonzero, say \(\beta_{uv}\ne0\), then
   \(Q=p_u\otimes R\), \(h_v=-\beta_{uv}R\), and \(h_u=0\), with \(R\ne0\).
   The \(uu\) cell forces \(R\parallel Y_u\), while the \(vv\) cell forces
   \(R\parallel Y_v\), contradicting independence.
4. If both off-diagonal scalars vanish, the off-diagonal cells again give
   \(h_u=h_v=0\).  The two diagonal cells make the same nonzero \(Q\)
   proportional to tensors whose \(Z\)-factors are the independent vectors
   \(Y_u,Y_v\).

As an exact counterexample search, I took \(Z=\operatorname{span}\{Y_u,Y_v\}\),
normalized \(p_u,p_v\) and \(Y_u,Y_v\) to coordinate bases, and computed the
polynomial ideal of all sixteen scalar coordinates of (A13).  For the three
rational choices

\[
 [e_u\ e_v]=
 I_2,\qquad
 \begin{pmatrix}1&1\\1&2\end{pmatrix},\qquad
 \begin{pmatrix}2&-1\\3&1\end{pmatrix},
\]

the exact Groebner basis is \({1}\) in every case.  This finite check is
only a sanity check; the four-case argument above proves inconsistency for
every pair of bases over \(\mathbb C\).  Applying it to (A12), with
\(Y_i=X_i'\), excludes \(T=0\) and completes the rank-one contradiction.

## 7. Rank-zero shore

If \(P_{\bar x}=0\), injectivity of \(P\) makes the three local vectors
\(p_0,p_1,p_2\in V_x\) a basis.  The same square-zero restriction used in
(A4) now gives all nine equations as

\[
 a_{ij}Q+p_i\otimes h_j
   =\delta_{ij}e_i^{(x)}\otimes X_i'.                  \tag{A14}
\]

Fix a column \(j\), and call the other two row indices \(i,k\).  Its two
off-diagonal equations exhaust the following possibilities.

* If \(a_{ij}\) and \(a_{kj}\) are both nonzero, they put \(Q\) in the zero
  intersection \((p_i\otimes Z)\cap(p_k\otimes Z)\).  Thus \(Q=0\), then
  \(h_j=0\), and the diagonal cell fails.
* If exactly one is nonzero, the zero-scalar cell first gives \(h_j=0\), the
  nonzero-scalar cell then gives \(Q=0\), and the diagonal again fails.
* Hence both are zero.  The two off-diagonal cells give \(h_j=0\), and the
  diagonal cell becomes

  \[
                   a_{jj}Q=e_j^{(x)}\otimes X_j'.      \tag{A15}
  \]

This holds for each column.  Every right side is nonzero, so every relevant
\(a_{jj}\) and \(Q\) is nonzero.  It would make one \(Q\) proportional to all
three independent coordinate tensors \(X_0,X_1,X_2\), a contradiction.
Thus rank zero is excluded without assuming \(Q\ne0\) in advance.

## 8. Endpoint transpose and selector routing

Interchanging endpoints requires transposing only the pair-index rectangle:

\[
 \widetilde a_{ji}=a_{ij},\qquad
 \widetilde p_j=s_j,\qquad
 \widetilde s_i=p_i.                                  \tag{A16}
\]

Commutativity gives \(s_jp_i=p_is_j\), and
\(\delta_{ji}X_i=\delta_{ji}X_j\).  Therefore the transposed system has the
same form with the first index \(j\) and target \(X_j\).  No physical colour
axis is transposed or changed.  The theorem for \(S\) consequently needs
injectivity of \(S\), but not injectivity of \(P\).

For an injective star, the rank form of Hall--Rado says that failure of a
three-site selector yields one of two alternatives: support on at most two
sites, or rank at most one away from one exceptional site.  The theorem just
proved eliminates the second alternative from (A1).  If

\[
                   r(K)=\sum_{i,j}K_{ij}p_i s_j,
                   \qquad r(K)^{[3]}\ne0,              \tag{A17}
\]

then support of the \(P\)-star on at most two sites kills \(r(K)^{[3]}\)
term by term: three surviving response edges would require three distinct
chosen \(P\)-endpoint sites.  The same holds for the \(S\)-star.  Therefore,
when both stars are injective, (A1) and (A17) force a selector at each
endpoint exactly as claimed.

This use of nonnilpotence is cancellation-safe and does not require \(K\) to
be invertible.  Invertibility of the canonical \(K_*\) is an upstream fact,
not a hypothesis of either sparse-shore exclusion.

## 9. Rootless scalar-zero specialization and hypothesis ledger

For an off-diagonal entry \(\alpha=a_{ab}\ne0\), \(a\ne b\), and
\(\tau=\operatorname{tr}a\), set

\[
                         K_*=\tau E_{ab}-\alpha I.
\]

Because \(E_{ab}\) is off diagonal,

\[
 \sum_{ij}(K_*)_{ij}a_{ij}=\tau a_{ab}-\alpha\operatorname{tr}a=0,
 \qquad \operatorname{diag}K_*=(-\alpha,-\alpha,-\alpha),
\]

and \(\det K_*=(-\alpha)^3\ne0\).  Contracting (A1) therefore gives

\[
 r_*q^{[2]}=-\alpha(X_0+X_1+X_2).                     \tag{A18}
\]

In the rootless branch, gcd one supplies \(r_*^{[3]}\ne0\).  This is exactly
the additional input needed for the two-site-support exclusion, not for the
rank-zero or rank-one proof.

The hypotheses are used as follows.

| Conclusion | Hypotheses actually used |
|---|---|
| \(\operatorname{rank}P_{\bar x}\ne1\) | all nine equations and injectivity of \(P\) |
| \(P_{\bar x}\ne0\) | all nine equations and injectivity of \(P\) |
| Corresponding two statements for \(S\) | all nine equations and injectivity of \(S\), after (A16) |
| No two-site-supported \(P\)-star | \(r(K)^{[3]}\ne0\); neither star injectivity nor \(K\)-invertibility |
| No two-site-supported \(S\)-star | \(r(K)^{[3]}\ne0\); neither star injectivity nor \(K\)-invertibility |
| Selector for each endpoint | all nine equations, injectivity of that endpoint, and \(r(K)^{[3]}\ne0\) |
| Canonical rootless packet | additionally \(a_{ab}\ne0\), \(a\ne b\), and the upstream gcd-one condition |

No part of Theorem 1.1 assumes \(q^{[3]}\ne0\), any nonzero \(h_j\), an
invertible or nonzero direct matrix \(a\), injectivity of the opposite star,
or a row/physical basis normalization.  The proof explicitly handles
\(Q=0\) wherever it could arise.

## 10. Counterexample search and scope conclusion

A counterexample over \(\mathbb C\) with rank-one off-\(x\) restriction would
have to lie in exactly one of \(T\ne0\) or \(T=0\).  In the former case,
(A5) leaves only \(J=\varnothing\) or one active index, and Sections 4.1--4.2
exclude both.  In the latter case, (A10) forces the literal coordinate
rectangle (A12), whose complete algebraic solution set is empty by the
two-row lemma.  A rank-zero counterexample is exhausted column by column in
Section 7.  Thus there is no unexamined algebraic stratum in which to place a
complex counterexample.

The earlier rational unary guard confirms the sharp boundary of the result:
one contracted response can satisfy nonnilpotence with an injective type-3
star, but its \((0,0)\) and \((1,2)\) physical rows fail separately.  The full
nine-row theorem therefore closes precisely the advertised exceptional-shore
alternative and no weaker contracted-row statement.

## 11. Uniform even-residual strengthening

The preceding proof gives the following stronger theorem, which is not stated
in the primary note.

**Theorem A (uniform full-nine exceptional-shore closure).**  Let
\(h\ge1\), let \(|W|=2h\), and work in

\[
 {\cal R}_W=\bigotimes_{y\in W}(\mathbb C\oplus V_y),
 \qquad V_yV_y=0,\qquad \dim V_y=3,
\]

with fixed physical bases \(e_0^{(y)},e_1^{(y)},e_2^{(y)}\).  Suppose
\(q\in({\cal R}_W)_2\), \(p_i,s_j\in({\cal R}_W)_1\), and
\(a\in\operatorname{Mat}_{3\times3}(\mathbb C)\) satisfy

\[
 a_{ij}q^{[h]}+p_i s_jq^{[h-1]}
   =\delta_{ij}X_i,\qquad
 X_i=\bigotimes_{y\in W}e_i^{(y)}
 \quad(0\le i,j\le2).                                 \tag{A19}
\]

If \(P(f_i)=p_i\) is injective, then

\[
                       \operatorname{rank}P_{\bar x}\ge2
                       \qquad(x\in W).                 \tag{A20}
\]

The corresponding assertion holds for \(S(g_j)=s_j\) whenever \(S\) is
injective.

### 11.1 Top degree and the exceptional-site factorization

Fix \(x\).  Top degree is now \(2h\), so

\[
 q^{[h]}\in
 V_x\otimes Z_x,\qquad
 Z_x=\bigotimes_{y\ne x}V_y.                          \tag{A21}
\]

If \(\operatorname{rank}P_{\bar x}=1\), define \(U,M,\lambda\) exactly as
before and put

\[
 Q=q^{[h]},\qquad T=(\lambda\otimes1)Q,\qquad
 q_0=q|_{W\setminus\{x\}},\qquad
 h_j=(s_j|_{W\setminus\{x\}})q_0^{[h-1]}.             \tag{A22}
\]

The degree of \(h_j\) is

\[
                  1+2(h-1)=2h-1,
\]

which is top degree on the \(2h-1\) sites away from \(x\); hence
\(h_j\in Z_x\).  Every term of \(s_jq^{[h-1]}\) which contains an \(x\)-slot
collides with \(P_x(c)\).  Restriction to the off-\(x\) algebra gives exactly

\[
 P(c)s_jq^{[h-1]}=P_x(c)\otimes h_j.                  \tag{A23}
\]

This remains valid at the smallest edge case \(h=1\): by convention
\(q_0^{[0]}=1\), so \(h_j=s_j|_{W\setminus\{x\}}\).

### 11.2 The contraction and both \(T\)-cases are unchanged

Taking the \(c_i\)-weighted sum of column \(j\) of (A19) and contracting at
\(x\) gives the same identity

\[
 (c^{\mathsf T}a)_jT
   =\epsilon_j(c)\lambda(e_j^{(x)})X_j',
 \qquad
 X_j'=\bigotimes_{y\ne x}e_j^{(y)}.                  \tag{A24}
\]

For every \(h\ge1\), the three tensors \(X_0',X_1',X_2'\) are nonzero and
linearly independent.  Therefore the definition of \(J\), the conclusion
\(|J|\le1\), and the no-active/one-active contradictions in Section 4 are
word for word unchanged.  They use only the two-dimensional row kernel,
the fixed three row coordinates, and injectivity of \(P_x|_U\), not the
number of residual sites.

When \(T=0\), (A24) forces exactly the same fixed coordinate flag (A11).
The kernel identity

\[
 \ker(\lambda\otimes1)=(\ker\lambda)\otimes Z_x
\]

holds for every \(Z_x\).  The literal \(u,v\) rectangle is again (A13), with
\(Y_u=X_u'\) and \(Y_v=X_v'\).  Lemma 4.1 uses only their independence and
therefore excludes the rank-one shore at every \(h\).

### 11.3 Rank zero and endpoint transposition are unchanged

If \(P_{\bar x}=0\), injectivity again makes \(p_0,p_1,p_2\) a basis of
\(V_x\), independently of \(h\).  Equation (A19) factors as

\[
 a_{ij}Q+p_i\otimes h_j
   =\delta_{ij}e_i^{(x)}\otimes X_i'.                 \tag{A25}
\]

The columnwise three-case argument of Section 7 uses only independence of
the \(p_i\) and of the three targets.  It excludes rank zero without any
site-count input.  Finally, transposition (A16) remains exact for (A19), so
the assertion for \(S\) is uniform as well.  This proves Theorem A.

### 11.4 What actually is six-site-specific

No step proving (A20) needs \(h=3\).  The phrases “degree six,” “five sites
away from \(x\),” \(q^{[3]}\), and \(q_0^{[2]}\) in the primary proof merely
specialize (A21)--(A23).

The later response/selector conclusion has a separate threshold.  If

\[
 r(K)=\sum_{i,j}K_{ij}p_i s_j,\qquad r(K)^{[h]}\ne0,  \tag{A26}
\]

and the \(P\)-star is supported on at most two sites, every monomial of
\(r(K)^{[h]}\) needs \(h\) distinct chosen \(P\)-endpoint sites.  Thus (A26)
rules out two-site support exactly when \(h\ge3\).  Hall--Rado together with
Theorem A consequently forces three-site selectors uniformly for all
\(2h\ge6\), provided the relevant endpoint stars are injective.

For \(h=2\), two response edges can use the two support sites, so
\(r(K)^{[2]}\ne0\) does not eliminate the two-site alternative.  For
\(h=1\), three distinct selector sites do not exist.  These small-order
limitations affect only the selector corollary, not Theorem A.

The \(h=2\) threshold failure is literal, even with injective stars satisfying
the rank conclusion (A20).  On sites \(1,2,3,4\), take independent local
vectors and set

\[
 \begin{aligned}
 p_0&=u_1+u_2,&p_1&=u_1',&p_2&=u_2',\\
 s_0&=v_3+v_4,&s_1&=v_3',&s_2&=v_4',
 \end{aligned}
\]

where subscripts denote sites and each primed vector is independent of the
unprimed vector at that site.  Both triples are injective, supported on two
sites, and have rank two after either support site is removed.  With
\(K=E_{00}\),

\[
 r(K)=(u_1+u_2)(v_3+v_4),\qquad
 r(K)^{[2]}=2u_1u_2v_3v_4\ne0.
\]

This is only a guard for the response-power inference, not a claimed
solution of the \(h=2\) full-nine equations.

On a uniform off-diagonal rootless curvature line with \(h\ge3\), the
scalar-zero packet is correspondingly

\[
 r_*q^{[h-1]}=-\alpha\sum_{i=0}^2X_i,\qquad
 r_*^{[h]}\ne0.
\]

Hence the primary note's six-site closure is the first member of a uniform
full-nine rank closure and selector routing, while its displayed cubic
matching powers are not essential to the annihilator-plane theorem itself.
