module mux2to1(
    input wire a,     // Giriş 1
    input wire b,     // Giriş 2
    input wire sel,   // Seçim sinyali
    output wire y     // Çıkış
);

    assign y = (sel) ? b : a; // Seçim mantığı

endmodule
