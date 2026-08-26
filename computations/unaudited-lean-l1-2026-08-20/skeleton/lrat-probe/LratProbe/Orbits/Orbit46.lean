/- UNAUDITED — lane L1, generated. Orbit 46 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit46Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_46.cnf")

def orbit46CNF : CNF Nat :=
  orbit46Parsed.map (·.cnf) |>.getD []

theorem orbit46Parsed_ok : orbit46Parsed.isSome = true := by
  native_decide

theorem orbit46Unsat : orbit46CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit46CNF
    (include_str "../../artifacts/n8k4_46.lrat")
  native_decide

end LratProbe.Orbits
