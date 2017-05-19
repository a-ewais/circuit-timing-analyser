// file: num_8.v
// author: @mohamedgadalla

`timescale 1ns/1ns

module num_8(input a, input b, output c);

assign c = a | b & a ^ b;

endmodule
