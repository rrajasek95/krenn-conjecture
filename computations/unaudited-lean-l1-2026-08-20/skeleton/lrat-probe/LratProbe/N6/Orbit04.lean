/- UNAUDITED — lane L1, generated. N=6 orbit 4 of 13 (z=0 encoding). -/
import LratProbe.CnfCheck

namespace LratProbe.N6

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit4Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n6/n6_4.cnf")

def orbit4CNF : CNF Nat :=
  orbit4Parsed.map (·.cnf) |>.getD []

theorem orbit4Parsed_ok : orbit4Parsed.isSome = true := by
  native_decide

theorem orbit4Unsat : orbit4CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit4CNF
    (include_str "../../artifacts/n6/n6_4.lrat")
  native_decide

end LratProbe.N6
