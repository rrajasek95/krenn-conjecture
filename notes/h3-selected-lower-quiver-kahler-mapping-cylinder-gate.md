# The shifted Kähler arrow is a derived quiver cylinder with one physical Eq descent class

## Exact quiver construction

Treat the two ridge grades as objects (L_{pq}) and (L_{xv}), rather than
forcing them into one commutative multidegree. On the canonical clean-C5
chart

\[
t=q_{pq}^{00}\ne0,
\]

the regular grade arrow is

\[
U={u\over t}:L_{pq}\longrightarrow L_{xv},
\qquad u=q_{xv}^{00}.
\]

Its first-principal-parts prolongation is the mapping-cylinder matrix

\[
J_1(U)=
\begin{pmatrix}
U&0\\ dU&U
\end{pmatrix}.
\]

The (dU) entry is forced by the product rule:

\[
d(Uf)=U,df+f,dU.
\]

The order-six/Cartan operator is disjoint from all four ridge coordinates,
so the pinned identities give

\[
[\Theta_6,U]=[\Theta_6,dU]=0.
\]

Thus there is no additional horizontal--vertical Cartan diagonal. The
minimal bicomplex has four vertices and one nonvertex entry, (dU). This is
an exact positive construction in the derived principal-parts category.

Checker:
[`verify_h3_selected_lower_quiver_kahler_mapping_cylinder_gate.py`](../computations/verify_h3_selected_lower_quiver_kahler_mapping_cylinder_gate.py).

## Why the toric connection is not the global physical answer

On the smaller overlap (D(tu)), (U) is invertible and the flat connection

\[
\nabla=d-d\log U
\]

satisfies

\[
\nabla(Uf)=U,df.
\]

This removes the Leibniz diagonal, but it does not extend regularly across
(u=0). Its connection form has logarithmic residue

\[
\operatorname {Res}_{u=0}(-d\log U)=-1.
\]

The canonical clean-C5 theorem localizes only (t), not (u). Therefore a
flat identification of the two grade lines is available only on (D(tu)).
Čech descent across (u=0) retains the displayed nonzero residue class.

The terminal covectors show the same obstruction. Objectwise,

\[
-d\Omega_v=-d(a-t)+d(b-u)
\]

has the exact laws

\[
\iota_{\eta_z}(-d\Omega_v)=1+\delta_{vz}u/t,
\qquad
\iota_\sigma(-d\Omega_v)=-a.
\]

After collapsing the (pq) half into (L_{xv}) by (U), ordinary scalar
readout instead gives

\[
(1+\delta_{vz})u/t,
\qquad -(u/t)a.
\]

Recovering the old covectors uses the contragredient transition
(U^{-1}=t/u), again unavailable at (u=0). The correct derived object is
therefore the two-object mapping cylinder with objectwise eta/sigma, not a
single scalar line equipped with a globally flat toric connection.

## The exact underived obstruction

The complete shifted-denominator Hasse/Koszul totalization already realizes
the two-direction cylinder with target and ordinary residue zero. Its
projection to the underived physical source leaves exactly

\[
\boxed{e=(H_0-u)e_{\rm Eq}.}
\]

The initial unprojected commutator has 273 labelled monomials, while its
(q=0) top is the displayed monic class. Thus the known Cartan commutator
does not supply the missing diagonal: that commutator is zero. The new
physical square is precisely a comparison killing (e) while preserving
the derived chart, target, residue, and terminal data.

## One reduced-Eq orbit serves Gate I and Interface III

This same row is the reduced-Eq debt in the generic even interface. The sign
is exact. Let a core comparison cell satisfy

\[
dC=-e.
\]

It cancels the (+e) left by the Gate-I quiver cylinder. For Interface III,
decorate it by

\[
-2D\otimes v,
\quad
D=(-1,1,-1,1),
\quad
v=(B_1+B_4)/2.
\]

Then

\[
d((-2D\otimes v)C)
=+2D(H_0-u)e_{\rm Eq}\otimes v,
\]

which is exactly the independently pinned Interface-III correction.

The parity qualification is load-bearing. Gate I needs the (ho)-odd
projection and Interface III needs the (ho)-even projection. A single
line in one parity cannot imply the other. The smallest common source datum
is one regular orbit

\[
\mathbf Q\{C,\rho C\}
=\mathbf Q C_+\oplus\mathbf Q C_-,
\qquad C_\pm=C\pm\rho C.
\]

This is one equivariant generator orbit but two vector-space dimensions.
If target, residue, and anchor rows factor through the even quotient, they
vanish automatically on (C_-), as Gate I requires, and may remain nonzero
on (C_+), as Interface III requires.

This unifies the reduced-Eq source theorem, not the whole augmented packet.
The same orbit must still be given:

- Gate I's private boundary and eta/sigma placement;
- Interface III's (delta_+) full-nine tail;
- mixed target (-2D\otimes v), labelled residue (v), and the mandatory
  `W`/anchor/ridge/word faces.

Thus one source-valid regular (ho)-orbit is the sharp common theorem, but
constructing only its even or odd projection does not close both interfaces.

## Site permutation does not replace the arrow

A site permutation can carry the uncoloured edge (pq) to (xv), and every
site permutation fixes the symmetric GHZ target. That observation does not
give the physical ridge comparison.

The checker exhausts all (8!) site permutations:

- 1440 permutations carry (pq) to each chosen (xv) edge;
- only 120 also preserve the selected repeated profile
  ((1,1,1,2,1,1,1,2)), all for the special face (v=3);
- none of those commutes with the endpoint-sign swap.

There is a more immediate fine-label obstruction. A site permutation and a
single global colour permutation preserve equality of the two endpoint
colours. They may carry (q_{pq}^{00}) to (q_{xv}^{00}), but can never
carry

\[
q_{pq}^{22}\longmapsto q_{xv}^{0m_v},
\]

because (m_v\ne0). A local recolouring can make the colours distinct, but
then it moves a pure GHZ word to a mixed word and is only orbit-relative.
Moreover the site permutation does not commute with the endpoint-sign bar,
so the double bar has a new group-commutator diagonal. It also exchanges
external and internal C5 roles, and hence does not transport the selected
six-matching-minus-anchor row (q) canonically.

## Physical (q) and Interface II

For a physically descended cylinder (Phi), extension of

\[
q=\sum_6m_i-\mathrm{ainc}
\]

is exactly the quotient condition

\[
[q_{xv}\Phi-q_{pq}]=0
\quad\text{in}\quad D_{pq}^*/\operatorname {row}(J_{pq}).
\]

Vanishing constructs the augmented row homotopy. Nonvanishing gives a
protected-kernel witness; once both sides and both (q) rows are physical,
that witness is the relative-generator branch. The checker exhausts 668
small protected maps as a mutation guard for this alternative.

Interface II's class

\[
[F_{[2]}(\xi)]\in\operatorname {coker}(A)
\]

is a plausible occurrence projection of the same comparison, but this is
not proved. The pinned graph counterguard fixes the response graph,
Jacobian, tangent, and occurrence Hessian while allowing two different
output obstruction classes. A physically typed output-to-relative Spencer
map on this one class is still required.

## Shortest positive lemma

> Construct one source-valid regular (ho)-orbit of reduced-Eq
> mapping-cylinder cells with (dC=-(H_0-u)e_{\rm Eq}), preserving the
> derived (J_1(u/t)) square and objectwise eta/sigma. Its odd projection is
> the Gate-I descent cell; its even projection, decorated by
> (-2D\otimes v), is the Interface-III reduced-Eq repair. Then supply the
> remaining augmented decorations and prove the physical (q)-defect is a
> protected row.

This replaces two apparently unrelated Eq constructions by one equivariant
source theorem. It does not claim the required physical orbit already
exists.

## Verification

```text
python3 computations/verify_h3_selected_lower_quiver_kahler_mapping_cylinder_gate.py
python3 -O computations/verify_h3_selected_lower_quiver_kahler_mapping_cylinder_gate.py
python3 -I -S computations/verify_h3_selected_lower_quiver_kahler_mapping_cylinder_gate.py
```

Frozen ledger SHA-256:

```text
77682303f22772e43968fe70065620639689a0af0b5d33a1451c1a2c643a00ea
```
