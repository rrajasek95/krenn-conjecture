/- UNAUDITED — lane L1, generated. Orbit 80 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit80Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_80.cnf")

def orbit80CNF : CNF Nat :=
  orbit80Parsed.map (·.cnf) |>.getD []

theorem orbit80Parsed_ok : orbit80Parsed.isSome = true := by
  native_decide

theorem orbit80Unsat : orbit80CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit80CNF
    (include_str "../../artifacts/n8k4_80.lrat")
  native_decide

end LratProbe.Orbits
