# Identificación de Señales de Tránsito de Costa Rica utilizando YOLOv5

Este proyecto permite detectar señales de tránsito en imágenes utilizando el modelo YOLOv5. Cuenta con dos modos de uso: una interfaz gráfica para selección manual de imágenes y un modo automático por línea de comandos para procesar carpetas completas.

---

## Requisitos

Antes de ejecutar el proyecto, es necesario instalar las dependencias con:

```bash
pip install -r yolov5/requirements.txt
```

---

## Modo Manual (Interfaz Gráfica)

Este modo permite seleccionar múltiples imágenes a través de una interfaz y ver los resultados por cada imagen con Bounding Boxes.

### Ejecutar GUI:

```bash
python detector_gui.py
```

## Modo Automático (Línea de Comandos)

Este modo está pensado para ejecutar detecciones de forma automatizada en una carpeta de imágenes.

### Ejecutar:

```bash
python detectar.py --ruta ./ruta/a/tu/carpeta
```

- `--ruta`: especifica la ruta a una carpeta que contenga imágenes (`.jpg`, `.jpeg`, `.png`).
- Genera como salida:
  - Archivos `.txt` con coordenadas y clases de detección.
  - Un archivo `predictions.csv` con el resumen de clases y confianzas.
  - Un archivo `resultado.json` con todos los datos estructurados por imagen.

---

## Formato del JSON de salida

Cada entrada en `resultado.json` contiene:

```json
{
  "imagen": "senal-26.png",
  "senales": [
    {
      "nombre": "alto",
      "confianza": 0.94,
      "x_centro": 0.613,
      "y_centro": 0.528,
      "ancho": 0.067,
      "alto": 0.128
    },
    ...
  ]
}
```

---
