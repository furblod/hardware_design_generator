module tb_error_checker;
    reg clk, reset;
    reg [7:0] data_in;
    wire error_flag;

    // Hata tespit modülü
    error_checker #(8) uut (
        .clk(clk),
        .reset(reset),
        .data_in(data_in),
        .error_flag(error_flag)
    );

    always #5 clk = ~clk; // Saat sinyali

    initial begin
        // VCD dosyasını başlat
        $dumpfile("error_checker.vcd");
        $dumpvars(0, tb_error_checker);

        clk = 0;
        reset = 0;

        #5; reset = 1; // Reset işlemi
        #5; reset = 0; // Reset kalkıyor


        data_in = 8'b00000000; // İlk durum: hatasız veri
        #10;
        data_in = 8'b11111111; // Geçerli veri
        #10;
        data_in = 8'b10101010; // Hata yaratacak
        #10;
        data_in = 8'bx; // Belirsiz veri (hata yaratacak)
        #10;
        $finish;
    end
endmodule
