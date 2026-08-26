/- UNAUDITED — lane L1, generated. N=6 orbit 12 of 13 (z=0 encoding). -/
import LratProbe.CnfCheck

namespace LratProbe.N6

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit12Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n6/n6_12.cnf")

def orbit12CNF : CNF Nat :=
  orbit12Parsed.map (·.cnf) |>.getD []

theorem orbit12Parsed_ok : orbit12Parsed.isSome = true := by
  native_decide

theorem orbit12Unsat : orbit12CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit12CNF
    (include_str "../../artifacts/n6/n6_12.lrat")
  native_decide

end LratProbe.N6
