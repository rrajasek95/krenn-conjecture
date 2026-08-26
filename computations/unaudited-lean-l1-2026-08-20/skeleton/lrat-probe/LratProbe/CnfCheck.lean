/-
UNAUDITED — lane L1, staged 2026-08-20, pinned HEAD f9a3bd6.
Standalone feasibility probe: no mathlib, no formal-conjectures. Depends only
on `Std.Tactic.BVDecide.Reflect`, which ships inside leanprover/lean4:v4.27.0.

Purpose: measure the real cost of replaying one of our 87 N=8 diagonal orbit
refutations inside Lean, so the UNSAT layer of the full formalization can be
costed before any of the algebra is written.

The DIMACS parser follows the one in algal's krenn-gu-6x3-certificate
(KrennGuCertificate/CnfCheck.lean); the parse result is checked, so a
malformed input makes `parseDimacs` return `none` rather than silently
producing a different formula.
-/

import Std.Tactic.BVDecide.Reflect

namespace LratProbe

open Std.Sat
open Std.Tactic.BVDecide

/-- The declared header of a DIMACS file together with the parsed formula. -/
structure ParsedDimacs where
  declaredVars : Nat
  declaredClauses : Nat
  cnf : CNF Nat

private partial def parseClauses
    (tokens : List String) (current : CNF.Clause Nat := [])
    (clauses : CNF Nat := []) : Option (CNF Nat) :=
  match tokens with
  | [] =>
      if current.isEmpty then
        some clauses.reverse
      else
        none
  | token :: rest =>
      match token.toInt? with
      | none => none
      | some 0 => parseClauses rest [] (current.reverse :: clauses)
      | some literal =>
          let varNum := literal.natAbs
          if varNum = 0 then
            none
          else
            parseClauses rest
              ((varNum - 1, if literal > 0 then true else false) :: current)
              clauses

/-- Parse a DIMACS string. Returns `none` unless the body has exactly the declared number of
clauses and every variable is below the declared variable count. -/
def parseDimacs (input : String) : Option ParsedDimacs := do
  let tokens :=
    (input.split Char.isWhitespace).filter (fun token => !token.isEmpty)
      |>.map (·.toString) |>.toList
  let "p" :: "cnf" :: vars :: clauses :: body := tokens
    | none
  let some declaredVars := vars.toNat?
    | none
  let some declaredClauses := clauses.toNat?
    | none
  let some cnf := parseClauses body
    | none
  let variablesInRange :=
    cnf.all (fun clause =>
      clause.all (fun literal => literal.1 < declaredVars))
  if cnf.length = declaredClauses && variablesInRange then
    some { declaredVars, declaredClauses, cnf }
  else
    none

end LratProbe
