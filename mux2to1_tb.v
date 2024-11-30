module testbench;
    reg a, b, sel;   // Test girişleri
    wire y;          // Test çıkışı

    // Test edilen modül bağlanıyor
    mux2to1 uut (
        .a(a),
        .b(b),
        .sel(sel),
        .y(y)
    );

    initial begin
        $dumpfile("mux2to1.vcd"); 
        $dumpvars(0, a, b, sel, y); // Yalnızca bu sinyalleri dump et

        // Test durumları
        a = 0; b = 0; sel = 0; #10; // Test 1: y = a (0)
        a = 1; b = 0; sel = 0; #10; // Test 2: y = a (1)
        a = 0; b = 1; sel = 1; #10; // Test 3: y = b (1)
        a = 1; b = 1; sel = 1; #10; // Test 4: y = b (1)

        $finish; // Simülasyonu sonlandır
    end
endmodule
