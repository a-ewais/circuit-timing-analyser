/* Generated by Yosys 0.7 (git sha1 61f6811, gcc 6.2.0-11ubuntu1 -O2 -fdebug-prefix-map=/build/yosys-OIL3SR/yosys-0.7=. -fstack-protector-strong -fPIC -Os) */

(* src = "Test_Designs/num_9.v:6" *)
module num_9(clk, A, B, C, D, cout);
  wire _00_;
  wire _01_;
  wire _02_;
  wire _03_;
  (* src = "Test_Designs/num_9.v:6" *)
  input A;
  (* src = "Test_Designs/num_9.v:6" *)
  input B;
  (* src = "Test_Designs/num_9.v:6" *)
  input C;
  (* src = "Test_Designs/num_9.v:6" *)
  input D;
  (* src = "Test_Designs/num_9.v:6" *)
  input clk;
  (* src = "Test_Designs/num_9.v:6" *)
  output cout;
  (* src = "Test_Designs/num_9.v:7" *)
  wire temp1;
  (* src = "Test_Designs/num_9.v:8" *)
  wire x;
  (* src = "Test_Designs/num_9.v:8" *)
  wire y;
  NOR2X1 _04_ (
    .A(A),
    .B(B),
    .Y(_02_)
  );
  AND2X2 _05_ (
    .A(A),
    .B(B),
    .Y(_03_)
  );
  NOR2X1 _06_ (
    .A(_02_),
    .B(_03_),
    .Y(x)
  );
  INVX1 _07_ (
    .A(D),
    .Y(_00_)
  );
  NAND2X1 _08_ (
    .A(temp1),
    .B(C),
    .Y(_01_)
  );
  NAND2X1 _09_ (
    .A(_00_),
    .B(_01_),
    .Y(y)
  );
  DFFPOSX1 _10_ (
    .CLK(clk),
    .D(y),
    .Q(cout)
  );
  DFFPOSX1 _11_ (
    .CLK(clk),
    .D(x),
    .Q(temp1)
  );
endmodule
