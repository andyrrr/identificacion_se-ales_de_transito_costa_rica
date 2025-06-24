import csv
import json
import os

CARPETA_RESULTADOS = "./archivos/resultados"
CSV_FILE = os.path.join(CARPETA_RESULTADOS, "predictions.csv")

# Cargar predicciones desde CSV
predicciones = {}
with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        imagen = row["Image Name"]
        if imagen not in predicciones:
            predicciones[imagen] = []
        predicciones[imagen].append({
            "nombre": row["Prediction"],
            "confianza": float(row["Confidence"])
        })

# Construir el JSON
resultado_json = []

for nombre_imagen in predicciones:
    nombre_base = os.path.splitext(nombre_imagen)[0]  # sin extensión
    txt_path = os.path.join(CARPETA_RESULTADOS, f"{nombre_base}.txt")

    if not os.path.exists(txt_path):
        continue  # Si no hay txt, omitir

    with open(txt_path, 'r') as f:
        lineas_txt = f.read().strip().splitlines()

    señales = []
    for i, linea in enumerate(lineas_txt):
        partes = linea.strip().split()
        if len(partes) != 6:
            continue

        if i >= len(predicciones[nombre_imagen]):
            break  # No hay más predicciones en CSV

        clase, x, y, w, h, conf_txt = partes
        pred = predicciones[nombre_imagen][i]

        señal = {
            "nombre": pred["nombre"],
            "confianza": pred["confianza"],
            "x_centro": float(x),
            "y_centro": float(y),
            "ancho": float(w),
            "alto": float(h)
        }
        señales.append(señal)

    resultado_json.append({
        "imagen": nombre_imagen,
        "senales": señales
    })

# Guardar como archivo JSON
with open(os.path.join("./archivos", "resultado.json"), "w", encoding='utf-8') as f:
    json.dump(resultado_json, f, ensure_ascii=False, indent=4)

print("JSON generado en 'resultado.json'")
