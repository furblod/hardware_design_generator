def parse_vcd(vcd_file):
    """
    ALU için VCD dosyasını analiz eder ve sinyal değişimlerini döndürür.
    """
    signal_changes = {}
    signals = {}
    current_time = 0

    with open(vcd_file, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("$var"):
                parts = line.split()
                signal_id = parts[3]
                signal_name = parts[4]
                signals[signal_id] = signal_name
                signal_changes[signal_name] = []
            elif line.startswith("#"):
                current_time = int(line[1:])
            elif line.startswith(("b", "0", "1")):
                if line.startswith("b"):
                    value, signal_id = line.split()
                    value = value[1:]  # 'b' sonrasını al
                else:
                    value = line[0]
                    signal_id = line[1:]
                if signal_id in signals:
                    signal_changes[signals[signal_id]].append((current_time, value))
    
    return signal_changes, signals


def analyze_alu_vcd(vcd_file):
    """
    ALU sinyallerini analiz eder ve anlamlı bir çıktı verir.
    """
    signal_changes, signals = parse_vcd(vcd_file)

    print(f"\nALU VCD Analysis: {vcd_file}")
    print("=" * 40)

    for signal_name, changes in signal_changes.items():
        print(f"\nSignal: {signal_name}")
        for time, value in changes:
            if signal_name == "opcode":
                op_desc = {
                    "00": "Toplama",
                    "01": "Çıkarma",
                    "10": "Çarpma",
                    "11": "Bölme"
                }.get(value.zfill(2), "Bilinmeyen İşlem")
                print(f"  Time: {time}, Opcode: {value} ({op_desc})")
            else:
                print(f"  Time: {time}, Value: {value}")


if __name__ == "__main__":
    vcd_file = "alu.vcd"
    analyze_alu_vcd(vcd_file)


from matplotlib import pyplot as plt

def plot_alu_signals(signal_changes, signals, output_file):
    """
    ALU sinyallerini zaman ekseninde görselleştirir.
    """
    plt.figure(figsize=(12, 8))

    # Her bir sinyali çiz
    for signal_name, changes in signal_changes.items():
        times = [t for t, v in changes]
        values = [int(v, 2) if v.isdigit() or v.startswith('b') else 0 for _, v in changes]
        
        if signal_name != "opcode":  # Opcode için özel grafik gerekebilir
            plt.step(times, values, label=signal_name)

    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("ALU Signals Over Time")
    plt.legend(loc="upper left")
    plt.grid(True)
    plt.savefig(output_file)
    print(f"Signal plot saved to {output_file}")
    plt.show()

vcd_file = "alu.vcd"
signal_changes, signals = parse_vcd(vcd_file)

# ALU sinyallerini görselleştir ve PNG olarak kaydet
plot_alu_signals(signal_changes, signals, "alu_vcd_signals.png")




#----------------------- OPCODE -------------------------------

import matplotlib.pyplot as plt

# Sinyaller
time_values = [0, 10, 20, 30, 40]
result_values = [11110, 100011, 111000, 10100, 'x']
ready_values = [1, 1, 1, 1, 1]
a_values = [1010, 110010, 111, 1100100, 0]
b_values = [10100, 1111, 1000, 101, 0]
opcode_values = [0, 1, 2, 3]  # 0: Toplama, 1: Çıkarma, 2: Çarpma, 3: Bölme
opcode_labels = ["Toplama", "Çıkarma", "Çarpma", "Bölme"]

# Grafik
plt.figure(figsize=(10, 6))

# Sinyallerin çizimi
plt.plot(time_values[:-1], result_values[:-1], label="result", marker="o")
plt.plot(time_values[:-1], a_values[:-1], label="a", marker="o")
plt.plot(time_values[:-1], b_values[:-1], label="b", marker="o")
plt.plot(time_values[:-1], ready_values[:-1], label="ready", marker="o")

# Opcode sinyalini anotasyon olarak ekleme
for i, opcode in enumerate(opcode_values):
    plt.text(time_values[i], max(result_values[:-1]) * 0.9, opcode_labels[opcode], fontsize=9, color="purple")

# Eksik verileri (x) vurgulama
for i, value in enumerate(result_values):
    if value == 'x':
        plt.scatter(time_values[i], 0, color="red", label="Eksik Veri (x)")

# Ayarlar
plt.title("ALU İşlemleri ve Sinyal Değerleri")
plt.xlabel("Time")
plt.ylabel("Value")
plt.grid()
plt.legend()
plt.tight_layout()

# Görselleştirme
plt.show()
