module ALU (
    input [31:0] a,       // 32-bit giriş 1
    input [31:0] b,       // 32-bit giriş 2
    input [1:0] opcode,   // İşlem kodu (00: +, 01: -, 10: *, 11: /)
    output reg [31:0] result, // Sonuç
    output reg ready          // Hazır sinyali
);

    always @(*) begin
        ready = 1; // İşlem sonucunun hazır olduğunu belirtir
        case (opcode)
            2'b00: result = a + b; // Toplama
            2'b01: result = a - b; // Çıkarma
            2'b10: result = a * b; // Çarpma
            2'b11: result = b != 0 ? a / b : 32'hx; // Bölme (sıfıra bölme kontrolü)
            default: result = 32'hx; // Geçersiz işlem
        endcase
    end

endmodule
