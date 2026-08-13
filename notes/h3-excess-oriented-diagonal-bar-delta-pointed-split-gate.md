# The oriented excess bar leaves one pure-column comparison class

## Result

The relative oriented-diagonal bar contracts the excess loop-label kernel
abstractly, but it does not yet produce the physical tau-plus repair.

There are five source loop labels

```text
02, 03, 05, 23, 25
```

mapping to the single target excess direction `2e4`.  Their augmentation
kernel has rank four.  Four normalized tree bars form an integral basis of
that kernel, while the selected rho-even `delta_plus` direction needs only
one aggregate bar combination.

The physical obstruction occurs because this bar lands in the bare
`Q_tail` row.  The desired repair is a complete pure full-nine boundary.
The smallest new selected cell is

```text
J_D : (pure, Eq, Q_tail) = (D, 0, -D),
D = (-1,2,-1,-1,2,-1),
```

in the actual tau-plus word/fine/repeated grade, with target, anchor, `W`,
ordinary residue, wrong-word, and ridge zero.  Adding the already physical
endpoint-bar packet `(0,0,D)` then gives `(D,0,0)`, the integral pure bridge.

Checker:
[`verify_h3_excess_oriented_diagonal_bar_delta_pointed_split_gate.py`](../computations/verify_h3_excess_oriented_diagonal_bar_delta_pointed_split_gate.py).

## 1. What the abstract bar really constructs

Let `e_l` denote the five source-loop vertices.  Since every vertex maps to
the same target normal, the target map is the augmentation

```text
epsilon(e_l)=1.
```

Choose `25` as base vertex.  The four boundaries

```text
e_02-e_25, e_03-e_25, e_05-e_25, e_23-e_25
```

are an integral basis of `ker(epsilon)`.  Thus there is no remaining
abstract group-homology obstruction to transporting among loop labels.

For the selected even direction, the shared-`02` resolutions give

```text
v=(B1+B4)/2,
```

while the actual tau-plus local resolutions give

```text
w_local=(B0+B2+B3+B5)/4.
```

Their difference is

```text
delta_plus = v-w_local
           = (-B0+2B1-B2-B3+2B4-B5)/4.
```

It is rho-even and augmentation zero.  Hence one aggregate oriented bar is
enough for this selected line, even though a uniform contraction of all
five source labels uses four edges.

## 2. Why the physical bar is still missing

The integral vector

```text
D=4 delta_plus=(-1,2,-1,-1,2,-1)
```

has the exact endpoint factorization

```text
D=(B1-B0)+(B1-B2)+(B4-B3)+(B4-B5).
```

Each difference is a source-valid endpoint-bar difference on a common
face.  Omega, ordinary residue, target, anchor incidence, and `W` cancel
inside each pair.  What survives is a bare three-edge `Q_tail` difference.

By contrast, a pure `B_i` is a complete 90-term full-nine column.  The
integral `D` combination has 540 literal seven-edge features.  In rows

```text
(private_B_6, Eq_6, Q_tail_6),
```

the known complete and `M_v` packets have type `(x,x,0)`, while endpoint
bars have type `(0,0,q)`.  The desired pure bridge is `(D,0,0)`.

The rho-even primitive covector

```text
chi_D = sum_i D_i (private_i-Eq_i)
```

kills the complete/Mv and endpoint-bar image but reads

```text
chi_D(D,0,0)=12.
```

Therefore the oriented bar has not killed the physical class.  The minimal
comparison cell is exactly

```text
J_D=(D,0,-D),
J_D+(0,0,D)=(D,0,0).
```

Equivalently, one may combine the zero-total `M_v` packet `(D,D,0)` with a
new Eq-only correction `(0,-D,0)`.  These are the same one-dimensional
mapping-cone extension.

## 3. Word, ridge, and W

The endpoint differences prove local Omega and `W` cancellation.  They do
not prove that a bar crossing from the shared-`02` object to an actual
tau-plus `01/04` or `12/24` object has no proper faces.  The current formal
carrier retains residual word `012112`, endpoint-ridge mismatch rank six,
and primitive-Omega rank five.

Thus `J_D` is shorthand for one nondegenerate relative common-tail cell
together with its forced source-labelled word-change and ridge/Omega caps.
Its required final signature is

```text
pure lower = D, Eq = 0, Q_tail = -D,
target = ainc = W = ores = ridge = wrong-word = 0.
```

No old-inventory combination has this signature.  The covector `chi_D` is
the first literal obstruction; the word/ridge packet is the next proper-face
obligation after adjoining the class.

## 4. It does not simultaneously supply the pointed diagonal

The selected delta bar has coefficient sum zero.  Accordingly it has
occurrence augmentation and protected anchor zero.  The pointed comparison
instead requires the degree-zero source relation

```text
d(u_f-u)=0,
```

which reads one on the marked tangent isolated in the anchor audit.  These
two quotient directions are independent.

They also occupy different filtered degrees:

- the pointed diagonal is a relation of source functions, with its Koszul
  graph generator;
- `J_D` is the next oriented common-tail bar comparing two excess labels.

One homogeneous source cell cannot supply both while retaining the required
zero anchor on `J_D`.  One **pointed comparison morphism** can package them,
but its minimal source extension has two homogeneous generators:

```text
P_f : the marked/global diagonal u_f-u,
J_D : the oriented pure/Q_tail comparison for delta_plus.
```

The word/ridge caps belong to the `J_D` totalization and do not replace
`P_f`.

## Exact frontier

The excess-label problem is no longer a rank-four search.  On the selected
even line it is one primitive extension:

> Construct `J_D` in the literal tau-plus word/fine/repeated grade, with its
> word/ridge caps and protected rows zero.

Together with the independent pointed generator `P_f`, this supplies the
first two homogeneous pieces of the sought `Phi_beta`.  The remaining
integral requirement is to extend this totalization over beta so that its
special Bockstein is the physical `V` face.

Run:

```text
python3 computations/verify_h3_excess_oriented_diagonal_bar_delta_pointed_split_gate.py
python3 -O computations/verify_h3_excess_oriented_diagonal_bar_delta_pointed_split_gate.py
python3 -I -S computations/verify_h3_excess_oriented_diagonal_bar_delta_pointed_split_gate.py
```

The checker prints its frozen ledger SHA-256.

```text
a47be3990418d2b7a4f0082ef4ede2bb7e21a343e990b5f0aec497560b05dc69
```
