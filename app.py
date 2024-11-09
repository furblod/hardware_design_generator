from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
import os
import subprocess
import tempfile
import os

load_dotenv()  # .env dosyasından çevre değişkenlerini yükle

app = Flask(__name__)

# OpenAI API anahtarını çevre değişkenlerinden al
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_design():
    specification = request.form['specification']
    try:
        # OpenAI API'yi kullanarak tasarım üret
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates Verilog code for hardware designs."},
                {"role": "user", "content": f"Generate Verilog code for the following specification: {specification}"}
            ]
        )
        generated_code = response.choices[0].message['content']
        
        # Verilog kodunu doğrula
        is_valid, validation_message = validate_verilog(generated_code)
        
        if is_valid:
            # Test bench üret
            testbench_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates Verilog testbenches."},
                    {"role": "user", "content": f"Generate a Verilog testbench for the following code:\n\n{generated_code}"}
                ]
            )
            testbench = testbench_response.choices[0].message['content']
            
            # Test et
            test_passed, test_result = test_verilog(generated_code, testbench)
            
            return jsonify({
                "success": True, 
                "code": generated_code, 
                "validation": validation_message,
                "testbench": testbench,
                "test_passed": test_passed,
                "test_result": test_result
            })
        else:
            return jsonify({
                "success": False, 
                "error": f"Invalid Verilog code generated. {validation_message}"
            })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)

def validate_verilog(code):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.v', delete=False) as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name

    try:
        result = subprocess.run(['iverilog', '-t', 'null', temp_file_path], 
                                capture_output=True, text=True, check=True)
        return True, "Verilog code is valid."
    except subprocess.CalledProcessError as e:
        return False, f"Verilog code is invalid. Error: {e.stderr}"
    finally:
        os.unlink(temp_file_path)

def test_verilog(code, testbench):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.v', delete=False) as temp_file:
        temp_file.write(code)
        code_file_path = temp_file.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.v', delete=False) as temp_file:
        temp_file.write(testbench)
        testbench_file_path = temp_file.name

    try:
        # Compile
        subprocess.run(['iverilog', '-o', 'test.vvp', code_file_path, testbench_file_path], 
                       check=True, capture_output=True, text=True)
        
        # Run simulation
        result = subprocess.run(['vvp', 'test.vvp'], 
                                capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Test failed. Error: {e.stderr}"
    finally:
        os.unlink(code_file_path)
        os.unlink(testbench_file_path)
        if os.path.exists('test.vvp'):
            os.unlink('test.vvp')