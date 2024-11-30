import sys

# Dinamik sinyal haritaları
signal_maps = {
    "counter.vcd": {
        "\"": "clk",
        "$": "reset",
        "#": "enable",
        "!": "count"
    },
     "mux2to1.vcd": {
        "!": "a",
        "\"": "b",
        "#": "sel",
        "$": "y"
    }
}

# VCD dosyasını terminalden alma
if len(sys.argv) < 2:
    print("Usage: python analyze_vcd.py <vcd_file>")
    sys.exit(1)

vcd_file = sys.argv[1]

# Haritayı belirleme
signal_map = signal_maps.get(vcd_file, None)
if not signal_map:
    print(f"No signal map found for {vcd_file}")
    sys.exit(1)

try:
    with open(vcd_file, 'r') as file:
        print(f"Analyzing {vcd_file}...\n")
        current_time = None
        last_values = {}  # Önceki sinyal değerlerini saklamak için

        for line in file:
            line = line.strip()
            if line.startswith(("$", "reset =", "end", "dump")):
                continue

            if line.startswith("#"):  # Zaman bilgisi
                current_time = line[1:]
                changes = []  # Değişen sinyalleri biriktirmek için
                for signal, value in last_values.items():
                    changes.append(f"  {signal} = {value}")
                if changes:
                    print(f"Time: {current_time}")
                    print("\n".join(changes))
            elif line.startswith("b"):  # Binary sinyal değişimi
                parts = line.split()
                value = parts[0][1:]  # "b" sonrasını al
                signal_char = parts[1]
                if signal_char in signal_map:
                    signal_name = signal_map[signal_char]
                    last_values[signal_name] = value
            elif line[0] in signal_map:  # 1 veya 0 ile başlayan sinyal
                signal_char = line[0]
                value = line[1:].strip()
                signal_name = signal_map[signal_char]
                last_values[signal_name] = value
except FileNotFoundError:
    print(f"Error: {vcd_file} not found. Make sure the file exists in the same directory.")
except Exception as e:
    print(f"An error occurred: {e}")
