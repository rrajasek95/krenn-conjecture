# The shared four-term class is a curvature near-hit with one residual-tail obstruction

## Exact outcome

Work in the four-coordinate quotient

\[
                   (E_+,E_-,\Omega_1,q_{1,23\mid45}).
\]

The proposed shared attachment has boundary

\[
                         A=(1,-1,1,-1).                 \tag{1}
\]

The complete bounded search does not contain (1).  It does, however, find
a much closer construction than an ordinary matching or bar identity: the
mixed bar--curvature Massey chain gives the first two entries of (1) with
the correct sign, full source word, and zero target.  Its only first failure
is the decorated polynomial read by ordinary residue.

Put

\[
 P_+=p_1@0\,s_1@1,\qquad P_-=p_1@1\,s_1@0,
\]

and align the rootless matching $23\mid45$ with the E14 matching
$24\mid35$ by interchanging sites $3,4$.  Then the two relevant tails
are

\[
 T_{\rm pure}=a_{24}^{11}a_{35}^{11},\qquad
 T_{\rm mix}=a_{24}^{21}a_{35}^{12}.                  \tag{2}
\]

The curvature construction has normalized endpoint and residue

\[
                 (P_+-P_-)T_{\rm pure},               \tag{3}
\]

whereas the determinant-multiplied physical rootless bar has companion and
residue

\[
                 (P_+-P_-)T_{\rm mix}.                \tag{4}
\]

Subtracting the bar gives the desired formal boundary signs, but leaves

\[
 \boxed{(P_+-P_-)
        \left(a_{24}^{11}a_{35}^{11}
              -a_{24}^{21}a_{35}^{12}\right)}         \tag{5}
\]

in ordinary residue.  Thus the curvature/bar product is a near-hit, not
the missing invisible chain.

## Why the mixed curvature endpoint is genuinely the right one

The mixed bar--curvature checker uses the complete seven-site word

```text
1211222.
```

This is exactly the physical rootless word `01211222` after deleting the
exposed site $x=0$.  In the normal identity

\[
                         \kappa=AU-BF,
\]

specialize

\[
 A=p_1@0,\quad U=(s_1@1)T',\quad
 B=p_1@1,\quad F=(s_1@0)T',\quad z=T'',
\]

with $T'T''=T_{\rm pure}$.  Then

\[
                         \kappa z=E_+-E_- .            \tag{6}
\]

The exact Massey identity is

\[
 d\bigl(D(n)+\mathsf H(\kappa z)\bigr)=L(\kappa z).  \tag{7}
\]

The unwanted $D$-endpoint cancels, and the full word makes the physical
target zero.  Normalized augmentation sends the surviving $L$-endpoint
to the same polynomial in both $q$-augmentation and ordinary residue.
Consequently (7) reads (3), not an invisible copy of (6).

This is meaningful positive progress: endpoint orientation, source word,
target, and curvature sign are no longer separate unknowns.

## The reciprocal Hasse--Bianchi identity does not remove (5)

For reciprocal response rows,

\[
 D_{kl}E_{ij}=d_{ij}R_{kl}+K_{ij;kl},\qquad
 K_{ij;kl}=K_{kl;ij}.                                  \tag{8}
\]

Hence the $K$-channel antisymmetrization is literally zero.  Equation
(3) of the reciprocal note leaves

\[
 D_{kl}E_{ij}-D_{ij}E_{kl}
                  =d_{ij}R_{kl}-d_{kl}R_{ij},          \tag{9}
\]

not an antisymmetric $K$-class.  The endpoint determinant in (6) can be
realized by the surviving direct-response/physical curvature term, but it
is not $K_{ij;kl}-K_{kl;ij}$.  Therefore reciprocal symmetry cannot
identify the two tails in (2).

The distinction in (2) is primitive.  The four colour-square corners are
linearly independent coefficient coordinates; only their quadratic Segre
minor vanishes.  In particular there is no linear same-word identity
setting $T_{\rm pure}=T_{\rm mix}$.  The complete canonical unary/G11
first-hit module gives the stronger source-level check: its 269 columns
have rank 269, and a rational dual of support 22 pairs $-1$ with the
remaining target (primitive integral pairing $-30$).

## Complete bounded inventory verdict

The checker audits every committed family capable of meeting a face of
(1):

1. all $3^6=729$ diagonal/crossed response rows in the canonical E14
   chart;
2. the complete unary/G11 first-hit module and the mapped rootless
   decorated $2K_2$ core;
3. both endpoint-bar orders, all fifteen face/matching routes, and all
   matching/Bianchi differences;
4. the formal fourth-Hasse candidate and its selected source-unit test;
5. all first repeated $P_3\sqcup K_2$ principal-parts comparison squares;
6. the ordinary incidence/Pluecker/matching-square/Tate module; and
7. the reciprocal Hasse--Bianchi and mixed bar--curvature candidates.

At the E14 tail, the only complete response row which hits $E_+,E_-$
has coefficients $(1,1)$.  The primitive coarse covector

\[
                         \chi=(1,-1,0,0)               \tag{10}
\]

kills this signless row and every endpoint-free rootless row, but
$\chi(A)=2$.  On the rootless side, endpoint bars retain the primitive
response/ordinary-residue companion.  First principal-parts cells give only
adjacent comparison differences plus the pure-Eq face; even after formally
removing that face, their $C_5$ incidence rank is four.  The cyclic
matching-square package is not an absolute cycle: its lower boundary is
$5abcde$.

So none of these older branches independently supplies (1), and their
curvature composition stops exactly at (5).

## One remaining tangent-lift hypothesis

The positive theorem can now be stated as a single source-level lift rather
than an unspecified new higher identity:

> **Residual response Kodaira--Spencer lift.**  In the endpoint-determinant
> sector and the labelled repeated comparison component, construct a
> source-provenant lift transporting
> $T_{\rm pure}=a_{24}^{11}a_{35}^{11}$ to
> $T_{\rm mix}=a_{24}^{21}a_{35}^{12}$.  Its ordinary-residue correction
> must be the negative of (5), with $W$, target, and anchor incidence zero.

If this lift exists, adding it to the curvature-minus-bar chain kills (5)
and produces (1) with every protected readout zero.  Its degree-zero shadow
breaks the E14 endpoint-orientation class; its relative boundary supplies
the rootless $\Omega/q$-companion cancellation and one comparison vertex.

This is the smallest current construction target.  It is not an ordinary
coordinate derivative: the reciprocal note already shows that residual
Hasse directions need not be tangent to the GHZ source fibre.  The theorem
must explicitly lift that residual direction, including its augmented
ordinary-residue correction.

## Scope and verification

This is an exact no-go for the pinned bounded inventories and a positive
reduction of the curvature candidate to one tangent lift.  It is not an
all-source-resolution no-go and does not exclude a higher Spencer or
relative mapping-cone generator realizing the stated lift.

Run:

```text
python3 computations/verify_h3_shared_four_term_endpoint_word_change_inventory_boundary.py
python3 -O computations/verify_h3_shared_four_term_endpoint_word_change_inventory_boundary.py
python3 -I -S computations/verify_h3_shared_four_term_endpoint_word_change_inventory_boundary.py
```

Frozen ledger SHA-256:

```text
a20e1bebe7eeb5051a18636938a5d5c5b75fee144615be5a239610bcc7d39a1d
```
