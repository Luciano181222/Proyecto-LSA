from pathlib import Path
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODELO_MANOS = Path("models/hand_landmarker.task")
MODELO_ROSTRO = Path("models/face_landmarker.task")
PUNTOS_MANO = 21
COORDENADAS = 3
MAX_MANOS = 2
PUNTOS_ROSTRO = 478
CARACTERISTICAS_MANOS = MAX_MANOS * PUNTOS_MANO * COORDENADAS  # 126
CARACTERISTICAS_ROSTRO = PUNTOS_ROSTRO * COORDENADAS          # 1434
TOTAL_CARACTERISTICAS = CARACTERISTICAS_MANOS + CARACTERISTICAS_ROSTRO  # 1560


def crear_detectores():
    if not MODELO_MANOS.exists():
        raise FileNotFoundError("Falta models/hand_landmarker.task. Ejecutá python descargar_modelo.py")
    if not MODELO_ROSTRO.exists():
        raise FileNotFoundError("Falta models/face_landmarker.task. Ejecutá python descargar_modelo_rostro.py")

    opciones_manos = vision.HandLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path=str(MODELO_MANOS)),
        num_hands=2,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    opciones_rostro = vision.FaceLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path=str(MODELO_ROSTRO)),
        num_faces=1,
        min_face_detection_confidence=0.5,
        min_face_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    return (vision.HandLandmarker.create_from_options(opciones_manos),
            vision.FaceLandmarker.create_from_options(opciones_rostro))


def _normalizar_puntos(puntos, indice_origen=0):
    origen = puntos[indice_origen]
    valores = []
    for p in puntos:
        valores.extend([p.x - origen.x, p.y - origen.y, p.z - origen.z])
    valores = np.asarray(valores, dtype=np.float32)
    escala = float(np.max(np.abs(valores))) if valores.size else 0.0
    if escala > 1e-6:
        valores /= escala
    return valores


def detectar_en_frame(detectores, frame):
    manos_detector, rostro_detector = detectores
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imagen = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    resultado_manos = manos_detector.detect(imagen)
    resultado_rostro = rostro_detector.detect(imagen)

    # Reservar dos bloques fijos. Se ordenan por x en pantalla para que el
    # vector tenga un orden estable; no representa necesariamente lateralidad anatómica.
    datos_manos = np.zeros(CARACTERISTICAS_MANOS, dtype=np.float32)
    manos_detectadas = resultado_manos.hand_landmarks or []
    manos_ordenadas = sorted(manos_detectadas, key=lambda mano: mano[0].x)
    for i, mano in enumerate(manos_ordenadas[:MAX_MANOS]):
        vector = _normalizar_puntos(mano, 0)
        inicio = i * PUNTOS_MANO * COORDENADAS
        datos_manos[inicio:inicio + len(vector)] = vector

    datos_rostro = np.zeros(CARACTERISTICAS_ROSTRO, dtype=np.float32)
    caras = resultado_rostro.face_landmarks or []
    if caras:
        cara = caras[0]
        # El Face Landmarker habitual devuelve 478 landmarks. Si la versión/modelo
        # devuelve otra cantidad, se ajusta a un vector de tamaño fijo.
        vector_cara = _normalizar_puntos(cara, min(1, len(cara) - 1))
        n = min(len(vector_cara), CARACTERISTICAS_ROSTRO)
        datos_rostro[:n] = vector_cara[:n]

    vector_completo = np.concatenate([datos_manos, datos_rostro])
    return resultado_manos, resultado_rostro, vector_completo


def dibujar_resultados(frame, resultado_manos, resultado_rostro):
    alto, ancho = frame.shape[:2]
    conexiones = [
        (0,1),(1,2),(2,3),(3,4), (0,5),(5,6),(6,7),(7,8),
        (5,9),(9,10),(10,11),(11,12), (9,13),(13,14),(14,15),(15,16),
        (13,17),(17,18),(18,19),(19,20),(0,17)
    ]
    for mano in (resultado_manos.hand_landmarks or []):
        pts = [(int(p.x * ancho), int(p.y * alto)) for p in mano]
        for x, y in pts:
            cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)
        for a, b in conexiones:
            cv2.line(frame, pts[a], pts[b], (255, 255, 255), 2)

    # Dibujar una selección de puntos faciales para visualizar la detección.
    indices = [1, 10, 33, 61, 133, 152, 199, 263, 291, 362]
    for cara in (resultado_rostro.face_landmarks or []):
        for i in indices:
            if i < len(cara):
                p = cara[i]
                cv2.circle(frame, (int(p.x * ancho), int(p.y * alto)), 3, (255, 0, 255), -1)
    return frame
