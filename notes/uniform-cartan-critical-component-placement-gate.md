# Every marked offdiagonal occurrence admits a nonzero Cartan placement

## Outcome

The ambient source-provenance problem is closed by the
[uniform physical Cartan prism](uniform-physical-cartan-source-prism.md).
The remaining root/transposition choice can also be made uniformly.

Let `mu` be a literal perfect-matching occurrence in a critical same-word
block, and suppose its edge `{x,y}` is decorated by two distinct colours
`a,b`.  At every even order at least six:

1. take the signed Weyl root plane to be `span(a,b)` at `x,y`;
2. choose `p,q`, disjoint from `x,y`, on two distinct complementary edges of
   `mu`; and
3. put `s=(p q)` and `G=(1-s)H_w`.

Then the four principal-boundary occurrences of `G` are pairwise distinct.
In particular the original occurrence `(mu,z)` has coefficient `-1`, so the
projection of `G` to any critical block containing it is nonzero in its
**exact word, tail, orientation, and fine-grade label**.

Thus the component-incidence part of the uniform Cartan attachment theorem
is constructive.  The first remaining physical datum is augmented
residue/ridge typing in a noncanonical component grade; after that, the only
remaining branch is promotion of a dark complete-lift residual to a typed
exit or an anchor-safe kernel move.

Checker:
[`verify_uniform_cartan_critical_component_placement_gate.py`](../computations/verify_uniform_cartan_critical_component_placement_gate.py).

## 1. The placement cannot cancel

Write `z` for the source word and use the operator convention

\[
                     dG=(1-s)(w-1).                  \tag{1}
\]

At the selected matching occurrence, (1) has the four labelled corners

\[
 (\mu,wz),\quad (\mu,z),\quad
 (s\mu,swz),\quad (s\mu,sz).                         \tag{2}

The Weyl action changes the two root colours `(a,b)` to `(b,a)` (with its
standard sign), so `wz` differs from `z`.  Because `p,q` lie on distinct
matching edges, `s mu` differs from `mu`.  These two independent facts make
all four labels in (2) distinct, regardless of whether `z_p=z_q`.
Consequently every coefficient has absolute value one and

\[
                         [\mu,z],dG=-1.               \tag{3}

No holonomy or component-shape enumeration enters this proof.

The checker audits the constructive rule for every matching, every marked
edge, and every ordered offdiagonal colour plane at orders six and eight.
Those finite audits freeze conventions; the two-line distinctness proof is
uniform.

## 2. The direct-free choice is also uniform

Suppose one physical edge `f` is removed and `mu` does not use it.  The
transposition must preserve `f` setwise.

* If `f` is disjoint from `{x,y}`, its two endpoints lie on distinct
  `mu`-edges, since `f` itself is not a matching edge.  Choose `(p,q)=f`.
* If `f` meets `{x,y}` once, let `r` be its outside endpoint.  Choose `p` to
  be the `mu`-mate of `r`, and choose `q` on another complementary
  `mu`-edge.  Then `p,q` avoid `f` pointwise.

In both cases `s` fixes the removed edge and crosses two matching edges, so
the four-corner argument survives in the direct-free chart.  At order six
there are already two complementary edges, which is exactly the threshold
needed.

## 3. Why projection is legitimate here

The physical source chain is the **complete** ambient prism `G`.  It is not
replaced by a partial matching sum.  Only its response vector

\[
                         g=\pi_M G                    \tag{4}

enters the Schur block of the critical component.  Equation (3) proves
`g!=0`.  This avoids an unnecessary and generally false demand that the
coordinate projection of a complete source row itself be a source
generator.

All target and protected-readout statements therefore remain statements
about `G`, not about a truncated chain.  The uniform source theorem gives
target zero.  In the canonical `h=3` repeated grade, `G` also inherits the
already proved residue `(-1,1,1,-1)`, zero protected readouts, and eta/sigma
ridge.  For an arbitrary component grade, placement preserves any such
augmented typing but does not create it: a physical comparison map from that
grade to residue and ridge rows is an explicit minimal hypothesis.

## 4. Saturation gives the exact exit alternative

Define `pi_M` using **all** source word, matching-tail, endpoint-orientation,
and fine-grade labels already belonging to the current component.  Then it
is fine-label saturated.  Every corner of (2) has a literal label, so each
one is unambiguously either

* retained by `pi_M`, hence part of the component connector; or
* outside the saturated label set, hence a literal word-changing or
  transposition exchange exit.

If a projection omits a label which still belongs to the component, a
nonzero complement is not an exit; it is only an unsaturated internal row.
This is exactly the counterguard already frozen by the dark-potential
promotion theorem.  Saturation, rather than a larger support census, is the
load-bearing hypothesis.

## 5. What remains on the dark branch

Let `ell` span the left cokernel of a minimal zero-holonomy block `M`.
With (4), the Schur alternative is now available for the constructed `G`:

\[
 \ell^Tg\ne0 \quad\Longrightarrow\quad
                 \text{Schur/Fitting unit}.           \tag{5}
\]

If `ell^Tg=0`, solve `My=g`.  For complete lifts `C,G`, form

\[
                           R=G-Cy.                    \tag{6}

Then `pi_M R=0`.  A nonzero `R` is a typed exit once every complementary
coordinate is proved to be a literal adjacency/exchange label.  If `R=0`,
one still needs the kernel `(-y,1)` to consist of occupied scalar cells in
one endpoint row, or another independently anchor-safe move.

The smallest type-split countermodel shows that `R=0` need imply neither an
exit nor a deletable same-row kernel.  Therefore (6), not the placement of
roots or `s`, is the first exact remaining obstruction after augmented
grade typing.

## Minimal hypotheses and shifted frontier

The positive placement theorem uses only:

1. even order at least six;
2. a marked matching occurrence with distinct endpoint colours;
3. the complete presentation, or a single removed edge preserved as above;
4. a component projection retaining its exact fine label; and
5. for full physical readouts, an augmented residue/ridge comparison in the
   chosen component grade.

Items 1--4 construct a source-provenant target-zero `G` with `g!=0`.  Item 5
upgrades it to the canonical fully typed packet.  The root/transposition
selection problem is therefore retired.  The live frontier is:

```text
augmented grade typing
        |
        v
ell^T g != 0 --------------------> Schur unit
        |
        `-- ell^T g = 0 --> R=G-Cy
                                  |
                     +------------+-------------+
                     |                          |
               typed R != 0          occupied/anchor-safe R=0
                     |                          |
                 typed exit               support move
```

## Verification

```text
python3 computations/verify_uniform_cartan_critical_component_placement_gate.py
python3 -O computations/verify_uniform_cartan_critical_component_placement_gate.py
python3 -I -S computations/verify_uniform_cartan_critical_component_placement_gate.py
```

Frozen ledger SHA-256:

```text
0fd0ad4578c04ad3a6c68e96c47136efda46ca72ffa6aecaa71e06d1400cfffd
```
