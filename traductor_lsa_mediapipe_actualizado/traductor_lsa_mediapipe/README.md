# Traductor educativo de señas con MediaPipe: dos manos + rostro

Proyecto de Python que detecta hasta dos manos y un rostro, extrae landmarks, entrena un clasificador Random Forest y muestra etiquetas en pantalla.

**Limitación:** es un prototipo educativo para un vocabulario de señas estáticas. No traduce automáticamente toda la Lengua de Señas Argentina (LSA). Las señas dinámicas y los componentes lingüísticos requieren secuencias temporales, datos anotados y validación con usuarios competentes en LSA.

## Archivos

- `descargar_modelo.py`: descarga el modelo de manos.
- `descargar_modelo_rostro.py`: descarga el modelo facial.
- `mediapipe_utils.py`: detectores, extracción y normalización de landmarks.
- `prueba_mediapipe.py`: verifica la cámara, dos manos y rostro.
- `capturar_dataset.py`: captura muestras etiquetadas en CSV.
- `entrenar.py`: entrena y evalúa el Random Forest.
- `traductor.py`: reconoce clases entrenadas y arma texto.

## Instalación (Windows)

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python descargar_modelo.py
python descargar_modelo_rostro.py
python prueba_mediapipe.py
```

Si la cámara no abre, probá cambiar `cv2.VideoCapture(0)` por `cv2.VideoCapture(1)` y cerrá otras aplicaciones que usen la cámara.

## Uso

1. Ejecutá `python prueba_mediapipe.py` y confirmá que aparecen las manos y puntos faciales. `Q` cierra la ventana.
2. Ejecutá `python capturar_dataset.py`.
3. Escribí una etiqueta, por ejemplo `HOLA`, y mantené la seña estática delante de la cámara. Para obtener muestras más variadas, mové ligeramente la mano entre capturas sin cambiar la seña. Repetí con cada etiqueta. Se guardan hasta 250 muestras por etiqueta.
4. Ejecutá `python entrenar.py`.
5. Ejecutá `python traductor.py`.

Controles del traductor: `Q` salir, `ESPACIO` insertar separación, `B` borrar última entrada, `C` limpiar y `R` permitir repetir la misma etiqueta consecutivamente.

## Formato de datos

Cada fila tiene 1.560 características: 126 para dos manos (2 × 21 landmarks × 3 coordenadas) y 1.434 para el rostro (478 × 3). Si no se detecta una mano, su bloque queda en cero; el capturador exige al menos una mano y un rostro visibles. El orden de las manos se basa en su posición horizontal en pantalla y no garantiza identificar la lateralidad anatómica.

Si cambiaste de la versión anterior que solo guardaba 63 características, **capturá un dataset nuevo**. Los CSV antiguos se omiten durante el entrenamiento.

## Consejos de calidad

- Grabá las clases con buena iluminación, manos y rostro visibles y fondo relativamente simple.
- Evitá tener casi todas las muestras consecutivas de una única toma: variá ligeramente distancia, orientación y sesión.
- La exactitud del test aleatorio por frames no equivale al rendimiento real; probá luego con otra sesión o persona.
- Para LSA completa, agregá secuencias de landmarks, orientación, expresión facial y contexto; un clasificador de una sola muestra no basta.
