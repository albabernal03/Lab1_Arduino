import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Si no quieres que se abran las ventanas de las figuras, pon esto a False
SHOW_FIGURES = True

# ============================================
# 1. LOAD ALL CSV FILES
# ============================================

# Accelerometer
phone_acc = pd.read_csv("Gravity.csv")
arduino_acc = pd.read_csv("Raw data (g)_arduino.csv")

# Gyroscope
phone_gyro = pd.read_csv("Raw Data.csv")
arduino_gyro = pd.read_csv("s_Arduino.csv")

# Magnetometer
phone_mag = pd.read_csv("Raw Data_Magnetometer.csv")
arduino_mag = pd.read_csv(r"Raw data (µT)_Arduino.csv")


# ============================================
# 2. HELPER FUNCTIONS
# ============================================

def get_stats(df, cols):
    """Return mean and std for selected columns."""
    return df[cols].describe().loc[["mean", "std"]]

def get_sampling_frequency(time_column):
    """Compute sampling interval and frequency."""
    dt = time_column.diff().mean()
    freq = 1.0 / dt
    return float(dt), float(freq)

def save_and_maybe_show(filename):
    """Save current figure to PNG and, optionally, show it."""
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    if SHOW_FIGURES:
        plt.show()
    plt.close()


# ============================================
# 3. ACCELEROMETER ANALYSIS
# ============================================

print("\n=== ACCELEROMETER ===")

acc_phone_cols = ["Gravity X (m/s^2)", "Gravity Y (m/s^2)", "Gravity Z (m/s^2)"]
acc_arduino_cols = ["Acceleration x (g)", "Acceleration y (g)", "Acceleration z (g)"]

acc_phone_stats = get_stats(phone_acc, acc_phone_cols)
acc_arduino_stats = get_stats(arduino_acc, acc_arduino_cols)

acc_phone_dt, acc_phone_f = get_sampling_frequency(phone_acc["Time (s)"])
acc_arduino_dt, acc_arduino_f = get_sampling_frequency(arduino_acc["Time t (s)"])

print("\nSmartphone accelerometer stats:\n", acc_phone_stats)
print("Smartphone accelerometer sampling freq:", acc_phone_f, "Hz")

print("\nArduino accelerometer stats:\n", acc_arduino_stats)
print("Arduino accelerometer sampling freq:", acc_arduino_f, "Hz")

# Convert Arduino accelerometer from g -> m/s^2 for plotting
G_CONST = 9.80665
arduino_acc["Ax_mps2"] = arduino_acc["Acceleration x (g)"] * G_CONST
arduino_acc["Ay_mps2"] = arduino_acc["Acceleration y (g)"] * G_CONST
arduino_acc["Az_mps2"] = arduino_acc["Acceleration z (g)"] * G_CONST

# ---------- Plots: Accelerometer ----------

# 3.1 Smartphone accelerometer time-series
plt.figure(figsize=(12, 5))
plt.plot(phone_acc["Time (s)"], phone_acc["Gravity X (m/s^2)"], label="X")
plt.plot(phone_acc["Time (s)"], phone_acc["Gravity Y (m/s^2)"], label="Y")
plt.plot(phone_acc["Time (s)"], phone_acc["Gravity Z (m/s^2)"], label="Z")
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (m/s^2)")
plt.title("Smartphone Accelerometer (Gravity) – Time Series")
plt.legend()
plt.tight_layout()
save_and_maybe_show("acc_phone_timeseries.png")

# 3.2 Arduino accelerometer time-series (converted)
plt.figure(figsize=(12, 5))
plt.plot(arduino_acc["Time t (s)"], arduino_acc["Ax_mps2"], label="X")
plt.plot(arduino_acc["Time t (s)"], arduino_acc["Ay_mps2"], label="Y")
plt.plot(arduino_acc["Time t (s)"], arduino_acc["Az_mps2"], label="Z")
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (m/s^2)")
plt.title("Arduino Accelerometer – Time Series (converted to m/s^2)")
plt.legend()
plt.tight_layout()
save_and_maybe_show("acc_arduino_timeseries.png")

# 3.3 Histogram Z-axis comparison (phone vs Arduino)
plt.figure(figsize=(8, 6))
phone_acc["Gravity Z (m/s^2)"].hist(bins=30, alpha=0.5, label="Phone Z")
arduino_acc["Az_mps2"].hist(bins=30, alpha=0.5, label="Arduino Z")
plt.xlabel("Z acceleration (m/s^2)")
plt.ylabel("Count")
plt.title("Accelerometer Z-axis Distribution – Phone vs Arduino")
plt.legend()
plt.tight_layout()
save_and_maybe_show("acc_z_hist.png")

# 3.4 Std dev bar plot (accelerometer)
labels = ["X", "Y", "Z"]
phone_acc_std = [
    acc_phone_stats.loc["std", "Gravity X (m/s^2)"],
    acc_phone_stats.loc["std", "Gravity Y (m/s^2)"],
    acc_phone_stats.loc["std", "Gravity Z (m/s^2)"],
]
# Convert Arduino std from g to m/s^2
arduino_acc_std = [
    acc_arduino_stats.loc["std", "Acceleration x (g)"] * G_CONST,
    acc_arduino_stats.loc["std", "Acceleration y (g)"] * G_CONST,
    acc_arduino_stats.loc["std", "Acceleration z (g)"] * G_CONST,
]

x = np.arange(len(labels))
width = 0.35

plt.figure(figsize=(8, 6))
plt.bar(x - width/2, phone_acc_std, width, label="Phone")
plt.bar(x + width/2, arduino_acc_std, width, label="Arduino")
plt.xticks(x, labels)
plt.ylabel("Std dev (m/s^2)")
plt.title("Accelerometer Noise (Std Dev) – Phone vs Arduino")
plt.legend()
plt.tight_layout()
save_and_maybe_show("acc_std_bar.png")


# ============================================
# 4. GYROSCOPE ANALYSIS
# ============================================

print("\n=== GYROSCOPE ===")

gyro_phone_cols = ["Gyroscope x (rad/s)", "Gyroscope y (rad/s)", "Gyroscope z (rad/s)"]
gyro_arduino_cols = ["Angular Velocity x (rad/s)", "Angular Velocity y (rad/s)", "Angular Velocity z (rad/s)"]

gyro_phone_stats = get_stats(phone_gyro, gyro_phone_cols)
gyro_arduino_stats = get_stats(arduino_gyro, gyro_arduino_cols)

gyro_phone_dt, gyro_phone_f = get_sampling_frequency(phone_gyro["Time (s)"])
gyro_arduino_dt, gyro_arduino_f = get_sampling_frequency(arduino_gyro["Time t (s)"])

print("\nSmartphone gyroscope stats:\n", gyro_phone_stats)
print("Smartphone gyroscope sampling freq:", gyro_phone_f, "Hz")

print("\nArduino gyroscope stats:\n", gyro_arduino_stats)
print("Arduino gyroscope sampling freq:", gyro_arduino_f, "Hz")

# ---------- Plots: Gyroscope ----------

# 4.1 Smartphone gyroscope time-series
plt.figure(figsize=(12, 5))
plt.plot(phone_gyro["Time (s)"], phone_gyro["Gyroscope x (rad/s)"], label="X")
plt.plot(phone_gyro["Time (s)"], phone_gyro["Gyroscope y (rad/s)"], label="Y")
plt.plot(phone_gyro["Time (s)"], phone_gyro["Gyroscope z (rad/s)"], label="Z")
plt.xlabel("Time (s)")
plt.ylabel("Angular velocity (rad/s)")
plt.title("Smartphone Gyroscope – Time Series")
plt.legend()
plt.tight_layout()
save_and_maybe_show("gyro_phone_timeseries.png")

# 4.2 Arduino gyroscope time-series
plt.figure(figsize=(12, 5))
plt.plot(arduino_gyro["Time t (s)"], arduino_gyro["Angular Velocity x (rad/s)"], label="X")
plt.plot(arduino_gyro["Time t (s)"], arduino_gyro["Angular Velocity y (rad/s)"], label="Y")
plt.plot(arduino_gyro["Time t (s)"], arduino_gyro["Angular Velocity z (rad/s)"], label="Z")
plt.xlabel("Time (s)")
plt.ylabel("Angular velocity (rad/s)")
plt.title("Arduino Gyroscope – Time Series")
plt.legend()
plt.tight_layout()
save_and_maybe_show("gyro_arduino_timeseries.png")

# 4.3 Histogram Z-axis gyroscope
plt.figure(figsize=(8, 6))
phone_gyro["Gyroscope z (rad/s)"].hist(bins=30, alpha=0.5, label="Phone Z")
arduino_gyro["Angular Velocity z (rad/s)"].hist(bins=30, alpha=0.5, label="Arduino Z")
plt.xlabel("Z angular velocity (rad/s)")
plt.ylabel("Count")
plt.title("Gyroscope Z-axis Distribution – Phone vs Arduino")
plt.legend()
plt.tight_layout()
save_and_maybe_show("gyro_z_hist.png")

# 4.4 Std dev bar plot (gyroscope)
labels = ["X", "Y", "Z"]
phone_gyro_std = [
    gyro_phone_stats.loc["std", "Gyroscope x (rad/s)"],
    gyro_phone_stats.loc["std", "Gyroscope y (rad/s)"],
    gyro_phone_stats.loc["std", "Gyroscope z (rad/s)"],
]
arduino_gyro_std = [
    gyro_arduino_stats.loc["std", "Angular Velocity x (rad/s)"],
    gyro_arduino_stats.loc["std", "Angular Velocity y (rad/s)"],
    gyro_arduino_stats.loc["std", "Angular Velocity z (rad/s)"],
]

x = np.arange(len(labels))
width = 0.35

plt.figure(figsize=(8, 6))
plt.bar(x - width/2, phone_gyro_std, width, label="Phone")
plt.bar(x + width/2, arduino_gyro_std, width, label="Arduino")
plt.xticks(x, labels)
plt.ylabel("Std dev (rad/s)")
plt.title("Gyroscope Noise (Std Dev) – Phone vs Arduino")
plt.legend()
plt.tight_layout()
save_and_maybe_show("gyro_std_bar.png")


# ============================================
# 5. MAGNETOMETER ANALYSIS
# ============================================

print("\n=== MAGNETOMETER ===")

mag_phone_cols = ["Magnetic Field x (µT)", "Magnetic Field y (µT)", "Magnetic Field z (µT)"]
mag_arduino_cols = ["Magnetometer x (µT)", "Magnetometer y (µT)", "Magnetometer z (µT)"]

mag_phone_stats = get_stats(phone_mag, mag_phone_cols)
mag_arduino_stats = get_stats(arduino_mag, mag_arduino_cols)

mag_phone_dt, mag_phone_f = get_sampling_frequency(phone_mag["Time (s)"])
mag_arduino_dt, mag_arduino_f = get_sampling_frequency(arduino_mag["Time t (s)"])

print("\nSmartphone magnetometer stats:\n", mag_phone_stats)
print("Smartphone magnetometer sampling freq:", mag_phone_f, "Hz")

print("\nArduino magnetometer stats:\n", mag_arduino_stats)
print("Arduino magnetometer sampling freq:", mag_arduino_f, "Hz")

# ---------- Plots: Magnetometer ----------

# 5.1 Smartphone magnetometer time-series
plt.figure(figsize=(12, 5))
plt.plot(phone_mag["Time (s)"], phone_mag["Magnetic Field x (µT)"], label="X")
plt.plot(phone_mag["Time (s)"], phone_mag["Magnetic Field y (µT)"], label="Y")
plt.plot(phone_mag["Time (s)"], phone_mag["Magnetic Field z (µT)"], label="Z")
plt.xlabel("Time (s)")
plt.ylabel("Magnetic field (µT)")
plt.title("Smartphone Magnetometer – Time Series")
plt.legend()
plt.tight_layout()
save_and_maybe_show("mag_phone_timeseries.png")

# 5.2 Arduino magnetometer time-series
plt.figure(figsize=(12, 5))
plt.plot(arduino_mag["Time t (s)"], arduino_mag["Magnetometer x (µT)"], label="X")
plt.plot(arduino_mag["Time t (s)"], arduino_mag["Magnetometer y (µT)"], label="Y")
plt.plot(arduino_mag["Time t (s)"], arduino_mag["Magnetometer z (µT)"], label="Z")
plt.xlabel("Time (s)")
plt.ylabel("Magnetic field (µT)")
plt.title("Arduino Magnetometer – Time Series")
plt.legend()
plt.tight_layout()
save_and_maybe_show("mag_arduino_timeseries.png")

# 5.3 Histogram Z-axis magnetometer
plt.figure(figsize=(8, 6))
phone_mag["Magnetic Field z (µT)"].hist(bins=30, alpha=0.5, label="Phone Z")
arduino_mag["Magnetometer z (µT)"].hist(bins=30, alpha=0.5, label="Arduino Z")
plt.xlabel("Z magnetic field (µT)")
plt.ylabel("Count")
plt.title("Magnetometer Z-axis Distribution – Phone vs Arduino")
plt.legend()
plt.tight_layout()
save_and_maybe_show("mag_z_hist.png")

# 5.4 Std dev bar plot (magnetometer)
labels = ["X", "Y", "Z"]
phone_mag_std = [
    mag_phone_stats.loc["std", "Magnetic Field x (µT)"],
    mag_phone_stats.loc["std", "Magnetic Field y (µT)"],
    mag_phone_stats.loc["std", "Magnetic Field z (µT)"],
]
arduino_mag_std = [
    mag_arduino_stats.loc["std", "Magnetometer x (µT)"],
    mag_arduino_stats.loc["std", "Magnetometer y (µT)"],
    mag_arduino_stats.loc["std", "Magnetometer z (µT)"],
]

x = np.arange(len(labels))
width = 0.35

plt.figure(figsize=(8, 6))
plt.bar(x - width/2, phone_mag_std, width, label="Phone")
plt.bar(x + width/2, arduino_mag_std, width, label="Arduino")
plt.xticks(x, labels)
plt.ylabel("Std dev (µT)")
plt.title("Magnetometer Noise (Std Dev) – Phone vs Arduino")
plt.legend()
plt.tight_layout()
save_and_maybe_show("mag_std_bar.png")


print("\n=== DONE! All stats and plots generated and saved. ===")
