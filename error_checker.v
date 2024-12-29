module error_checker #(parameter WIDTH = 8) (
    input clk,
    input reset,
    input [WIDTH-1:0] data_in,
    output reg error_flag
);
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            error_flag <= 0; // Reset sırasında hata bayrağı sıfırlanır
        end else begin
            // Hata kontrolü: Belirsiz, üç durumlu veya belirli desene göre
            if (data_in === {WIDTH{1'bx}} || data_in === {WIDTH{1'bz}} || data_in == 8'b10101010) begin
                error_flag <= 1; // Hata tespit edildi
            end else begin
                error_flag <= 0; // Hata yok
            end
        end
    end
endmodule
