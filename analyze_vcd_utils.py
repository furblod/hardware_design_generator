import matplotlib.pyplot as plt
import csv

def parse_vcd(vcd_file):
    """
    Parse the VCD file and extract signal changes and signal names.
    """
    signal_changes = {}
    signals = {}

    with open(vcd_file, "r") as file:
        current_time = 0
        for line in file:
            line = line.strip()

            # Parse signal definitions ($var lines)
            if line.startswith("$var"):
                parts = line.split()
                signal_id = parts[3]
                signal_name = parts[4]
                signals[signal_id] = signal_name
                signal_changes[signal_name] = []

            # Parse time markers (# lines)
            elif line.startswith("#"):
                current_time = int(line[1:])

            # Parse signal value changes (e.g., bxxxx or 1/0)
            elif line.startswith("b") or line.startswith("1") or line.startswith("0"):
                if " " in line:
                    value, signal_id = line.split()
                else:
                    value = line
                    signal_id = value[1:]  # Handle binary values

                # Clean up value to remove invalid characters (e.g., ")
                value = value.strip('"')

                if signal_id in signals:
                    signal_name = signals[signal_id]
                    if signal_name in signal_changes:
                        signal_changes[signal_name].append((current_time, value))

    return signal_changes, signals


def save_to_csv(signal_changes, signals, output_file):
    """
    Save signal changes to a CSV file.
    """
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Signal", "Value"])

        for signal_name, changes in signal_changes.items():
            for time, value in changes:
                writer.writerow([time, signal_name, value])

    print(f"Signal changes saved to {output_file}")


def plot_signals(signal_changes, signals, output_file):
    """
    Plot signal changes over time and save as an image.
    """
    plt.figure(figsize=(12, 6))
    for signal_name, changes in signal_changes.items():
        times = [time for time, _ in changes]
        values = []

        for _, value in changes:
            try:
                # Convert binary values to integers
                if value.startswith("b"):
                    values.append(int(value[1:], 2))
                else:
                    values.append(int(value))
            except ValueError:
                # Skip invalid values
                print(f"Skipping invalid value: {value}")
                continue

        plt.step(times, values, label=signal_name)

    plt.xlabel("Time")
    plt.ylabel("Signal Value")
    plt.title("Decoder VCD Signal Changes Over Time")
    plt.legend()
    plt.grid(True)
    plt.savefig(output_file)
    plt.close()

    print(f"Signal plot saved to {output_file}")

