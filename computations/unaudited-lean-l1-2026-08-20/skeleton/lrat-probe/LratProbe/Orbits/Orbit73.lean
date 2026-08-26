/- UNAUDITED — lane L1, generated. Orbit 73 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit73Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_73.cnf")

def orbit73CNF : CNF Nat :=
  orbit73Parsed.map (·.cnf) |>.getD []

theorem orbit73Parsed_ok : orbit73Parsed.isSome = true := by
  native_decide

theorem orbit73Unsat : orbit73CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit73CNF
    (include_str "../../artifacts/n8k4_73.lrat")
  native_decide

end LratProbe.Orbits
