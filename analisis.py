import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Cargar el archivo CSV ---
df = pd.read_csv("Gravity.csv")

# Mostrar las primeras filas para verificar
print("Primeras filas del dataset:")
print(df.head())

# --- 2. Calcular mean y std para todas las columnas numéricas ---
stats = df.describe().loc[["mean", "std"]]
print("\nMedia (mean) y desviación estándar (std):")
print(stats)

# --- 3. Graficar cada eje (opcional) ---
plt.figure(figsize=(12,6))
plt.plot(df["Time (s)"], df["Gravity X (m/s^2)"], label="Gravity X")
plt.plot(df["Time (s)"], df["Gravity Y (m/s^2)"], label="Gravity Y")
plt.plot(df["Time (s)"], df["Gravity Z (m/s^2)"], label="Gravity Z")
plt.xlabel("Time (s)")
plt.ylabel("Gravity (m/s^2)")
plt.title("Smartphone Gravity Sensor Data (100 Hz)")
plt.legend()
plt.show()
