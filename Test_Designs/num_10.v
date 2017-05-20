// file: num_8.v
// author: @mohamedgadalla

`timescale 1ns/1ns

module num_8(input clk, input d, output cout);

always @ (posedge clk)
begin
cout = d;
end

endmodule