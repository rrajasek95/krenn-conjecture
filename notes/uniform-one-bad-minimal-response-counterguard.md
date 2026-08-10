# Minimum response support does not force square-zero stars without top provenance

## Exact verdict

There is a uniform formal counterguard to the proposed first-variation proof.
For every `h>=3`, the complete four binary response tensors can hold at a
globally minimum-total-site-support representation while two endpoint rows
have nonzero self-square.  The guard fails one precise source-faithful datum:
its common cofactor tensors are not the derivatives of a quadratic satisfying
the unary top `q^[h]=X0`.

Thus the full top-provenant concentration theorem remains open, but it cannot
be proved from response joint kernels and entry minimality alone.

## Uniform formal packet

Let the residual sites be `0,...,2h-1`.  Define global words

```text
X1 = 11...1,              X2 = 22...2,
Y  = X1 with site 2 changed to 0,
Z  = X2 with site 0 changed to 0.
```

Write `F_uv` for a formal degree-`2h-2` cofactor tensor on the complement of
`u,v`.  Its only nonzero entries are

\[
\begin{array}{c|c}
05 & X_1|_{\widehat{05}}+Y|_{\widehat{05}}\\
15 & -Y|_{\widehat{15}}\\
24 & X_2|_{\widehat{24}}+Z|_{\widehat{24}}\\
34 & -Z|_{\widehat{34}}.
\end{array}                                             \tag{1}
\]

Choose

\[
\begin{aligned}
p_1&=e_1^{(0)}+e_1^{(1)},&s_1&=e_1^{(5)},\\
p_2&=e_2^{(2)}+e_2^{(3)},&s_2&=e_2^{(4)}.
\end{aligned}                                           \tag{2}
\]

Literal hole-labelled contraction gives

\[
                         p_i s_jF=\delta_{ij}X_i
                         \quad(i,j\in\{1,2\}).          \tag{3}
\]

The cross rows are zero because the relevant holes `04,14,25,35` carry no
cofactor.  No output-only identification is used: (1) retains every hole
label and every residual word.

## Why the displayed representation is minimum

In the colour-one channel, `X1` occurs only in `F_05`, tied with `+Y` at the
same coefficient.  The only available cancellation is `-Y` in `F_15`.
Therefore any representation of that pure response must realize both
physical hole pairs `05` and `15`.  Their union has three sites, so

\[
                    |\operatorname{supp}p_1|
                    +|\operatorname{supp}s_1|\ge3.     \tag{4}
\]

The same argument with `X2+Z` and `-Z` on `24,34` gives the corresponding
lower bound three for `p2,s2`.  Hence every four-row representation has total
star-site support at least six, and (2) attains six.

In particular

\[
                         p_1^{[2]}\ne0,qquad p_2^{[2]}\ne0. \tag{5}
\]

Holding `s1,s2` fixed makes the first-variation obstruction explicit.  The
two occupied `p1` columns of the joint response map are `X1+Y` and `-Y`; the
two occupied `p2` columns are `X2+Z` and `-Z`.  Each pair is linearly
independent.  No joint-kernel direction deletes either occupied site while
preserving the two response outputs.

This is a block-matroid circuit, not an artifact of a nonminimal choice.

## The one missing row

For an actual internal quadratic `q`, the cofactors are not independent:

\[
 F_{uv}=q^{[h-1]}_{U\setminus\{u,v\}}.                 \tag{6}
\]

Euler's matching identity at a global word `w` is

\[
 \sum_{u<v}q_{uv}(w_u,w_v)
       F_{uv}(w|_{U\setminus\{u,v\}})
 =h\,[q^{[h]}]_w.                                     \tag{7}
\]

At the pure-zero word, every coefficient of the formal family (1) on the
left is zero.  The unary top requires the right side to be `h`.  Thus (7) is
the literal contradiction

\[
                              0=h.                     \tag{8}
\]

This sharply identifies the extra input: a valid concentration proof must
couple its joint-kernel first variation to the common-hafnian derivative
identity (6)--(7).  Merely adjoining the scalar assertion `q^[h]=X0` to an
abstract response map is not enough; its provenance through the same `q`
and the same hole cofactors is load-bearing.

The guard is therefore not an ordinary source packet, not a Krenn
counterexample, and not a refutation of the full statement in the task.  It
refutes the response-only/minimality implication and leaves exactly the
top-provenant first-variation lemma as the remaining all-order target.

This scope is only the projection-degenerate one-bad branch.  It is not a
generic landing for the rootless full-nine packet.  The committed type-3
annihilator-plane closure shows that rootless nonnilpotence excludes the
corresponding endpoint-star support-at-most-two alternative.  Therefore a
theorem forcing (5) here would close this degenerate branch by descent; it
must not be advertised as an exhaustive `SP-CLEAN-BRIDGE` normal form.

## Relation to the clean-cap interface

Commit `ca6362b` proves that four square-zero rows complete
`SP-CLEAN-BRIDGE` uniformly by an explicit active cap and `N->N-2` descent.
The present counterguard says where an extraction proof must spend the unary
top: use (7), or an equivalent source syzygy, to rule out every minimum block
circuit before invoking that descent.  Further `N=8` support layers do not
address this interface.

## Reproduction

```sh
python3 computations/verify_uniform_one_bad_minimal_response_counterguard.py
python3 -O computations/verify_uniform_one_bad_minimal_response_counterguard.py
python3 -I -S computations/verify_uniform_one_bad_minimal_response_counterguard.py
```

The checker reconstructs all four formal response tensors at representative
orders `h=3,...,8`, verifies the joint-kernel columns and minimum support, and
audits the pure-zero Euler failure.  The displayed formulas prove the same
claims for every `h>=3`.
