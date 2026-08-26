/- UNAUDITED — lane L1, generated. Orbit 33 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit33Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_33.cnf")

def orbit33CNF : CNF Nat :=
  orbit33Parsed.map (·.cnf) |>.getD []

theorem orbit33Parsed_ok : orbit33Parsed.isSome = true := by
  native_decide

theorem orbit33Unsat : orbit33CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit33CNF
    (include_str "../../artifacts/n8k4_33.lrat")
  native_decide

end LratProbe.Orbits
