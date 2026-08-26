/- UNAUDITED — lane L1, generated. Orbit 70 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit70Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_70.cnf")

def orbit70CNF : CNF Nat :=
  orbit70Parsed.map (·.cnf) |>.getD []

theorem orbit70Parsed_ok : orbit70Parsed.isSome = true := by
  native_decide

theorem orbit70Unsat : orbit70CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit70CNF
    (include_str "../../artifacts/n8k4_70.lrat")
  native_decide

end LratProbe.Orbits
