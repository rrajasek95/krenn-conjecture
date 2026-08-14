# Full-tail descent is fibrewise; matching exchange changes (H_0)

## Verdict

Conditional on one genuinely natural, source-labelled `Phi` schema and the
signed Hasse deletion tower, the full-tail cover has an exact normalized
Čech descent at (h=5,6): perform the Čech coequalizer separately on the
\(\binom m2\) two-edge windows of each perfect matching (M), then take the
direct sum over all (M).  The normalized section is

\[
                 s(M)=\frac1{\binom m2}
                       \sum_{W\in\binom M2}(M,W).       \tag{1}
\]

Every matching coefficient occurs with total coefficient one.  Literal
matching-indexed (H_0) is preserved:

```text
                         h=5       h=6
tail edges m               4         5
perfect tail matchings   105       945
windows per matching       6        10
window objects            630      9450
H0 after fibre Cech       105       945.
```

This covers the `96/900` matchings outside a fixed four-site partition by
independent natural instantiation of `Phi`.  It does not require—and must
not be replaced by—identifying different matching monomials.

The four-cycle matching-exchange graph is connected, and every outside tail
is at distance at most two from the fixed partition.  But a raw exchange bar
changes the spectator fine/repeated label and the coefficient monomial.
Using a minimal forest to attach the outside tails lowers (H_0) by exactly
`96/900`; using all exchanges lowers it to one.  BC and higher Hasse cells
cannot repair this because they do not change \(\operatorname {im}d_1\).

Exact checker:
[`verify_h5_h6_full_tail_window_cech_matching_exchange_descent_gate.py`](../computations/verify_h5_h6_full_tail_window_cech_matching_exchange_descent_gate.py).

## 1. The matching-indexed window cover

Let \(\mathcal M_m\) be the perfect matchings of (2m) labelled tail sites,
and set

\[
 \mathcal U_m=\{(M,W):M\in\mathcal M_m,\ W\in\tbinom M2\}.
\]

For fixed (M), the window fibre is the Johnson graph (J(m,2)).  It has

\[
 \binom m2\text{ vertices},\qquad
 3\binom m3\text{ edges},\qquad
 \operatorname {rank}d_1=\binom m2-1.                \tag{2}
\]

The inherited triangles, disjoint-edge BC squares, and—for (m\ge5)—the
signed higher deletion cells make the chosen transports coherent.  They do
not alter (2).  Thus the disjoint union over all matchings has

\[
 H_0\cong\bigoplus_{M\in\mathcal M_m}\mathbf Q[M].    \tag{3}
\]

For the two orders checked exactly:

```text
                         h=5       h=6
internal connectors       1260     28350
rank d1                    525      8505
dimension C0               630      9450
dimension H0               105       945.
```

The projection \(\pi(M,W)=M\) and section (1) obey
\(\pi s=1\).  The checker enumerates every matching and presentation and
verifies that all fine and full repeated labels remain distinct inside a
fibre, while the coefficient on each (M) after averaging is exactly one.

Consequently, if `Phi` is natural on every labelled window and its
`PP/AugP2` rows are modules over the full Hasse tower, the descended cell is

\[
                         \sum_{M\in\mathcal M_m}\Phi(M),             \tag{4}
\]

with every source coefficient retained once.  This is the correct
full-source descent.  It preserves rather than quotients the basis (3).

## 2. Exact coverage beyond the fixed partition

Fix tail sites `0,1,2,3` for the original (h=3) partition.  A matching can
have zero, two, or four edges leaving this block.

- Zero leaving edges gives the fixed-partition family
  \(3(2m-5)!!\).
- With two leaving edges, one four-cycle flip returns to the fixed family.
- With four leaving edges, two flips suffice and one cannot suffice.

The exact counts are

\[
\begin{array}{c|c|c}
\text{distance}&\text{formula}&\text{meaning}\\ \hline
0&3(2m-5)!!&\text{fixed partition},\\
1&6\binom{2m-4}{2}\,2(2m-7)!!&\text{two sites leave},\\
2&\binom{2m-4}{4}4!(2m-9)!!&\text{four sites leave}.
\end{array}                                           \tag{5}
\]

The complete enumerations give

```text
h=5: distance profile 0:9, 1:72, 2:24   (96 outside)
h=6: distance profile 0:45,1:540,2:360  (900 outside).
```

So matching exchange proves combinatorial reachability.  Under the
conditional naturality hypothesis it is unnecessary: relabelled instances
of `Phi` already exist on every (M), and (1) descends their windows
objectwise.

## 3. The strongest literal exchange lift

Two adjacent matching vertices differ by replacing two disjoint edges with
one of the other pairings of their four endpoints.  The exchange graph has

\[
 \deg(M)=2\binom m2,qquad
 |E|=|\mathcal M_m|\binom m2.                         \tag{6}
\]

Hence it has `630` edges at (h=5) and `9450` at (h=6).

Adjacent matchings share (m-2) edges.  The strongest possible physical
lift chooses a two-edge window entirely inside this common part.  There are
\(\binom{m-2}{2}\) such lifts per exchange: one at (h=5), three at
(h=6).  The checker audits all `630/28350` lifted comparisons.

For every one of them:

```text
site word                         equal
q_(v,W) two-edge window           equal
operation parent                  equal
spectator T_S fine label          different
removed/reinserted repeated data  different
full matching coefficient q_M     different.
```

The word equality is not a coarsening accident.  The selected common window
marks the same physical tail edge by `12`, while every other tail endpoint
is `2`; therefore both site words agree.  The first mismatch is the
spectator matching in

\[
                     T_S q_{(v,W)},                  \tag{7}
\]

and the tied removed/reinserted label.  Algebraically the two coefficient
tops differ by replacing two independent factors.  The complete hafnian
sums both monomials; it does not assert their equality.

## 4. Why raw exchange changes (H_0)

Before cross-matching edges, (3) has dimension (N=105) or (945).  A
multi-source exchange forest rooted at the fixed family needs precisely one
edge for each outside matching.  Adding the raw boundaries

\[
                            d\phi_e=M'-M              \tag{8}
\]

therefore gives

```text
                         h=5       h=6
H0 before exchange        105       945
forest edges added         96       900
H0 after forest             9        45.
```

Adding the full connected exchange graph reduces (H_0) to one in either
order.  This is exactly the coinvariant quotient which forgets the
independent matching monomials.

Triangles, BC squares, the (h=6) `sgn tensor Std_5` cells, and every higher
Hasse cell map to (C_1).  They may remove cycles in \(\ker d_1\), but no
higher differential changes \(\operatorname {im}(d_1:C_1\to C_0)\).
Consequently they cannot restore the lost matching-indexed (H_0).

## 5. Presentation-safe cylinder and terminal debt

One can preserve (H_0) formally by retaining an exchange coordinate
\(u_e\) and using

\[
                         db_e=(M'-M)-u_e.             \tag{9}
\]

For a forest with (N-F) edges, (9) adds (N-F) new (C_0) coordinates
and has rank (N-F), so its (H_0) dimension remains (N).  But it has not
descended the fixed-partition proof: the changed coefficient/fine/repeated
data now survives as the (u_e) debt.

The terminal alternative is exact.  Every matching-coordinate covector
\(\chi\) extends across (9) by

\[
                       \chi(u_e)=\chi(M')-\chi(M).     \tag{10}
\]

In particular the `96/900` outside-coordinate detectors remain independent.
Killing them requires a new physical coefficient-changing exchange
comparison, not another BC/Hasse coherence among existing connectors.

## 6. Conditional theorem and scope

The full-tail issue closes conditionally in the following precise form:

> If `Phi_KS,r0/P_f` is a source-labelled natural schema on every labelled
> two-edge window and its complete word/fine/repeated and protected rows are
> linear for the signed matching-Hasse tower, then (1) descends the window
> cover separately for every matching.  Summing the resulting \(\Phi(M)\)
> covers every full-tail coefficient exactly once and preserves the complete
> matching-indexed source.

The phrase “natural schema on every window” is essential.  If only one
fixed-partition cell is known, matching-exchange reachability does not
promote it: equations (7)--(10) give the exact obstruction.

This theorem is an exact complete census for (h=5,6), with every matching
flip and strongest common-window lift checked in literal site word, fine,
removed/reinserted, repeated, coefficient, and operation labels.  It does
not construct `Phi`, prove its full Hasse-linearity, or add a new physical
coefficient-exchange generator.
