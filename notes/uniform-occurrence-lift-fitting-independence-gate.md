# A complete occurrence lift still needs a horizontal clean-parameter map

## Outcome

Grant the strongest natural form of the missing centered-occurrence
theorem:

1. the matching and endpoint association projectors lift to one augmented
   chain complex;
2. every centered occurrence class is the boundary of a physical relative
   cell;
3. all residual-edge restriction and insertion maps lift as chain maps;
4. their Euler sum is exact;
5. all component constants identify with one common carrier; and
6. these maps commute with multiplication by the internal \(q,r\) variables
   and with every clean binary parameter.

These clauses still do **not**, by themselves, force

\[
                         \bigwedge^h\mathcal M_f=0        \tag{1}
\]

or a common Bezout kernel.

The reason is an exact module separation. The occurrence lift resolves the
augmentation ideal of a finite occurrence module and retracts onto one
constant carrier line. It is parameter-degree zero. The Fitting wedge is a
statement about multiplication by degree-\(h\) clean binary forms on that
surviving carrier. Nothing in clauses 1--6 relates different binary
coefficients of those forms.

This is not only a type objection. For every \(h\ge3\) there is an explicit
filtered differential graded countermodel

\[
                         Q_{r,h}=L_r\otimes C_h          \tag{2}
\]

which satisfies clauses 1--6, carries the complete coefficientwise leading
moment lift and \(c_0=(r-2q)H_0\) as a boundary, but retains both:

* the exceptional adjacent class \(x_h\); and
* a two-copy common-carrier clean family
  \(\langle u^h,v^h\rangle\), whose Macaulay map has rank \(2h\).

Thus (1) fails in the countermodel. The missing datum after the occurrence
lift is exactly a **horizontal clean-parameter comparison with zero
based-loop residue**. It must send the physically lifted occurrence cell to
all required weighted Hilbert--Cauchy moments—or directly to one
simultaneous Bezout section.

The construction is a logical filtered-DGM counterguard, not a decorated
matching source and not a counterexample to Krenn's conjecture. It proves
that the proposed occurrence theorem and the Fitting theorem are distinct
statements even after granting strict chain-level restriction/insertion
naturality.

## 1. The universal occurrence resolution

Let

\[
 \Omega_r(V)=\{(p,s,R):p\ne s,\ R\text{ a perfect matching on }
                         V\setminus\{p,s\}\},
\qquad N_r=|\Omega_r|.
\]

Put \(O_r=k^{\Omega_r}\) and let
\(\epsilon_r:O_r\to k\) be the normalized augmentation

\[
                         \epsilon_r(o)={1\over N_r}\sum_f o_f. \tag{3}
\]

Define the two-term complex

\[
 (L_r)_1=O_r,\qquad (L_r)_0=O_r\oplus kH_0,
\qquad d_r(o)=(o,-\epsilon_r(o)H_0).                   \tag{4}
\]

There is a strict deformation retract

\[
 \begin{aligned}
 p_r(o,aH_0)&=(\epsilon_r(o)+a)H_0,\\
 i_r(aH_0)&=(0,aH_0),\\
 s_r(o,aH_0)&=o,
 \end{aligned}
\qquad
 d_rs_r+i_rp_r=\operatorname{id}.                      \tag{5}
\]

For a marked occurrence \(f\), the centered class

\[
                         c_{f,r}=N_re_f-\mathbf1         \tag{6}
\]

has zero augmentation, so

\[
                         d_r(c_{f,r})=(c_{f,r},0).       \tag{7}
\]

Thus every centered class has a literal relative filler while the complete
constant carrier survives.

This is deliberately stronger than merely postulating the one marked
centered cell produced by the association polynomial: (4) fills the entire
augmentation ideal simultaneously.

## 2. Every restriction/insertion square lifts canonically

Let \(T:O_r\to O_s\) be any occurrence-linear map and suppose its intended
map on the constant carrier is multiplication by \(c\in k\). There is a
canonical chain lift

\[
\begin{aligned}
 T_1^\#(o)&=To,\\
 T_0^\#(o,aH_0)
   &=\bigl(To,\,
       ca+c\epsilon_r(o)-\epsilon_s(To)\bigr)H_0.
\end{aligned}                                           \tag{8}
\]

Direct substitution gives

\[
                         T_0^\#d_r=d_sT_1^\#,\qquad
                         p_sT^\#=c\,p_r.                \tag{9}
\]

Composition is strict:

\[
                         (UT)^\#=U^\#T^\#.              \tag{10}
\]

Indeed, the two augmentation-correction terms telescope.

Apply (8) to every residual-edge restriction \(D_e\) with \(c=1\).
Apply it to reinsertion \(I_e\) with

\[
                         c={1\over\alpha_r},\qquad
 \alpha_r={N_r\over N_{r-1}}
          ={r(2r-1)\over r-1}.                         \tag{11}
\]

The coefficient identity

\[
                         \sum_e I_eD_e=(r-1)\operatorname{id} \tag{12}
\]

and

\[
 {|\binom{V}{2}|\over\alpha_r}=r-1                    \tag{13}
\]

give, by strict functoriality,

\[
                         \sum_e I_e^\#D_e^\#
                            =(r-1)\operatorname{id}_{L_r}. \tag{14}
\]

Thus \(L_r\) realizes not only the centered projector but also all of its
restriction/insertion faces, component constant transport, and Euler
reconstruction. The checker enumerates every occurrence and every
restriction/insertion component for \(r=2,3,4\).

Formula (8) also handles matching switches, endpoint moves, their mixed
commutator squares, and all polynomial combinations such as the cubic
endpoint association projector. Once the coefficient maps are specified,
their chain lifts exist and compose strictly in \(L_r\). Hence the
countermodel grants the complete formal physical-lift package at the
abstract augmented-chain level.

## 3. Why the Fitting module remains independent

Let \(C_h\) be the exact based-loop filtered module from the pinned
moment-lift theorem. It is a \(k[q,r]\)-linear complex with:

\[
 u_h=\sum_{j=2}^h q^{[h-j]}r^{[j]}=0,\qquad
 c_0=(r-2q)H_0\text{ exact},                            \tag{15}
\]

and even the coefficientwise associated-graded boundary

\[
                         (r-2q)(q+tr)^{[h-2]}.          \tag{16}
\]

Nevertheless its total homology contains

\[
                         0\ne[x_h],
 \qquad x_h=q^{[h]}+q^{[h-1]}r.                        \tag{17}
\]

The ambiguity is the based-loop space generated by

\[
 \eta_j(t)={d^{j-1}\over dt^{j-1}}
                  \bigl(t^j(1-t)^j\bigr),              \tag{18}
\]

whose weighted residues satisfy

\[
 \int_0^1t^s\,d\eta_j=0\ (s<j),\qquad
 \int_0^1t^j\,d\eta_j
       =(-1)^j{(j!)^3\over(2j+1)!}\ne0.                \tag{19}
\]

All loops in (18) have zero unweighted residue. Thus they preserve the
common \(H_0\), every occurrence restriction/insertion square, and the
entire coefficientwise associated graded, while independently moving the
higher moments needed by the Hilbert--Cauchy theorem.

Tensor (4) with \(C_h\). The maps

\[
                         p_r\otimes1,\qquad i_r\otimes1 \tag{20}
\]

exhibit \(Q_{r,h}=L_r\otimes C_h\) as a deformation retract of \(C_h\).
Therefore

\[
                         [x_h]\ne0\quad\text{in }H(Q_{r,h}). \tag{21}
\]

Every map \(T^\#\) acts on the first factor and the identity on \(C_h\).
It consequently commutes strictly with \(q,r\), with (15)--(16), and with
every binary clean parameter. This proves the claimed independence after
all occurrence faces have been physically lifted.

There is also a direct Fitting witness. Take two copies of the common
carrier line and put on them the clean forms

\[
                         f_0=u^h,\qquad f_1=v^h.        \tag{22}
\]

The \(h\) degree-\((h-1)\) shifts of \(f_0\) occupy

\[
 u^{2h-1},u^{2h-2}v,\ldots,u^hv^{h-1},
\]

while those of \(f_1\) occupy

\[
 u^{h-1}v^h,\ldots,v^{2h-1}.
\]

Together they are the complete monomial basis of
\(\operatorname {Sym}^{2h-1}k^2\). Hence

\[
                         \operatorname {rank}\mu_{\langle
                              u^h,v^h\rangle}=2h,       \tag{23}
\]

so the simultaneous Bezout kernel is zero and the top Fitting wedge is
nonzero. Occurrence-centered directions remain exact in each copy, because
the clean forms multiply the surviving carrier coordinate after the
deformation retract.

This two-copy witness is not asserted to be the clean family of a physical
Krenn source. It proves that even a complete occurrence lift, viewed as a
chain-theoretic hypothesis, does not constrain the surviving carrier-valued
binary forms without an additional map.

## 4. The exact additional theorem

The occurrence theorem would imply the Fitting cut only after adding a map

\[
 \mathcal H_h:
 H_1(\text{physically lifted occurrence bicomplex})
       \longrightarrow
 \{\text{horizontal polynomial one-forms in the clean parameter}\} \tag{24}
\]

with all of the following properties.

1. **Moment image.** Its coefficientwise boundary is
   \[
                 (r-2q)(q+tr)^{[h-2]}\,dt.
   \]
2. **Zero loop residue.** Every vertical cycle in the kernel of the
   physical occurrence evaluation has zero image under all required
   moments
   \[
                 \int_0^1t^s(\cdot),\qquad
                 1\le s\le\max(1,h-3).
   \]
3. **Clean-family compatibility.** The resulting relations act on every
   scalar coordinate of the same clean error family, not on one selected
   word or resultant.
4. **Fitting normalization.** Their final readout is either a nonzero
   common Bezout section or a source-provenant Hilbert--Burch matrix of
   total column degree at most \(h-1\).
5. **Physical terminal typing.** Failure of any clause lands in the
   complete target/anchor/\(q\)/\(W\)/residue/terminal quotient, rather than
   an occurrence-only cokernel.

Equivalently, one may construct a source saturation theorem proving that
the based vertical loop module in (19) is zero after the physical
restriction/insertion lift. Mere contractibility of the occurrence
augmentation ideal does not prove this: the loop lives in the independent
horizontal clean-parameter direction.

At \(h=3\), clauses 1--2 reduce to the already isolated first weighted
relation

\[
                         c_1=(r-2q)H_1=0.               \tag{25}
\]

The occurrence lift can give the unweighted active-clean-or-\(c_0\)
alternative, but (25) is still required to kill \(x_3\). Uniformly, the
same distinction persists through the full required moment tower.

## 5. Scope and audit

This theorem does **not** say that a genuine physical occurrence lift is
useless. It would be major progress: it constructs the common \(H_0\)
carrier, closes the active-clean-or-\(c_0\) fork, and supplies the domain on
which the higher horizontal obstruction is physically typed.

It says only that the occurrence lift does not *formally imply* the Fitting
wedge. The additional horizontal/zero-residue theorem is load-bearing.
The countermodel is not a finite decorated source, does not satisfy the
full GHZ matching equations, and does not refute a source-specific theorem
which proves that physical site gluing kills every based loop.

The dependency-pinned checker
[verify_uniform_occurrence_lift_fitting_independence_gate.py](../computations/verify_uniform_occurrence_lift_fitting_independence_gate.py)

* constructs the exact deformation retract (4)--(5);
* enumerates and lifts every residual restriction/insertion at
  \(r=2,3,4\);
* verifies (7), (9), and the normalized Euler law (14);
* verifies the exact \(c_0\)-only nonmembership and the full-rank based-loop
  residue matrix for \(3\le h\le12\); and
* verifies the pure-axis Macaulay rank \(2h\) for the same orders.

The displayed constructions and triangular residue proof are uniform; the
finite ranges are regression audits. The checker is standard-library only
and runs unchanged under normal, optimized, and isolated/no-site Python.
