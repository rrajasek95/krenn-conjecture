/- UNAUDITED — lane L1, generated. Orbit 19 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit19Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_19.cnf")

def orbit19CNF : CNF Nat :=
  orbit19Parsed.map (·.cnf) |>.getD []

theorem orbit19Parsed_ok : orbit19Parsed.isSome = true := by
  native_decide

theorem orbit19Unsat : orbit19CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit19CNF
    (include_str "../../artifacts/n8k4_19.lrat")
  native_decide

end LratProbe.Orbits
