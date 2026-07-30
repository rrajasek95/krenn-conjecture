# Minimality forces a nonzero odd monochromatic residue

## 1. Outcome

Let \(W\) have \(2h\) sites, \(h\geq3\), choose \(x\in W\), and put
\(D=W\setminus\{x\}\). In the site-square-zero algebra on \(D\), let

\[
 q_0\in {\cal R}_2(D),\qquad
 A=q_0^{[h-1]},\qquad
 C_{q_0}={{\cal R}_{2h-1}(D)\over {\cal R}_1(D)A}.
 \tag{1}
\]

For the three fixed physical colours, write

\[
 Y_c=\bigotimes_{y\in D}e_c^{(y)},\qquad
 \overline Y_c=[Y_c]\in C_{q_0}.
 \tag{2}
\]

The following elementary alternative is uniform in \(h\).

> **Odd-residue survival lemma.** If
> \(\overline Y_0=\overline Y_1=\overline Y_2=0\), then there is a
> quadratic \(\widetilde q\in{\cal R}_2(W)\) with
> \[
>                         \widetilde q^{[h]}
>                           =\sum_{c=0}^2X_c^W.              \tag{3}
> \]

Consequently, use the standard minimal-counterexample setup: choose \(B\)
of minimum even cardinality among exact ternary sources in the forbidden
range \(|B|\geq6\). The proved order-six theorem makes \(|B|\geq8\). If a
selected cap has \(W=B\setminus\{p,q\}\), then at least one of the three
classes in (2) is nonzero. Otherwise (3) is an exact ternary source on
\(|W|=|B|-2\geq6\), contradicting this choice of \(B\). This wording is
essential: exact ternary sources do exist at order four.

For the off-diagonal scalar-zero endpoint of
[the base-locus--ternary routing theorem](offdiagonal-base-locus-ternary-omega-residue.md),

\[
       \operatorname {res}_{q_0}(r;t_c)=-\alpha\overline Y_c,
       \qquad \alpha\ne0.                                  \tag{4}
\]

The coefficient \(-\alpha\) is nonzero for every one of the three labels.
Hence minimum-order survival supplies a colour \(c\) for which both the
routed class \(-\overline Y_c\) and the unnormalized residue in (4) are
nonzero. On that off-diagonal all-inactive branch, nonzero-label survival
is therefore not an additional overlap hypothesis. The remaining issue is
the source-filtered correction of the unique torus--Koszul middle
coefficient. This lemma does not construct that correction, treat the
unequal diagonal endpoint coefficients, produce an active clean point, or
resolve the conjecture.

## 2. Proof of the survival lemma

The vanishing of the three quotient classes means that there are linear
forms \(z_c\in{\cal R}_1(D)\) satisfying

\[
                              z_cA=Y_c
                     \qquad(c=0,1,2).                       \tag{5}
\]

Put

\[
 \rho=\sum_{c=0}^2e_c^{(x)}z_c,
 \qquad \widetilde q=q_0+\rho.                              \tag{6}
\]

Every monomial of \(\rho\) uses the site \(x\), so
\(\rho^{[j]}=0\) for \(j\geq2\). Moreover \(q_0^{[h]}=0\), because a
degree-\(2h\) monomial cannot be supported on the \(2h-1\) sites of \(D\).
The divided-power binomial identity therefore gives, without a numerical
binomial coefficient,

\[
 \begin{aligned}
       \widetilde q^{[h]}
          &=q_0^{[h]}+\rho q_0^{[h-1]}\\
          &=\sum_{c=0}^2e_c^{(x)}z_cA\\
          &=\sum_{c=0}^2e_c^{(x)}Y_c
            =\sum_{c=0}^2X_c^W.
 \end{aligned}                                               \tag{7}
\]

Only multiplication by the already defined tensor \(A\) occurs. No
matching power, site form, or scalar is cancelled.

## 3. Why (3) is a legitimate smaller decorated source

Write every site-pair block of \(\widetilde q\) in the fixed
endpoint-colour bases. For each nonzero block coefficient, introduce one
degree-two source on its two sites, with that ordered endpoint-colour pair
and that complex weight. There are at most

\[
                            9\binom{2h}{2}                 \tag{8}
\]

such sources. Expanding \(\widetilde q^{[h]}\) selects each perfect
matching once: the \(h!\) edge orders in \(\widetilde q^h\) are exactly
cancelled by the divided-power normalization. Thus the aggregate matching
tensor of these sources is exactly (3). Endpoint asymmetry, parallel-source
cancellation already absorbed into a block coefficient, and arbitrary
complex weights are all retained.

Conversely, the coefficient of each \(X_c^W\) in (3) is one. Its
perfect-matching expansion therefore contains at least one nonzero
summand, and every block coefficient in that summand has endpoint colours
\((c,c)\). Hence each of the three colours occurs on a nonzero source.
No other colours were introduced, so the palette is exactly the selected
ternary palette.

This is a source on the even site set \(W\), not merely a formal tensor
identity. Since \(|W|=|B|-2\geq6\) in the setup of Section 1, it contradicts
minimality inside the forbidden range. The allowed order-four ternary
construction is never reached by this one-step contradiction.

## 4. Exact scope on the inactive off-diagonal branch

The conclusion uses minimum-order reduction only after the selected line
has been produced. It does not assert that every odd quotient contains a
nonzero monochromatic class in isolation: all three can vanish only if the
lifts (5) assemble the smaller source (3). Nor does it say which colour
survives.

The latter ambiguity is harmless for an off-diagonal scalar-zero endpoint,
because its diagonal target vector is
\((-\alpha,-\alpha,-\alpha)\). It is not harmless for a diagonal endpoint
whose target can have a zero coordinate. This is the structural advantage
of the off-diagonal route: coefficient routing plus minimum-order survival
leaves exactly one named chain-level obstruction, rather than a further
colour-selection problem.

The dependency-free checker
[verify_odd_residue_minimality_survival.py](../computations/verify_odd_residue_minimality_survival.py)
checks the square-zero divided-power bookkeeping on deterministic exact
examples through \(h=8\), the three target words and the finite
aggregate-to-source ledger, and the equal nonzero off-diagonal coefficients.
All failure conditions remain active under `python3 -O`. The proof above,
rather than the finite examples, is uniform.
