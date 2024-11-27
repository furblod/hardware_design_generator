module testbench;
    reg clk, reset, enable;
    wire [3:0] count;

    // Test edilen modülün bağlanması
    counter uut (
        .clk(clk),
        .reset(reset),
        .enable(enable),
        .count(count)
    );

    // Test senaryoları
    initial begin
        $dumpfile("testbench.vcd"); // Dalga formu dosyası
        $dumpvars(0, testbench);

        // Test başlangıcı
        clk = 0; reset = 1; enable = 0; #10; // Reset durumu
        reset = 0; enable = 1; #50;         // Enable ile sayma
        enable = 0; #50;                    // Enable olmadan durma
        $finish;
    end

    // Saat sinyali oluşturma
    always #5 clk = ~clk;
endmodule
