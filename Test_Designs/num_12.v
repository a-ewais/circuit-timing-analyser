// file: num_12.v
// author: @amrsaeed

`timescale 1ns/1ns

module num_12(LDbar, CLRbar, P, T, CLK, D, count, RCO);

input LDbar, CLRbar, P, T, CLK;
input [3:0] D;
output [3:0] count;
output RCO;

reg [3:0] Q;
always @ (posedge CLK) begin
if (!CLRbar) Q <= 4'b0000;
else if (!LDbar) Q <= D;
else if (P && T) Q <= Q + 1;
end
assign count = Q;
assign RCO = Q[3] & Q[2] & Q[1] & Q[0] & T;
endmodule
