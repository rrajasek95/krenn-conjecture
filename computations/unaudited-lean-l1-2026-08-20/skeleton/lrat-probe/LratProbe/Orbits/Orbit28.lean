/- UNAUDITED — lane L1, generated. Orbit 28 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit28Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_28.cnf")

def orbit28CNF : CNF Nat :=
  orbit28Parsed.map (·.cnf) |>.getD []

theorem orbit28Parsed_ok : orbit28Parsed.isSome = true := by
  native_decide

theorem orbit28Unsat : orbit28CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit28CNF
    (include_str "../../artifacts/n8k4_28.lrat")
  native_decide

end LratProbe.Orbits
