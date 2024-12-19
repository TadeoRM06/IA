import cv2
import numpy as np

def main():
    # Inicializar la cámara
    video_capture = cv2.VideoCapture(0)

    # Definir los límites de color en HSV para rastreo
    color_range = {
        "lower": np.array([40, 150, 0]),
        "upper": np.array([85, 255, 255])
    }

    while True:
        # Leer cada cuadro de la cámara
        is_frame_captured, frame = video_capture.read()
        if not is_frame_captured:
            print("No se pudo capturar el frame.")
            break

        # Convertir el frame al espacio de color HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Crear una máscara para el color seleccionado
        color_mask = cv2.inRange(hsv_frame, color_range["lower"], color_range["upper"])

        # Aplicar operaciones morfológicas para limpiar la máscara
        processed_mask = cv2.morphologyEx(color_mask, cv2.MORPH_OPEN, None, iterations=2)
        processed_mask = cv2.morphologyEx(processed_mask, cv2.MORPH_CLOSE, None, iterations=2)

        # Detectar contornos en la máscara procesada
        contours, _ = cv2.findContours(processed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Identificar y dibujar el objeto más grande
        if contours:
            main_contour = max(contours, key=cv2.contourArea)
            (center_x, center_y), radius = cv2.minEnclosingCircle(main_contour)

            # Dibujar solo si el radio del círculo es significativo
            if radius > 10:
                center = (int(center_x), int(center_y))
                cv2.circle(frame, center, int(radius), (255, 0, 0), 2)
                cv2.circle(frame, center, 5, (0, 255, 0), -1)

        # Mostrar los cuadros
        cv2.imshow('Camara', frame)
        cv2.imshow('Mascara', processed_mask)

        # Salir al presionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Saliendo del programa...")
            break

    # Liberar recursos
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
