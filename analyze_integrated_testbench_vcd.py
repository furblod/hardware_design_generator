import sys
import csv
import matplotlib.pyplot as plt

def parse_integrated_testbench_vcd(file_path):
    """
    Integrated testbench VCD dosyasını analiz et.
    """
    signals = {}  # Sinyal tanımları
    signal_changes = {}  # Sinyal değişimleri
    current_time = 0

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()

                # Sinyal tanımlamaları
                if line.startswith("$var"):
                    parts = line.split()
                    signal_id = parts[3]
                    signal_name = parts[4]
                    signals[signal_id] = signal_name
                    signal_changes[signal_id] = []

                # Zaman bilgisi
                elif line.startswith("#"):
                    current_time = int(line[1:])

                # Sinyal değişimleri
                elif line and len(line) > 1:
                    value = line[0]
                    signal_id = line[1:]
                    if signal_id in signals:
                        signal_changes[signal_id].append((current_time, value))

        return signals, signal_changes

    except FileNotFoundError:
        print(f"VCD dosyası bulunamadı: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        sys.exit(1)

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
    Sinyalleri grafik olarak görselleştir.
    """
    plt.figure(figsize=(12, 8))

    for signal_id, changes in signal_changes.items():
        times = []
        values = []

        for time, value in changes:
            # Geçersiz değerleri atla
            if value in ['z', 'x']:
                continue
            try:
                # Binary değerler için dönüşüm
                if value.startswith('b'):
                    values.append(int(value[1:], 2))  # 'b' sonrası binary değeri al
                else:
                    values.append(int(value))  # Decimal değerler için dönüşüm
                times.append(time)
            except ValueError:
                print(f"Skipping invalid value: {value}")

        signal_name = signals.get(signal_id, f"UNDEFINED_{signal_id}")
        plt.step(times, values, label=signal_name, where='post')

    plt.xlabel("Time")
    plt.ylabel("Signal Value")
    plt.title("Integrated Testbench Signals")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.savefig(output_image)
    plt.show()


# Komut satırından dosya adı al
if len(sys.argv) < 2:
    print("Usage: python analyze_integrated_testbench_vcd.py <vcd_file>")
    sys.exit(1)

vcd_file = sys.argv[1]

# VCD dosyasını analiz et
signals, signal_changes = parse_integrated_testbench_vcd(vcd_file)

# Analiz sonuçlarını CSV dosyasına kaydet
save_to_csv(signal_changes, signals, "integrated_testbench_vcd_analysis.csv")

# Sinyalleri grafik olarak görselleştir ve PNG dosyasına kaydet
plot_signals(signal_changes, signals, "integrated_testbench_vcd_signals.png")
