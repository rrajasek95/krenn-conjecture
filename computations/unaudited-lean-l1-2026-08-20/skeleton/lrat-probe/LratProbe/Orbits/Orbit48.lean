/- UNAUDITED — lane L1, generated. Orbit 48 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit48Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_48.cnf")

def orbit48CNF : CNF Nat :=
  orbit48Parsed.map (·.cnf) |>.getD []

theorem orbit48Parsed_ok : orbit48Parsed.isSome = true := by
  native_decide

theorem orbit48Unsat : orbit48CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit48CNF
    (include_str "../../artifacts/n8k4_48.lrat")
  native_decide

end LratProbe.Orbits
