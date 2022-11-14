`default_nettype none

module rc5 (
  input wire i_clk,
  input wire i_rst,

  input wire i_rc5,

  output reg o_valid,
  output reg o_field,
  output reg o_control,
  output reg [4:0] o_address,
  output reg [5:0] o_command
);
    
    reg [3:0] counter;
    reg active;
    reg [12:0] sr;

    always @(posedge i_clk) begin
        if (i_rst) begin
            o_valid <= 1'b0;
            active <= 1'b0;
            counter <= 13;
            sr <= 14'b0;
        end else begin
            o_valid <= 1'b0;

            if (active) begin
                sr <= sr << 1;
                sr[0] <= i_rc5;
                counter <= counter-1;

                if (counter == 0) begin
                    active <= 1'b0;

                    o_valid <= 1'b1;
                    o_field <= sr[12];
                    o_control <= sr[11];
                    o_address <= sr[10:6];
                    o_command <= sr[5:0];
                end
            end

            if (!active && i_rc5) begin
                sr <= sr << 1;
                sr[0] <= i_rc5;
                active <= 1'b1;
                counter <= 13-1;
            end
        end
    end

endmodule
