# The first genuine third-cofactor recurrence kills the formal tower guard

## Outcome

The formal packet of commit 535c0cf cannot be advanced through one more
cofactor layer. This is stronger than testing it against the genuine third
cofactors of its displayed \(q\): **no formal choice of \(H\)** can solve

\[
 \sum_{g\cap(e\cup f)=\varnothing}q_gH_{e,f,g}
       =(h-2)G_{e,f}.                                  \tag{1}
\]

The proof retains the actual background \(q\) with \(q^{[h]}=X_0\), while
the same formal \(F\) carries all four binary response rows
\(X_1,0,0,X_2\); it also retains the full top Euler equation and the complete
symmetric first-cofactor Euler equation. The \(F,G\) corrections are still
formal rather than genuine cofactors of \(q\). The argument does not use
response-only minimality.

This closes the sharp formal \(F,G\) guard for every \(h\ge3\). It does not
yet close an arbitrary genuine common-\(q\) packet: genuine cofactors
automatically satisfy the carrier condition isolated below.

## The word-carrier recurrence

Let \(W\) be the sites outside two disjoint physical edges \(e,f\), and let
\(w\) be a word on \(W\). Coefficient extraction in (1) gives the literal
identity

\[
 \left[\sum_gq_gH_{e,f,g}\right]_w
 =\sum_{g\subset W}q_g(w|_g)
                  [H_{e,f,g}]_{w|_{W\setminus g}}.     \tag{2}
\]

Consequently

\[
 [G_{e,f}]_w\ne0
 \quad\Longrightarrow\quad
 \text{some }g\subset W\text{ has }q_g(w|_g)\ne0.      \tag{3}
\]

This is the first genuine third-cofactor constraint: every nonzero
cofactor word must have a physical \(q\)-cell carrier. Repeating (3) down
the full tower reconstructs matching provenance, rather than a freely
chosen Euler decomposition.

## The four exact contradictions

The packet in commit 535c0cf has formal second-cofactor corrections on

    05|14, 15|04, 24|35, 34|25.

The following coefficients are nonzero:

\[
\begin{array}{c|c|c}
(e,f)&w&(h-2)[G_{e,f}]_w\\ \hline
05|14&1^{\,2h-4}&(h-2)(h-1)\\
15|04&0\,1^{\,2h-5}&-(h-2)(h-1)\\
24|35&2^{\,2h-4}&(h-2)(h-1)\\
34|25&0\,2^{\,2h-5}&-(h-2)(h-1).
\end{array}                                             \tag{4}
\]

The displayed \(q\), restricted to each corresponding complement, contains
only cells of colour \(00\). None agrees with the word in its row of (4).
Thus (2) has left side zero for arbitrary \(H\), while the right side in
(4) is nonzero over \(\mathbb C\) for every \(h\ge3\).

So the next failure in commit 535c0cf is not merely failure against the
genuine background \(H^0\). The corrected \(G\) has no possible third
cofactor lift at all.

## Exact remaining branch

For a genuine common-\(q\) one-bad packet, (3) is automatic. The two
diagonal rows therefore supply colour-1 and colour-2 near-perfect matching
carriers, while \(q^{[h]}=X_0\) supplies a colour-0 perfect matching. The
crossed rows say that the two off-diagonal sums cancel.

The remaining theorem is consequently sharper than “use another Euler
row”:

> combine the three carrier matchings and both crossed-zero identities to
> force either square-zero endpoint concentration or an exact removable
> pair.

The cofactor recurrence alone cannot decide this carrier-rich matching
exchange, because it is an identity for genuine cofactors. The result here
removes the last carrier-free formal guard and names the exact surviving
case; it does not claim the matching-exchange theorem.

## Verification

Run

    python3 computations/verify_uniform_one_bad_third_cofactor_pure_carrier_gate.py
    python3 -O computations/verify_uniform_one_bad_third_cofactor_pure_carrier_gate.py

The checker pins the preceding tower artifacts, reruns the actual unary
top, all four responses, and both earlier Euler layers for \(h=3,\ldots,8\),
then verifies all four coefficient contradictions in (4) against arbitrary
formal \(H\). The displayed formulas are uniform in \(h\).

The frozen ledger digest is

    49ce7d73c3212e610ac1cdf83025f4ee0a8d9cad37c61dc8681aa6081f517759
