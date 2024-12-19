import numpy as np
import cv2 as cv

# Inicializa la captura de video
cap = cv.VideoCapture(0)

# Leer el primer cuadro para usarlo como referencia
ret, frame_referencia = cap.read()
if not ret:
    print("No se pudo acceder a la cámara.")
    cap.release()
    cv.destroyAllWindows()
    exit()

frame_referencia_gray = cv.cvtColor(frame_referencia, cv.COLOR_BGR2GRAY)
frame_referencia_gray = cv.GaussianBlur(frame_referencia_gray, (15, 15), 0)

contador = 0

while cap.isOpened():
    ret, frame_actual = cap.read()
    if not ret:
        break

    # Convertir el cuadro actual a escala de grises y aplicar un desenfoque
    frame_actual_gray = cv.cvtColor(frame_actual, cv.COLOR_BGR2GRAY)
    frame_actual_gray = cv.GaussianBlur(frame_actual_gray, (15, 15), 0)

    # Calcular la diferencia absoluta entre el cuadro de referencia y el cuadro actual
    diferencia = cv.absdiff(frame_referencia_gray, frame_actual_gray)

    # Aplicar un umbral adaptativo para obtener la imagen binaria
    umbral = cv.adaptiveThreshold(diferencia, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)

    # Erosionar y luego dilatar para limpiar el ruido
    umbral = cv.morphologyEx(umbral, cv.MORPH_CLOSE, None)

    # Encontrar los contornos en la imagen binaria
    contornos, _ = cv.findContours(umbral, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for contorno in contornos:
        if cv.contourArea(contorno) < 700:  # Ignorar pequeñas áreas
            continue

        # Dibujar el contorno detectado en el cuadro actual
        cv.drawContours(frame_actual, [contorno], -1, (0, 0, 255), 2)

        # Obtener las coordenadas del rectángulo delimitador
        (x, y, w, h) = cv.boundingRect(contorno)

        # Recortar y procesar el área de interés
        objeto_movimiento = frame_actual[y:y+h, x:x+w]
        objeto_resized = cv.resize(objeto_movimiento, (100, 100), interpolation=cv.INTER_CUBIC)

        # Mostrar el área recortada
        cv.imshow('Área en Movimiento', objeto_resized)

        # Guardar el recorte del objeto
        cv.imwrite(f'captured_objects/control_{contador}.jpg', objeto_resized)
        contador += 1

    # Mostrar el cuadro con los contornos
    cv.imshow('Detección de Movimiento', frame_actual)

    # Actualizar el cuadro de referencia con un promedio ponderado para mayor estabilidad
    frame_referencia_gray = cv.addWeighted(frame_referencia_gray, 0.9, frame_actual_gray, 0.1, 0)

    # Presionar 'q' para salir
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv.destroyAllWindows()
