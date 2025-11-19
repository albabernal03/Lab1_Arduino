import pandas as pd

# --- 1. Load the CSV file ---
df = pd.read_csv("Raw data (g)_arduino.csv")

# --- 2. Compute the average time difference between consecutive samples ---
dt = df["Time t (s)"].diff().mean()

# --- 3. Compute the real sampling frequency ---
freq = 1 / dt

print("Average time difference between samples (dt):", dt)
print("Real sampling frequency:", freq, "Hz")

# --- Compute mean and standard deviation for all numeric channels ---
stats = df.describe().loc[["mean", "std"]]
print(stats)
print("\nMean and std:")

