module decoder (
    input wire [3:0] in,    // 4-bit giriş
    input wire enable,      // Enable sinyali
    output reg [15:0] out   // 16-bit çıkış
);

    always @(*) begin
        if (enable) begin
            out = 16'b0;          // Tüm çıkışları sıfırla
            out[in] = 1'b1;       // Giriş adresine karşılık gelen çıkışı 1 yap
        end else begin
            out = 16'b0;          // Enable düşükse tüm çıkışlar sıfır
        end
    end
endmodule
