import cv2
import os
import re
import numpy as np

def extract_car_frames(video_path, output_dir, start_minute=0, frame_interval=50, image_size=(80, 80)):
    
    net = cv2.dnn.readNet("src/yolov3.weights", "src/yolov3.cfg")  # Reemplaza con tu modelo YOLO
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

   
    with open("src/coco.names", "r") as f:
        classes = f.read().strip().split("\n")

    # Crear la carpeta de salida si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Obtener el último índice en la carpeta
    existing_files = [f for f in os.listdir(output_dir) if f.startswith("volvoXC40_") and f.endswith(".jpg")]
    if existing_files:
        last_index = max([int(re.search(r"(\d+)", f).group()) for f in existing_files])
    else:
        last_index = -1 

    frame_count = last_index + 1

    cap = cv2.VideoCapture(video_path)
    
    # Configurar el inicio del video en el minuto especificado
    fps = cap.get(cv2.CAP_PROP_FPS) 
    start_frame = int(start_minute * 60 * fps)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    count = start_frame

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break


        if count % frame_interval == 0:
            height, width, _ = frame.shape
            
            # Crear blob para YOLO
            blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
            net.setInput(blob)
            detections = net.forward(output_layers)

            for detection in detections:
                for obj in detection:
                    scores = obj[5:]
                    class_id = int(scores.argmax())
                    confidence = scores[class_id]

                    if classes[class_id] == "car" and confidence > 0.5:
                        # Obtener coordenadas del bounding box
                        center_x, center_y, w, h = (obj[0:4] * [width, height, width, height]).astype("int")
                        x = max(0, int(center_x - w / 2))
                        y = max(0, int(center_y - h / 2))
                        w = min(w, width - x)
                        h = min(h, height - y)

                        if w > 0 and h > 0:
                            cropped_car = frame[y:y+h, x:x+w]
                            resized_car = cv2.resize(cropped_car, image_size)

                            # Guardar la imagen original y las rotaciones
                            for angle in range(0, 360, 30):
                                M = cv2.getRotationMatrix2D((image_size[0] // 2, image_size[1] // 2), angle, 1.0)
                                rotated_car = cv2.warpAffine(resized_car, M, image_size)

                                frame_name = os.path.join(output_dir, f"volvoXC40_{frame_count:05d}.jpg")
                                cv2.imwrite(frame_name, rotated_car)
                                print(f"Saved {frame_name}")
                                frame_count += 1

        count += 1

    cap.release()
    print(f"Extracted {frame_count - (last_index + 1)} car frames to {output_dir}")

# Ejemplo de uso
extract_car_frames(
    video_path="src/videos/volvoxc40/volvo xc400.mp4",
    output_dir="src/dataset/volvoXC40",
    start_minute=0,
    frame_interval=50,
    image_size=(80, 80)
)
