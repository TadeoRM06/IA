import numpy as np
import cv2 as cv
import math

# Cargamos el clasificador para rostros
rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()  # Capturamos el frame actual
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  # Convertimos el frame a escala de grises
    rostros = rostro.detectMultiScale(gray, 1.3, 5)  # Detectamos los rostros en la imagen

    for (x, y, w, h) in rostros:
        # Dibujamos un rectángulo alrededor del rostro detectado
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Extraemos la región del rostro del frame
        frame2 = frame[y:y + h, x:x + w]

        # Redimensionamos la imagen del rostro a un tamaño de 80x80 píxeles
        frame2 = cv.resize(frame2, (80, 80), interpolation=cv.INTER_AREA)

        # Convertimos la imagen redimensionada a escala de grises
        gray_face = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)

        # Mostramos el rostro en color y en escala de grises
        cv.imshow('Rostro', frame2)
        cv.imshow('Gray', gray_face)

        # Calcular el número de píxeles del rostro
        total_pixels_face = w * h  # Total de píxeles en el rostro detectado
        print(f'Tamaño del rostro: {total_pixels_face} píxeles.')

        # Definimos un rango de grises para la máscara
        min_gray = int(0.5 * np.mean(gray_face))
        max_gray = int(1.5 * np.mean(gray_face))

        # Contamos los píxeles que están en el rango de grises definido
        mask = cv.inRange(gray_face, min_gray, max_gray)
        count_pixels_in_range = cv.countNonZero(mask)

        # Mostramos el resultado de la máscara
        cv.imshow('Mask', mask)

        # Imprimimos el número de píxeles que están dentro del rango de grises
        print(f'Píxeles dentro del rango de grises [{min_gray}, {max_gray}]: {count_pixels_in_range}')

    # Mostramos la imagen con los rectángulos dibujados
    cv.imshow('Rostros', frame)

    k = cv.waitKey(1)
    if k == 27:  # Presionamos 'Esc' para salir
        break

# Liberamos los recursos
cap.release()
cv.destroyAllWindows()
