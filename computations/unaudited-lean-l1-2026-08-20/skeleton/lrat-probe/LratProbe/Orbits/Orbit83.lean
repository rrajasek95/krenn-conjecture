/- UNAUDITED — lane L1, generated. Orbit 83 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit83Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_83.cnf")

def orbit83CNF : CNF Nat :=
  orbit83Parsed.map (·.cnf) |>.getD []

theorem orbit83Parsed_ok : orbit83Parsed.isSome = true := by
  native_decide

theorem orbit83Unsat : orbit83CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit83CNF
    (include_str "../../artifacts/n8k4_83.lrat")
  native_decide

end LratProbe.Orbits
