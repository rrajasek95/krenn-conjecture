# PAComp proof continuation: the first physical factorization

Status: **NOT PROMOTED — conditional symbolic reduction only**  
Date: 2026-08-25

## Outcome

The earliest unresolved implication in the uniform physical `PAComp(h)`
routing is still the operation-changing response-to-cap arrow.  The direct
citation chain does not construct it.  It does, however, reduce the `h=3`
balanced branch to one falsifiable physical factorization: identify the two
intrinsic EqSystem composites

\[
 O_B=I_cD_c\Phi d,
 \qquad
 O_{Eq}=dI_c\Phi_{\widehat q}D_r
\]

with the protected `B` and `Eq` cap readouts, respectively, using the same
normalization and retaining the hidden `-E` and `+E` faces.  The intrinsic
identity `O_B=O_E` is exact; the readout identification is not proved.

This is earlier than either output of the desired dichotomy.  Once a physical
comparison produces an active clean pair, exact clean-pair descent is already
available.  If the balanced packet instead reaches the displayed
factorization, the identity forces `B=Eq` while the balanced right-hand side
is `B`-only, giving the terminal contradiction.  Without the physical
factorization, the anti-diagonal `B-Eq` covector is presentation data, not a
functional on the official EqSystem, so declaring the terminal would be
circular.

## Fixed `h=3` source data

Work over characteristic zero on the official 252-variable EqSystem and its
canonical first Spencer/Tate stage.  Fix

\[
 r=11110000,\qquad c=01211222,\qquad q\in\{23,45\}.
\]

Here `D_r` and `D_c` differentiate the response- and cap-coloured edge
variables, `I_c` reinserts the cap-coloured occurrence, `Phi` is the product
of divided root operators at the six changed sites, and
`Phi_hat_q` uses the remaining occurrence multiplicity after deletion.
The selected carrier is the normalized endpoint-even part of the automatic
`h=3` packet, with word, root, fine, repeated-site, operation, target, private,
ordinary-residue, and hidden-face labels retained.

The source-side exact result is

\[
 I_cD_c\Phi d=dI_c\Phi_{\widehat q}D_r. \tag{1}
\]

The structural checker replays (1) on 6,561 official rows, 105 matching
occurrences per row, and both cuts: 1,377,810 cut-labelled squares.  It also
checks the marked missing/doubled-site collision descendants.  Separately,
the endpoint-even gate proves that no endpoint-odd `PSQJet` filler is needed
for Gate II; the first relevant protected survivor is the `B/Eq` separator.

## Conditional lemma: endpoint-even protected factorization

**Lemma (sufficient `h=3` balanced-branch factorization).**  Let `xi` range
over the selected normalized endpoint-even PAComp carrier.  Suppose there is
a source-labelled physical response-to-cap realization `Theta_q`, natural in
the two root labels and both cuts, with protected cap readouts `B` and `Eq`,
such that:

1. `Theta_q` preserves the response/cap word, root, head, fine,
   repeated-site, operation, target, anchor, `W`, ordinary-residue, ridge,
   `eta`, and `sigma` labels required by `PAComp(3)`;
2. on the selected carrier, the protected `B` readout of `Theta_q` is the
   physical realization of `I_c D_c Phi d`;
3. on the same carrier, the protected `Eq` readout is the physical
   realization of `d I_c Phi_hat_q D_r`;
4. the two identifications have one common nonzero normalization and include
   the hidden lower/private face `-E` and word-resolved ordinary-residue face
   `+E`; and
5. the comparison is augmentation-preserving and the factorization holds on
   the full physical boundary image in this selected grade, not merely on a
   declared generator subalgebra; hence these readouts are functionals on
   actual physical boundaries rather than freely adjoined copies.

Then every physical boundary in this selected carrier satisfies `B=Eq`.
Consequently the balanced private right-hand side, whose protected landing is
`(delta_plus,0)`, is not a physical boundary: the primitive integral
anti-diagonal detector `(d6,-d6)`, with

\[
 d_6=(-1,2,-1,-1,2,-1),\qquad \delta_+=d_6/4,
\]

vanishes on tied `(B,Eq)` landings and reads `3` on the required `B`-only
landing.  Hence this branch is a physical terminal contradiction.

### Proof

1. By hypotheses 2 and 3, the two protected readouts on a physical boundary
   are represented, with the same normalization, by `O_B(xi)` and
   `O_Eq(xi)`.
2. Equation (1) is an equality in the original occurrence-labelled EqSystem,
   not in an artificially split `B direct-sum Eq` target.  Therefore
   `O_B(xi)=O_Eq(xi)` for every selected carrier element and both cuts.
3. The common normalization in hypothesis 4 is nonzero, so hypotheses 2–4
   identify the protected values themselves: `B(Theta_q xi)=Eq(Theta_q xi)`.
   Hypothesis 5 makes this a statement about actual physical boundaries.
4. Thus the anti-diagonal detector annihilates every such boundary.  The
   balanced right-hand side has landing `(delta_plus,0)`, and the pinned
   integral normalization evaluates it to `3`, not zero.  It cannot be a
   physical boundary, which is the claimed terminal contradiction.  QED.

This lemma proves only the displayed conditional implication.  It does not
prove its hypotheses.

## Exact first unproved subclaim

The smallest next symbolic target is the following one-representative
statement.

> **`Q23-PROTECTED-FACTOR`.**  On the canonical `q=23` marked,
> endpoint-even descendant, construct an occurrence-local source-labelled
> operation in the off-diagonal corner `e_C A e_R`, acting on the canonical
> cyclic response carrier and its full physical boundary image, whose cap
> realization simultaneously identifies the protected `B` face with
> `I_c D_c Phi d` and the protected `Eq` face with
> `d I_c Phi_hat_23 D_r`, with one normalization and the literal hidden
> faces `lower/private=-E` and `ordinary-residue=+E`.

The map must preserve the literal word/head/fine/repeated/operation labels.
Cut symmetry should then give `q=45`, and root naturality should supply the
separate `AB` and `AC` instances.  Those covariance extensions must be
proved, not inferred, but they need not be built into the first representative
test.

Why this is the first subclaim:

- the relative odd Boolean carrier and its product-rule faces already exist;
- endpoint-even Reynolds splitting removes the proposed absolute odd filler
  from the Gate-II debt;
- the complete full-star coefficient average covers the 66-term complement
  conditionally on one operation-changing action;
- current constructors generate only `e_R A e_R` and `e_C A e_C`; their
  `e_C A e_R` component is zero; and
- native Taylor/Schreyer resolution cannot choose the anti-diagonal
  `B-Eq` readout, because forgetting `(B,Eq)` to the common occurrence sends
  `(b,e)` to `b+e`.

Therefore another rank calculation, coefficient average, or intrinsic
commutator replay cannot prove `Q23-PROTECTED-FACTOR`.  It requires a new
source-labelled physical operation or a source theorem identifying an
existing literal operation with that off-diagonal map.

## Dependency chain and remaining gaps

The valid implication chain is:

```text
certified six-site obstruction + exact active-clean descent
    <- active clean pair supplied by uniform PAComp(h)

official h=3 EqSystem identity (1)
    + Q23-PROTECTED-FACTOR
    + proved cut/root covariance
    -> h=3 balanced physical terminal
```

The following arrows remain open even if `Q23-PROTECTED-FACTOR` is proved:

1. extend the representative to the complete `h=3` physical packet and all
   simultaneous face-zero/rootless/inactive strata;
2. prove source-grade exhaustiveness/terminal promotion, rather than treating
   a protected formal cokernel as a source terminal;
3. prolong the physical construction uniformly to every `h>=3`; ordinary
   spectator suspension is not known to preserve all normal faces or the
   terminal Macaulay degree; and
4. assemble those statements into the full `PAComp(h)` alternative.

Accordingly, neither this note nor any cited `h=3` working gate changes
`SP-CLEAN-BRIDGE`, `PAComp(h)`, or the status of the Krenn–Gu conjecture.
The certified baseline still records `SP-CLEAN-BRIDGE` as open, and no cited
working note appears as a supersession closing it.

## Replay performed for this note

Two bounded source-side replays were run from the pinned scripts:

```text
python3 computations/verify_h3_eqsystem_divided_root_restriction_chain_commutator_intrinsic_gate.py --mode structural
# PASS; 1,377,810 squares; commutator 0; B/Eq identification CONDITIONAL

python3 computations/verify_h3_gate_ii_endpoint_even_cap_operator_module_gate.py --mode full --json
# PASS; endpoint-even quotient exact; full physical A-action not constructed

python3 computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py --mode all
# PASS; generated Hom(response,cap)=0; two root-labelled sections absent
```

These replays verify only the source-labelled working lemmas stated above.
They do not certify or promote the missing factorization.
