# Cost-32 mixed-endpoint one-site Laurent closure is empty

## 1. Outcome

Continue in the coordinate-cell and one-site response-row class of the
[support-frontier note](mixed-endpoint-one-site-support-frontier.md).  The
necessary Boolean support relaxation there first reaches 32 active cells
after all smaller supports are excluded.  This note closes that next layer.

**Theorem 1.1.** There is no exact mixed-endpoint coordinate solution with
one-site coordinate response rows and at most 32 active aggregate cells.
More precisely, after imposing exact Laurent consistency on every forced
two-term quadratic cancellation, the minimum necessary support is at least
33 in the path--edge row geometry and at least 34 in the matching row
geometry.

This remains a restricted sparse theorem.  It does not cover multi-site
response rows or non-coordinate edge blocks, and it does not assert that a
support at 33 or 34 has compatible weights.

## 2. Exact sign-lattice test

For a fixed support, consider every required-zero coefficient of
\(q^{[2]}\) having exactly two supported matching terms.  Since all active
cell weights are nonzero, division by one term gives

\[
                         x^{d_k}=-1.                    \tag{1}
\]

Adjoin a formal sign coordinate.  The augmented integer lattice is generated
by

\[
                         (d_k,1)\quad\text{and}\quad(0,2).          \tag{2}
\]

Equations (1) are inconsistent exactly when this lattice contains
\((0,1)\).  An exact FLINT Hermite normal form tests membership.  When the
answer is inconsistent, its transformation matrix returns integers
\(r_k,t\) satisfying

\[
              \sum_k r_kd_k=0,\qquad \sum_k r_k+2t=1.              \tag{3}
\]

The checker independently substitutes the returned relation into every
exponent column and checks the odd sum.  Thus every rejected support carries
an explicit characteristic-zero Laurent contradiction.

## 3. Sound cancellation-aware CEGAR cuts

It would be unsound merely to forbid all cells used by (3): a denser support
could activate the third matching term in one coefficient and replace its
binomial by a trinomial.  The learned clauses retain precisely this escape.

For each used binomial \(k\), let \(T_{k,0},T_{k,1}\) be its two active
cell monomials and let \(Z_{k,2}\) be the exact conjunction indicator for
its currently inactive third matching.  From one odd relation the checker
learns

\[
 \bigvee_{r_k\ne0}
 \left(
   \bigvee_{z\in T_{k,0}\cup T_{k,1}}\neg z
   \ \vee\ Z_{k,2}
 \right).                                               \tag{4}
\]

Indeed, if (4) were false, all two displayed terms would remain active and
every third term would remain inactive, so every binomial used in (3) would
persist verbatim.  Equation (3) would still give \(1=-1\).  Clause (4)
therefore excludes no Laurent-compatible support, including a denser support
which repairs a binomial by gaining its third term.

After each cut, exact weighted MaxSAT recomputes the smallest support
satisfying the original quadratic and cubic support rules together with all
learned clauses.  Term indicators are equivalences, not one-way witnesses.

## 4. Exhaustion data

For path--edge rows, the run learns 32 exact circuit cuts:

\[
 \begin{array}{c|ccc|c}
 \text{support cost}&30&31&32&\text{next minimum}\\ \hline
 \text{cuts learned}&8&12&12&33.
 \end{array}
\]

For matching rows, it learns 30 cuts:

\[
 \begin{array}{c|cc|c}
 \text{support cost}&30&32&\text{next minimum}\\ \hline
 \text{cuts learned}&5&25&34.
 \end{array}
\]

These cut counts are CEGAR rounds, not counts of all supports: one valid
clause may remove several supports at once.  The deterministic ledgers hash
the round number, cost, active support, exact HNF relation, and learned clause:

~~~text
path-edge:
6b19a3776861df1d6a7b4a2280ecd624df2b79d431c2c22bf0722847722f8969
matching:
fbde1edf4126a9172fa3bb03634b41fee5fd55c456d12445e33b4449b70a8d16
~~~

Because all learned clauses are necessary for an exact weighting, the final
MaxSAT lower bounds prove Theorem 1.1.

## 5. Reproducibility and next test

Run

~~~sh
uv run python computations/verify_mixed_endpoint_one_site_laurent_closure.py
~~~

The first unresolved path--edge layer is cost 33; the first unresolved
matching layer is cost 34.  The next counterexample test is to continue the
same cancellation-aware Laurent closure until a sign-consistent support
appears.  Only then is it useful to solve that support's full quadratic and
cubic weight equations and target normalizations.
