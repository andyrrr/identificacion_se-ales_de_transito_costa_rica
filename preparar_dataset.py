import os
import shutil
import random
import yaml

# === CONFIGURACIÓN ===
DATASET_DIR = "dataset"
IMAGES_DIR = os.path.join(DATASET_DIR, "images")
LABELS_DIR = os.path.join(DATASET_DIR, "labels")
TRAIN_RATIO = 0.9

# === CREAR SUBCARPETAS ===
for subfolder in ["train", "val"]:
    os.makedirs(os.path.join(IMAGES_DIR, subfolder), exist_ok=True)
    os.makedirs(os.path.join(LABELS_DIR, subfolder), exist_ok=True)

# === LISTAR Y MEZCLAR IMÁGENES ===
image_files = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith((".jpg", ".png"))]
random.shuffle(image_files)

# === DIVIDIR EN TRAIN Y VAL ===
split_index = int(len(image_files) * TRAIN_RATIO)
train_files = image_files[:split_index]
val_files = image_files[split_index:]

# === FUNCIONES DE COPIA ===
def mover_archivos(file_list, destino):
    for fname in file_list:
        name_stem = os.path.splitext(fname)[0]
        # Imagen
        src_img = os.path.join(IMAGES_DIR, fname)
        dst_img = os.path.join(IMAGES_DIR, destino, fname)
        shutil.move(src_img, dst_img)
        # Etiqueta
        src_lbl = os.path.join(LABELS_DIR, name_stem + ".txt")
        dst_lbl = os.path.join(LABELS_DIR, destino, name_stem + ".txt")
        if os.path.exists(src_lbl):
            shutil.move(src_lbl, dst_lbl)

mover_archivos(train_files, "train")
mover_archivos(val_files, "val")

# === LEER CLASSES.TXT ===
classes_txt_path = os.path.join(DATASET_DIR, "classes.txt")
with open(classes_txt_path, "r") as f:
    class_names = [line.strip() for line in f.readlines()]

# === CREAR data.yaml ===
yaml_data = {
    "train": os.path.join(IMAGES_DIR, "train"),
    "val": os.path.join(IMAGES_DIR, "val"),
    "nc": len(class_names),
    "names": class_names
}

with open(os.path.join(DATASET_DIR, "data.yaml"), "w") as f:
    yaml.dump(yaml_data, f, sort_keys=False)

print("✅ Dataset preparado con éxito.")
