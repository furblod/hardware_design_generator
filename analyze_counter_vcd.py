
def parse_counter_vcd(filename):
    signals = {}
    current_time = 0
    signal_names = {}
    last_count_value = None

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            
            for line in lines:
                if '$var' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        signal_char = parts[3]
                        signal_name = parts[4].rstrip('$end').strip()
                        signal_names[signal_char] = signal_name

            print(f"\n{'='*40}")
            print(f"Counter VCD Analysis: {filename}")
            print(f"{'='*40}")
            
            print("\n[Signal Mapping]")
            for char, name in signal_names.items():
                print(f"{char} -> {name}")

            print("\n[Counter Signal Changes]")
            print(f"{'Time':<10}{'Signal':<10}{'Decimal':<10}{'Binary'}")
            print("-" * 40)

            for line in lines:
                line = line.strip()
                
                # Zaman bilgisi
                if line.startswith('#'):
                    current_time = int(line[1:])
                    continue

                # Sinyal değişimleri
                if len(line) >= 2:
                    # Binary değerler için işlem
                    if line.startswith('b'):
                        parts = line.split()
                        binary_value = parts[0][1:]
                        signal_char = parts[1]
                        
                        if signal_char in signal_names:
                            signal_name = signal_names[signal_char]
                            if signal_name == 'count':
                                decimal_value = int(binary_value, 2)
                                print(f"{current_time:<10}{signal_name:<10}{decimal_value:<10}{binary_value}")
                                last_count_value = binary_value

                    # 0 ve 1 sinyalleri için işlem
                    elif line[0] in ['0', '1']:
                        signal_char = line[1]
                        
                        if signal_char in signal_names:
                            signal_name = signal_names[signal_char]
                            value = line[0]
                            
                            if signal_name != 'count':
                                print(f"{current_time:<10}{signal_name:<10}{value:<10}-")
                            elif last_count_value:
                                decimal_value = int(last_count_value, 2)
                                print(f"{current_time:<10}{signal_name:<10}{decimal_value:<10}{last_count_value}")

    except FileNotFoundError:
        print(f"Dosya bulunamadı: {filename}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
import sys
# Komut satırından dosya adını al
if len(sys.argv) < 2:
    print("Usage: python svript.py <counter_vcd_file>")
    sys.exit(1)

parse_counter_vcd(sys.argv[1])

def parse_vcd(file_path):
    """
    VCD dosyasını satır satır okur ve analiz eder.
    """
    signals = {}  
    signal_changes = {}  
    
    # VCD dosyasını aç ve satır satır işle
    with open(file_path, 'r') as file:
        for line in file:
            # Sinyal tanımlamaları ($var ile başlayan)
            if line.startswith("$var"):
                parts = line.split()
                signal_id = parts[3]
                signal_name = parts[4]
                signals[signal_id] = signal_name
            # Sinyal değişimleri (0, 1, b ile başlayan)
            elif line.startswith(('0', '1', 'b')):
                value = line[0]
                signal_id = line[1:].strip()
                if signal_id not in signal_changes:
                    signal_changes[signal_id] = []
                signal_changes[signal_id].append((0, value))  # Örnek zaman için 0 kullanıldı

    return signals, signal_changes

import sys
import csv
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


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



def parse_vcd(file_path):
    """
    VCD dosyasını satır satır okur ve analiz eder.
    """
    signals = {}  # Sinyal tanımları (ID -> İsim)
    signal_changes = {}  # Zaman içerisindeki sinyal değişimleri (ID -> [(zaman, değer)])
    current_time = 0  # Mevcut zaman

    # VCD dosyasını aç ve satır satır işle
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            # Sinyal tanımlamaları ($var ile başlayan)
            if line.startswith("$var"):
                parts = line.split()
                signal_id = parts[3]
                signal_name = parts[4].rstrip('$end')
                signals[signal_id] = signal_name
                signal_changes[signal_id] = []
            # Zaman bilgisini oku (# ile başlayan)
            elif line.startswith("#"):
                try:
                    current_time = int(line[1:])
                except ValueError:
                    current_time = 0  # Geçersiz bir zaman varsa 0 olarak kabul et
            # Sinyal değişimleri (0, 1, b ile başlayan)
            elif line.startswith(('0', '1', 'b')):
                value = line[0]
                signal_id = line[1:].strip()
                if line.startswith('b'):
                    # Eksik binary değeri kontrol et
                    parts = line.split()
                    if len(parts) == 2:
                        value = parts[0]
                        signal_id = parts[1]
                    else:
                        continue  # Eksik binary değeri atla
                if signal_id in signal_changes:
                    signal_changes[signal_id].append((current_time, value))

    return signals, signal_changes


# Komut satırından dosya adını al
if len(sys.argv) < 2:
    print("Usage: python analyze_counter_vcd.py <counter_vcd_file>")
    sys.exit(1)

vcd_file = sys.argv[1]  # VCD dosya adı
signals, signal_changes = parse_vcd(vcd_file)

# Analiz ve rapor oluşturma
save_to_csv(signal_changes, signals, "counter_vcd_analysis.csv")
plot_signals(signal_changes, signals, "counter_vcd_signals.png")
