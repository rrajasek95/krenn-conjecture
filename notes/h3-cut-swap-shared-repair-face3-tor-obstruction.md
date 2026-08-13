# The Gate-I shared repair is one obstructed face-3 Tor packet

The two labelled-residue sections isolated in `e5eb1fe` have a canonical
common endpoint presentation.  Choose the allowed fixed repair `B4` and
the allowed rho pair `B0,B5`.  The literal decorated multipliers are

```text
B0 = q12:12 q34:11 q45:12,
B4 = q14:11 q25:22 q34:11,
B5 = q15:12 q24:21 q34:11.
```

Therefore

\[
 B_0+B_4+B_5
 =q_{34}^{11}\bigl(q_{3,12|45}+q_{3,14|25}+q_{3,15|24}\bigr)
 =q_{34}^{11}h_3.                                    \tag{1}
\]

This is not a support analogy.  In the first collapse of `f59bbc6`, the
literal C4 choices `10,7,2` send the three shared matching labels `3,4,5`
to `B0,B4,B5`.  The physical target involution exchanges `B0,B5` and fixes
`B4`.  Thus (1) respects both the repeated `P3+K2` fine degree and rho.

## Consequence for the standard source route

Within the endpoint-bar / same-labelled principal-parts / denominator-Tor
construction, realizing all three occurrence sections in (1) forces the
selected face projection

\[
                              e_3\in\operatorname{im}\tau,              \tag{2}
\]

where `tau` is the selected denominator-kernel transgression.  This is the
single exact membership behind the formerly separate fixed and paired
repairs.

On the exact clean `R=0` C5 slice, the reset-word equation already proved
in `a4c687c` says

\[
             \sum_{v=1}^5 h_v y_v=0
             \quad\text{for every }y\in\operatorname{im}\tau.
\]

Here `h_v=1` for all five faces.  Hence the primitive covector

\[
                        \epsilon=(1,1,1,1,1)                           \tag{3}
\]

kills the physical denominator-Tor image, whereas
`epsilon(e3)=1`.  Equation (2) is therefore impossible in this standard
clean-slice route.

Same-face matching PP/Bianchi differences have zero epsilon, and the
physical endpoint-odd Cartan residue

```text
B0 + B2 - B3 - B5
```

also has augmentation zero.  Neither can change (3).  The one coarse
ordinary-residue column cannot be inserted here: `e5eb1fe` showed that it
has no constructed section to these multiplier-labelled directions.

The rational `direct_free` and `tilted` denominator packets from `b15d1ad`
do hit `e3`, but both are explicitly counterguard specializations rather
than points of the full source scheme.  They are evidence that the Tor
condition can jump, not a construction on the clean physical slice.

## Remaining statement

This is a no-go for the complete standard denominator-kernel/endpoint-PP
route, not for an enlarged resolution.  Gate I now needs one of:

1. a higher relative occurrence-splitting cell, outside that standard
   route, whose three protected-zero outputs are `B0,B4,B5`; or
2. an extension of epsilon across the enlarged physical source and terminal
   rows, which would turn the source obstruction into the physical
   separator/Fredholm branch.

The latter promotion still has the already recorded Omega-to-rootless-ridge
and terminal zero-indeterminacy guards; this calculation does not silently
claim a physical annihilator.

## Verification

Run:

```text
python3 computations/verify_h3_cut_swap_shared_repair_face3_tor_obstruction.py
python3 -O computations/verify_h3_cut_swap_shared_repair_face3_tor_obstruction.py
python3 -I -S computations/verify_h3_cut_swap_shared_repair_face3_tor_obstruction.py
```

Frozen ledger SHA-256:

```text
ef2c8f58a5fd0fe33082fd79460477fbdacabb9c7d1ef1628a0487c7eccc0253
```
