/- UNAUDITED — lane L1, generated. Orbit 76 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit76Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_76.cnf")

def orbit76CNF : CNF Nat :=
  orbit76Parsed.map (·.cnf) |>.getD []

theorem orbit76Parsed_ok : orbit76Parsed.isSome = true := by
  native_decide

theorem orbit76Unsat : orbit76CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit76CNF
    (include_str "../../artifacts/n8k4_76.lrat")
  native_decide

end LratProbe.Orbits
