module testbench;
    reg [3:0] in;          // 4-bit giriş
    reg enable;            // Enable sinyali
    wire [15:0] out;       // 16-bit çıkış

    // Test edilen modül bağlanıyor
    decoder_4to16 uut (
        .in(in),
        .enable(enable),
        .out(out)
    );

    initial begin
        $dumpfile("decoder.vcd");  // VCD dosyası oluştur
        $dumpvars(0, testbench);  // Tüm sinyalleri kaydet

        // Test durumları
        enable = 0; in = 4'b0000; #10;  // Enable kapalı, tüm çıkışlar sıfır
        enable = 1; in = 4'b0000; #10;  // Enable açık, 0. bit 1
        in = 4'b0001; #10;              // 1. bit 1
        in = 4'b0010; #10;              // 2. bit 1
        in = 4'b0100; #10;              // 4. bit 1
        in = 4'b1000; #10;              // 8. bit 1
        enable = 0; in = 4'b1111; #10;  // Enable kapalı, tüm çıkışlar sıfır

        $finish;  // Simülasyonu sonlandır
    end
endmodule
