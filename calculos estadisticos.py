import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# =======================
# PARTE 2: Estadística descriptiva
# =======================

ruta = "C:/Users/FranciscoR/Desktop/Nueva carpeta/datos_respuesta.csv"
df = pd.read_csv(ruta)

media = df["tiempo_ms"].mean()
mediana = df["tiempo_ms"].median()
desv_std = df["tiempo_ms"].std(ddof=1)
minimo = df["tiempo_ms"].min()
maximo = df["tiempo_ms"].max()
percentil_25 = df["tiempo_ms"].quantile(0.25)
percentil_75 = df["tiempo_ms"].quantile(0.75)


print("=== Estadística Descriptiva ===")
print(f"Media: {media:.2f} ms")
print(f"Mediana: {mediana:.2f} ms")
print(f"Desviación estándar (s): {desv_std:.2f} ms")
print(f"Mínimo: {minimo:.2f} ms")
print(f"Máximo: {maximo:.2f} ms")
print(f"Percentil 25%: {percentil_25:.2f} ms")
print(f"Percentil 75%: {percentil_75:.2f} ms")

# =======================
# PARTE 3.1: IC para la media
# =======================
n = len(df)
t_critico = stats.t.ppf(0.975, df=n-1)
se = desv_std / np.sqrt(n)
IC_media_inf = media - t_critico * se
IC_media_sup = media + t_critico * se

print("\n=== IC para la Media ===")
print(f"IC 95%: [{IC_media_inf:.2f} ms, {IC_media_sup:.2f} ms]")

# =======================
# PARTE 3.2: IC para la proporción (>250 ms)
# =======================
x = sum(df["tiempo_ms"] > 250)
p_hat = x / n
z = 1.96

# Wilson
numerador = p_hat + (z**2) / (2 * n)
ajuste = z * np.sqrt((p_hat * (1 - p_hat) / n) + (z**2) / (4 * n**2))
denominador = 1 + (z**2) / n
IC_prop_inf = (numerador - ajuste) / denominador
IC_prop_sup = (numerador + ajuste) / denominador

print("\n=== IC para la Proporción de tiempos > 250 ms ===")
print(f"Proporción: {p_hat:.3f}")
print(f"IC 95%: [{IC_prop_inf:.3f}, {IC_prop_sup:.3f}]")

# =======================
# PARTE 4: Visualizaciones
# =======================

# Histograma con línea de media
plt.figure(figsize=(8, 5))
sns.histplot(df["tiempo_ms"], bins=10, kde=False, color="skyblue", edgecolor="black")
plt.axvline(media, color='red', linestyle='dashed', linewidth=2, label=f'Media = {media:.2f} ms')
plt.title("Histograma de tiempos de respuesta")
plt.xlabel("Tiempo de respuesta (ms)")
plt.ylabel("Frecuencia")
plt.legend()
plt.tight_layout()
plt.show()

# Gráfico de barras con IC para proporción
plt.figure(figsize=(5, 6))
plt.bar(["> 250 ms"], [p_hat], color="orange",
        yerr=[[p_hat - IC_prop_inf], [IC_prop_sup - p_hat]],
        capsize=10)
plt.ylim(0, 1)
plt.ylabel("Proporción")
plt.title("Proporción de tiempos > 250 ms con IC 95%")
plt.tight_layout()
plt.show()
