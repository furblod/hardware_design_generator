module testbench;
    reg clk, reset, enable; // Girişler
    wire [3:0] count;       // Çıkışlar

    // Test edilecek modülü bağla
    counter uut (
        .clk(clk),
        .reset(reset),
        .enable(enable),
        .count(count)
    );

    // Test senaryoları
    initial begin
        $dumpfile("testbench.vcd"); // Dalga formu dosyası
        $dumpvars(0, testbench);    // Tüm değişkenleri kaydet

        // Test başlangıcı
        clk = 0; reset = 1; enable = 0; #10; // Reset durumu
        reset = 0; enable = 1; #50;         // Enable aktifken sayaç
        enable = 0; #50;                    // Enable kapalıyken sayaç durur
        $finish;                            // Testi bitir
    end

    // Saat sinyali üretimi
    always #5 clk = ~clk;
endmodule
