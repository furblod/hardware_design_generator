module testbench;
    reg clk, reset, enable;
    wire [3:0] count;

    // Test edilen modül bağlanıyor
    counter uut (
        .clk(clk),
        .reset(reset),
        .enable(enable),
        .count(count)
    );

    // Saat sinyali üretimi
    always #5 clk = ~clk; // Clock her 5 birimde bir değişir

    initial begin
        $dumpfile("counter.vcd"); // VCD dosyasını oluştur
        $dumpvars(0, clk, reset, enable, count); // Tüm sinyalleri kaydet

        // Test durumları
        clk = 0; reset = 1; enable = 0; #10;  // Reset aktif, sayaç sıfırlanır
        reset = 0; enable = 1; #50;          // Sayaç artar
        enable = 0; #30;                     // Sayaç durur
        enable = 1; #40;                     // Sayaç tekrar artar
        $finish;                             // Simülasyonu sonlandır
    end
endmodule
