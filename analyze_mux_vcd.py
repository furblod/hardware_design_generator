def parse_mux_vcd(filename):
    signals = {
        'a': {'value': '0', 'changes': {}},
        'b': {'value': '0', 'changes': {}},
        'sel': {'value': '0', 'changes': {}},
        'y': {'value': '0', 'changes': {}}
    }
    
    signal_mapping = {}
    signal_chars = {}
    current_time = 0
    
    def calculate_y(a, b, sel):
        return b if sel == '1' else a

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

            for line in lines:
                if '$var' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        signal_char = parts[3]
                        signal_name = parts[4].rstrip('$end').strip()
                        signal_mapping[signal_char] = signal_name
                        signal_chars[signal_name] = signal_char

            print(f"\n{'='*40}")
            print(f"Mux2to1 VCD Analysis: {filename}")
            print(f"{'='*40}")
            
            print("\n[Signal Mapping]")
            for char, name in signal_chars.items():
                print(f"{char} -> {name}")

            print("\n[MUX Signal Changes]")
            print(f"{'Time':<10}{'a':<5}{'b':<5}{'sel':<5}{'y'}")
            print("-" * 30)

            for line in lines:
                line = line.strip()
                
                if line.startswith('#'):
                    current_time = int(line[1:])
                    continue

                if len(line) >= 2 and line[0] in ['0', '1']:
                    signal_char = line[1]
                    value = line[0]

                    if signal_char in signal_mapping:
                        signal_name = signal_mapping[signal_char]
                        signals[signal_name]['changes'][current_time] = value
                        signals[signal_name]['value'] = value

            unique_times = sorted(set().union(
                signals['a']['changes'].keys(),
                signals['b']['changes'].keys(),
                signals['sel']['changes'].keys()
            ))

            for time in unique_times:
                for sig in ['a', 'b', 'sel']:
                    if time in signals[sig]['changes']:
                        signals[sig]['value'] = signals[sig]['changes'][time]
                
                y_value = calculate_y(
                    signals['a']['value'], 
                    signals['b']['value'], 
                    signals['sel']['value']
                )
                
                print(f"{time:<10}"
                      f"{signals['a']['value']:<5}"
                      f"{signals['b']['value']:<5}"
                      f"{signals['sel']['value']:<5}"
                      f"{y_value}")

    except FileNotFoundError:
        print(f"Dosya bulunamadı: {filename}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Dosya adını komut satırından al
import sys
if len(sys.argv) < 2:
    print("Usage: python script.py <vcd_file>")
    sys.exit(1)

parse_mux_vcd(sys.argv[1])

import sys
import csv
import matplotlib.pyplot as plt

def save_to_csv(signal_changes, signals, output_file):
    """
    Sinyal değişimlerini CSV dosyasına kaydet.
    """
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Signal Name', 'Time', 'Value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for signal_id, changes in signal_changes.items():
            signal_name = signals.get(signal_id, f"UNDEFINED_{signal_id}")
            for time, value in changes:
                writer.writerow({'Signal Name': signal_name, 'Time': time, 'Value': value})


def plot_signals(signal_changes, signals, output_image):
    """
    Sinyalleri zaman ekseninde görselleştirir.
    """
    plt.figure(figsize=(10, 6))
    
    for idx, (signal_id, changes) in enumerate(signal_changes.items()):
        times = [time for time, _ in changes]
        values = []
        for _, value in changes:
            # Eğer değer binary bir diziyse
            if value.startswith('b'):
                # Binary değer boşsa atla
                if len(value) > 1:
                    try:
                        values.append(int(value[1:], 2))  # 'b' sonrası binary değeri al
                    except ValueError:
                        values.append(0)  # Geçersiz değerleri 0 olarak kabul et
                else:
                    values.append(0)  # 'b' ama boş bir değer varsa 0 yap
            else:
                try:
                    values.append(int(value))  # Normal değerleri integer'a çevir
                except ValueError:
                    values.append(0)  # Hatalı değerleri 0 olarak işaretle
        
        signal_name = signals.get(signal_id, f"UNDEFINED_{signal_id}")
        # UNDEFINED sinyalleri atla
        if signal_name.startswith("UNDEFINED_"):
            continue
        plt.step(times, values, where='post', label=signal_name)

    plt.xlabel("Time")
    plt.ylabel("Signal Value")
    plt.title("VCD Signal Changes Over Time")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.savefig(output_image)
    plt.show()


# Komut satırından dosya adını al
if len(sys.argv) < 2:
    print("Usage: python analyze_counter_vcd.py <counter_vcd_file>")
    sys.exit(1)


def parse_vcd(file_path):
    """
    VCD dosyasını satır satır okur ve analiz eder.
    """
    signals = {}  
    signal_changes = {}  
    current_time = 0  

    # VCD dosyasını aç ve satır satır işle
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("$var"):
                parts = line.split()
                signal_id = parts[3]
                signal_name = parts[4].rstrip('$end')
                signals[signal_id] = signal_name
                signal_changes[signal_id] = []
            elif line.startswith("#"):
                try:
                    current_time = int(line[1:])
                except ValueError:
                    current_time = 0  
            # Sinyal değişimleri (0, 1, b ile başlayan)
            elif line.startswith(('0', '1', 'b')):
                value = line[0]
                signal_id = line[1:].strip()
                if line.startswith('b'):
                    parts = line.split()
                    if len(parts) == 2:
                        value = parts[0]
                        signal_id = parts[1]
                    else:
                        continue  
                if signal_id in signal_changes:
                    signal_changes[signal_id].append((current_time, value))

    return signals, signal_changes

vcd_file = sys.argv[1]  # VCD dosya adı
signals, signal_changes = parse_vcd(vcd_file)

save_to_csv(signal_changes, signals, "mux_vcd_analysis.csv")
plot_signals(signal_changes, signals, "mux_vcd_signals.png")

