import cv2

# Cargar el clasificador para detección de rostros
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

# Iniciar la captura de video
video_stream = cv2.VideoCapture(0)

def draw_face_features(image, x, y, w, h):
    """Dibuja un rectángulo y características faciales sobre el rostro detectado."""
    # Dibujar rectángulo alrededor del rostro
    cv2.rectangle(image, (x, y), (x + w, y + h), (234, 23, 23), 2)

    # Dibujar una segunda área en la parte inferior del rostro
    cv2.rectangle(image, (x, y + h // 2), (x + w, y + h), (0, 255, 0), 5)

    # Dibujar los ojos como círculos
    left_eye = (x + int(w * 0.3), y + int(h * 0.4))
    right_eye = (x + int(w * 0.7), y + int(h * 0.4))
    for eye in [left_eye, right_eye]:
        cv2.circle(image, eye, 21, (0, 0, 0), 2)
        cv2.circle(image, eye, 20, (255, 255, 255), -1)
        cv2.circle(image, eye, 5, (0, 0, 255), -1)

while True:
    # Leer cada cuadro
    ret, frame = video_stream.read()
    if not ret:
        print("Error al capturar el frame.")
        break

    # Convertir a escala de grises
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en el frame
    detected_faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

    # Dibujar características en cada rostro detectado
    for (x, y, w, h) in detected_faces:
        draw_face_features(frame, x, y, w, h)

    # Mostrar el resultado
    cv2.imshow('Detección de Rostros', frame)

    # Salir al presionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Saliendo del programa...")
        break

# Liberar recursos
video_stream.release()
cv2.destroyAllWindows()
