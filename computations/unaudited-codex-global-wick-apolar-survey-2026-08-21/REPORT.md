# Global Wick/apolar/Artinian survey at `n=8`

Status: **exact bounded negative survey PASS**.  The Artinian encoding is
source-faithful, but its first natural differential, catalecticant, Hessian,
Lefschetz, and Jordan tests do not obstruct ternary GHZ and do not detect a
clean cap.  The surviving problem is a relative identity for the labelled
pair `(q,q^4)`, not an intrinsic invariant of `q^4`.

## 1. Literal squarefree matching algebra

Put

```text
B_i = C + V_i,       V_i^2=0,       dim(V_i)=3,
B   = tensor_(i=0)^7 B_i,
q   = sum_(i<j,a,b) A_ij[a,b] x_(i,a)x_(j,b) in B_2.
```

Then products of incident edge terms vanish and every perfect matching is
counted in all `4!` orders, so

```text
q^4/4! = H_8(A) in B_8.
```

The exact Hilbert census of `B` is

```text
[1,24,252,1512,5670,13608,20412,17496,6561].
```

The even moment tower has sector dimensions

```text
[1,252,5670,20412,6561], total 32896.
```

Thus `q^4=24 Delta_(8,3)` is exactly the original `6561`-row source
equation.  Writing `log(exp(q))=q` repackages those rows: cumulants in degrees
four and six vanish identically for every `q`, while the degree-eight
cumulant equation is just the original fourth-power equation once the lower
moments are restored.  It gives no smaller new relation.

Under `prod_i GL(V_i)`, the source is `direct_sum_(i<j) V_i tensor V_j`, of
dimension `252`, the target is the irreducible module `tensor_i V_i`, of
dimension `6561`, and the map has degree four.  Hence there is no nonzero
equivariant linear output equation.  Every word coordinate has site-colour
weight `product_i lambda_(i,w_i)` and contains `105` generic matching
monomials.

## 2. Smallest apolar candidate: exact but not a fibre equation

For a fixed colour word, its scalar coordinate is the weighted size-four
matching polynomial `Phi_(8,4)` in the `28` compatible edge variables.  Its
degree-two apolar relations are exactly organized by

```text
28 edge squares
+ 168 products of two incident edges
+ 140 differences d_M-d_M' between two 2-matchings on the same four sites
= 336 relations.
```

Since `dim Sym^2(C^28)=406`, the quotient has dimension `70=C(8,4)`.
The complete apolar Hilbert vector is

```text
[1,28,70,28,1].
```

This agrees with Numata's strong-Lefschetz theorem for matching generating
polynomials (Y. Numata, *The Lefschetz property for an algebra defined by
matchings*, arXiv:2302.11039, Theorem 3.1 and Lemma 3.2).

The smallest candidate outside the failed degree-one tail contraction is
therefore

```text
(d_M-d_M') Phi_(8,4)=0,        supp(M)=supp(M'), |M|=|M'|=2.
```

It is not an equation in the output coordinates.  It differentiates the
universal polynomial `H_w(A)` in source variables.  From the pointwise fibre
equation `H_w(A_0)=delta_w` one may not infer a differentiated equation at
`A_0`.  Formally differentiating the constant right side would erase exactly
the lower four-site Hafnian that the source derivative retains.

There is also no scalar value/Hessian shortcut.  The checker constructs two
exact rational `K_8` weight systems:

| prescribed `Phi_(8,4)` | solved `x_01` | ordinary Hessian rank |
|---:|---:|---:|
| `0` | `-62875/1852` | `28/28` |
| `1` | `-125749/3704` | `28/28` |

Thus the target values zero and one do not individually force even the first
matching Hessian to drop rank.

## 3. Intrinsic target apolar algebra passes maximally

The apolar algebra of

```text
Delta_(8,3)=sum_(c=0)^2 product_i x_(i,c)
```

has Hilbert vector

```text
[1,24,84,168,210,168,84,24,1].
```

For

```text
Theta=sum_(c,i<j) z_(ij,c)=L^2/2,
```

the maps `Theta^(4-k):G_k -> G_(8-k)` have exact ranks

```text
[1,24,84,168,210],       k=0,1,2,3,4.
```

They are the largest possible.  Also

```text
Theta^4 = 7560 omega,
det Hess(Delta_(8,3))(1,...,1) = -343.
```

Hence Hilbert functions, multiplication ranks, Jordan type, ordinary
Hessians, and higher Hessians of the target's intrinsic apolar quotient all
pass in the strongest direction.  This independently confirms the frozen
`zeon-lefschetz-apolar-obstruction` counterguard.  Numata's theorem concerns
the apolar algebra of the generic scalar matching polynomial; it does not
turn these target-intrinsic maps into constraints on a common root of the
`6561` coloured equations.

## 4. Source multiplication does not see cap activity at first order

The first honest lower multiplication map is

```text
mu_q : B_1 (dimension 24) -> B_3 (dimension 1512).
```

Exact rational/source-symbolic evaluation gives:

| source | cap status / scope | rank |
|---|---|---:|
| frozen `W40` | active star cap, X4 not X5 | `24` |
| deterministic dense positive source | all 728 carriers blocked | `24` |
| explicit remote counterpoint | D611-open, fails 138/360 332 rows | `24` |

For the remote point over `Q(lambda)/(105 lambda^4-1)`, the checker selects
one literal singleton-output row for every input port.  The resulting
`24 by 24` minor is diagonal with determinant

```text
lambda^24 != 0.
```

Thus maximal first lower multiplication rank occurs on an active-cap
control, an all-blocked control, and the remote tail counterpoint.  It cannot
unconditionally force a clean cap.  These controls do not prove that no
higher relative rank identity exists *after* imposing full X5; they show
that such an identity must use the X5 fibre equations and labelled carrier
incidence, rather than the global rank alone.

The support-six artifact is a reduced diagonal/Q coefficient family, and the
support-eight artifact records only a Q-support orbit.  They do not freeze a
full `252`-coordinate `q` for numerical multiplication ranks.  The universal
matching apolar identities nevertheless hold termwise on every completion,
so neither support class is separated by them.

## 5. Top-output equations are ruled out by the existing boundary

The checker independently reconstructs the eight-site Laurent output

```text
00000000 : 1
11111111 : 1
22222222 : 1
12012000 : t
21000012 : t
```

from the first vertex-to-triangle expansion of the prism.  Hence its output
tends to `Delta_(8,3)` while the frozen construction keeps the full covariance
nonsingular.  It follows that every polynomial equation of the top Wick
image, and every rational equation regular at the target, also holds at the
target.  This rules out top-only flattening, catalecticant, cumulant, and
Wick-variety separators, regardless of degree.

## 6. Ranked verdict

1. **Top-only polynomial/differential elimination:** impossible by Laurent
   closure.
2. **Intrinsic target apolar/Jordan/Hessian tests:** false lead; the target
   is maximally strong Lefschetz.
3. **Numata scalar matching apolarity:** useful organization only; scalar
   values zero and one both coexist with full Hessian rank.
4. **Global first lower multiplication rank:** false lead; cap-active,
   all-blocked, and remote controls all have rank `24`.
5. **Only surviving apolar formulation:** a relative, source-labelled
   identity for `(q,q^2,q^3,q^4)` coupled to a particular carrier response
   block and the full X5 equations.  No such identity is supplied by current
   matching-apolar/Lefschetz theory.

## Replay

```sh
python3 computations/unaudited-codex-global-wick-apolar-survey-2026-08-21/audit_global_wick_apolar_survey.py --write-results
python3 -O computations/unaudited-codex-global-wick-apolar-survey-2026-08-21/audit_global_wick_apolar_survey.py
python3 -I -S computations/unaudited-codex-global-wick-apolar-survey-2026-08-21/audit_global_wick_apolar_survey.py
```

All modes print logical SHA-256

```text
03c6dbb14bab684b9426130cdb7af3a83cdabf4ba714b78091701480712d7fd1
```
