// file: ALU.v
// author: @amrsaeed

`timescale 1ns/1ns

module ThirtyTwoBitALU(
    input [3:0] ctrl,
    input [31:0] x,
    input [31:0] y,
    output reg V,
    output reg Z,
    output reg S,
    output reg C,
    output reg [31:0] result
    );

parameter ADD = 4'b0001;
parameter SUB = 4'b0010;
parameter AND = 4'b0011;
parameter OR =  4'b0100;
parameter XOR = 4'b0101;
parameter SLT = 4'b0110;
parameter ULT = 4'b0111;
parameter LSL = 4'b1000;
parameter LSR = 4'b1001;
parameter ASR = 4'b1010;

always @(ctrl or x or y)
    begin
        C = 1'b0;
        case (ctrl)
            ADD: {C, result} = {1'b0, x} + {1'b0, y};
            SUB: {C, result} = {1'b0, x} - {1'b0, y};
            AND: result = x & y;
            OR: result = x | y;
            XOR: result = x ^ y;
            SLT: result = ($signed(x) < $signed(y)) ? 1 : 0;
            ULT: result = (x < y) ? 1 : 0;
            LSL: result = x << y[4:0];
            LSR: result = x >> y[4:0];
            ASR: result = $signed(x) >>> y[4:0];
        endcase
    end

always @(result or C)
    begin
        Z = ~(|result);
        V = ({C,result[31]} == 2'b01);
        S = result[31];
    end
endmodule


