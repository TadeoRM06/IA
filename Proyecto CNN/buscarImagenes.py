import cv2
import os
import re
from bing_image_downloader import downloader

def process_images(query_string, output_dir, limit=5, image_size=(80, 80)):
    os.makedirs(output_dir, exist_ok=True)

    # Obtener el último índice en la carpeta
    existing_files = [f for f in os.listdir(output_dir) if f.startswith("fordGT_") and f.endswith(".jpg")]
    if existing_files:
        last_index = max([int(re.search(r"(\d+)", f).group()) for f in existing_files])
    else:
        last_index = -1 

    frame_count = last_index + 1

    # Descargar las imágenes con bing_image_downloader
    downloader.download(
        query_string,
        limit=limit,
        output_dir="temp",
        adult_filter_off=True,
        force_replace=False,
        timeout=120,
        verbose=True
    )

    # Procesar cada imagen descargada
    downloaded_dir = os.path.join("temp", query_string)
    for file_name in os.listdir(downloaded_dir):
        image_path = os.path.join(downloaded_dir, file_name)
        image = cv2.imread(image_path)
        if image is None:
            continue

        # Redimensionar la imagen
        resized_image = cv2.resize(image, image_size)

        # Guardar la imagen original y las rotaciones
        for angle in range(0, 360, 30):
            M = cv2.getRotationMatrix2D((image_size[0] // 2, image_size[1] // 2), angle, 1.0)
            rotated_image = cv2.warpAffine(resized_image, M, image_size)

            frame_name = os.path.join(output_dir, f"fordGT_{frame_count:05d}.jpg")
            cv2.imwrite(frame_name, rotated_image)
            print(f"Saved {frame_name}")
            frame_count += 1

    # Eliminar la carpeta temporal
    for file_name in os.listdir(downloaded_dir):
        os.remove(os.path.join(downloaded_dir, file_name))
    os.rmdir(downloaded_dir)
    print(f"Processed and saved {frame_count - (last_index + 1)} images to {output_dir}")

# Ejemplo de uso
process_images(
    query_string="ford gt40 mk1 1964",
    output_dir="src/dataset/fordGT/",
    limit=2,                           # Número de imágenes a descargar
    image_size=(80, 80),               # Tamaño de salida de las imágenes
)
