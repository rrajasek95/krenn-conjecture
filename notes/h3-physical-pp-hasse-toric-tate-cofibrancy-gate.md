# The physical PP/Hasse packet first misses the toric Tate resolution in degree one

## Exact result

Fix response head/word `11:110000`.  With two endpoint orientations `e0,e1`
and the three residual `K4` matchings `q0,q1,q2`, the six occurrence
coordinates form the physical Segre block

\[
 U=(u_{rj})=\begin{pmatrix}e_0q_0&e_0q_1&e_0q_2\\
                             e_1q_0&e_1q_1&e_1q_2\end{pmatrix}.
\]

The committed complete unary/response and endpoint/matching PP/Hasse packet
is **not** a cofibrant resolution of this occurrence presentation.  Its first
missing source cells occur already in homological degree one: the three
quadratic toric homotopies

\[
 d\epsilon_{ij}=F_{ij}=u_{0i}u_{1j}-u_{0j}u_{1i},\qquad 0\le i<j\le2. \tag{1}
\]

At a generic physical point the factor tangent has rank `4` in the
six-dimensional occurrence space, while the three gradients `dFij` have
rank `2` and annihilate that tangent.  Thus (1) is a genuine two-dimensional
conormal deficit, not a redundant rewriting of complete response rows.

Checker:

```text
computations/verify_h3_physical_pp_hasse_toric_tate_cofibrancy_gate.py
```

Frozen ledger digest:

```text
6d23b4b0f1bed023acf058479c275c8a20b7d7b0220f439c4897868a86ff42ee
```

## Minimal Tate comparison through cubic degree

The Segre ideal has the Hilbert--Burch resolution

\[
 0\longrightarrow S(-3)^2\longrightarrow S(-2)^3
 \longrightarrow S\longrightarrow S/I\longrightarrow0. \tag{2}
\]

After adjoining the three degree-one generators in (1), its first two
coherence cells have boundaries given by

\[
\begin{aligned}
 u_{02}F_{01}-u_{01}F_{02}+u_{00}F_{12}&=0,\\
 u_{12}F_{01}-u_{11}F_{02}+u_{10}F_{12}&=0. \tag{3}
\end{aligned}
\]

For the generic test point
`(e0,e1;q0,q1,q2)=(1,2;1,3,5)`, the constant occurrence shear reads the
three conormals by `(2,4,2)`.  Both coefficient vectors in (3) kill this
triple, providing an exact differentiated cubic check.

Equations (3) exist as polynomial identities, but they are not presently
source-labelled physical degree-two Tate cells.  More importantly, no
cubic identity can repair the missing degree-one homotopies (1).

## Why the known PP/Hasse faces do not supply (1)

- Complete unary and response derivatives are factor tangents of
  `u_rj=e_r q_j`, hence every `dFij` kills them.
- The endpoint `B-4`, `B-2`, and `B+2` product-rule packets have independent
  private rank `3` but only one common target-normal line.  Their bare
  two-step diamonds are flat.
- The six-term matching face `db01` has target and central-Eq readouts zero,
  but is aggregate: it forgets the termwise matching-standard occurrence
  classes detected by the toric conormal.
- Endpoint length-three Hasse paths have residual `C2` matching isotropy.
  Maschke contracts that standard isotropy only after a termwise natural
  pointed source section has been supplied.  It is coherence for a section,
  not the missing quadratic section itself.

Thus the quadratic/mixed/cubic PP hierarchy is compatible with a future
Tate augmentation, but it is not that augmentation.

## Exact grading and augmented rows

Each `u_rj` is a literal occurrence monomial with one `p`, one `s`, and the
two `q` factors of residual matching `j`.  The two terms in `Fij` have the
same doubled word, fine, and repeated-edge multidegree
`e0 e1 qi qj`.  They have target `0` and central Eq-incidence `0`.

The two cubic rows have respective multidegrees
`e0^2 e1 q0 q1 q2` and `e0 e1^2 q0 q1 q2`, again with target and central Eq
zero.  This equality of polynomial grades does not identify them with the
existing Hasse cells, whose source labels and PP order are attached to a
single physical response occurrence.

## Sharp frontier

The minimal local repair is therefore:

1. construct a source-valid, word/fine/repeated-grade family of the three
   cells `epsilon_ij` in (1) (two are generically independent);
2. supply the two Hilbert--Burch coherence cells (3), equivariantly over the
   endpoint/matching action groupoid;
3. only then transport the already-audited target-normal, Eq, q, ridge and
   cap readouts.

This theorem concerns the canonical `h=3` fixed-head response packet and
the currently committed complete unary/response/endpoint/matching PP/Hasse
inventory.  It does not exclude a larger, as-yet-unconstructed physical
Tate/PP source complex.
