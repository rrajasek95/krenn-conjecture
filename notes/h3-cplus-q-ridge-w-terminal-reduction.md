# Physical q closes by dichotomy; the ridge still needs its labelled lift

## Exact reduction

Start with the conditional generic `C_plus` core of `649b7eb`.  Assuming
physical constructions of `P2`, pointed `K_Eq`, and `d_even`, every lower,
Eq, target, and labelled-residue debt vanishes.  The three augmented rows
listed there do not have the same status.

1. Physical `q` is closed by the existing comparison alternative.
2. Eta/sigma have a unique compatible Kähler packet and commute strictly
   with the complete Hasse tower, but its labelled repeated-grade lift is
   not implied by the current degree-zero hypotheses.
3. `W=0` is a genuinely separate scalar compatibility; endpoint-evenness
   does not force it.

Checker:
[`verify_h3_cplus_q_ridge_w_terminal_reduction.py`](../computations/verify_h3_cplus_q_ridge_w_terminal_reduction.py).

## 1. Physical q is no longer a construction target

Let `Phi` be the comparison supplied by the physical `P2/K_Eq` assembly on
the complete protected relative domains, and suppose both domains carry the
literal terminal

\[
                       q=\sum_{i=1}^6m_i-\operatorname{ainc}.
\]

Commit `7efd10d` gives the exhaustive alternative

\[
 q-q_3\Phi=\lambda J
 \quad\hbox{or}\quad
 \exists x\in\ker J:\ (q-q_3\Phi)(x)\ne0.             \tag{1}
\]

In the first branch, `lambda` constructs the augmented `q` comparison.  In
the second, `J_3 Phi x=0`, and at least one of `q(x)` and `q_3(Phi x)` is
nonzero.  Normalizing on that side gives the already accepted physical
relative-generator exit.  Therefore `q` does not remain as an independent
construction after physical typing of the comparison and the two `q` rows.

The qualification is essential: (1) does not define `q` on a merely
projected or formal P2 column.  It consumes physical `q` on both complete
domains.

## 2. What ridge commutation proves—and what it does not

For one face write

\[
 a=q_{pq}^{22},\quad t=q_{pq}^{00},\quad
 b=q_{xv}^{0m_v},\quad u=q_{xv}^{00}.
\]

The prescribed terminal packet is uniquely

\[
 \gamma_v=-d\Omega_v=-da+dt+db-du,                   \tag{2}
\]

with

\[
 \iota_{\eta_z}\gamma_v=1+\delta_{vz}u_z/t,
 \qquad
 \iota_\sigma\gamma_v=-q_{pq}^{22}.                 \tag{3}
\]

Its source boundary, main rows, physical `q`, and `W` are zero.  The complete
8,580-operator calculation proves

\[
                         [\Theta_6,\gamma_v]=0.        \tag{4}
\]

Thus once a physical labelled copy of (2) exists, it tensors with the P2
Hasse totalization without any new mixed face.  Equations (2)--(4) remove a
possible higher compatibility theorem and fix every eta/sigma coefficient.

They do **not** construct the labelled copy.  The two halves have degrees

\[
 \deg(-da+dt)=e_p+e_q,
 \qquad
 \deg(db-du)=e_x+e_v.                                \tag{5}
\]

Adding the same spectator/reinsertion tail preserves their difference.  A
degree-zero P2 source column, the pure terminal-zero `d_even` section, and a
degree-zero pointed `K_Eq` comparison therefore do not imply image
membership of their shifted Kähler sum.  The formal class (2) can be added
or omitted without changing any row used in the core assembly.  Strict
commutation says either choice is compatible; it does not select the
physical one.

This distinguishes two conditional statements precisely:

```text
649b7eb hypotheses as written:
    remaining = W equation + labelled shifted Kähler image membership.

fully augmented principal-parts P2/KEq hypothesis,
including the physical labelled ridge (2):
    remaining = W equation only.
```

So eta/sigma are not a new numerical formula or a new mixed Hasse cell.
They are one still-load-bearing physical typing clause.

## 3. W is not killed by even parity

Let `rho` reverse the two endpoint roles.  A physical endpoint-even `W` row
satisfies `W rho=W`.  Hence

\[
 W(1-\rho)=0,
 \qquad
 W(1+\rho)=2W.                                       \tag{6}
\]

The generic `C_plus` orbit uses the even operator `1+rho`, so its parity
doubles rather than kills a generic `W` value.  Neither `d_even` nor the
canonical ridge changes `W`; both have `W=0`.  After the main assembly, the
unreduced scalar equation is exactly

\[
                  W(P2\text{ total})+W(\Phi K_{Eq})=0. \tag{7}
\]

Therefore, under a fully augmented P2/K_Eq theorem, (7) is the sole
remaining generic scalar compatibility.  Under the current narrower
hypotheses it sits alongside the labelled ridge lift, not by itself.

## Frontier

The shortest honest terminal theorem is now:

> Construct the physical P2/pointed-K_Eq comparison in the labelled
> principal-parts grade so that it carries the canonical ridge (2), and
> prove (7).  Physical q then closes automatically by (1), while eta/sigma
> close uniquely and without another mixed correction by (3)--(4).

This result is generic.  It does not address the separate beta-zero
`D0`/Bockstein clause.

Run:

```text
python3 computations/verify_h3_cplus_q_ridge_w_terminal_reduction.py
python3 -O computations/verify_h3_cplus_q_ridge_w_terminal_reduction.py
python3 -I -S computations/verify_h3_cplus_q_ridge_w_terminal_reduction.py
```

Frozen ledger SHA-256:

```text
dc32ed6288ce40f668f3b0a7f881683b3fd4c95d2900fec57df0d15e46343897
```
