# Symmetry does not kill or pair the eight strict `kappa_mix` scalars

## Outcome

The symmetry audit is conclusive and negative.  For the eight literal
fixed-packet mixed cells

\[
 \Pi_{B/Eq}(\kappa_i)\equiv\lambda_i(\delta,0),
 \qquad \chi(\kappa_i)=4\lambda_i,
 \qquad \delta=(1,1,-1,-1),                         \tag{1}
\]

no source-grade stabilizer negates `chi`.  In fact the full marked-packet
site/root stabilizer is the identity.  Ordered endpoint reversal fixes each
instance but has sign `+1` on `chi`.  Hence symmetry forces neither
`lambda_i=0` nor an equality between two of the eight fixed-packet scalars.

There is a tempting coarser action.  After forgetting the marked physical
occurrence, the lower word stabilizer is `V4` and its eight-word orbits have
sizes `4+2+2`.  But every nonidentity transport moves the marked endpoint
and residual cut, so those are arrows to different packet objects, not
endomorphisms of the fixed physical grade.  Even if one grants an extra
identification of transported packets, all signs are positive and three
arbitrary orbit scalars remain.

Exact checker:
[`verify_h3_kappa_mix_eight_instance_symmetry_covariance_gate.py`](../computations/verify_h3_kappa_mix_eight_instance_symmetry_covariance_gate.py).

## 1. The eight full tags

The common cap-grade data are retained literally:

```text
response source word   11:110000
cap output word        01211222
fine                   t*q_(v,N), selected six P3+K2 occurrences
repeated               P3+K2
operation parent       response-to-AugP2 mixed orbit/K_Eq kappa_mix
cap window             2345 with literal occurrence labels
lower parent           0112 on sites 0,1,4,5
marked lower packet    ordered 0->1, residual q45:12
reinsertion            q23:21.
```

The eight lower one-root word labels are

```text
0012  0102  0110  0111  0122  0212  1112  2112.       (2)
```

These labels record the source ancestry of the eight cap-grade instances;
they do not license forgetting the occurrence, source parent, operation,
or physical window.

## 2. Exact coarse `V4` action

Let `a` exchange the two lower sites of colour `1`, namely `1<->4`.  Let
`b` exchange sites `0<->5` and simultaneously exchange colours `0<->2`.
On the words in the order (2), the exact action is

```text
1   0012 0102 0110 0111 0122 0212 1112 2112
a   0102 0012 0110 0111 0212 0122 1112 2112
b   0212 0122 2112 1112 0102 0012 0111 0110
ab  0122 0212 2112 1112 0012 0102 0111 0110.
```

Thus

\[
\begin{aligned}
 \mathcal O_{211}&=\{0012,0102,0122,0212\},\\
 \mathcal O_{220}&=\{0110,2112\},\\
 \mathcal O_{310}&=\{0111,1112\}.                    \tag{3}
\end{aligned}
\]

The permutation character in the order `(1,a,b,ab)` is `(8,4,0,0)`.
The four words `0110,0111,1112,2112` have coarse stabilizer `{1,a}`;
the other four have trivial coarse stabilizer.

But the selected ordered occurrence `P=(0,1;45)` is transported to

```text
1.P   (0,1;45)
a.P   (0,4;15)
b.P   (5,1;04)
ab.P  (5,4;01).                                       (4)
```

Even allowing the ordered mate `(1,0;45)`, only the identity preserves the
fixed packet.  Covariance therefore has the groupoid form

\[
             \lambda_{(P,w)}=\lambda_{(gP,gw)},       \tag{5}
\]

conditional on constructing a natural `kappa_mix` family.  Equation (5)
does not compare `lambda_(P,w)` with `lambda_(P,gw)`.

## 3. Exact action on `chi`

The literal corner order is

```text
0  DQ[a|b]
1  DQ[b|a]
2  PS[P0,S1]
3  PS[P1,S0].
```

On the eight `(B,Eq)` coordinates,

\[
 \chi=(1,1,-1,-1\mid-1,-1,1,1).                     \tag{6}
\]

The admissible local corner group swaps the two DQ corners and/or the two
PS corners.  Every element fixes (6).  In particular endpoint reversal is
the simultaneous permutation `(0 1)(2 3)` and has `chi` sign `+1`.  Literal
site/root transport also has sign `+1` when (6) is carried with its DQ/PS
and `B/Eq` labels.

There are two obvious sign-negating controls:

- `(0 2)(1 3)` exchanges the DQ and PS shores and sends `delta` to
  `-delta`, but changes the retained operation shore/parent;
- exchanging the `B` and `Eq` blocks sends `B-Eq` to `-(B-Eq)`, but changes
  the private versus reduced-Eq row type.

Neither is a source-grade automorphism.  Thus there is no element which
both fixes a literal `kappa_i` and negates its `chi` value.

## 4. What covariance can and cannot reduce

For the strict source-labelled packet the symmetry-invariant scalar space
still has dimension eight:

\[
                      (\lambda_0,\ldots,\lambda_7)\in\mathbb Q^8. \tag{7}
\]

No pairings and no forced zeros follow.

If one *forgets* the marked occurrence, the positive-sign `V4` covariance
equations have rank five.  The invariant space then has dimension three,
with conditional equalities

\[
\begin{aligned}
 \lambda_{0012}=\lambda_{0102}=\lambda_{0122}=\lambda_{0212},\\
 \lambda_{0110}=\lambda_{2112},\qquad
 \lambda_{0111}=\lambda_{1112}.                       \tag{8}
\end{aligned}
\]

Even this deliberately coarsened quotient leaves three unrestricted
parameters.  More importantly, (8) is not available in the physical
source presentation without a new canonical identification of the four
transported marked packets in (4).

Therefore the symmetry lane does not shorten the accepted terminal test:
the exact `Psi` theorem still needs the eight strict equations
`lambda_i=0`, or a new source-labelled packet-identification theorem plus
three subsequent darkness equations.  Symmetry alone proves none of them.

Run all modes:

```text
python3 computations/verify_h3_kappa_mix_eight_instance_symmetry_covariance_gate.py
python3 computations/verify_h3_kappa_mix_eight_instance_symmetry_covariance_gate.py --mode tags
python3 computations/verify_h3_kappa_mix_eight_instance_symmetry_covariance_gate.py --mode group
python3 computations/verify_h3_kappa_mix_eight_instance_symmetry_covariance_gate.py --mode chi
python3 computations/verify_h3_kappa_mix_eight_instance_symmetry_covariance_gate.py --mode lambda
python3 -O computations/verify_h3_kappa_mix_eight_instance_symmetry_covariance_gate.py
python3 -I -S computations/verify_h3_kappa_mix_eight_instance_symmetry_covariance_gate.py
```

Frozen ledger SHA-256:

```text
21624985da5bbebf865fffe091901ec8819455db5c3becd931059225e36ff91a
```
