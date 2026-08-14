# Support 16: directed-incidence response orbits

The exact checker is
[`verify_n8_support16_directed_incidence_response_orbits.py`](../computations/verify_n8_support16_directed_incidence_response_orbits.py).

## Result

The 376 directed high/high incidences left by the arbitrary-anchor scope
audit are not globally invisible.  Quotienting separately inside each of the
22 two-`RRX` support representatives by its literal graph automorphism
stabilizer gives

```text
directed incidences                         376
stabilizer orbits                           281
orbit sizes                     1:208, 2:62, 4:11
shared roles                                  52
never-private roles                          324
blocks occurring in another cap response    376
```

Here `shared` means the directed incidence is the high endpoint's shared
edge in at least one minimum cubic/high two-`RRX` face.  It is invisible to
that face's selected crossed two-term tensor, but may occur elsewhere.
`never-private` means it is not a private high-endpoint role in any such
minimum face.  These two cases exhaust the old unlanded register.

The role and endpoint-degree census, first weighted by directed incidences
and then by stabilizer orbits, is

```text
role             degree pair     incidences     orbits
shared              (4,4)             18           15
shared              (4,5)             29           19
shared              (4,6)              5            2
never-private       (4,4)            137          106
never-private       (4,5)            156          114
never-private       (4,6)             11            8
never-private       (5,5)             20           17
```

Every underlying high/high block occurs as a literal response factor for
between two and seven other cap edges.  The incidence-weighted histogram is

```text
number of response caps       2    3    4    5    6   7
directed incidences          52  121  139   48   14   2
```

Thus there is a genuine finite routing theorem: no member of the 376-cell
register is absent from the physical response grammar.  Appearance is not,
however, the same as a clean landing.

## The smallest response-sparse orbit

There are many singleton stabilizer orbits.  Order them first by the number
of response terms and caps, preferring never-private roles.  The first is

```text
support representative index       1
directed incidence                  0 -> 02
endpoint degrees                    (6,4)
stabilizer orbit size               1
other response caps                 35, 45
terms containing R02                1 at each cap
```

The representative support is

```text
01 02 03 04 05 07 14 16 17 23 25 27 35 36 45 46.
```

In the free response-factor algebra the complete physical response at cap
`35` is

\[
 x_{17}\bigl(
 R_{02}R_{46}+R_{04}R_{26}+R_{06}R_{24}
 \bigr).                                                \tag{1}
\]

The complete response at cap `45` is

\[
\begin{aligned}
 &x_{27}R_{01}R_{36}+x_{17}R_{02}R_{36}
 +x_{17}R_{03}R_{26}\\
 &\qquad{}+x_{27}R_{06}R_{13}
 +x_{07}R_{12}R_{36}+x_{07}R_{13}R_{26}.               \tag{2}
\end{aligned}
\]

The products in (1)--(2) denote the source-labelled tensor contractions of
the response grammar; the checker retains the live `x` tag and both response
block labels for every residual matching.  No support-only abbreviation was
used to delete companion terms.

## Basis-free rank-stratum test

Let `M` be one response block and let `I_M` be the contraction ideal generated
by its image factors.  A kernel choice through `M` can kill a complete
response for arbitrary companion blocks only if the response lies in
`I_M`.  In the free physical-monomial grading this is equivalent to every
monomial containing `M`.  The converse is immediate by evaluating `M=0`;
the formulation is basis-free because the image/contraction ideal is
preserved by changes of basis on the two endpoint spaces.

This recovers the old private-role theorem: its selected two-term tensor has
the anchored response factor in every term.  It does **not** land `0 -> 02`.
Modulo `I_{R02}`, (1) retains two monomials and (2) retains five.  Hence a
noncoordinate kernel of `R02` only removes the displayed `R02` summand; it
does not force either full response to vanish.

This is an exact no-go for the companion-independent kernel extension.  It
is not an exact GHZ source counterexample.  The shortest remaining positive
statement must use cross-cap relations to cancel or constrain the residues
of (1) and (2), or prove that exact mixed rows forbid this rank stratum.  A
mere response-occurrence argument cannot close the arbitrary directed-anchor
caveat.

## Reproduction

```sh
python3 computations/verify_n8_support16_directed_incidence_response_orbits.py
python3 -O computations/verify_n8_support16_directed_incidence_response_orbits.py
python3 -I -S computations/verify_n8_support16_directed_incidence_response_orbits.py
```

Pinned ledger SHA-256:

```text
dcc23f485e692fa493b829ae5b73bb7ffef348d746bcebbfbb5301cce3373b54
```
