module testbench;
    reg [31:0] a, b;       // 32-bit girişler
    reg [1:0] opcode;      // İşlem kodu
    wire [31:0] result;    // Sonuç
    wire ready;            // Hazır sinyali

    // Test edilen ALU modülünü bağlayalım
    alu uut (
        .a(a),
        .b(b),
        .opcode(opcode),
        .result(result),
        .ready(ready)
    );

    initial begin
        $dumpfile("alu.vcd"); // VCD dosyasını oluştur
        $dumpvars(0, testbench); // Tüm sinyalleri kaydet
        
        // Test 1: Toplama (10 + 20)
        a = 10; b = 20; opcode = 2'b00; #10;
        
        // Test 2: Çıkarma (50 - 15)
        a = 50; b = 15; opcode = 2'b01; #10;
        
        // Test 3: Çarpma (7 * 8)
        a = 7; b = 8; opcode = 2'b10; #10;
        
        // Test 4: Bölme (100 / 5)
        a = 100; b = 5; opcode = 2'b11; #10;

        // Test 5: Bölme (Sıfıra bölme)
        a = 100; b = 0; opcode = 2'b11; #10;

        $finish; // Simülasyonu sonlandır
    end
endmodule
