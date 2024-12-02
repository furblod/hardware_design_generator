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

import sys

def parse_vcd(filename):
    signals = {}
    current_time = 0
    signal_names = {}
    signal_changes = {}

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            
            # Header parsing
            for line in lines:
                if '$var' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        signal_char = parts[3]
                        signal_name = parts[4].rstrip('$end').strip()
                        signal_names[signal_char] = signal_name

            print(f"\n{'='*40}")
            print(f"VCD File Analysis: {filename}")
            print(f"{'='*40}")
            
            print("\n[Signal Mapping]")
            for char, name in signal_names.items():
                print(f"{char} -> {name}")

            print("\n[Signal Changes Timeline]")
            print(f"{'Time':<10}{'Signal':<10}{'Value':<10}{'Binary'}")
            print("-" * 40)

            # Data parsing
            for line in lines:
                line = line.strip()
                
                # Zaman bilgisi
                if line.startswith('#'):
                    current_time = int(line[1:])
                    continue

                # Sinyal değişimleri
                if len(line) >= 2:
                    if line[0] in ['0', '1', 'b']:
                        signal_char = line[1] if line[0] in ['0', '1'] else line[2]
                        
                        if signal_char in signal_names:
                            signal_name = signal_names[signal_char]
                            
                            # Binary değerler için özel işlem
                            if line.startswith('b'):
                                value = line.split()[0][1:]
                                # Binary değeri decimal'e çevir
                                decimal_value = int(value, 2)
                                print(f"{current_time:<10}{signal_name:<10}{decimal_value:<10}{value}")
                            else:
                                value = line[0]
                                print(f"{current_time:<10}{signal_name:<10}{value:<10}-")
                            
                            # Her sinyal için son değeri ve değişim zamanını kaydet
                            if signal_name not in signal_changes or signal_changes[signal_name][-1]['value'] != value:
                                if signal_name not in signal_changes:
                                    signal_changes[signal_name] = []
                                
                                signal_changes[signal_name].append({
                                    'time': current_time,
                                    'value': value
                                })

            print(f"\n{'='*40}")
            print("Analysis Complete")
            print(f"{'='*40}")

    except FileNotFoundError:
        print(f"Dosya bulunamadı: {filename}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Komut satırından dosya adını al
if len(sys.argv) < 2:
    print("Usage: python analyze_vcd.py <vcd_file>")
    sys.exit(1)

parse_vcd(sys.argv[1])