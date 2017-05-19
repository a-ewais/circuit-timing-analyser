// file: num_5.v
// author: @mohamedgadalla

`timescale 1ns/1ns

module num_5(input A, input B, input sel, output Y);
assign Y = (sel) ? A : B;
endmodule