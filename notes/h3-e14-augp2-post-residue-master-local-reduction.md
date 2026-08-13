# The post-E14 local frontier is three faces of one augmented `P2` schema

## Result

Assume the source-labelled private placement

```text
E -> R_E14
```

and the same-word/fine/repeated/root-labelled section

```text
+2 D_root tensor d_even.
```

The first map makes the old unary column land the full E14 target.  The
second cancels the exact post-placement residue

\[
 -E=-2D_{\rm root}\otimes d_{\rm even}.
\]

There is no new residue coefficient direction and, after this same-grade
grant, no further residue transport.  If only an unrooted or coarse
`d_even` is granted, however, its placement into the E14 summand is still a
physical map; the coefficient identity alone does not provide it.

Modulo these granted E14/main faces, the shortest remaining local quotient
has rank three:

\[
 \boxed{P_f=d(u_f-u),\qquad z_{\rm cap},\qquad
        \gamma_v=-d\Omega_v.}
\]

Checker:
[`verify_h3_e14_augp2_post_residue_master_local_reduction.py`](../computations/verify_h3_e14_augp2_post_residue_master_local_reduction.py).

## Why exactly these three faces remain

The three coordinates lie in distinct augmented/graded rows:

| face | row detected by | exact reduction |
|---|---|---|
| `P_f` | marked tangent/conormal | `[dG]=-[d(u_f-u)]` modulo the complete response row |
| `z_cap` | scalar ordinary residue in the cap word/grade | `p_y=z_cap-n_y`, with `n_y` supplied by physical `K_Eq` |
| shifted ridge `gamma` | terminal forgetful-kernel coordinate | main rows and strict Hasse commutation do not construct its labelled placement |

Their coordinate vectors are the three standard basis vectors, hence have
rank three.  This proves independence as homogeneous **faces**.  It does not
say that three unrelated source objects or three unrelated
conjecture-level theorems are required: one augmented comparison
totalization may carry all three.

The mate slack is not a fourth face.  In the literal selected response block,

\[
 [dG]=-{1\over90}[c_f],\qquad
 [d(u_f-u)]={1\over90}[c_f],
\]

so it is exactly `-P_f` in the quotient.  The old 5+84 mate split and its
two local occurrence duals therefore reduce to the same centered-occurrence
descent, not a second pointed theorem.

Likewise the primitive cap is not a fourth face after `K_Eq`:

\[
 p_y=z_{\rm cap}-n_y.
\]

The scalar cap-residue covector kills `P_f`, `d_even`, the response gauge,
and `K_Eq`, and reads one on `z_cap`; this is the sharp reason `z_cap`
survives independently.

## The other rows do not add generators

- Residual `q` private pivots transfer by
  `d Gamma_p=t_p-p` to the same retained centered occurrence carrier.
  This requires the full source-labelled four-pivot embedding; one selected
  E14 coefficient is not enough.
- The physical `W` row is the existing cap identity
  `Phi_cap(Yw_E)=W_E`, supplied by `r0-T`.  No fourth `W` generator is
  needed, but a proof which projects away `W` is still invalid.
- `dq` reinsertion follows from the Leibniz law once the comparison is a
  principal-parts module map.
- Once the labelled shifted ridge is physical, eta/sigma are its unique
  contractions.  Summing
  `1+delta_(vz) u_z/t` over the five exposed `v` gives
  `5+u_z/t`, exactly the terminal mate required to promote the `z_cap`
  covector.

Thus the shifted ridge and `z_cap` are independent homogeneous data, but
their augmented terminal laws fit one comparison cell without another
numerical correction.

## Shortest exact master local theorem

It is enough to construct one source-labelled augmented principal-parts
`P2` placement schema on the complete centered occurrence orbit, with:

1. the already isolated `E -> R_E14` private face and same-grade rooted
   `d_even` face;
2. the pointed conormal face `P_f`;
3. the scalar cap-residue face `z_cap`; and
4. the labelled shifted Kähler face `gamma=-dOmega`.

Then the committed identities close the mate slack, primitive cap, main
lower/Eq/target/residue rows, residual `q`, `W`, and eta/sigma.  This is one
theorem schema, not one homogeneous column.  The source-labelled schema
itself remains open, as do its integral `beta=0` and uniform spectator-tail
extensions.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
0f16930591e9c90d8fb57c294e59d4f60c61dd84f81d08cbcf1222b40aa7a901
```
