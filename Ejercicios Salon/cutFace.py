import numpy as np
import cv2 as cv

# Cargar el clasificador para rostros
rostro_cascade = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')

# Iniciar la captura de video
cap = cv.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error al acceder a la cámara.")
        break

    # Convertir a escala de grises
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detectar rostros en el fotograma
    detected_faces = rostro_cascade.detectMultiScale(
        gray_frame, scaleFactor=1.2, minNeighbors=4, minSize=(30, 30)
    )

    # Procesar cada rostro detectado
    for idx, (x, y, w, h) in enumerate(detected_faces):
        # Dibujar un círculo en lugar de un rectángulo para destacar el rostro
        center = (x + w // 2, y + h // 2)
        radius = max(w, h) // 2
        cv.circle(frame, center, radius, (255, 0, 0), 2)

        # Extraer el área del rostro
        face_roi = gray_frame[y:y + h, x:x + w]

        # Aplicar un filtro GaussianBlur al rostro detectado
        blurred_face = cv.GaussianBlur(face_roi, (15, 15), 0)

        # Redimensionar la región para mostrarla por separado
        resized_face = cv.resize(blurred_face, (80, 80), interpolation=cv.INTER_LINEAR)

        # Mostrar el rostro redimensionado en una ventana
        window_name = f"Rostro {idx + 1}"
        cv.imshow(window_name, resized_face)

    # Mostrar el fotograma completo con los rostros destacados
    cv.imshow('Video en Vivo', frame)

    # Salir con la tecla 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv.destroyAllWindows()
