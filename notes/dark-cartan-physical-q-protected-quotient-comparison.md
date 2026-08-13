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

This apparent obstruction closes positively when the comparison is physical
on both complete relative source domains.  Equation (2) gives

\[
                         J_3(\Phi x)=0,                             \tag{9}
\]

and (8) implies

\[
                         q(x)\ne0
              \quad\text{or}\quad q_3(\Phi x)\ne0.                 \tag{10}
\]

In the first case `x/q(x)` is the physical relative generator in `L`; in
the second, `Phi x/q_3(Phi x)` is the canonical `h=3` relative generator.
Thus any fully physical protected comparison has the closed dichotomy

```text
o_q(Phi) != 0   -> relative generator on the source or canonical side;
o_q(Phi)  = 0   -> augmented q comparison, then generator/Fredholm.
```

The qualification is load-bearing.  `Phi x` must be a class in the
complete physical relative source domain, with physical `q_3`, rather than
only a vector in an analytical component projection or presentation
quotient.  Likewise `q=M-ainc` must already be a physical terminal on `L`.
Without these typings, (10) is only a discrepancy of formal row values and
cannot be normalized to the generator of `0373033`.

The checker audits both possible positive arms (source visible and canonical
image visible).  This is earlier and sharper than a residue/ridge failure:
`Phi` may already be a protected chain map.  For example, with

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
4. otherwise extract the protected-kernel witness (8) and normalize the
   nonzero physical terminal guaranteed by (10).

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
bada633c6b28040aa5b67ba279a1d8a48042ac8b3eaa5eccd2cfd72e97369163
```
