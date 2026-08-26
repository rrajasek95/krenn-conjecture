/- UNAUDITED — lane L1, generated. Orbit 45 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit45Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_45.cnf")

def orbit45CNF : CNF Nat :=
  orbit45Parsed.map (·.cnf) |>.getD []

theorem orbit45Parsed_ok : orbit45Parsed.isSome = true := by
  native_decide

theorem orbit45Unsat : orbit45CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit45CNF
    (include_str "../../artifacts/n8k4_45.lrat")
  native_decide

end LratProbe.Orbits
