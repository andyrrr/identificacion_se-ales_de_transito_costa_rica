import sys
import os
import subprocess
import shutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QMovie


# CONFIGURACIÓN DE RUTAS
YOLO_SCRIPT = "./yolov5/detect.py"
WEIGHTS = "./yolov5/runs/train/senales_cr3/weights/best.pt"
RESULT_DIR = "./yolov5/runs/detect/manual" 
CARPETA_IMAGENES = "./imagenes/cargadas"
CARPETA_RESULTADOS = "./imagenes/resultados"

class DetectorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Detector de Señales")
        self.setGeometry(100, 100, 1800, 900)

        # === Layout principal horizontal ===
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)


        # === Controles generales (seleccionar y detectar) ===
        self.controles_generales = QVBoxLayout()
        self.main_layout.addLayout(self.controles_generales)

        self.btn_seleccionar = QPushButton()
        self.btn_seleccionar.setIcon(QIcon("./icons/cargar.png"))
        self.btn_seleccionar.setIconSize(QSize(100, 100))
        self.btn_seleccionar.setToolTip("Seleccionar imagen")
        self.btn_seleccionar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_seleccionar.setStyleSheet("border: none; background: transparent;")
        self.btn_seleccionar.clicked.connect(self.seleccionar_imagen)
        self.controles_generales.addSpacing(250)
        self.controles_generales.addWidget(self.btn_seleccionar)

        self.btn_detectar = QPushButton()
        self.btn_detectar.setIcon(QIcon("./icons/buscar.png"))  # Reemplazá por tu ícono
        self.btn_detectar.setIconSize(QSize(100, 100))
        self.btn_detectar.setToolTip("Detectar señales")
        self.btn_detectar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_detectar.setStyleSheet("border: none; background: transparent;")
        self.btn_detectar.clicked.connect(self.detectar)
        self.btn_detectar.setEnabled(False)
        self.controles_generales.addWidget(self.btn_detectar)


        self.btn_cargando = QPushButton()
        self.btn_cargando.setIcon(QIcon("./icons/buscando.png"))  # Reemplazá por tu ícono
        self.btn_cargando.setIconSize(QSize(100, 100))
        self.btn_cargando.setCursor(Qt.CursorShape.BusyCursor)
        self.btn_cargando.setStyleSheet("border: none; background: transparent;")
        self.btn_cargando.setEnabled(False)
        self.controles_generales.addWidget(self.btn_cargando)
        self.controles_generales.addSpacing(250)

        self.btn_cargando.setVisible(False)

        # === Layout izquierdo: imágenes cargadas ===
        self.layout_cargadas = QVBoxLayout()
        self.main_layout.addLayout(self.layout_cargadas)

        self.label_cargadas = QLabel("Imágenes cargadas")
        self.label_cargadas.setFixedSize(700, 700)
        self.label_cargadas.setStyleSheet("border: 0px solid gray; background-color: #f0f0f0;")
        self.label_cargadas.setAlignment(Qt.AlignCenter)
        self.layout_cargadas.addWidget(self.label_cargadas)

        # Controles carrusel cargadas < contador >
        controles_cargadas = QHBoxLayout()
        btn_ant_cargadas = QPushButton()
        btn_ant_cargadas.setIcon(QIcon("./icons/anterior.png"))  # Reemplazá por el ícono que quieras
        btn_ant_cargadas.setIconSize(QSize(50, 50))  # Tamaño más pequeño que los botones generales
        btn_ant_cargadas.setToolTip("Anterior imagen cargada")
        btn_ant_cargadas.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_ant_cargadas.setStyleSheet("border: none; background: transparent;")
        btn_ant_cargadas.clicked.connect(self.mostrar_anterior_cargada)
        controles_cargadas.addSpacing(200)
        controles_cargadas.addWidget(btn_ant_cargadas)


        self.contador_cargadas = QLabel("0 de 0")
        self.contador_cargadas.setAlignment(Qt.AlignCenter)
        controles_cargadas.addWidget(self.contador_cargadas)

        btn_sig_cargadas = QPushButton()
        btn_sig_cargadas.setIcon(QIcon("./icons/siguiente.png"))  # Reemplazá por tu ícono
        btn_sig_cargadas.setIconSize(QSize(50, 50))
        btn_sig_cargadas.setToolTip("Siguiente imagen cargada")
        btn_sig_cargadas.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_sig_cargadas.setStyleSheet("border: none; background: transparent;")
        btn_sig_cargadas.clicked.connect(self.mostrar_siguiente_cargada)
        controles_cargadas.addWidget(btn_sig_cargadas)
        controles_cargadas.addSpacing(200)


        self.layout_cargadas.addLayout(controles_cargadas)

        # === Layout derecho: imágenes resultado ===
        self.layout_resultados = QVBoxLayout()
        self.main_layout.addLayout(self.layout_resultados)

        self.label_resultados = QLabel("Resultados")
        self.label_resultados.setFixedSize(700, 700)
        self.label_resultados.setStyleSheet("border: 0px solid gray; background-color: #f0f0f0;")
        self.label_resultados.setAlignment(Qt.AlignCenter)
        self.layout_resultados.addWidget(self.label_resultados)

        # Controles carrusel resultados < contador >
        controles_resultados = QHBoxLayout()
        btn_ant_resultado = QPushButton()
        btn_ant_resultado.setIcon(QIcon("./icons/anterior.png"))  # Ruta al ícono "anterior"
        btn_ant_resultado.setIconSize(QSize(50, 50))
        btn_ant_resultado.setToolTip("Anterior resultado")
        btn_ant_resultado.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_ant_resultado.setStyleSheet("border: none; background: transparent;")
        btn_ant_resultado.clicked.connect(self.mostrar_anterior_resultado)
        controles_resultados.addSpacing(200)
        controles_resultados.addWidget(btn_ant_resultado)

        self.contador_resultados = QLabel("0 de 0")
        self.contador_resultados.setAlignment(Qt.AlignCenter)
        controles_resultados.addWidget(self.contador_resultados)

        btn_sig_resultado = QPushButton()
        btn_sig_resultado.setIcon(QIcon("./icons/siguiente.png"))  # Ruta al ícono "siguiente"
        btn_sig_resultado.setIconSize(QSize(50, 50))
        btn_sig_resultado.setToolTip("Siguiente resultado")
        btn_sig_resultado.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_sig_resultado.setStyleSheet("border: none; background: transparent;")
        btn_sig_resultado.clicked.connect(self.mostrar_siguiente_resultado)
        controles_resultados.addWidget(btn_sig_resultado)
        controles_resultados.addSpacing(200)

        self.layout_resultados.addLayout(controles_resultados)

        

        # Inicializar variables de imágenes
        self.imagenes_cargadas = []
        self.imagenes_resultado = []
        self.indice_cargadas = 0
        self.indice_resultados = 0






    def seleccionar_imagen(self):
        rutas, _ = QFileDialog.getOpenFileNames(
            self, "Seleccionar imágenes", "", "Imágenes (*.jpg *.png *.jpeg)"
        )
        if rutas:
            # Crear carpeta 'imagenes/cargadas/' si no existe
            os.makedirs(CARPETA_IMAGENES, exist_ok=True)

            for path in rutas:
                nombre = os.path.basename(path)
                destino = os.path.join(CARPETA_IMAGENES, nombre)
                shutil.copy(path, destino)

            # Actualizar lista de imágenes cargadas
            self.imagenes_cargadas = [
                os.path.join(CARPETA_IMAGENES, f)
                for f in os.listdir(CARPETA_IMAGENES)
                if f.lower().endswith((".jpg", ".png", ".jpeg"))
            ]
            self.imagenes_cargadas.sort()

            # Mostrar la última imagen agregada
            self.indice_cargadas = len(self.imagenes_cargadas) - 1
            self.mostrar_imagen_cargada()

            self.btn_detectar.setEnabled(True)



    def detectar(self):

        self.btn_cargando.setVisible(True)
        self.btn_detectar.setVisible(False)
        QApplication.processEvents()

        # Limpiar carpeta de resultados anteriores
        if os.path.exists(CARPETA_RESULTADOS):
            shutil.rmtree(CARPETA_RESULTADOS)

        comando = [
            "python", YOLO_SCRIPT,
            "--weights", WEIGHTS,
            "--img", "640",
            "--source", CARPETA_IMAGENES,
            "--name", "manual",
            "--exist-ok"
        ]

        print("Ejecutando comando YOLO:")
        print(" ".join(comando))

        subprocess.run(comando)

        # Mover resultados a 'imagenes/resultados/'
        os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
        if os.path.exists(RESULT_DIR):
            for archivo in os.listdir(RESULT_DIR):
                origen = os.path.join(RESULT_DIR, archivo)
                destino = os.path.join(CARPETA_RESULTADOS, archivo)
                if os.path.isfile(origen):
                    shutil.move(origen, destino)

        # Actualizar lista de imágenes de resultados
        self.imagenes_resultado = [
            os.path.join(CARPETA_RESULTADOS, f)
            for f in os.listdir(CARPETA_RESULTADOS)
            if f.lower().endswith((".jpg", ".png", ".jpeg"))
        ]
        self.imagenes_resultado.sort()

        # Mostrar la primera imagen detectada
        self.indice_resultados = 0
        self.mostrar_imagen_resultado()

        self.btn_cargando.setVisible(False)
        self.btn_detectar.setVisible(True)


    def mostrar_anterior_cargada(self):
        if self.imagenes_cargadas:
            self.indice_cargadas = (self.indice_cargadas - 1) % len(self.imagenes_cargadas)
            self.mostrar_imagen_cargada()

    def mostrar_siguiente_cargada(self):
        if self.imagenes_cargadas:
            self.indice_cargadas = (self.indice_cargadas + 1) % len(self.imagenes_cargadas)
            self.mostrar_imagen_cargada()

    def mostrar_anterior_resultado(self):
        if self.imagenes_resultado:
            self.indice_resultados = (self.indice_resultados - 1) % len(self.imagenes_resultado)
            self.mostrar_imagen_resultado()

    def mostrar_siguiente_resultado(self):
        if self.imagenes_resultado:
            self.indice_resultados = (self.indice_resultados + 1) % len(self.imagenes_resultado)
            self.mostrar_imagen_resultado()

    def mostrar_imagen_cargada(self):
        if self.imagenes_cargadas:
            ruta = self.imagenes_cargadas[self.indice_cargadas]
            pixmap = QPixmap(ruta)

            # Redimensionar con ancho fijo (800px) y altura proporcional
            ancho_deseado = 800
            ancho_original = pixmap.width()
            alto_original = pixmap.height()

            if ancho_original > 0:
                escala = ancho_deseado / ancho_original
                alto_escalado = int(alto_original * escala)
                pixmap = pixmap.scaled(ancho_deseado, alto_escalado, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            self.label_cargadas.setPixmap(pixmap)
            self.contador_cargadas.setText(
                f"{self.indice_cargadas + 1} de {len(self.imagenes_cargadas)}"
            )
        else:
            self.label_cargadas.setText("No hay imágenes cargadas.")
            self.contador_cargadas.setText("0 de 0")


    def mostrar_imagen_resultado(self):
        if self.imagenes_resultado:
            ruta = self.imagenes_resultado[self.indice_resultados]
            pixmap = QPixmap(ruta)

            # Redimensionar con ancho fijo (500px) y altura proporcional
            ancho_deseado = 800
            ancho_original = pixmap.width()
            alto_original = pixmap.height()

            if ancho_original > 0:
                escala = ancho_deseado / ancho_original
                alto_escalado = int(alto_original * escala)
                pixmap = pixmap.scaled(ancho_deseado, alto_escalado, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            self.label_resultados.setPixmap(pixmap)
            self.contador_resultados.setText(
                f"{self.indice_resultados + 1} de {len(self.imagenes_resultado)}"
            )
        else:
            self.label_resultados.setText("No hay imágenes resultantes.")
            self.contador_resultados.setText("0 de 0")






        

if __name__ == "__main__":
    # Limpiar carpeta 'imagenes/cargadas/' al iniciar
    if os.path.exists(CARPETA_IMAGENES):
        for archivo in os.listdir(CARPETA_IMAGENES):
            archivo_path = os.path.join(CARPETA_IMAGENES, archivo)
            if os.path.isfile(archivo_path):
                os.remove(archivo_path)

    app = QApplication(sys.argv)
    ventana = DetectorApp()
    ventana.show()
    sys.exit(app.exec_())
