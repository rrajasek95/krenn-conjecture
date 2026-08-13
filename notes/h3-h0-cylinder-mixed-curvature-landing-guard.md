# The `H0`-cylinder target curvature reduces to a mixed residue debt

## Result

The nonzero curvature

\[
                         t k_{ij}
\]

from the `H0`-preserving cylinder is a genuine endpoint-odd by
matching-standard class.  It does not yet enter the active-fan/four-good/
coloop theorem or the actual source-terminal/Macaulay quotient.

As a bare formal output, a single scalar `t` is not yet a physical
fine-graded source column.
Writing

\[
 F_{01}=u_{00}u_{11}-u_{01}u_{10},
\]

the fine-homogeneous cylinder curvature must be the tagged family

\[
 t_{00}u_{11}+u_{00}t_{11}-t_{01}u_{10}-u_{01}t_{10},             \tag{1}
\]

with `gr(t_rj)=gr(u_rj)`.  All four terms in (1) then have the common
doubled Segre grade.  No ungraded scalar symbol by itself supplies the four
distinct occurrence labels.  The pointwise equality `t=L=90f` does not
identify them.

Checker:

```text
computations/verify_h3_h0_cylinder_mixed_curvature_landing_guard.py
```

Frozen ledger digest:

```text
ad57a54598097268164aadccb703e8d37d5988fc0b9a789ac8909b4e3dbba0e7
```

## Polynomial/Macaulay closure is positive on the target row

Once a target-normal correction is a **physical source-module generator**,
there is no further target-module obstruction.  If `C_t` has target row one
and the source contains all homogeneous coefficient multiples, then
`k_ij C_t` is an admitted Macaulay column.  Fine grading is handled
componentwise: every homogeneous occurrence term of `k_ij` lands in its
exact product grade.

For a pure target generator with signature

```text
(target,ores,anchor/q,W,ridge,eta/sigma)=(1,0,0,0,0,0),
```

the column `-k_ij C_t` cancels the cylinder curvature completely.  The
curvature is then not a new terminal.

The already physical cap graph has, after the still-open cross-word
placement,

```text
T+Y*rho=(target,ores,anchor/q,W,ridge,eta/sigma)
       =(1,1,0,0,0,0).
```

Multiplication by `-k_ij` cancels `t k_ij` in the target row but leaves

\[
                   (0,-k_{ij},0,0,0,0).              \tag{2}
\]

Thus polynomial closure moves the frontier from mixed target to the
word-resolved mixed ordinary-residue row.  It does not close the whole
augmented packet.

## Identification with the residual-`q` graph lock

The coefficient character of (2) is exactly the pinned four-corner
character

```text
(1,-1,-1,1)=(P_+-P_-)(q00-q11).
```

The cylinder therefore introduces no second abstract residue
representation.  Its literal physical grade, however, is not yet the graph
lock's grade:

```text
cylinder:   word 11:110000, endpoint p1*s0-p0*s1,
            residual q23:00*q45:00-q24:00*q35:00;
graph lock: word 1211222, first labelled repeated P3+K2 grade,
            endpoint P_+-P_-, decorated q00-q11 (11/21/12 cells).
```

Identifying these packets is precisely the open physical Cartan/cap
cross-word descent.  Once it is proved, the residual cylinder debt is the
already named graph-breaking Physical Cartan Descent cell, including its
eta/sigma law; no new residue theorem is needed.

Ordinary graph transport cannot supply it.  The pinned law `R_w=D_w` says
that a standard combination with zero main boundary has zero ordinary
residue, whereas (2) is residue-only.  Coefficient equality compresses the
frontier but does not establish source placement.

## Existing physical rows remain dark

In occurrence order

```text
u00,u01,u02,u10,u11,u12
```

the three curvature characters are

```text
(-1, 1, 0, 1,-1, 0),
(-1, 0, 1, 1, 0,-1),
( 0,-1, 1, 0, 1,-1).
```

They span the rank-two module

\[
       \operatorname{sgn}_{\rm endpoint}\otimes
       \operatorname{Std}_{\rm matching}.                         \tag{3}
\]

Every scalar/complete-target row, endpoint sum, and matching sum kills
(2).  The committed aggregate anchor and physical-`q` shadows also kill it.
`W`, shifted ridge, eta, and sigma occupy independent labelled output
summands and have zero disclosed restriction to (3).  Thus the coarse
formal cylinder alone does not construct a physical output map.  After the
cap graph is physically placed, polynomial closure supplies the mixed target
family but carries the ordinary-residue debt (2).

## Active-fan and support guard

At the exact local values

```text
e0=1, e1=0, q0=1, q1=2, f=e0*q0=1,
t=90f=90, t*k01=-90,
```

two pure-support completions retain the identical nonzero curvature.

- In the dense completion all fifteen colour-zero `K6` matchings occur and
  there is no literal pure coloop.
- In the sparse completion the only colour-zero matching is
  `05|14|23`, so `23` is a literal coloop.

Both local packets use only the diagonal `00` residual cells and contain no
named offdiagonal decorated reference cell.  Hence the private-site identity
cannot be invoked in either packet.  The same nonzero `t*k` value therefore
does not determine an active-clean incidence or choose the four-good/coloop
branch.

## Sharp output two-completion guard

Modulo all existing output rows, the local mixed module (3) remains rank
two.  There are two exact extensions of the same disclosed output packet:

```text
dark extension:      K -> 0,
terminal extension:  K -> K (a new mixed target family).
```

They agree on the scalar target, endpoint/matching aggregates, anchor,
physical `q`, `W`, shifted ridge, eta, and sigma.  Before cap placement only
the unconstructed mixed target row distinguishes them.  After placement,
the target distinction disappears and the same fork lives in the mixed
ordinary-residue quotient.

This is the exact terminal analogue of the support fork.  An abstract
covector on (3) becomes a Macaulay terminal only after extending across the
complete source-terminal columns; the cylinder construction supplies no
such extension.

## Shortest positive theorem

Place the physical cap graph/Cartan descent across the response/E14 word in
the exact doubled word/fine/repeated grade.  Polynomial closure then cancels
the target curvature and identifies its residue with the existing graph
lock.  Prove one of:

1. the graph-breaking Physical Cartan Descent cell cancels the residue (with
   its eta/sigma law), or its fully augmented dual survives as an actual
   Macaulay terminal; or
2. it maps source-validly to an offdiagonal decorated cell and its cofactor,
   entering the committed private-site fan and hence four-good or a literal
   pure-colour coloop.

The same comparison must retain scalar/target, anchor and `q`, `W`, shifted
ridge, eta, and sigma.  No further coefficient case split is needed.

Scope is the canonical `h=3` fixed-endpoint Segre block.  The two
completions are exact local support/output guards, not complete GHZ source
points and not a no-go theorem for constructing the tagged cylinder.
