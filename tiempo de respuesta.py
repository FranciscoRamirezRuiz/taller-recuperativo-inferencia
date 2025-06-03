import requests 
import time
import csv


url = 'https://mi.utem.cl'

tiempos_respuesta = []


num_mediciones = 30

for i in range(num_mediciones):
    inicio = time.time()
    try:
        response = requests.get(url)
        fin = time.time()
        tiempo_ms = (fin - inicio) * 1000
        tiempos_respuesta.append(tiempo_ms)
        print(f'Medición {i+1}: {tiempo_ms:.2f} ms')
    except requests.exceptions.RequestException as e:
        print(f'Error en la medición {i+1}: {e}')
        tiempos_respuesta.append(None)


with open('datos_respuesta.csv', mode='w', newline='') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    escritor_csv.writerow(['tiempo_ms'])
    for tiempo in tiempos_respuesta:
        if tiempo is not None:
            escritor_csv.writerow([f'{tiempo:.2f}'])
        else:
            escritor_csv.writerow([''])

print('Mediciones completadas y guardadas en datos_respuesta.csv')
