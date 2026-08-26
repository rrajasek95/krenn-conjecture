/- UNAUDITED — lane L1, generated. Orbit 29 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit29Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_29.cnf")

def orbit29CNF : CNF Nat :=
  orbit29Parsed.map (·.cnf) |>.getD []

theorem orbit29Parsed_ok : orbit29Parsed.isSome = true := by
  native_decide

theorem orbit29Unsat : orbit29CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit29CNF
    (include_str "../../artifacts/n8k4_29.lrat")
  native_decide

end LratProbe.Orbits
