# A physical central Eq cone removes Interface II as an independent lane

## Exact conditional theorem

The associated-graded Interface-II response symbol is complete: the
fixed-right Hessian supplies eight endpoint-tail terms and the physical
transpose supplies the other eight.  The minimal two-object grade groupoid
has

```text
d theta = 0,        theta^2 = 1,
LambdaT theta = Lambda,
```

with target, `W`, anchor, residue, eta, and sigma transported
equivariantly.  Consequently the complete augmented Interface-II defect
has only one remaining coordinate:

\[
                         E=(H_0-u)e_{\rm Eq}.           \tag{1}
\]

It follows immediately that a source-labelled central cell satisfying

\[
 dK_{\rm Eq}|_{II}=-E,                                 \tag{2}
\]

with zero (or protected-exact) Interface-II `q` and terminal rows closes
Interface II.  No additional occurrence, transpose, grade, or terminal
cell is required.

Checker:
[`verify_h3_interface_ii_central_eq_conditional_assembly.py`](../computations/verify_h3_interface_ii_central_eq_conditional_assembly.py).

This changes the proof frontier: Interface II is now a conditional
projection of the common reduced-Eq cone, not an independent construction
theorem.  The single remaining construction is the physical
`K_Eq(beta)` family already demanded by Interfaces I and III.

## 1. Exact failure alternative

Let `d:C_phys->Y_aug` be the complete physical boundary map in the relevant
projected grade, retaining every augmented row, and let `b_E` be the desired
boundary (2).  Exact linear algebra gives

\[
 b_E\in\operatorname{im}d
 \quad\hbox{or}\quad
 \exists\lambda:\ \lambda d=0,
                    \ \lambda(b_E)\ne0.                \tag{3}
\]

Thus failure is the augmented cokernel class `[E]_II`.  It is the
occurrence-sector projection of the same universal central class whose odd
and even projections are the remaining Eq debts in Interfaces I and III.
There is no extra class contributed by the `theta` loop.

“Same class” in this statement is functorial, not a false equality of
labelled covectors: the numerical detecting functional in each sector
lives in that sector's augmented terminal module.  The projectors need not
send all three duals to one literal row.  What is common is the universal
source generator and conormal direction.

## 2. What the derived-intersection route already constructs

The complete Boolean Hasse/Koszul totalization constructs a derived top
chain and cancels every proper product-rule face.  Its diagonal projection
to the underived physical source has the exact commutator (1).  Algebraically
this is the regular derived intersection with

\[
                       F_0=H_0-u,                      \tag{4}
\]

whose two-term Koszul/Tate resolution has a degree-one generator
`epsilon_F0` with `d epsilon_F0=F0`.

This formal generator does not yet solve the physical problem.  There is a
sharp augmentation fork:

- identifying it with the existing pure source row `r0` gives the correct
  Eq boundary but physical target `1`;
- assigning a new copy target `0` gives exactly the desired relative
  `K_Eq` cell and therefore cannot be inferred from the old resolution.

The source-base-change candidate makes this obstruction literal.  At an
active coefficient `kappa`, after all old normal, cap, and residue
corrections are included, its boundary is

\[
       \kappa F_0e_{\rm Eq}+\kappa Yw,                 \tag{5}
\]

with target and ordinary residue zero.  Killing `F0` by base change makes
the desired chain appear, but its connecting class is

\[
                       \kappa[F_0]\in J/J^2,           \tag{6}
\]

detected by the selected-`u` conormal functional.  This is tautological Tor,
not an underived physical source identity.

The complete absolute source/bar/Tate inventories do not fix (6).  Their
natural Tate kernels have zero physical augmentation, and the canonical
six-term covector survives the entire absolute resolution and first-flat
operator block.  Hence the positive derived route has now been reduced to
one exact promotion theorem:

> Promote the regular Tate generator for `F0` to one target-zero,
> source-labelled relative generator whose boundary is (1) and whose
> `q`, ordinary-residue, eta, and sigma projections have the common
> `K_Eq(beta)` typing.

That promotion is precisely the master reduced-Eq comparison; it is not a
new Interface-II-specific obligation.

## Scope

The theorem proves conditional Interface-II assembly, zero grade/q
holonomy, the exact augmented cokernel alternative, and the first
underived conormal obstruction to the derived/Tate route.  It does not
construct the target-zero physical Tate generator, nor assert that the
three sectorwise detecting covectors are literally identical.

Run:

```text
python3 computations/verify_h3_interface_ii_central_eq_conditional_assembly.py
python3 -O computations/verify_h3_interface_ii_central_eq_conditional_assembly.py
python3 -I -S computations/verify_h3_interface_ii_central_eq_conditional_assembly.py
```

Frozen ledger SHA-256:

```text
a5cd69b09039556ced4ddb35e952b8a6c0c76e580fca1a8d51e019d3b6ebc057
```
