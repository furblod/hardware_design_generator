vcd_file = "testbench.vcd"

try:
    with open(vcd_file, 'r') as file:
        for line in file:
            if line.startswith("#"):  # Zaman bilgisi
                print(f"Time: {line.strip()}")
            elif line.startswith("$"):
                continue  # Yorum veya yapı bilgilerini atla
            else:
                print(f"Signal Change: {line.strip()}")
except FileNotFoundError:
    print(f"Error: {vcd_file} not found.")
except Exception as e:
    print(f"An error occurred: {e}")
