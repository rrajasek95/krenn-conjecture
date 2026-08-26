/- UNAUDITED — lane L1, generated. Orbit 61 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit61Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_61.cnf")

def orbit61CNF : CNF Nat :=
  orbit61Parsed.map (·.cnf) |>.getD []

theorem orbit61Parsed_ok : orbit61Parsed.isSome = true := by
  native_decide

theorem orbit61Unsat : orbit61CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit61CNF
    (include_str "../../artifacts/n8k4_61.lrat")
  native_decide

end LratProbe.Orbits
