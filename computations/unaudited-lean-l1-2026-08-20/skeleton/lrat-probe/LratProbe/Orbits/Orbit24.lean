/- UNAUDITED — lane L1, generated. Orbit 24 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit24Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_24.cnf")

def orbit24CNF : CNF Nat :=
  orbit24Parsed.map (·.cnf) |>.getD []

theorem orbit24Parsed_ok : orbit24Parsed.isSome = true := by
  native_decide

theorem orbit24Unsat : orbit24CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit24CNF
    (include_str "../../artifacts/n8k4_24.lrat")
  native_decide

end LratProbe.Orbits
