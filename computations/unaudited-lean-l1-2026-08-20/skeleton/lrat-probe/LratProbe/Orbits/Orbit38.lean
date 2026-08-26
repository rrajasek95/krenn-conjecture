/- UNAUDITED — lane L1, generated. Orbit 38 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit38Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_38.cnf")

def orbit38CNF : CNF Nat :=
  orbit38Parsed.map (·.cnf) |>.getD []

theorem orbit38Parsed_ok : orbit38Parsed.isSome = true := by
  native_decide

theorem orbit38Unsat : orbit38CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit38CNF
    (include_str "../../artifacts/n8k4_38.lrat")
  native_decide

end LratProbe.Orbits
