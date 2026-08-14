# The ordered root return transports the parent anti-diagonal to a relative carrier

## Verdict

For one collision sector, the smallest genuine parent-split mapping cylinder
is completely explicit.  Let `c_A,c_B` denote the two occurrence-labelled
copies of one collision monomial and let `c` denote the collected collision
coordinate.  Then

\[
 d\theta_A=c_A-c,\qquad d\theta_B=c_B-c              \tag{1}
\]

preserves the one-dimensional collected `H0` and gives the absolute
boundary

\[
                  d(\theta_A-\theta_B)=c_A-c_B.       \tag{2}
\]

However, the ordered hyperbolic root operation supplies neither comparison
cell in (1).  Its minimal presentation-safe bar must retain a carrier for
each parent:

\[
 d\beta_A=c_A-t_A,\qquad d\beta_B=c_B-t_B.           \tag{3}
\]

This preserves the two-dimensional parent occurrence `H0`, but only gives

\[
 d(\beta_A-\beta_B)
       =(c_A-c_B)-(t_A-t_B).                          \tag{4}
\]

Thus the exact answer is: **the ordered root path supplies a relative
anti-carrier, not an absolute physical boundary**.  Applying the opposite
root transports (4) to

\[
                         d\Gamma=(A-B)-\rho,          \tag{5}
\]

and similarly for `A-C`.  Agreement of the two root orders makes their
carrier difference exact, but retains one common `rho` class.

Exact checker:
[`verify_h3_collision_parent_split_relative_bar_terminal_gate.py`](../computations/verify_h3_collision_parent_split_relative_bar_terminal_gate.py).

## 1. Minimality and `H0`

In coordinates `(c_A,c_B,c)`, the two columns in (1) have rank two.  Hence

\[
                          3-2=1,                     \tag{6}
\]

the dimension of the old collected coordinate.  One comparison column has
rank one and leaves a two-dimensional quotient, so both are necessary for
the full parent-to-collected cylinder.  Subtracting them gives (2) with no
retained term.

The formal root does not construct (1).  If its two first faces were simply
declared absolute bar boundaries `c_A,c_B`, the parent occurrence `H0`
would drop from dimension two to zero.  The presentation-safe construction
is (3): four degree-zero coordinates, two monic graph columns, and quotient
dimension two.

Put

\[
 \kappa=c_A-c_B,\qquad \tau=t_A-t_B.                 \tag{7}
\]

Then `kappa-tau` is in the relative boundary image, while neither `kappa`
nor `tau` is.  The normalized dual

\[
                  \psi={1\over2}(1,-1,1,-1)          \tag{8}
\]

on `(c_A,c_B,t_A,t_B)` kills both graph columns and reads one on each of
`kappa,tau`.  The exact rational point

```text
c_A=t_A=1,  c_B=t_B=-1
```

also shows directly that the relative rows vanish while the anti-class is
nonzero.

An absolute column with boundary `tau` makes `kappa` a boundary by (4).
Landing only the diagonal carrier `t_A+t_B` does not.  Equivalently, one may
identify both retained carriers with the collected coordinate `c`; adjoining

\[
                         t_A-c,\qquad t_B-c            \tag{9}

to (3) recovers (1), reduces parent `H0` from two to the collected one, and
kills the anti-diagonal.

## 2. Why the opposite root remains relative

Let `R` be the opposite root.  On coefficients,

\[
                       R\kappa=A-B=:q.                \tag{10}

Naturality applies `R` to the retained term as well.  Writing
`rho=R tau`, equation (4) becomes exactly (5).  In the two coordinates
`(q,rho)`, its one boundary column is `(1,-1)`.  It has rank one; both `q`
and `rho` survive and represent the same `H0` class.  The dual `(1,1)` kills
`q-rho` and reads one on each.

The reverse root order gives another graph

\[
                  q-\rho_{\rm reverse}.              \tag{11}

Together (5) and (11) make
`rho_forward-rho_reverse` a boundary.  Their rank is two in the three
coordinates `(q,rho_forward,rho_reverse)`, so one common carrier still
survives.  Formal flatness therefore proves path independence of the
**relative** carrier; it does not make `q` absolute.

An absolute physical landing `dE=rho` would finish the return.  Without it,
the polynomial identity `R kappa=A-B` specifies the leading face but is not
a source boundary.

## 3. First PP and reinsertion labels

Take the literal first collision and tail

\[
                         D s_1q_{23}q_{45},            \tag{12}

in response word `11:110000`.  Its two parent labels are

```text
from A=D*q01,   from B=p0*s1.
```

The complete first principal-parts boundary has four faces:

| removed edge | retained monomial | type |
|---|---|---|
| `D=PS` | `s1*q23*q45` | `3K2` path cofactor |
| `s1=S1` | `D*q23*q45` | `3K2` path cofactor |
| `q23` | `D*s1*q45` | `P3+K2` tail cofactor |
| `q45` | `D*s1*q23` | `P3+K2` tail cofactor |

Every face retains both the parent occurrence label and its carrier copy.
Applying `PP` to (4) gives

\[
 d(PP\beta_A-PP\beta_B)
       =(f_A-f_B)-(s_A-s_B)                           \tag{13}
\]

for each row of the table.  Thus `[d,PP]=0` exactly.  Removing `q23` or
`q45` and reinserting that same labelled edge reverses the tail restriction
and returns the top carrier.

This makes the load-bearing naturality condition precise.  A physical
`dEta=tau` must have four proper faces satisfying

\[
                         d(PP\Eta)=s_A-s_B.            \tag{14}

A top-only scalar kill of `tau` is not a chain map.  The two tail cofactors
in (12) remain in response word `11:110000`; their transport to canonical
AugP2 word `01211222` is still the separately missing word-changing
comparison, together with reduced Eq and the shifted ridge.

## 4. Sharp filler/terminal criterion

The local positive datum can be stated in either equivalent form:

1. construct both physical parent-to-collected cells (1), natural on all
   four faces; or
2. construct one occurrence-labelled absolute anti-carrier family
   `dEta=tau`, with (14), and an absolute landing of the returned `rho`.

Either construction makes the collision anti-diagonal and hence the
returned `A-B`/`A-C` switch absolute.  After the shore gauge, the two root
pairs are exactly the `A+B` and `A+C` families needed to close Gate II.

Conversely, exhaust the physical map in the identical

```text
word / fine / repeated grade / window / parent occurrence
```

and include all four PP/reinsertion descendants and augmented readouts.
Extend (8) by giving every parent face and its retained carrier the same
forced value.  Then:

```text
some complete face-natural column has nonzero tau/rho value
    -> filler branch;
every complete column is killed and no tau/rho landing exists
    -> normalized parent-anti dual is an augmented terminal.
```

The terminal claim becomes unconditional only after that same-grade map is
proved exhaustive and the dual is extended through the word-changing
AugP2, `q`, anchor, `W`, ordinary-residue and shifted-ridge rows.  The
relative bar itself establishes the exact fork but does not choose its arm.

## Verification

Run

```text
python3 computations/verify_h3_collision_parent_split_relative_bar_terminal_gate.py
python3 -O computations/verify_h3_collision_parent_split_relative_bar_terminal_gate.py
python3 -I -S computations/verify_h3_collision_parent_split_relative_bar_terminal_gate.py
```

The checker uses exact rational ranks, verifies both minimal cylinders, the
normalized dual, the two-order return, and every labelled first-PP relative
face.
