// file: num_4.v
// author: @mohamedgadalla

`timescale 1ns/1ns

module num_4(input A, input B, input C, input D, output Y);

assign Y = A&B|C^D;

endmodule