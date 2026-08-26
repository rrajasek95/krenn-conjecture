# Face `0:31:15`, `R=0,J!=0` exact characteristic-zero gate

Status: **exact full-source interface and terminal timeout frozen; no
algebraic verdict.**

## Exact two-step elimination

On `d2-1!=0`, raw 16 solves

```text
a2=-B/[b4*(d2-1)].
```

The shortest reduced row raw 9 has

```text
raw9=a5*b3*J*b5+S,
J=a4*b4*d3-b3.
```

On the present `J!=0` branch, already-live `a5,b3` therefore give the
faithful second solve

```text
b5=-S/(a5*b3*J).
```

After fraction-free substitution, every nonzero literal source numerator is
retained: raw `6,7,8,10,11,12,13,14,15,17,18,19,20,21`. Raw 9 and raw 16
vanish under their own solves. Raw 11 remains exactly live-equivalent to the
transformed resultant through `A*raw11=R`, where
`A=b4*(d2-1)` is live; primitive numerator cancellation is recorded rather
than misreported as byte equality.

The ten remaining geometric variables are

```text
a0,a1,a3,a4,a5,b3,b4,d1,d2,d3.
```

The Rabinowitsch row contains every surviving original live numerator after
both substitutions and the explicit branch guards `d2-1,J`. It does not
localize the numerator `S`, because the eliminated `b5` was not an original
live coordinate. The expanded localizer has 55,408 terms. The strict
coefficient-first characteristic-zero input SHA-256 is
`e173be4ce4da1cfbd77327c11e1262bd699991fd106546394d299241da4e519c`.

## Sole bounded exact run

Exactly one guarded msolve process was launched with characteristic zero,
DRL, 8 threads, deterministic seed 1, and a 600-second cap. It reached the
cap at 600.688 seconds and was terminated by the runner (`returncode=-15`).
The output is zero bytes and contains no empty, positive-dimensional, or RUR
sentinel. The terminal manifest logical digest is
`55dd2cc7add19461936b6d53325de7612a2568f93d3611b0c6170cef70f564b5`.
No alternate or duplicate solver run was made.

## Replay

The exact source exporter was replayed under standard, `-O`, and isolated
`-I -S`; each produced the identical input SHA, 14-row ledger, 55,408-term
localizer profile, and source-export logical digest
`136487768ed26054df87d90ff0f83a5db2ce2acfe05c6634f78b90b421ad1a91`.
The terminal auditor verifies every frozen polynomial digest, the timeout
manifest, zero-byte sentinel rejection, and source/Rabinowitsch mutations.
Its mode digests are

```text
standard  145f4a2094a1054f4bb5b58081e4cccfafd1a89f176ad140e984e9cdb7269bed
-O        071b28d971f31c3a9ee82c0b698cf5ba0d5b8f7f93472773e6cf9508314f61ae
-I-S      4ab3734943dac7a0514a52d237fd838af6f433fcd4bfa70931e39df773b2df76
```

Exporter, auditor, input, and manifest SHA-256 values are
`be40a207bbcfb98929c261323fd86c35f25f00848f6549cd9a256ac4dd9c0aa8`,
`639e8cbfbb19db6806d1b38f2bfe2db1b94e77d0417065b1156d443576352a28`,
`e173be4ce4da1cfbd77327c11e1262bd699991fd106546394d299241da4e519c`,
and `4ed44f92f7b35db569595511d87cbed583df1a5b695e85fb12b6eba54cef5f31`.

## Residual

The timeout is a resource terminal only. It neither closes nor exhibits a
component of the `J!=0` branch. Together with the separately frozen timeouts
for `d2=1` and `J=0,U=0`, all three exact subbranches of the current
`0:31:15` structural split remain open.
