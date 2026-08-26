/- UNAUDITED — lane L1, generated. Orbit 60 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit60Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_60.cnf")

def orbit60CNF : CNF Nat :=
  orbit60Parsed.map (·.cnf) |>.getD []

theorem orbit60Parsed_ok : orbit60Parsed.isSome = true := by
  native_decide

theorem orbit60Unsat : orbit60CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit60CNF
    (include_str "../../artifacts/n8k4_60.lrat")
  native_decide

end LratProbe.Orbits
