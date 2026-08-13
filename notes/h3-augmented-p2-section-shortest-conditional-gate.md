# The shortest generic theorem is one augmented `P2` section—with distinct faces

## Verdict

With the physical `W` row now supplied by the old `Yw -> W` cap law, the
generic `C_plus` frontier can be stated as one theorem schema:

> Construct a sigma-covariant pointed source-presentation/principal-parts
> section, natural in the marked `P2` occurrence, its two root directions,
> and spectator reinsertion.  Require its reduced-cap/Koszul faces to be the
> primitive `p` and physical `K_Eq` descent with the literal `B4/B1` label
> map, and require its relative Kähler face to be `gamma_v=-dOmega_v` in the
> shifted repeated grade.

This is one augmented comparison theorem, but it is not one bare source
column.  It is one natural schema with eight literal fixed-grade occurrence
instantiations.  The pointed conormal, primitive cap, reduced-Eq descent,
and shifted ridge are distinct homogeneous faces.  The theorem is shorter
because its functoriality makes `dq`, `d_even`, `W`, physical `q`, anchor,
and eta/sigma consequences—not because those independent face types become
equal.

Checker:
[`verify_h3_augmented_p2_section_shortest_conditional_gate.py`](../computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py).

## 1. Pointed occurrence does not imply the primitive cap

The pointed occurrence generator and primitive cap have different literal
types:

\[
 P_f:\ dP_f=u_f-u,
 \qquad
 p:\ (Q,\operatorname{ores})=(-1,-1).
\]

In the quotient with rows

```text
(pointed conormal, cap Q, scalar ores)
```

they are

\[
                       P_f=(1,0,0),
 \qquad                 p=(0,-1,-1).                 \tag{1}
\]

They have rank two.  The marked-tangent covector detects `P_f` and kills
`p`; scalar ordinary residue detects `p` and kills `P_f`.  Thus a pointed
source-algebra comparison gives the anchor/conormal law by differentiating
`u_f-u`, but it does **not** automatically construct the primitive cap in
word `01211222`, fine/repeated grade `t q_(v,N)` / `P3+K2`.

Calling the desired object a “pointed occurrence/cap section” is legitimate
only if the cap face `p` is included explicitly in the theorem.  It is a
second face, not a consequence of the word “pointed.”

## 2. The `dq` conormal is automatic at exactly one strength

For a literal reinsertion `q`, the first-principal-parts law is

\[
                  J^1(qS)=qJ^1(S)+dq\otimes S.        \tag{2}
\]

If `S` is pointed, its base coefficient is one, so the coefficient of the
labelled `dq` face in (2) is forced to be one.  Therefore no independent
`dq` generator is needed once the occurrence section is a module/algebra
map for reinsertion.

A degree-zero section alone does not imply (2).  Its zero-jet stays fixed if
the `dq` coefficient is changed arbitrarily.  This resolves the apparent
conflict between the two existing gates:

```text
bare pointed occurrence column       does not supply dq;
pointed PP-module section             supplies dq by Leibniz.
```

The labelled two-direction Hasse cobar is likewise functorial after this
section exists: the two roots commute on the literal marked factors and the
ordered totalization has `d^2=0`.

## 3. `d_even` is a composite face, not an additional theorem

Let

\[
 p_i=(-Q_i,-\operatorname{ores}),
 \qquad n_i=(+Q_i,0),                                \tag{3}
\]

where `n_i` is the invisible cap face supplied by physical descent of the
central `K_Eq` comparison.  Then `p_i+n_i` is the pure scalar-residue face.
If the augmented occurrence label map sends face 3 to `B4` and face 5 to
`B1`, the exact composition is

\[
 \boxed{
 d_{\rm even}
 =-{1\over2}\big[(p_3+n_3)_{B_4}+(p_5+n_5)_{B_1}\big]
 ={B_1+B_4\over2}.}                                  \tag{4}
\]

Thus `d_even` need not remain as a separate hypothesis once one augmented
`P2` section supplies all three ingredients in (4): `p`, physical `K_Eq`
descent, and the literal occurrence-to-residue label map.

None of those ingredients can be suppressed.  Before the label map, the
primitive covector

\[
                 \chi=(0,1,-1,0,1,-1)                \tag{5}
\]

kills the scalar and Cartan residue lines and reads one on `d_even`.
Likewise, removing `d_even` from the final assembly exposes root residue
`-E`, while removing the pointed `K_Eq` face exposes complete Eq
`delta_plus`.  They are independent projections even when one comparison
morphism packages them.

## 4. The labelled ridge remains a load-bearing face

The unique terminal packet is

\[
 \gamma_v=-d\Omega_v=-da+dt+db-du,
\]

with

\[
 \iota_{\eta_z}\gamma_v=1+\delta_{vz}u_z/t,
 \qquad
 \iota_\sigma\gamma_v=-q_{pq}^{22}.                 \tag{6}
\]

It commutes with the complete order-six Hasse tower, so it creates no new
mixed correction.  It is not implied by the degree-zero occurrence/cap,
`d_even`, or `K_Eq` signatures: its `pq` and `xv` halves lie in different
site degrees, and the shifted Kähler coordinate is in the kernel of every
degree-zero forgetful projection used by the core assembly.

Consequently the ridge is redundant only in the following precise sense:
if the sought theorem is formulated from the start as a **relative
principal-parts/Kähler** comparison and includes (6), eta/sigma follow
uniquely.  A degree-zero augmented `P2` section still needs this extra
typing clause.

## 5. Updated shortest dependency map

The single theorem `AugP2(3)` should contain four face certifications:

1. the pointed source-algebra face `u_f-u`, natural in every marked
   occurrence/root pair;
2. the primitive cap `p` in the literal word/fine/repeated grade;
3. the physical central `K_Eq`/invisible-cap descent and the `B4/B1` label
   map;
4. the shifted Kähler face `gamma_v`.

Then the remaining rows close as follows:

```text
root Hasse squares      <- occurrence/root functoriality
dq reinsertion          <- Leibniz (2)
d_even                  <- p+n+label formula (4)
W                       <- existing literal r0-T cap, Yw=W
physical q              <- existing generator/row-homotopy alternative
anchor                  <- pointed source-algebra conormal functoriality
eta/sigma               <- unique contractions (6)
```

So the fastest generic construction target is one enriched comparison, not
separate proofs of `d_even`, `dq`, and `W`.  Its irreducible content is still
multi-face: `P_f`, `p`, `K_Eq` descent/label transport, and `gamma_v` have
independent primitive detectors.

The statement here is the generic `h=3` theorem.  Closing the beta-zero
branch requires the same comparison integrally over `k[beta]` with its
Bockstein face; extending uniformly to larger `h` requires monoidality under
spectator matching-tail multiplication.

Run:

```text
python3 computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py
python3 -O computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py
python3 -I -S computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py
```

Frozen ledger SHA-256:

```text
20f9514812d4cf181aff707b51bfaa3a67e6751503befd29d0396a3dba8b7aa0
```
