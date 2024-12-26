`timescale 1ns/1ps

module integrated_testbench;

  // Ortak sinyallerin tanımlanması
  reg clk;
  reg reset;
  reg enable;
  reg [3:0] alu_a, alu_b;
  reg [1:0] alu_op;
  wire [7:0] alu_result;
  reg mux_select;
  reg [3:0] mux_in0, mux_in1;
  wire [3:0] mux_out;
  wire [3:0] counter_out;
  reg [3:0] decoder_input;
  wire [15:0] decoder_output;

  // Saat sinyali üretimi
  initial begin
    clk = 0;
    forever #5 clk = ~clk; // 10 ns period
  end

  // Modül örnekleri
  ALU alu_inst (
    .a({28'b0, alu_a}), // 32-bit genişlik için sıfır ile doldur
    .b({28'b0, alu_b}),
    .opcode({1'b0, alu_opcode}), // 2-bit genişlik için sıfır ile doldur
    .result(alu_result),
    .ready(alu_ready)
);


  mux2to1 mux_inst (
    .a(mux_in0[0]), // Eğer sadece 1-bit kullanıyorsanız
    .b(mux_in1[0]),
    .sel(mux_sel),
    .y(mux_out[0])
);


  counter counter_inst (
    .clk(clk),
    .reset(reset),
    .enable(enable),
    .count(counter_out)
  );

  decoder decoder_inst (
    .in(decoder_input),
    .out(decoder_output)
  );

  // Test senaryoları
  initial begin
    $dumpfile("integrated_testbench.vcd"); // Dalgaform dosyasını tanımla
    $dumpvars(0, integrated_testbench);    // Tüm sinyalleri kaydet
    
    // Başlangıç değerleri
    reset = 1; enable = 0;
    alu_a = 4'b0000; alu_b = 4'b0000; alu_op = 2'b00;
    mux_in0 = 4'b0000; mux_in1 = 4'b1111; mux_select = 0;
    decoder_input = 4'b0000;

    // Reset işlemi
    #10 reset = 0; enable = 1;

    // ALU işlemi test
    #10 alu_a = 4'b0101; alu_b = 4'b0011; alu_op = 2'b00; // Toplama
    #10 alu_op = 2'b01; // Çıkarma
    #10 alu_op = 2'b10; // Çarpma (destekliyorsa)

    // MUX işlemi test
    #10 mux_select = 1;

    // Counter işlemi test
    #50 reset = 1; #10 reset = 0; // Reset sonrası sayma

    // Decoder işlemi test
    #10 decoder_input = 4'b0010;
    #10 decoder_input = 4'b0100;

    // Simülasyonu sonlandır
    #100 $finish;
end


endmodule
