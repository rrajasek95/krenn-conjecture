/- UNAUDITED — lane L1, generated. Orbit 54 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit54Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_54.cnf")

def orbit54CNF : CNF Nat :=
  orbit54Parsed.map (·.cnf) |>.getD []

theorem orbit54Parsed_ok : orbit54Parsed.isSome = true := by
  native_decide

theorem orbit54Unsat : orbit54CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit54CNF
    (include_str "../../artifacts/n8k4_54.lrat")
  native_decide

end LratProbe.Orbits
