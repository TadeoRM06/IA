def generate_opacity_variants(input_folder, alphas):
    import os
    import cv2
    
    # Generar variantes con diferentes opacidades
    for file_name in os.listdir(input_folder):
        base_name, ext = os.path.splitext(file_name)
        image_path = os.path.join(input_folder, file_name)
        image = cv2.imread(image_path)

        for alpha in alphas:
            # Aplicar opacidad
            variant = apply_opacity(image, alpha)

            # Guardar la imagen resultante en la misma carpeta de entrada
            output_name = f"{base_name}_opacity_{int(alpha * 100)}{ext}"
            output_path = os.path.join(input_folder, output_name)
            cv2.imwrite(output_path, variant)
            print(f"Guardada: {output_path}")

# Parámetros
input_folder = r"D:\cnn (3)\cnn\src\Tsuru"  # Ruta de la carpeta con las imágenes
opacity_levels = [0.3, 0.5, 0.7]  # Niveles de opacidad (30%, 50%, 70%, 100%)

# Generar variantes
generate_opacity_variants(input_folder, opacity_levels)
