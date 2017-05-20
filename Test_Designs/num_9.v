// file: num_9.v
// author: @mohamedgadalla

`timescale 1ns/1ns

module num_9(input clk, input A, input B, input C, input D, output reg cout);
reg temp1;
wire x, y;

assign x = (A&B)^(A|B);
assign y = (temp1&C)|D;


always @ (posedge clk)
begin
temp1 = x;
cout = y;
end

endmodule