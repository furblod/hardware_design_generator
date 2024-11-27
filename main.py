from transformers import AutoModelForCausalLM, AutoTokenizer

# Model ve tokenizer yükle
model_name = "codellama/CodeLlama-7b-hf"  # Hugging Face üzerinde ücretsiz bir model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_verilog(prompt, max_length=200):
    # Prompt'u tokenlara çevir
    inputs = tokenizer(prompt, return_tensors="pt")
    # Model ile yanıt üret
    outputs = model.generate(
        inputs["input_ids"], 
        max_length=max_length, 
        temperature=0.7, 
        top_p=0.95, 
        do_sample=True
    )
    # Yanıtı çöz ve döndür
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    # Verilog kodu üretmek için prompt
    prompt = "Create a Verilog module for a 4-bit binary counter with enable and reset."
    verilog_code = generate_verilog(prompt)
    print("Generated Verilog Code:\n", verilog_code)

verilog_code = """
module counter (
    input clk,
    input reset,
    input enable,
    output reg [3:0] count
);
    always @(posedge clk or posedge reset) begin
        if (reset)
            count <= 4'b0000;
        else if (enable)
            count <= count + 1;
    end
endmodule
"""

# Üretilen Verilog kodunu dosyaya yaz
with open("generated_module.v", "w") as file:
    file.write(verilog_code)
print("generated_module.v dosyası oluşturuldu.")
