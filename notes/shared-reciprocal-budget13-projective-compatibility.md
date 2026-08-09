# Flat compatibility kills every transverse budget-thirteen direction

## 1. Result

Retaining the actual projective directions of the transverse planes resolves
the first compatibility question cleanly.  For shared reciprocal arms
`pq,pr`, vanishing of their canonical transition has only two forms:

- independent shared-`p` factors force both restricted outer stars to zero;
- proportional shared-`p` factors force the two restricted stars to have one
  common five-site output.

The independent case is incompatible with every budget-thirteen chart,
because it would make both distinguished residual incident spaces zero.
In the proportional case, flatness forces

1. the two distinguished residual spaces to be distinct target lines; and
2. the two chart spaces to be literally equal at every one of the five
   common sites, including equality of any transverse \(\mathbb P^1\)
   parameter.

Applying these conditions to the 47,530 exact relative states from
[`shared-reciprocal-budget13-overlap-frontier.md`](shared-reciprocal-budget13-overlap-frontier.md)
leaves exactly three signatures:

\[
                         47,530\longrightarrow3.
\]

They lie in form pairs

\[
                         (0,0),\qquad(0,1),\qquad(5,5),
\]

and all three are coordinate.  **No transverse \(\mathbb P^1\) direction
survives flat compatibility.**

This is sharp at the structural level.  The first coordinate signature has
an exact rational aggregate packet with two flat doubly-good rank-one arms,
a rank-two opposite chord, full endpoint spans at all eight sites, and no
literal cubic site.  It is not an exact GHZ source.  Thus projective
compatibility closes the transverse gate but does not by itself eliminate
the three coordinate flat signatures.

In particular, the `(0,6)` control packet from the preceding overlap note
has full distinguished spaces on both sides and proportional shared factors.
It cannot be flat.  Both outer deleted stars are already full, and equality
of the shared factors makes both `p` deletions full as well, so this control
does force a curved transition on two doubly-good rank-one arms.

## 2. The flat-star lemma

Factor the two direct blocks in endpoint order as

\[
 A_{pq}=x_q\otimes y_q,\qquad A_{pr}=x_r\otimes y_r.
\]

Let `C` be the five-site common complement and let

\[
 T_q=S_q|_C,\qquad T_r=S_r|_C
\]

be the restricted endpoint stars.  Vanishing of every canonical transition
is the tensor identity

\[
 a(x_q)y_q(\beta)T_r(\gamma)
 =a(x_r)y_r(\gamma)T_q(\beta)                 \tag{1}
\]

for all covectors \(a,\beta,\gamma\).

If \(x_q,x_r\) are independent, choose \(a\) to kill either one in turn.
Equation (1) gives

\[
                              T_q=T_r=0.        \tag{2}
\]

In the `pr` deletion chart, the exceptional space at `q` is spanned exactly
by the `q-C` blocks, hence by \(T_q\); the analogous statement holds at `r`
in the `pq` chart.  Equation (2) would make both spaces zero, contradicting
the site-cover part of the full-nine theorem.

Suppose instead that \(x_q,x_r\) are proportional and normalize them to the
same vector.  Choose \(\beta_0,\gamma_0\) with
\(y_q(\beta_0)=y_r(\gamma_0)=1\).  Equation (1) gives one common output
\(z\in\bigoplus_{u\in C}V_u\) such that

\[
                  T_q(\beta)=y_q(\beta)z,
       \qquad T_r(\gamma)=y_r(\gamma)z.          \tag{3}
\]

Consequently the two exceptional incident spaces are the lines
\(\langle y_q\rangle,\langle y_r\rangle\).  Their target colours are the
two outgoing witness colours and are distinct.

At a common site \(u\), let \(U_u\) be the span supplied by common `C-C`
blocks.  Taking the `u` component of (3) yields

\[
 W_u^{pq}=U_u+\langle z_u\rangle
          =W_u^{pr}.                              \tag{4}
\]

This is the projective compatibility equation.  If the common record is a
marked plane

\[
 W=\langle e_k,e_i+\lambda e_j\rangle,qquad
 \lambda\in\mathbb C^*,
\]

then (4) requires the same target line \(e_k\) and the same parameter
\(\lambda\) in both charts.  Distinct incidence masks cannot conceal an
equal plane: their contained target-axis sets would differ.

## 3. Exact finite filtration

Among the 47,530 relative states, the exceptional-dimension histogram is

```text
(3,3): 4827   (3,2): 15090   (3,1): 4887
(2,2):12804   (2,1):  6854   (1,2): 1501
(1,1): 1567
```

The proportional-flat conditions filter the last row as follows:

```text
both exceptional spaces are lines                  1567
their target colours are distinct                  1020
all five common projective spaces are equal           3
survivors carrying a transverse P^1 parameter          0
```

The three surviving common-record multisets, with exceptional lines
`e2,e1`, are

```text
(0,0): 000,000,000,001,110
(0,1): 000,000,000,010,101
(5,5): 000,000,001,010,100
```

Every displayed common record occurs identically in the two charts.

## 4. Sharp rational flat counterguard

Use sites `p,q,r,3,4,5,6,7`.  Put

\[
 A_{pq}=e_0e_1^{\mathsf T},\qquad
 A_{pr}=e_0e_2^{\mathsf T},
\]

so the shared factors are proportional and the outgoing colours are
distinct.  Let

\[
 A_{qr}=e_0e_0^{\mathsf T}+e_2e_1^{\mathsf T},              \tag{5}
\]

which has rank two and supplies the complements of the outer lines
\(e_1\) at `q` and \(e_2\) at `r`.

On the common set, take

\[
 A_{34}=I,quad A_{35}=I,quad
 A_{36}=e_0e_1^{\mathsf T}+e_1e_2^{\mathsf T},quad
 A_{37}=e_2e_0^{\mathsf T}.                                \tag{6}
\]

The two restricted outer stars are

\[
 A_{q7}=e_1e_0^{\mathsf T},qquad
 A_{r7}=e_2e_0^{\mathsf T}.                                \tag{7}
\]

Thus they share the same common output at site `7`, and (3) holds exactly.
Four additional `p-C` blocks fill the original endpoint spans but disappear
from both internal deletion charts.  The checker verifies directly that

- the two six-site chart records are the first surviving `(0,0)` signature;
- every original endpoint star has rank three;
- both direct arms have goodness ranks `(3,3,3,3)`;
- the chord (5) has rank two;
- every canonical transition between the arms is zero; and
- no site is incident with exactly three rank-one blocks.

This counterguard is a rational structural realization of the remaining
flat signature.  It deliberately does not satisfy the full 6,561 coefficient
equations.

## 5. Reproduction and proof consequence

Run

```bash
python3 computations/verify_shared_reciprocal_budget13_projective_compatibility.py
python3 -O computations/verify_shared_reciprocal_budget13_projective_compatibility.py
```

Both modes reproduce ledger

```text
d14b6ad138fd5e423a7474a40b8c278bbfec64b40deaf77888a15cea73b581d7
```

The checker is solver-free.  It pins the complete relative-state census,
filters it by the exact flat-star equations, and audits the counterguard by
rational row reduction.

The projective branch is therefore finished at the incidence level:

\[
 \boxed{\text{transverse state}\Longrightarrow\text{nonflat transition}}
 \quad\text{and}\quad
 \boxed{\text{flat state}\Longrightarrow
        \text{one of three coordinate signatures}.}
\]

To finish the shared-reciprocal proof one must now use source exactness only
on those three coordinate flat signatures, while routing nonflat transitions
through the existing curved-overlap machinery whenever the corresponding
deleted stars are good.  The rational counterguard prevents replacing this
last coefficient step by another rank/incidence argument.
