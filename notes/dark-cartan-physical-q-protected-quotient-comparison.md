# Physical `q` transport is equality of two defect classes

## Exact theorem

Let

\[
 J:L\longrightarrow E,qquad
 J_3:L_3\longrightarrow E_3
\]

be the complete protected maps in an arbitrary exhaustive Cartan component
grade and the canonical faces-`(3,5)`, `h=3` grade.  Write

\[
 q=M-a,qquad q_3=M_3-a_3,                                      \tag{1}
\]

where `M` is the aggregate of the six selected literal matching rows and
`a=ainc` is physical anchor incidence.  Suppose a source-valid,
word/fine/repeated-grade comparison satisfies

\[
                         J_3\Phi=A J.                             \tag{2}
\]

Define the two row defects

\[
 \delta_M=M-M_3\Phi,qquad \delta_a=a-a_3\Phi.                   \tag{3}
\]

Then the following are equivalent:

\[
\begin{aligned}
 q(x)&=q_3(\Phi x) &&(x\in\ker J),\\
 \delta_M-\delta_a&=\lambda J &&\text{for some }\lambda,\\
 [\delta_M]&=[\delta_a] &&\text{in }L^*/\operatorname{row}(J).
\end{aligned}                                                    \tag{4}
\]

This is the weakest comparison needed by the all-dark
generator/Fredholm branch.  When (4) holds, it constructs the augmented
target comparison

\[
 \binom{J_3\Phi}{q_3\Phi}
  =
 \begin{pmatrix}A&0\\-\lambda&1\end{pmatrix}
 \binom{J}{q}.                                                    \tag{5}
\]

Thus the protected-zero property and the physical `q` value transport
together, and the existing whole-kernel alternative applies.

Checker:
[`verify_dark_cartan_physical_q_protected_quotient_comparison.py`](../computations/verify_dark_cartan_physical_q_protected_quotient_comparison.py).

## Reduction to aggregate matching and `ainc`

Separate chain-homotopy laws

\[
 \delta_M=\mu J,qquad \delta_a=\nu J                            \tag{6}
\]

are a transparent sufficient condition: then
`q-q_3 Phi=(mu-nu)J`.  They are not necessary.  The two defects may
represent the same nonzero quotient class.  In that case neither `M` nor
`ainc` transports separately, but their common error cancels in `q`.

Accordingly, the exact hierarchy is

```text
individual six matching rows + ainc       strongest labelled comparison
matching aggregate M + ainc separately    physical two-row comparison
[delta_M]=[delta_ainc] mod row(J)          weakest q/kernel comparison.
```

The two-row comparison is preferable if later arguments need anchor
incidence separately.  The last line is sufficient for the dark
generator/Fredholm decision, which consumes only `q|ker(J)`.

No ordinary residue, eta/sigma, or shifted-Kähler hypothesis occurs in
(1)--(6).  Those data belong to the independent terminal packet and do not
alter this quotient obstruction.

## First exact obstruction

The obstruction is the single class

\[
 \mathfrak o_q(\Phi)
  =[\delta_M-\delta_a]
  \in L^*/\operatorname{row}(J)
  \simeq (\ker J)^*.                                               \tag{7}
\]

If it is nonzero, row-space/kernel duality supplies a literal witness

\[
 x\in\ker J,qquad
 (q-q_3\Phi)(x)\ne0.                                               \tag{8}
\]

This is earlier and sharper than a residue/ridge failure: `Phi` may already
be a protected chain map.  For example, with

\[
 J=J_3=(1\;0\;0),\qquad \Phi=I,
\]

the matching aggregate can transport exactly while `ainc` differs by
`(0,-1,0)`.  The protected kernel vector `(0,1,0)` then pairs to one with
`o_q`.  Interchanging the roles gives the equally small aggregate-matching
obstruction.

The checker also records the genuinely weaker success case: take
`delta_M=delta_a=(0,1,0)`.  Both constituent defects are nonzero modulo the
protected row, yet `o_q=0` and `q` transports exactly.

## Consequence after global dark absorption

Commit `bcc75e1` produces a unit kernel class of the complete physical map
when every exhaustive critical component is dark.  It does not construct a
map to the canonical `h=3` grade and does not determine either class in
(3).  Component charges remain analytically useful for solving the global
potential, but they are not elements of the physical quotient (7).

The five old repeated `P3+K2` grades already have literal six-matching
aggregates, and the canonical grade has the physical identification (1).
For a new relative component grade the next calculation is now exact:

1. construct any source-valid grade-preserving protected `Phi` satisfying
   (2);
2. compute only the two aggregate defects (3), not six individual rows;
3. if their quotient classes agree, use (5);
4. otherwise extract the protected-kernel witness (8).

The current component-placement and global-absorption theorems do not force
step 3, so a uniform physical comparison is not yet constructed.  The
remaining obstruction is precisely (7), rather than an unspecified
terminal naturality condition.

## Verification

Run:

```text
python3 computations/verify_dark_cartan_physical_q_protected_quotient_comparison.py
python3 -O computations/verify_dark_cartan_physical_q_protected_quotient_comparison.py
python3 -I -S computations/verify_dark_cartan_physical_q_protected_quotient_comparison.py
```

Frozen ledger SHA-256:

```text
687d148288b8f72dec015dc9d920a3dc865234add97972978ed5598bef91eb58
```
