// file: num_6.v
// author: @mohamedgadalla

`timescale 1ns/1ns

module num_6(input A, input B, input C, input D, output Y);

assign Y = (A&B) |C|(B&D) ^ A;

endmodule