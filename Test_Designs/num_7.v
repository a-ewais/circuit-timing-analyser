// file: num_7.v
// author: @mohamedgadalla

`timescale 1ns/1ns

module num_7(input A, input B, input C, input D, output Y);

assign Y = A&B&C&D;

endmodule