# Full endpoint induction leaves a coefficient-one centered residual

## Exact verdict

Summing the centered (h)-packet over every way the two new sites can enter
an occurrence does **not** give (c_{f,h+1}), even after Reynolds
normalization and addition of the complete response row.  This is stronger
than the fixed-spectator obstruction: the transfer includes new residual
edges, one-new-endpoint bridges, and two-new-endpoint replacements.

For a fixed marked occurrence (f), the full pull-push transfer has two
unmarked coefficients `0` and `-1`.  A linear combination of
(c_{f,h+1}) and the complete row is constant on every unmarked
occurrence, so no such combination equals the transfer.  The difference
of those two coefficients is exactly one at every (h\ge3).

The termwise product-rule faces do form a pointed permutation covariant,
but reattaching their inserted edge recovers this same nonuniform transfer.
They therefore do not yet define the clean-line covariant or filtered
homology class required by (operatorname {Tr}_h).  The first positive
repair is exact: cancel the coefficient-one association-scheme residual
by a physical product-rule cell before proving clean-line type and the
common Hankel equations.

Checker:
[`verify_uniform_centered_occurrence_full_endpoint_transfer_gate.py`](../computations/verify_uniform_centered_occurrence_full_endpoint_transfer_gate.py).

## 1. The full all-role insertion correspondence

Let

\[
 \Omega_h(V)=\{(p,s,R):p\ne s,\ R\text{ a perfect matching of }
                           V\setminus\{p,s\}\},\qquad |V|=2h.
\]

Its cardinality is

\[
                 N_h=2h(2h-1)(2h-3)!!.                    \tag{1}
\]

For a two-element complement ({a,b}), an occurrence on the old
(2h) sites extends to the (2h+2) sites in seven chart types:

\[
\begin{array}{c|c}
\text{type}&\text{extension of }(p,s,R)\\ \hline
0&(p,s,R\cup\{ab\})\\
p_a&(a,s,R\cup\{bp\})\\
p_b&(b,s,R\cup\{ap\})\\
s_a&(p,a,R\cup\{bs\})\\
s_b&(p,b,R\cup\{as\})\\
2_{ab}&(a,b,R\cup\{ps\})\\
2_{ba}&(b,a,R\cup\{ps\}).
\end{array}                                                \tag{2}
\]

Thus (2) includes every role of the new pair; it is not fixed-edge
suspension.  The first five chart types are injective.  A two-new-endpoint
chart has fibre (2h), since any of the (h) final residual edges, in
either orientation, can have been the old endpoint pair.

For every chart (T), write (m_T(g)=|T^{-1}(g)|).  Pull the marked
center back through every preimage and push it forward again:

\[
 K_{f,h}=\sum_T\sum_{x\in T^{-1}(f)}
       T\left(N_he_x-1_{\Omega_h}\right).                 \tag{3}
\]

This is the unnormalized pointed Reynolds sum.  Dividing it by any orbit or
stabilizer scalar does not affect the obstruction below.  Put

\[
                     k_h(f,g)=\sum_Tm_T(f)m_T(g).          \tag{4}
\]

Then

\[
 K_{f,h}(g)=7hN_h\,\delta_{fg}-k_h(f,g).                  \tag{5}
\]

Indeed, (f) has (h) type-zero preimages, (4h) one-endpoint
preimages, and (2h) old-endpoint orientations in its unique compatible
two-endpoint chart.  Hence it has (7h) preimage columns.  Moreover

\[
 k_h(f,f)=h+4h+(2h)^2=4h^2+5h.                            \tag{6}
\]

The Gram row has sum (7hN_h), so (5) has augmentation zero.  Centering is
not the problem; uniformity on the complement is.

## 2. The exact coefficient-one residual

Take

\[
 f=(0,1;23|45|67|\cdots|(2h)(2h+1)).                     \tag{7}
\]

Reverse the ordered endpoints for two test occurrences.  Let

\[
\begin{aligned}
 g_0={}&(1,0;34|56|\cdots|(2h-1)(2h)|(2h+1)2),\\
 g_1={}&(1,0;23|56|78|\cdots|(2h-1)(2h)|(2h+1)4).
                                                               \tag{8}
\end{aligned}
\]

The cyclic notation in the second line omits an empty middle range at the
smallest order; at (h=3), it is (23|56|74).  Both are perfect matchings.
The first shares no residual edge with (f); the second shares exactly
`23`.

Because both ordered endpoints are reversed, (f) and (g_i) share no
one-new-endpoint chart and no ordered two-new-endpoint chart.  Their only
common charts are type-zero charts indexed by a common residual edge.
Therefore

\[
                  k_h(f,g_0)=0,\qquad k_h(f,g_1)=1.       \tag{9}
\]

By (5),

\[
                  K_{f,h}(g_0)=0,\qquad K_{f,h}(g_1)=-1.  \tag{10}
\]

Every vector in
(operatorname {span}\{c_{f,h+1},1_{\Omega_{h+1}}\}) has one common
coefficient on (Omega_{h+1}\setminus\{f\}).  Equation (10) proves

\[
 K_{f,h}\notin
 \operatorname {span}\{c_{f,h+1},1_{\Omega_{h+1}}\}      \tag{11}
\]

for every (h\ge3).  Reynolds division only scales the `0/-1` difference,
and a complete-row correction shifts both coefficients equally.  Neither
operation removes (11).

The exact first step has (N_3=90), (N_4=840), 196 charts, 21 preimage
columns at (f), and

\[
 k_3(f,f)=51,\qquad K_{f,3}(f)=21\cdot90-51=1839.         \tag{12}
\]

Exact enumeration gives complement Gram values

```text
0, 1, 2, 3, 5, 6, 7, 48, 49,
```

so the coefficient-one debt is only the first of several pointed
association-scheme components.  The uniform proof (9) needs no finite
enumeration.

## 3. Product-rule faces do not yet give the \(\operatorname {Tr}_h\) covariant

Every chart in (2) inserts exactly one edge (q_e), though for the endpoint
charts the identity of (e) depends on the old occurrence.  Termwise,

\[
                       d(q_ex)=q_e\,dx+dq_e\otimes x.     \tag{13}
\]

Summing the second term in (13) over the same preimages as (3) gives a
canonical edge-labelled pointed face (F_{f,h}).  Multiplying each labelled
face back by its own (q_e) gives

\[
                     \operatorname {attach}(F_{f,h})=K_{f,h}. \tag{14}
\]

Hence (10) is a necessary-boundary obstruction for the product-rule face,
not merely an objection to the top occurrence coefficient.  Before the
face can represent the missing

\[
                  \rho_{2h-6}\in\operatorname {Sym}^{2h-6}U
\]

or an input to (operatorname {Tr}_h), a physical correction must make
its reattachment the desired centered boundary.  At present the face is an
edge-labelled permutation covariant carrying the nonzero residual (10).
No clean-line (SL(U)) type, boundary-independence, nonzero terminal value,
or common-Hankel annihilation follows from the Reynolds sum.

The smallest exact positive continuation is therefore:

> Construct a source-valid product-rule correction whose reattachment is
> the negative of (K_{f,h}-a_hc_{f,h+1}) (with whatever normalization
> (a_h) is chosen), beginning with the coefficient-one class (10).  Then
> prove that the corrected face has clean-line type
> (operatorname {Sym}^{2h-6}U), is invariant under filtered source
> boundaries, is nonzero, and satisfies every common Hankel shift.

Those last conditions are exactly the load-bearing properties of
(operatorname {Tr}_h); the occurrence Reynolds average alone supplies
none of them.

## Scope

This theorem audits the complete bare occurrence-species induction and its
formal product-rule faces.  It does not exclude a higher Hasse/Spencer cell
which cancels (10), nor a source-dependent transfer using the activity or
another clean-line covariant.  It proves that such a correction is required
before full endpoint induction can serve as the centered physical descent.

Run:

```text
python3 computations/verify_uniform_centered_occurrence_full_endpoint_transfer_gate.py
python3 -O computations/verify_uniform_centered_occurrence_full_endpoint_transfer_gate.py
python3 -I -S computations/verify_uniform_centered_occurrence_full_endpoint_transfer_gate.py
```

Frozen ledger SHA-256:

```text
2020967237fea2cf8457b2e825574c7be6789a00da3eef0a7c0a882ca2f19535
```
