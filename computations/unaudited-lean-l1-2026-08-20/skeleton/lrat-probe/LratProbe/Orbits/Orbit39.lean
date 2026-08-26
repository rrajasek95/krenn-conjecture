/- UNAUDITED — lane L1, generated. Orbit 39 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit39Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_39.cnf")

def orbit39CNF : CNF Nat :=
  orbit39Parsed.map (·.cnf) |>.getD []

theorem orbit39Parsed_ok : orbit39Parsed.isSome = true := by
  native_decide

theorem orbit39Unsat : orbit39CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit39CNF
    (include_str "../../artifacts/n8k4_39.lrat")
  native_decide

end LratProbe.Orbits
