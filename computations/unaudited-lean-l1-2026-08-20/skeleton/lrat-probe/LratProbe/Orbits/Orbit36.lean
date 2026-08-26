/- UNAUDITED — lane L1, generated. Orbit 36 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit36Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_36.cnf")

def orbit36CNF : CNF Nat :=
  orbit36Parsed.map (·.cnf) |>.getD []

theorem orbit36Parsed_ok : orbit36Parsed.isSome = true := by
  native_decide

theorem orbit36Unsat : orbit36CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit36CNF
    (include_str "../../artifacts/n8k4_36.lrat")
  native_decide

end LratProbe.Orbits
