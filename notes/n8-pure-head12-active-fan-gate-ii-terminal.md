# The forced pure head-12 row is already an active-fan terminal

## Result

The first nonlinear SCC branch does not require another mate recursion after
the forced pure response face

\[
 G_{12}=P_1Rce,
 \qquad(111111;12),\qquad
 \mathrm{PS},\quad65\mid73\mid02\mid14.                 \tag{1}
\]

Restoring the response endpoints as (P=6,S=7), the new cell is literally

\[
 R=s_2(3;1)=A_{S3}[2,1].                                \tag{2}
\]

It is therefore an off-diagonal endpoint cell on the pure-one target word,
not an off-grade or diagonal pure-row packet.  Any complete exact-source
closure of (1) enters the pinned target-augmented private-site theorem.  It
forces a source-provenant active fan, which is either four-good or contains a
literal pure-colour coloop.  Four-good is already landed; finite Hall
saturation of the coloop outcome is exactly the existing Gate-II fan-grade
(Phi/q) frontier.

Checker:
[`verify_n8_pure_head12_active_fan_gate_ii_terminal.py`](../computations/verify_n8_pure_head12_active_fan_gate_ii_terminal.py).

## Literal word, head, and fine typing

The pure diagonal response row and the mixed row use the same internal word
and differ only at endpoint (S):

\[
 \begin{aligned}
 G_{11}&=S_1P_1ce-1,\\
 G_{12}&=RP_1ce.
 \end{aligned}                                          \tag{3}
\]

Here

```text
S1 = A_73[1,1],       R = A_73[2,1],
P1 = A_65[1,1],       c = q02[1,1],       e = q14[1,1].
```

Thus the private-site theorem has

```text
full order N = 8,       changed site v = S = 7,
reference u = 3,        pure colour a = 1,
changed head b = 2,     common cofactor C_3 = P1*c*e.
```

Deleting (S,3) leaves exactly the fine cofactor matching
(65\mid02\mid14); restoring the reference edge (73) gives the complete fine
grade (65\mid73\mid02\mid14) in (1).  Both rows have operation tag `PS`.

On the sparse symbolic packet, the target augmentation is already visible as

\[
                    S_1G_{12}-RG_{11}=R.                \tag{4}
\]

At the normalized chart point,

\[
                 G_{11}=0,\qquad R=-1,\qquad G_{12}=-1. \tag{5}
\]

Equation (5) is not presented as a full exact source.  It says precisely that
the forced (R) makes the mixed row fail.  If additional complete-row terms
repair that failure while retaining (R\ne0), the general identity

\[
 p_uG_{\mathrm{mixed}}-q_uG_{\mathrm{pure}}
 =q_u+\sum_{s\ne u,v}(p_uq_s-q_up_s)C_s                \tag{6}
\]

forces at least one nonzero determinant/cofactor summand.  That is the
source-provenant distinct-head active fan.

## Pinned landing dependency

The route uses, in order:

1. `verify_n8_pure21_head02_pure_anchor_exit_gate.py` for the unique
   (R)-mate and the exact face (1);
2. `verify_uniform_target_augmented_private_site_active_minor.py` for (6) at
   all even orders, in particular (N=8);
3. `verify_h3_active_fan_coloop_or_four_good.py` for the exhaustive split of
   the resulting physical fan; and
4. `verify_h3_active_coloop_extra_mate_deletion_or_gate_ii.py` for finite
   coloop/Hall saturation and identification of its sole survivor.

The terminal map is

```text
G12 complete-row repair
    -> source-provenant private-site active fan
    -> no fan edge is a pure coloop -> four-good existing landing
    -> some fan edge is a coloop     -> finite Hall saturation
                                      -> existing Gate-II Phi/q packet.
```

The coloop branch is not claimed solved: the source-valid protected odd
(Phi) with literal (q=M-a) rows is still the central Gate-II construction.
What is closed is the **independent nonlinear SCC branch**.  It reaches an
already named proof interface and creates no new pure-head terminal theorem.

The local `P5` shear/Ward identity is not needed for this conclusion.  Its
modulo-mixed-ideal statement does not by itself supply a filtered full-germ
lift, whereas the route above uses the literal target-augmented source rows.

## Verification

Run

```text
python3 computations/verify_n8_pure_head12_active_fan_gate_ii_terminal.py
python3 -O computations/verify_n8_pure_head12_active_fan_gate_ii_terminal.py
python3 -I -S computations/verify_n8_pure_head12_active_fan_gate_ii_terminal.py
```

The checker pins every dependency, verifies the exact symbolic rows and
fine matching, replays the normalized values, invokes the (N=8) private-site
identity, and checks the four-good/coloop/Gate-II terminal map.
