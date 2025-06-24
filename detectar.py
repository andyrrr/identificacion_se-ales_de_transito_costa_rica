import argparse
import subprocess
import os
import shutil



# CONFIGURACIÓN DE RUTAS
YOLO_SCRIPT = "./yolov5/detect.py"
WEIGHTS = "./yolov5/runs/train/senales_cr3/weights/best.pt"
RESULT_DIR = "./yolov5/runs/detect/auto" 
CARPETA_RESULTADOS = "./archivos/resultados"

def main():
    parser = argparse.ArgumentParser(description="Ejecutar detección con YOLOv5")
    parser.add_argument('--ruta', required=True, help='Ruta a imagen o video a procesar')
    args = parser.parse_args()

    # Limpiar carpeta de resultados anteriores
    if os.path.exists(CARPETA_RESULTADOS):
        shutil.rmtree(CARPETA_RESULTADOS)

    # Construcción del comando
    comando = [
        "python", "yolov5/detect.py",
        "--weights", "yolov5/runs/train/senales_cr3/weights/best.pt",
        "--img", "640",
        "--source", args.ruta,
        "--name", "auto",
        "--exist-ok",
        "--save-txt",
        "--save-csv",
        "--save-conf",
        "--nosave"
    ]

    print("Ejecutando comando YOLOv5:")
    print(" ".join(comando))
    
    subprocess.run(comando)
    
    # Mover resultados a 'archivos/resultados/'
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

    if os.path.exists(RESULT_DIR):
        # Mover archivos directamente en RESULT_DIR
        for archivo in os.listdir(RESULT_DIR):
            origen = os.path.join(RESULT_DIR, archivo)
            destino = os.path.join(CARPETA_RESULTADOS, archivo)
            if os.path.isfile(origen):
                shutil.move(origen, destino)

        # Mover archivos de la subcarpeta 'labels'
        labels_dir = os.path.join(RESULT_DIR, "labels")
        if os.path.exists(labels_dir):
            for archivo in os.listdir(labels_dir):
                origen = os.path.join(labels_dir, archivo)
                destino = os.path.join(CARPETA_RESULTADOS, archivo)
                if os.path.isfile(origen):
                    shutil.move(origen, destino)

    subprocess.run(["python", "crear_JSON.py"])

if __name__ == '__main__':
    main()
