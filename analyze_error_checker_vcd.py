import matplotlib.pyplot as plt

# VCD dosyasını okuyun
vcd_file = "error_checker.vcd"
signal_mapping = {
    '!': "error_flag",
    '"': "clk",
    '#': "data_in [7:0]",
    '$': "reset",
    '%': "data_in [7:0] (uut)",
    '&': "WIDTH"
}

def parse_vcd(vcd_file):
    signal_changes = {}
    signals = {}
    timestamp = None  # Başlangıçta zaman damgası tanımsız

    with open(vcd_file, 'r') as file:
        vcd_lines = file.readlines()

    for line in vcd_lines:
        line = line.strip()
        if line.startswith('$var'):
            parts = line.split()
            signal_id = parts[3]
            signals[signal_id] = signal_mapping.get(signal_id, f"UNDEFINED_{signal_id}")
        elif line.startswith('#'):
            timestamp = int(line[1:])  # Zaman damgasını güncelle
        elif line.startswith(('0', '1', 'b', 'x', 'z')):
            if timestamp is not None:  # Zaman damgası tanımlıysa işlem yap
                value = line[:-1].strip()
                signal_id = line[-1]
                if signal_id not in signal_changes:
                    signal_changes[signal_id] = []
                signal_changes[signal_id].append((timestamp, value))
            else:
                print(f"Warning: Signal change ignored due to undefined timestamp. Line: {line}")

    return signals, signal_changes

def plot_signals(signal_changes, signals, output_file):
    plt.figure(figsize=(10, 6))
    for signal_id, changes in signal_changes.items():
        times, values = zip(*changes)
        # 'b', 'x', 'z' gibi değerlerin işlenmesi
        processed_values = []
        for value in values:
            value = value.strip()  # Fazladan boşlukları kaldır
            if value.startswith('b'):
                try:
                    processed_values.append(int(value[1:], 2))  # İkili sayıyı int'e çevir
                except ValueError:
                    processed_values.append(0)  # Hatalı değerler için varsayılan
            elif value in {'x', 'z'}:
                processed_values.append(None)  # Geçersiz değerler için 0
            else:
                processed_values.append(int(value))  # Diğer durumlar için int çevir
        plt.step(times, processed_values, label=signals.get(signal_id, f"UNDEFINED_{signal_id}"))
    plt.xlabel("Time")
    plt.ylabel("Signal Value")
    plt.title("Error Checker Signals Over Time")
    plt.legend()
    plt.savefig(output_file)
    plt.show()

signals, signal_changes = parse_vcd(vcd_file)
plot_signals(signal_changes, signals, "error_checker_signals.png")
