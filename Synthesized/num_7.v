/* Generated by Yosys 0.7 (git sha1 61f6811, gcc 6.2.0-11ubuntu1 -O2 -fdebug-prefix-map=/build/yosys-OIL3SR/yosys-0.7=. -fstack-protector-strong -fPIC -Os) */

(* src = "Test_Designs/num_7.v:6" *)
module num_7(A, B, C, D, Y);
  wire _0_;
  wire _1_;
  (* src = "Test_Designs/num_7.v:6" *)
  input A;
  (* src = "Test_Designs/num_7.v:6" *)
  input B;
  (* src = "Test_Designs/num_7.v:6" *)
  input C;
  (* src = "Test_Designs/num_7.v:6" *)
  input D;
  (* src = "Test_Designs/num_7.v:6" *)
  output Y;
  NAND2X1 _2_ (
    .A(A),
    .B(B),
    .Y(_0_)
  );
  NAND2X1 _3_ (
    .A(C),
    .B(D),
    .Y(_1_)
  );
  NOR2X1 _4_ (
    .A(_0_),
    .B(_1_),
    .Y(Y)
  );
endmodule
