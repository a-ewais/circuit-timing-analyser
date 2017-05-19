// file: num_2.v
// author: @mohamedgadalla

`timescale 1ns/1ns
module num_2 (input x, input y, input cin, output A, output cout);
 
assign {cout,A} =  cin + y + x;
 
endmodule