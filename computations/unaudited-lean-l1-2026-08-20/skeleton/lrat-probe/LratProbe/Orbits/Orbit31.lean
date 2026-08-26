/- UNAUDITED — lane L1, generated. Orbit 31 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit31Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_31.cnf")

def orbit31CNF : CNF Nat :=
  orbit31Parsed.map (·.cnf) |>.getD []

theorem orbit31Parsed_ok : orbit31Parsed.isSome = true := by
  native_decide

theorem orbit31Unsat : orbit31CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit31CNF
    (include_str "../../artifacts/n8k4_31.lrat")
  native_decide

end LratProbe.Orbits
