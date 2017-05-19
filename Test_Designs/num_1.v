// file: num_1.v
// author: @mohamedgadalla

`timescale 1ns/1ns

module num_1(input A, input B, output Y);
 
assign Y = (A&B)^(A|B);

endmodule