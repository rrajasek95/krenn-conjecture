/- UNAUDITED — lane L1, generated. Orbit 74 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit74Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_74.cnf")

def orbit74CNF : CNF Nat :=
  orbit74Parsed.map (·.cnf) |>.getD []

theorem orbit74Parsed_ok : orbit74Parsed.isSome = true := by
  native_decide

theorem orbit74Unsat : orbit74CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit74CNF
    (include_str "../../artifacts/n8k4_74.lrat")
  native_decide

end LratProbe.Orbits
