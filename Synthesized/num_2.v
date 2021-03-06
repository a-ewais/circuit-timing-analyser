/* Generated by Yosys 0.7 (git sha1 61f6811, gcc 6.2.0-11ubuntu1 -O2 -fdebug-prefix-map=/build/yosys-OIL3SR/yosys-0.7=. -fstack-protector-strong -fPIC -Os) */

(* src = "Test_Designs/num_2.v:5" *)
module num_2(x, y, cin, A, cout);
  wire _00_;
  wire _01_;
  wire _02_;
  wire _03_;
  wire _04_;
  wire _05_;
  wire _06_;
  (* src = "Test_Designs/num_2.v:5" *)
  output A;
  (* src = "Test_Designs/num_2.v:5" *)
  input cin;
  (* src = "Test_Designs/num_2.v:5" *)
  output cout;
  (* src = "Test_Designs/num_2.v:5" *)
  input x;
  (* src = "Test_Designs/num_2.v:5" *)
  input y;
  NAND2X1 _07_ (
    .A(cin),
    .B(y),
    .Y(_03_)
  );
  OR2X2 _08_ (
    .A(cin),
    .B(y),
    .Y(_04_)
  );
  NAND3X1 _09_ (
    .A(x),
    .B(_03_),
    .C(_04_),
    .Y(_05_)
  );
  INVX1 _10_ (
    .A(x),
    .Y(_06_)
  );
  AND2X2 _11_ (
    .A(cin),
    .B(y),
    .Y(_00_)
  );
  NOR2X1 _12_ (
    .A(cin),
    .B(y),
    .Y(_01_)
  );
  OAI21X1 _13_ (
    .A(_01_),
    .B(_00_),
    .C(_06_),
    .Y(_02_)
  );
  AND2X2 _14_ (
    .A(_05_),
    .B(_02_),
    .Y(A)
  );
  OAI21X1 _15_ (
    .A(_06_),
    .B(_01_),
    .C(_03_),
    .Y(cout)
  );
endmodule
