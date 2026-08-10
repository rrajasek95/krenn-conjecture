# The minimal one-bad response circuit fails at the common-\(q\) Hessian

## Outcome

The formal minimum-response counterguard in `9b26452` cannot be promoted to
a genuine common-\(q\) packet.  If

\[
 F_{uv}=q^{[h-1]}_{U\setminus\{u,v\}},\qquad q^{[h]}=X_0,
                                                               \tag{1}
\]

then its pure-zero top Euler row is the contradiction `0=h`.

That first contradiction is not yet the sharp interface.  There is a
uniform augmentation with all of the following properties:

1. an actual unary quadratic \(q\) satisfies \(q^{[h]}=X_0\);
2. all four binary response tensors remain exact;
3. the same six-port response representation remains and
   \(p_1^{[2]},p_2^{[2]}\ne0\);
4. the complete coefficientwise top Euler identity holds.

The augmented family still is not a common-\(q\) family.  Its first
failure is one layer lower: the Euler recurrence for the first cofactors,
or equivalently the common symmetric Hessian identity.  Therefore neither
response minimality nor the top Euler equation can force the square-zero
cap.  A successful uniform modification must use the common second
cofactors.

The exact checker is
`computations/verify_uniform_one_bad_common_q_euler_hessian_gate.py`.

## 1. The immediate common-provenance contradiction

The `9b26452` family has nonzero first cofactors only at holes

\[
                         05,\quad15,\quad24,\quad34, \tag{2}
\]

and every displayed cofactor word has at least one colour `1` or `2`.
Consequently

\[
                         [F_{uv}]_{0^{2h-2}}=0
                         \qquad\text{for every }uv.    \tag{3}
\]

For actual first hafnian cofactors, coefficientwise Euler is

\[
 \sum_{u<v}q_{uv}(w_u,w_v)
 [F_{uv}]_{w|_{\widehat{uv}}}
 =h[q^{[h]}]_w.                                           \tag{4}
\]

At \(w=0^{2h}\), equations (1), (3), and (4) give

\[
                               0=h.                       \tag{5}
\]

Thus the exact formal family in `9b26452` is excluded uniformly for every
\(h\ge3\).  This uses genuine common provenance, not a bounded support
search.

## 2. Repairing the whole top Euler identity

Let the residual sites be `0,...,2h-1`, and take the unary quadratic
supported on the single perfect matching

```text
01 | 23 | 45 | 67 | 89 | ... .
```

Every edge has endpoint colours `00` and coefficient one.  Hence

\[
                              q^{[h]}=X_0.               \tag{6}
\]

Let \(F^0_{uv}\) be its genuine first cofactor family.  It is the pure-zero
complementary matching when `uv` is one of the displayed matching edges,
and zero otherwise.

Now adjoin to \(F^0\) the four formal response entries from `9b26452`:

\[
\begin{array}{c|c}
05&X_1|_{\widehat{05}}+Y|_{\widehat{05}}\\
15&-Y|_{\widehat{15}}\\
24&X_2|_{\widehat{24}}+Z|_{\widehat{24}}\\
34&-Z|_{\widehat{34}}.
\end{array}                                             \tag{7}
\]

None of the four holes in (7) is an edge of the unary matching.  Conversely,
none of the matching-edge holes is queried by the four response products

\[
\begin{aligned}
p_1&=e_1^{(0)}+e_1^{(1)},&s_1&=e_1^{(5)},\\
p_2&=e_2^{(2)}+e_2^{(3)},&s_2&=e_2^{(4)}.
\end{aligned}                                           \tag{8}
\]

Therefore the augmented family \(\tilde F\) retains

\[
 p_i s_j\tilde F=\delta_{ij}X_i
 \qquad(i,j\in\{1,2\}),                            \tag{9}
\]

and retains the nonzero self-squares of `p1,p2`.  At the same time, only
the genuine matching-edge cofactors contribute to (4), so

\[
 \sum_{u<v}q_{uv}\tilde F_{uv}=hX_0=hq^{[h]}          \tag{10}
\]

as a full tensor equality, not only at the pure-zero word.

Thus (6), (9), response minimality, non-square rows, and the complete top
Euler identity are mutually compatible at the formal cofactor level.  The
augmentation is deliberately not claimed to satisfy (1).

## 3. The first exact failure: cofactor Euler

For genuine common-\(q\) cofactors put

\[
 G_{uv,rs}=q^{[h-2]}_{U\setminus\{u,v,r,s\}}
 \qquad(\{u,v\}\cap\{r,s\}=\varnothing).           \tag{11}
\]

The family is symmetric in its two physical edges.  Euler on the
complement of `uv` gives the source identity

\[
 (h-1)F_{uv}
   =\sum_{\{r,s\}\cap\{u,v\}=\varnothing}
          q_{rs}G_{uv,rs}.                               \tag{12}
\]

For the unary matching \(q\), take any response hole in (2).  It removes
one endpoint from each of two distinct matching edges.  A nonzero second
cofactor in (12) can occur only when `rs` is the edge joining the two
stranded partners, but that edge has coefficient zero in \(q\).  If `rs`
is one of the supported matching edges, its second cofactor is zero.
Consequently the right side of (12) is zero.

The left side is \((h-1)\tilde F_{uv}\ne0\) at all four response
holes.  Hence the augmented guard fails (12) exactly at

```text
05, 15, 24, 34.
```

This is stronger localization than the original `0=h` guard: after all top
Euler rows are repaired, the first nonintegrable datum is the common
hafnian Hessian.

## 4. The next necessary source identity

Contract (12) with the two endpoint stars and use the four response rows.
Every genuine one-bad packet must satisfy

\[
 (h-1)\delta_{ij}X_i
 =\sum_{u\ne v}p_i(u)s_j(v)
   \sum_{rs\cap\{u,v\}=\varnothing}q_{rs}G_{uv,rs}
 \qquad(i,j\in\{1,2\}).                     \tag{13}
\]

Equation (13), with one symmetric common family \(G_{uv,rs}\), is the
next necessary identity.  The augmented guard violates it, whereas the
response equations and top Euler equation do not detect the violation.

A source-preserving concentration theorem must now do one of two things:

1. use (13) to produce a joint-kernel deletion which reduces a multisite
   endpoint row while preserving the unary top and all four responses; or
2. show that every nontrivial Hessian circuit in (13) exports an active
   clean cap or another exact descent.

No such uniform Hessian-to-modification theorem is currently proved.  In
particular, this note does not force the four square-zero rows and does not
close the projection-degenerate branch.  It shows exactly why a proof using
only the top Euler identity cannot do so.

## Exact scope

The original `9b26452` circuit is uniformly contradictory under genuine
common-\(q\) provenance.  The augmented family is the sharp next formal
counterguard: it has a genuine unary-top \(q\) and satisfies the whole top
Euler identity, but its response cofactors are not derivatives of that
\(q\).  It is not an ordinary one-bad source, not a Krenn counterexample,
and not evidence that such a source exists.

The surviving proof obligation is all-order and source-level: integrate
the symmetric second-cofactor identity (13) into an exact modification or
contradiction.  No `N=8` face enumeration is involved.

## Reproduction

```bash
.venv/bin/python computations/verify_uniform_one_bad_common_q_euler_hessian_gate.py
.venv/bin/python -O computations/verify_uniform_one_bad_common_q_euler_hessian_gate.py
python3.14 computations/verify_uniform_one_bad_common_q_euler_hessian_gate.py
```
