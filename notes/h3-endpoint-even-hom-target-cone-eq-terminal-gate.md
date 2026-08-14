# The target cone kills the target `H1`; only the Eq class survives

The endpoint-even reduction turns the cap comparison into a small relative
Hom calculation.  Its outcome is sharper than treating all three protected
directions as terminal covectors:

```text
omega_Eq                         genuine obstruction/terminal candidate,
N23, N45                         required target proper faces.
```

Conditionally adjoining the canonical sigma-covariant target cone kills the
entire rank-two target block.  The sole remaining class is
`omega_Eq=delta.(B-Eq)`.  It is already an exhaustive *local* augmented
terminal, but not yet an accepted global physical Fredholm terminal.

The exact checker is

```text
computations/verify_h3_endpoint_even_hom_target_cone_eq_terminal_gate.py
```

with frozen ledger

```text
0e171d7cb8523627d4a86eec86316aa720897dfb149b1ae5ccd017ad931837e1
```

## 1. The literal Hom corner is absent

For each response parent, the six trigger branches and their higher faces
form the augmented simplex resolution

```text
dimensions C0,...,C5 = 6,15,20,15,6,1,
boundary ranks        = 5,10,10,5,1.
```

The present operation category nevertheless has

```text
e_C A e_R = 0,
Hom_A^0(response,cap) = 0,
primitive Hom_A^1(response,cap) = 0.
```

This is a typing statement: the simplex is a free response resolution, but
none of its generators changes the response idempotent to the cap
idempotent.

The endpoint-even Reynolds section fixes a coefficient comparison, so its
failure to be an `A`-map is naturally an *inhomogeneous* obstruction.  Let

```text
O = Q{omega_Eq,N23,N45}.
```

The smallest shifted relative Hom complex of corrections is

```text
K0 = e_C A e_R = 0,
K1 = O tensor C^0(Delta^5),
K2 = O tensor C^1(Delta^5),
K3 = O tensor C^2(Delta^5).
```

Exact ranks are

```text
dim K1,K2,K3 = 18,45,60,
rank d1,d2   = 15,30.
```

The three natural defects are constant on the six full-star branches.
They span the complete kernel of `d1`.  Since `K0=0`, while the ordinary
simplex `H1` vanishes,

```text
H0(K) = 0,
H1(K) = Q{omega_Eq,N23,N45},
H2(K) = 0.
```

Before root covariance the two root copies have `H1` dimension six.  The
root-natural diagonal has dimension three.  Thus no higher full-star
simplex face can repair the defect: it is precisely a constant,
operation-changing obstruction.

This shifted `H1` is not in conflict with the literal `Hom_A^1=0`.  The
latter says the current category contains no cross operation; the former is
the obstruction space after the endpoint-even coefficient section is fixed.

## 2. The target normals are faces, not vanishing equations

The two lower cuts have target normals with exact pairing

```text
                    N23  N45
X_00211122^*          2    0
X_00111222^*          0    2.
```

Their sum is sigma-even and nonzero.  A physical cap action is supposed to
export these normals into an augmented target cone; it is not supposed to
make the normals vanish.

On the constant obstruction module the canonical target-cone incidence is

```text
d T23 = N23,
d T45 = N45.
```

It has rank two, and sigma exchanges the two objectwise columns.  Adjoining
this orbit gives

```text
target H1:          2 -> 0,
total relative H1: 3 -> 1,
relative H0:       0 -> 0.
```

The surviving basis is exactly `omega_Eq`.  The unchanged `H0` means the
cone creates no new homogeneous comparison ambiguity.

This is a conditional adjoining, not a claim that the physical cone already
exists.  The target vectors and their covariance are canonical, but the
occurrence-local source section and its one-endpoint Hasse faces remain part
of the desired `A`-action.

## 3. The surviving Eq class extends across current external rows

The exhaustive local `U_C4` map has

```text
output dimension = 127,
rank             = 126,
cokernel         = 1.
```

It includes all literal PP/reinsertion flags and the entire current external
space:

```text
target, q, anchor, W, ordinary residue, ridge, eta, sigma.
```

Its unique normalized left-kernel generator is

```text
Psi_loc = delta.(B-Eq)/12,
```

transported through the direction and tail flags.  Its coefficients on

```text
q, anchor, W, ores, ridge, eta, sigma
```

are all zero.  Hence `omega_Eq` extends over the *entire current local
augmented codomain*, not merely the coefficient block.  The target normals
do not extend as annihilating terminal covectors after the target cone is
adjoined: they pair nontrivially with `T23,T45` and are thereby killed as
`H1` classes.  This is the required face/obstruction distinction.

## 4. Why this is not yet the accepted Fredholm terminal

Fredholm promotion requires one fixed exhaustive physical map, a literal
RHS in the same codomain, a normalized covector annihilating that map, and
all protected rows retained.  The local map meets the last two conditions.
The global source condition is still open:

```text
C1_phys,Gamma*/(canonical + chi-dark generators)
```

has not been proved to be exhausted by the known relative cells.  A new
same-word/fine/repeated cross-profile column can have nonzero
`delta.(B-Eq)` while remaining invisible to the canonical source grammar.
Neither `q=M-anchor` nor the anchor row detects this missing class.

Therefore the present status is

```text
omega_Eq on exhaustive local map       accepted local terminal,
omega_Eq on exhaustive physical map    not yet proved,
global Fredholm terminal                open.
```

## 5. The exact first filling column

After the target cone is granted, the first and only protected class is
`omega_Eq`.  A filler must therefore be one endpoint-even, two-root
DQ-to-PS/AugP2 relative-C4 column with

```text
delta.(B-Eq) != 0.
```

Its proper target faces must be the sigma-paired `T23,T45` cone orbit.  In
the relative Hom complex, adjoining this Eq column changes

```text
Eq H1:    1 -> 0,
total H1: 1 -> 0,
H0:       0 -> 0.
```

There are then exactly two branches:

1. construct this column and totalize its target/Hasse faces, producing the
   cap comparison; or
2. prove that no such bright column occurs in the exhaustive physical
   same-grade domain, promoting `omega_Eq` to the accepted Fredholm
   terminal.

No endpoint-odd selector and no additional target cone is required.

## Scope

The calculation is exact over `Q` for the full-star simplex resolution, the
root-covariant three-defect quotient, the two canonical lower target
normals, and the complete local augmented `U_C4` map.  It tests the target
cone and Eq column as possible adjoinings; it does not assert either is
already a source-provenant operation in the current `A`-category.
