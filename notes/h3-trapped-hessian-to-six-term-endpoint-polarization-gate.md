# Endpoint transpose completes the trapped Hessian symbol in a conjugate grade

## Exact result

The proposed Spencer map has no word or principal-symbol mystery.  Embed
the marked trapped occurrence at the two external endpoint sites `P=6` and
`S=7`:

\[
 f=P0{:}11\mid S1{:}11\mid23{:}00\mid45{:}00.          \tag{1}
\]

Swap tail sites `3,4` and recolour `0->1` at tail sites `2,3,4,5`.  This
sends (1) exactly to the Interface-I corner

\[
 E_+T_0=P0{:}11\mid S1{:}11\mid24{:}11\mid35{:}11     \tag{2}
\]

in the pure word `11111111`.  The tail Weyl action at sites `2,5` sends it
to the mixed word `11211211`, and the endpoint swap `s=(0 1)` changes
`E_+` to `E_-`.  Therefore

\[
 (1-s)(w-1)E_+T_0
   =-E_+T_0+E_-T_0+E_+T_1-E_-T_1,                     \tag{3}
\]

with the required `alpha=(-1,1,1,-1)` signs.

Before adjoining the transpose chart, the first exact obstruction occurs
after polarization.  Interface II fixed
the right endpoint rows and varied only `p,q`.  Its second Hasse symbol can
therefore contain a `P` endpoint direction and a tail direction, but never
an `S` endpoint direction.  After (3) it gives exactly eight labelled
`P-tail` pairs.  The physical Interface-I class has sixteen terms:

\[
 C_2^{\rm full}=C_2^P\oplus C_2^S,
 \qquad \dim C_2^P=\dim C_2^S=8.                      \tag{4}
\]

The missing eight `S-tail` pairs are the endpoint-polarization Ext packet.
Physical Cartan source-orbit descent preserves the `P/S` endpoint type and
cannot fill it by itself.  The combined physical endpoint transpose below
does fill it, but transports the canonical six-term readout to a conjugate
repeated fine grade.

Checker:
[`verify_h3_trapped_hessian_to_six_term_endpoint_polarization_gate.py`](../computations/verify_h3_trapped_hessian_to_six_term_endpoint_polarization_gate.py).

## 1. Literal Hasse calculation

Order the four corners as

```text
E+T0, E-T0, E+T1, E-T1
```

and sum their second Hasse shadows with coefficients `alpha`.  The complete
four-edge calculation has six pairs per corner.  Endpoint-endpoint and
tail-tail pairs cancel in the signed sum.  What remains is exactly the
sixteen endpoint-tail products already identified with `-delta`.

For the fixed-right source map `A` of `dac1248`, omit the `S` edge before
taking the second shadow.  Each corner then has three moving factors:

```text
one P endpoint edge + two q tail edges.
```

The tail-tail term again cancels between endpoint orientations, leaving two
`P-tail` terms per corner, eight in total.  The transpose fixed-left chart
omits `P` and leaves the disjoint eight `S-tail` terms.  Exact enumeration
gives

\[
             C_2^P+C_2^S=C_2^{\rm full},
             \qquad C_2^P\cap C_2^S=0.                \tag{5}
\]

Both the endpoint swap and the tail Weyl action preserve whether the
external edge is incident with `P` or `S`; hence the split (4) is invariant
under the Cartan square.

There is a useful warning.  Forgetting the literal pair labels and retaining
only four corner coefficients sends both halves to

\[
                         2\alpha,                      \tag{6}
\]

while the complete class maps to `4 alpha`.  Thus either half can be
rescaled to the expected coarse `-delta` vector.  A four-coordinate residue
check cannot detect the missing right-endpoint polarization; the sixteen
physical endpoint-tail labels are load-bearing.

## 2. The exact commuting square and its defect

The naturality supplied by polarization and physical Cartan descent defines
the upper and left arrows in

\[
\begin{CD}
 H^2_{p,q}(f) @>{\text{tail normalization}}>>
       H^2_{P,q}(E_+T_0)\\
 @V{\text{odd Cartan/Weyl}}VV @VV{\text{corner shadow}}V\\
 \text{fixed-right Hessian cone} @>>> C_2^{\rm full}.
\end{CD}                                                \tag{7}
\]

The bottom image is `C_2^P`, not `C_2^full`.  Consequently the obstruction
to completing (7) is the single labelled packet

\[
                 \epsilon_S=[C_2^S]
                 \in C_2^{\rm full}/C_2^P.             \tag{8}

It has eight independent coordinate pivots.  This is one Ext class (one
equivariant packet), not eight unrelated support cases.

The smallest positive extension is symmetric and concrete: append the 36
right-endpoint `s` columns to the existing `36 p + 135 q` domain and use
the full marked polar

\[
 df=sq_{23}q_{45}\,dp+pq_{23}q_{45}\,ds
    +psq_{45}\,dq_{23}+psq_{23}\,dq_{45}.              \tag{9}

Then construct the transpose fixed-left Hessian comparison in the same
word/fine/repeated grade.  Its associated symbol must be exactly
`epsilon_S`; the remaining work is compatibility with the augmented
target/residue/anchor/eta/sigma rows.  Without the `s` columns, no
combination of the existing tail Weyl and endpoint-site Cartan operations
can create (8).

There is in fact a canonical transpose construction at the associated
symbol.  Endpoint transpose alone exchanges `E+` and `E-` and reverses
`alpha`.  Compose it with the residual endpoint-site swap `0<->1`.  The
resulting involution

\[
 \vartheta=(P\leftrightarrow S,\;G_{ij}\leftrightarrow G_{ji})
             \circ(0\leftrightarrow1)                 \tag{9a}
\]

fixes every four-edge corner `E+/- T0/1`, fixes the protected marked product
`f`, and sends `C2^P` exactly to `C2^S` with the correct coefficient.  The
complete source equations are equivariant:

\[
 p_i s_jq^{[2]}=\delta_{ij}X_i
 \quad\longleftrightarrow\quad
 p_j s_iq^{[2]}=\delta_{ji}X_j,                        \tag{9b}
\]

while the unary equation is fixed.  Target and word are fixed because the
two selected endpoint colours agree.  Ordinary residue and eta/sigma
transport equivariantly; `eta_0,eta_1` are relabelled and the external
`P-S` sigma edge is fixed.  Consequently the full 16-term
associated-graded Spencer square **is constructed** after adjoining the
right endpoint columns.

The construction stops at the next, literal grading layer.  Applying
`vartheta` to the pinned canonical faces-`(3,5)` fine degree changes that
24-coordinate degree, and applying it to the six private matching features
gives six disjoint features.  Hence

\[
                    \vartheta(\Lambda)=\Lambda^\top
                    \ne\Lambda                         \tag{9c}
\]

as labelled readouts.  Both are physical, but they live in conjugate
repeated components.  Thus transpose removes the endpoint-polarization Ext
packet; the remaining arrow is a shifted repeated-grade comparison taking
the transpose component back to the canonical component while preserving
the augmented terminals.

## 3. The curvature-dual shortcut is not yet typed for active landing

If a tangent `xi` does not prolong, the graph/Hessian theorem gives a
physical output covector

\[
                  \psi A=0,
          \qquad \psi(F_{[2]}(\xi))\ne0.               \tag{10}

This makes `psi o F` an intrinsic second-fundamental-form carrier.  The
currently committed active-fan/Fitting theorems require more: a contraction
in one response head/output packet, a nonzero evaluated decorated
cofactor/minor, and visible endpoint arms.  Exact Fredholm duality does not
force `psi` to be supported in one word or response head; cancellations
between unary and response blocks or between heads are allowed.  Nor does a
nonzero scalar pairing in (10) factor it into the common-`q` endpoint minor
used by the active route.

Therefore (10) is not yet a terminal active carrier.  It would become one
under either of the following precise additional theorems:

1. **block-local curvature:** choose a detecting `psi` in one response
   head/word whose Hessian is a decomposable endpoint/common-`q` minor; or
2. **curvature decomposition:** split every detecting physical output dual
   into typed response-head carriers, one of which has nonzero endpoint
   visibility.

Either theorem could bypass `epsilon_S`.  Neither follows from the existing
row-space or common-covector statements.

## 4. The raw symbol does not project to the common reduced-Eq class

The odd and even comparison lanes both expose the physical conormal

\[
                         (H_0-u)e_{\rm Eq}.             \tag{11}
\]

It is tempting to identify (8), or the original trapped Hessian, with (11).
The complete response-to-principal-parts symbol does not make this
identification.  Hasse polarization preserves the source-generator label:
the Interface-II class is the second face of the response generator
`R_11,110000`, and after the exact normalization above its image is
`C2^P` in the response endpoint-tail sector.  Its projection to the
independent unary/pure-Eq conormal row is zero.

The occurrence graph does not supply the missing label change.  Its private
coordinate satisfies

\[
                              u_f=f,                   \tag{12}
\]

so it varies with the marked occurrence.  The `u` in (11) is the global
homogenizing target coordinate of the normalized pure row.  Identifying
`u_f` with `u` would add the new source equation `f=u`; it is not the
contractible graph base change audited in `46ec0f4`.

Thus the three interfaces may still share one final cell, but only in the
following precise sense: an **off-diagonal response-to-Eq mapping-cone
comparison** could carry both the missing endpoint packet `epsilon_S` and
the reduced-Eq face (11), together with the augmented readouts.  That cell
is the missing descent map.  After the transpose construction above,
`epsilon_S` itself is no longer missing at associated grade; what remains is
to transport its conjugate repeated grade and attach the Eq face.  The
diagonal PP/Hasse symbol itself sends the trapped Hessian to response grade,
not to (11).

## Scope

This proves the associated-graded word normalization, Cartan signs, full
literal endpoint-polarization split, and constructs the missing half by the
physical endpoint transpose.  It isolates the next failure at the canonical
repeated fine grade/six-term readout and rules out a direct diagonal-symbol
identification with the common reduced-Eq class.  It does not construct the
shifted-grade/off-diagonal Eq comparison, its augmented terminals, or a
block-local active carrier from an arbitrary curvature dual.

Run:

```text
python3 computations/verify_h3_trapped_hessian_to_six_term_endpoint_polarization_gate.py
python3 -O computations/verify_h3_trapped_hessian_to_six_term_endpoint_polarization_gate.py
python3 -I -S computations/verify_h3_trapped_hessian_to_six_term_endpoint_polarization_gate.py
```

Frozen ledger SHA-256:

```text
7f7f7b08d626af8ef8f27276f43b6b558d54cb6b11b7b1a065ba2176a4d1d98c
```
