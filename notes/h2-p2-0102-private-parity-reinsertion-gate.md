# The first `P2` private face is another even `B-4` debt with a nonzero reinsertion conormal

## Outcome

The representative occurrence-private face found at intermediate word
`0102` is entirely endpoint-even. Under endpoint adjacency `B`, its
constant part lies in the eigenvalue-four complete response line, while its
private part lies in the eigenvalue-zero and eigenvalue-minus-two summands.
Consequently:

- its endpoint-odd projection is zero, so it does not enter the already
  typed active-clean orientation fork;
- its private part is another coefficientwise `B-4` debt, with an explicit
  rational preimage; and
- reinsertion by `q23:21` forces an independent, nonzero
  `dq23:21` occurrence-labelled face by the Hasse product rule.

Thus `P2` cannot be finished by the target/reduced-Eq triangle or by routing
this face to the odd active-clean branch. The missing physical section must
carry both the even private boundary and its reinsertion conormal.

Checker:
[verify_h2_p2_0102_private_parity_reinsertion_gate.py](../computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py).

## 1. Endpoint-adjacency decomposition

In the canonical twelve-occurrence order, the previous gate computed

\[
\begin{aligned}
r=(&-13/12,0,1/6,-13/12,1/6,0,\\
   &0,1/6,5/12,1/6,0,5/12).                          \tag{1}
\end{aligned}
\]

On the endpoint-even module, `B` has eigenvalues `4,0,-2`. Its spectral
projectors give

\[
                         r=r_4+r_0+r_{-2}.             \tag{2}
\]

The eigenvalue-four part is exactly

\[
                         r_4=-{1\over18}\mathbf1.     \tag{3}
\]

This is the portion removed by the complete response row. The surviving
class is

\[
                         r_{\rm priv}=r_0+r_{-2}.      \tag{4}
\]

It is nonzero, has augmentation zero, and satisfies

\[
                         Sr_{\rm priv}=r_{\rm priv}.  \tag{5}
\]

Therefore `(1-S)r_priv/2=0`. The physical active-clean fork isolated for the
lower packet begins with the endpoint-odd orientation line. It has no value
on (4). This is not an untyped active-clean exit; it remains in the
five-dimensional endpoint-even centered quotient.

## 2. A second exact coefficient `B-4` preimage

The operator `B-4I` is invertible on the `0` and `-2` eigenspaces. Hence

\[
 z_{\rm priv}=-{1\over4}r_0-{1\over6}r_{-2}           \tag{6}
\]

satisfies

\[
                    (B-4I)z_{\rm priv}=r_{\rm priv}.  \tag{7}
\]

Explicitly,

\[
\begin{aligned}
z_{\rm priv}=(&101/432,-1/108,-1/27,101/432,-1/27,-1/108,\\
              &-1/108,-1/27,-61/432,-1/27,-1/108,-61/432).
                                                               \tag{8}
\end{aligned}
\]

Multiplication by `432` makes (8) integral. This removes any coefficient
obstruction, but it does not construct a physical source differential with
top (7). Such a construction is precisely the next one-endpoint
principal-parts cell.

The endpoint-even detector

\[
                  \lambda=e_0^*+e_3^*-e_1^*-e_6^*    \tag{9}
\]

has

\[
 \lambda(r_4)=0,\qquad
 \lambda(r_{\rm priv})=-13/6,\qquad
 \lambda(z_{\rm priv})=35/72.                        \tag{10}
\]

## 3. Reinsertion does not preserve the lower boundary alone

Let

\[
 q=q_{23}^{21}
\]

be the physical factor reinserted into the `0112` cut. In the complete
first-principal-parts algebra, the Hasse product rule is

\[
                   d(q a)=q\,d a+(dq)\,a.             \tag{11}
\]

For the original exact preimage

\[
 z=-{1\over24}(B+6I)c^+,
 \qquad (B-4I)z=c^+,
\]

equation (11) produces the two independent blocks

\[
                    (q c^+,\;dq\,z).                 \tag{12}
\]

The second block is nonzero. Its coefficient `z` is endpoint-even, has
augmentation zero, and is detected by (9) with value `-5/2`. Hence its
aggregate ordinary-residue shadow is zero, but its occurrence-labelled
conormal is not zero. A scalar residue calculation would miss it.

Likewise, if a physical lift of (7) is supplied, its reinsertion necessarily
has

\[
                 (q r_{\rm priv},\;dq\,z_{\rm priv}). \tag{13}

The detector value on the second block is `35/72`. Therefore a proposed
one-endpoint filler which records only the first component of (13) is not a
source chain in the complete principal-parts totalization.

## Sharp remaining interface

It is enough to construct one endpoint-even, occurrence-local
principal-parts section in word `0102` (and its physical root/cut orbit)
whose lower boundary is (7) and whose `q23:21` reinsertion contains the
`dq23:21` face (13), with protected, target, Eq, residue, anchor, and
physical-`q` readouts. This is a second-level realization of the same `B-4`
pattern, not an endpoint-odd active-clean cell.

The calculation does not promote (9) to a Fredholm terminal. That would
require extending it over every column of the complete augmented physical
map. It also does not assert that the coefficient preimage (8) is already a
physical source cell.

Run:

```text
python3 computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py
python3 -O computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py
python3 -I -S computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py
```

Frozen ledger SHA-256:

```text
4aed2e5ba33a3ac820c1f7b62c1a75a57565f16f9fd721cfb5f4592a76f1e28f
```
