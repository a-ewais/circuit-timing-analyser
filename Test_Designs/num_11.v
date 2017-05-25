// file: num_11.v
// author: @amrsaeed

`timescale 1ns/1ns

module num_11(
input a,         //data in a
input b,         //data in b
input cin,       //carry in
output sum_out,  //sum output
output c_out     //carry output
);

wire c1, c2, c3; //wiring needed
assign sum_out = a ^ b ^ cin; //half adder (XOR gate)
assign c1      = a & cin;     //carry condition 1
assign c2      = b & cin;     //carry condition 1
assign c3      = a & b;       //carry condition 1
assign c_out   = (c1 + c2 + c3);

endmodule
