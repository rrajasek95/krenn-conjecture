# `PSQJet_01` exists relatively, but its nine collision faces are not absolute

## Outcome

There are two different questions, and they have opposite answers.

1. **Does `PSQJet_01` require a new relative Tate generator?** No.  In the
   full plus/transposed Boolean occurrence DGA, the odd graph generator
   `b^-` already exists.  Closure under multiplication and Kähler
   prolongation gives

   \[
                   J_{\rm rel}=d(q_{01}b^-)
                    =dq_{01}b^-+q_{01}db^- .          \tag{1}
   \]

   Equation (1) has the full literal `6+6+3` signed product-rule boundary.

2. **Is this an absolute physical divided-Hasse cell?** No.  Its boundary is
   the physical jet relative to the retained carrier jet
   `d(q01*u^-)`.  Actual divided-Hasse extraction from complete source rows
   also contains `J*eta` and every compatible same-grade pair face; it does
   not isolate the selected endpoint fibre.  Current Hall/fan/Cartan rows
   transport the nine collision faces but do not make them absolute.

Thus the relative `PSQJet_01` construction is finished.  The next physical
map must land its retained carrier jet in the two root-labelled `r0` cap
sections.

Exact checker:
[`verify_h3_psqjet01_divided_hasse_relative_dga_gate.py`](../computations/verify_h3_psqjet01_divided_hasse_relative_dga_gate.py).

## The exact product rule

Put

\[
 B=p_0s_1,
 \qquad C=p_1s_0,
 \qquad
 H=q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}.
\]

The physical top is

\[
                           (B-C)q_{01}H.               \tag{2}
\]

It consists of six literal monomials and has repeated-site type
`P4+2K2`.  Direct squarefree differentiation verifies

\[
\begin{aligned}
d((B-C)q_{01}H)={}&(dB-dC)q_{01}H\\
                  &+(B-C)dq_{01}H\\
                  &+(B-C)q_{01}dH.                    \tag{3}
\end{aligned}
\]

The literal census is:

| family | literal flags | signed pairs | cofactor type |
|---|---:|---:|---|
| endpoint `(dB-dC)q01H` | 12 | 6 | `P3+2K2` |
| tail `(B-C)q01dH` | 12 | 6 | `P4+K2` |
| coloop `(B-C)dq01H` | 6 | 3 | `4K2` |

Every flag retains word `11110000 = 11:110000`, repeated sites `0,1`, its
removed edge, endpoint orientation, and the `PS-over-q01 mixed first-jet`
operation tag.

## Why the relative jet is automatic

For each of the fifteen signed face pairs, retain four coordinates:

```text
physical B, physical C, carrier B, carrier C.
```

The two monic graph rows and the complete even row have rank three in each
four-coordinate block.  Across all fifteen faces the rank is 45.

The relative jet is

\[
 (B-C)_{\rm physical}-(B-C)_{\rm carrier}.            \tag{4}
\]

It is the signed difference of the two existing graph rows, so adjoining
(4) leaves the rank at 45.  This is the finite linear shadow of (1):

\[
 \partial_{\rm pres}d(q_{01}b^-)
    =d((B-C)q_{01}H)-d(q_{01}u^-).                    \tag{5}
\]

The standard first-jet mapping-cylinder matrix

```text
[[U,0],[dU,U]]
```

gives the same conclusion categorically: `dU` is the forced Leibniz
diagonal, not a new generator.  Therefore `PSQJet_01` is a genuine mixed
first jet of the existing **relative** full source presentation.

By contrast, the absolute physical vector `(B-C)_physical` raises rank
`45 -> 46`.  It kills the retained carrier term in (5), so it is genuinely
new source data.

## Actual divided-Hasse extraction does not isolate it

For an actual bivariate source lift

\[
 X(s,t)=x+s\xi+t\zeta+st\eta+\cdots,
\]

multiaffinity gives

\[
 [st]F(X)=J_xF(\eta)+B_xF(\xi,\zeta).                 \tag{6}
\]

The second term is the sum over every compatible ordered pair in every
literal matching.  A `PS` response pair has three `C4` complements, but
the complete row also contains all other endpoint pairs and the mixed
correction `J eta`.

The pinned literal guard has one marked pair of value `+1` and a silent
same-grade mate of value `-1`, while both its complete target and direct
response polynomials vanish.  Hence (6) reads `1-1=0`; it does not imply
the marked pair is zero.  The relative Boolean cylinders perform the
occurrence selection in (1).  No existing absolute complete source row
performs it.

## Routing all current faces

The audit gives the named inventory its strongest legitimate scope.

- All six endpoint signed pairs are granted absolute fan/Cartan exits.
  The eventual dual is zero on them.
- Every `P4+K2` and `4K2` face gets a `B` recurrence/coloop exit graph and a
  `C` recurrence/coloop exit graph.
- Every fine label gets a complete even `B+C` row at both source and exit.
- Endpoint oddness kills the coarse target, `D`, `W`, anchor and pure-`Eq`
  readouts.  Ordinary residue remains labelled.

The Hall/fan rows transport endpoint orientation; they do not mix `B` and
`C`.  On the nine tail/`dq01` signed pairs their rank is 27.  The selected
orientation raises it to 28.  Equivalently, even after all six endpoint
pairs are granted in the fifteen-pair model, the rank changes

```text
51 -> 52
```

when the absolute jet is adjoined.

An exact normalized dual is

```text
(1/18)*(+B-C on physical and carrier coordinates)
```

on the six `P4+K2` and three `4K2` pairs, and zero on the endpoint pairs and
protected rows.  It reads

```text
relative PSQJet   0
absolute PSQJet   1.
```

This is the exhaustive local no-go against the named Hall/fan/Cartan
inventory.  It is not yet a global terminal because it has not been
extended across every external complete-source, cap, residue, ridge and
mixed-`K_Eq` column.

## Shortest remaining map

The domain side is now complete:

```text
relative u^- Boolean carrier          present
four transported first faces          present
relative PSQJet_01=d(q01*b^-)          present
literal 6+6+3 carrier-jet faces        present.
```

What remains is the landing

```text
d(q01*u^-)  -->  two root-labelled AugP2/K_Eq r0 cap sections.
```

At the recorded interface the words and operations already match.  The
missing content is the literal head/fine section map.  Constructing it
makes the relative jet physical; failing to construct it requires extending
the normalized nine-pair dual across those two sections and the downstream
mixed `K_Eq`/ridge inventory.

## Verification

```text
python3 computations/verify_h3_psqjet01_divided_hasse_relative_dga_gate.py
python3 -O computations/verify_h3_psqjet01_divided_hasse_relative_dga_gate.py
python3 -I -S computations/verify_h3_psqjet01_divided_hasse_relative_dga_gate.py
```

Frozen ledger SHA-256:

```text
3d52e6b3b06869766bca889117b053f3eece6a83f898910a407f0ae99e8c0acd
```
