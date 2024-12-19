import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Cargar los datos desde el JSON
df = pd.read_json('datos_juego.json')

# Asegurarse de que las columnas tengan los nombres correctos
df.columns = ['x1', 'x2', 'target']  # Ajusta si los nombres en tu JSON son diferentes

# Crear la figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Graficar puntos con target=0
ax.scatter(df[df['target'] == 0]['x1'], df[df['target'] == 0]['x2'], df[df['target'] == 0]['target'],
           c='blue', marker='o', label='target=0')

# Graficar puntos con target=1
ax.scatter(df[df['target'] == 1]['x1'], df[df['target'] == 1]['x2'], df[df['target'] == 1]['target'],
           c='red', marker='x', label='target=1')

# Etiquetas de los ejes
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('Target')

# Mostrar leyenda
ax.legend()

# Mostrar el gráfico
plt.show()
