# Theta removes the independent repeated-grade return from the cylinder frontier

## Correction to `5702312`

The item “transport `LambdaT` back to canonical `Lambda`” is not an
independent physical gate.  The correct fine-graded source category has two
objects

```text
g  --theta-->  gT  --theta-->  g,
theta^2=id.
```

The involution is a literal constant physical permutation.  Hence
`d theta=0`, its first-principal-parts lift has no diagonal term, and there
is no grade holonomy.  Keeping both objects is the physical solution; one
must not collapse `gT` into `g` first and then request an artificial return
cell.

Checker:

```text
computations/verify_h3_cylinder_theta_groupoid_frontier_correction.py
```

Frozen ledger digest:

```text
54addc4fab4edd483cb4e4969eece194dcaaf753e26e07cef1d74c9fb7b49187
```

## One attachment supplies both endpoint halves

Let `a_g` be a source-labelled attachment at the canonical object `g`.
Because theta is a chain automorphism, the conjugate attachment is forced:

\[
                         a_{g^T}=\theta(a_g).           \tag{1}
\]

Applying theta twice returns `a_g`.  Thus (1) is one equivariant attachment
schema, not a second existence theorem.

On the two disjoint six-feature sets,

\[
 \Lambda_g=\sum_{F_g}F-\operatorname{ainc},\qquad
 \Lambda_{g^T}=\sum_{F_{g^T}}F-\operatorname{ainc},
\]

and the marked anchor incidence is fixed.  Exact transport gives

\[
                   \Lambda_{g^T}\theta=\Lambda_g.      \tag{2}
\]

Therefore the physical-`q` cocycle of the grade arrow is zero.  Target and
`W` are fixed; ordinary residue moves to its conjugate labelled copy;
`eta0,eta1` are exchanged; sigma is fixed.  These are objectwise physical
labels, not identifications made after forgetting the grade.

The central reduced-Eq cone is also theta-fixed:

\[
                   E=(H_0-u)e_{\rm Eq}.
\]

Consequently `K_Eq` cancels `E` objectwise at `g` and `gT`, and its square
with theta commutes.  No further Eq or terminal coherence cell is needed
after (1).

## Corrected cylinder composition

Commit `5702312` correctly found that the D4--Cartan image of the complete
cylinder matching difference is

\[
                       \delta_{M_1}-\delta_{M_0},
\]

two covariant graph-lock packets.  It also correctly found that the
fixed-right symbol supplies only the `P` endpoint half and theta supplies
the conjugate `S` half.  The overcount was treating the conjugate repeated
grade as a third attachment problem.

Once `a_g` is physical:

1. theta supplies the conjugate half at `gT` automatically;
2. both graph-lock packets are handled by the existing matching-covariant
   Physical Cartan Descent;
3. (2) transports physical `q` with no defect;
4. all target/residue/eta/sigma labels transport equivariantly; and
5. the central `K_Eq` correction is objectwise and flat.

## Sole irreducible local datum

The remaining theorem is exactly one source-valid multiplicative attachment
at `g`:

```text
11:110000 / pure-00 response-centered cylinder
    ->
01211222 / labelled repeated P3+K2 cap packet,
```

carrying in the same physical cell:

```text
the cap graph and its principal companion,
the central reduced-Eq/K_Eq boundary,
ordinary residue and the two graph-lock packets,
anchor incidence and physical q,
W and the shifted Kähler ridge with eta/sigma.
```

Theta does not construct this first attachment.  It proves that constructing
it once is sufficient.  Thus the cylinder lane now has one independent
cross-word cap/central attachment theorem, not separate P-half, S-half, and
`LambdaT -> Lambda` theorems.

This note supersedes only the frontier item (4) of `5702312`; its literal
D4/Cartan matching calculation and cap-word obstruction remain valid.
