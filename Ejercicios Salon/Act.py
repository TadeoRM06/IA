import numpy as np
import cv2 as cv
import math

# Cargar el clasificador de rostros
rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture(0)
i = 0

# Inicializar lista para almacenar cambios en los píxeles blancos
diferencias_blancos = []

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el video.")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4)

    for (x, y, w, h) in rostros:
        # Recortar el rostro detectado y redimensionarlo
        rostro_detectado = frame[y:y+h, x:x+w]
        rostro_resized = cv.resize(rostro_detectado, (100, 100), interpolation=cv.INTER_CUBIC)

        # Convertir a escala de grises
        rostro_gray = cv.cvtColor(rostro_resized, cv.COLOR_BGR2GRAY)

        # Aplicar umbral adaptativo para mejorar la detección
        binario = cv.adaptiveThreshold(rostro_gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv.THRESH_BINARY, 11, 2)

        # Contar píxeles blancos
        blancos_actual = cv.countNonZero(binario)

        # Calcular y almacenar la diferencia respecto al anterior
        if i > 0:
            diferencia_blancos = blancos_actual - diferencias_blancos[-1]
            print(f'Frame {i}: Blancos actuales: {blancos_actual}, Diferencia: {diferencia_blancos}')
        else:
            print(f'Frame {i}: Blancos actuales: {blancos_actual}')

        diferencias_blancos.append(blancos_actual)

        # Guardar la imagen procesada (opcional)
        cv.imwrite(f'capturas/TadeoFaceProcessed_{i}.jpg', binario)

        # Mostrar la imagen binaria procesada
        cv.imshow('Rostro Procesado', binario)

    # Mostrar la imagen original con rectángulos alrededor de los rostros detectados
    for (x, y, w, h) in rostros:
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv.imshow('Detección de Rostros', frame)

    i += 1
    if cv.waitKey(1) & 0xFF == 27:  # Presionar 'Esc' para salir
        break

cap.release()
cv.destroyAllWindows()
