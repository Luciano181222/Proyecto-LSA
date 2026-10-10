import time
from pathlib import Path
import cv2
import joblib
import numpy as np
from mediapipe_utils import crear_detectores, detectar_en_frame, dibujar_resultados

RUTA_MODELO = Path("modelos/modelo.pkl")
CONFIANZA_MINIMA = 0.70
FRAMES_CONFIRMACION = 8


def main():
    if not RUTA_MODELO.exists():
        raise FileNotFoundError("Falta modelos/modelo.pkl. Ejecutá python entrenar.py primero.")
    modelo = joblib.load(RUTA_MODELO)
    detectores = crear_detectores()
    camara = cv2.VideoCapture(0)
    if not camara.isOpened():
        for detector in detectores:
            detector.close()
        raise RuntimeError("No se pudo abrir la cámara.")

    palabras = []
    prediccion_anterior = None
    contador = 0
    ultima_agregada = None
    permitir_repeticion = False
    try:
        print("Traductor activo: Q salir | ESPACIO espacio | B borrar | C limpiar | R habilitar repetición")
        while True:
            ok, frame = camara.read()
            if not ok:
                break
            frame = cv2.flip(frame, 1)
            manos, rostro, vector = detectar_en_frame(detectores, frame)
            frame = dibujar_resultados(frame, manos, rostro)
            clase = "---"
            confianza = 0.0
            if manos.hand_landmarks and rostro.face_landmarks:
                probabilidades = modelo.predict_proba([vector])[0]
                idx = int(np.argmax(probabilidades))
                clase = str(modelo.classes_[idx])
                confianza = float(probabilidades[idx])
                if confianza >= CONFIANZA_MINIMA:
                    if clase == prediccion_anterior:
                        contador += 1
                    else:
                        prediccion_anterior = clase
                        contador = 1
                    if contador >= FRAMES_CONFIRMACION and (clase != ultima_agregada or permitir_repeticion):
                        palabras.append(clase)
                        ultima_agregada = clase
                        permitir_repeticion = False
                        contador = 0
                else:
                    prediccion_anterior = None
                    contador = 0
            else:
                prediccion_anterior = None
                contador = 0

            cv2.putText(frame, f"Seña: {clase} ({confianza:.0%})", (15, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Manos: {len(manos.hand_landmarks or [])} | Rostro: {len(rostro.face_landmarks or [])}",
                        (15, 67), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            texto = " ".join(palabras)[-65:]
            cv2.rectangle(frame, (8, frame.shape[0]-65), (frame.shape[1]-8, frame.shape[0]-12), (0,0,0), -1)
            cv2.putText(frame, texto, (18, frame.shape[0]-30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2)
            cv2.imshow("Traductor de señas", frame)
            tecla = cv2.waitKey(1) & 0xFF
            if tecla == ord('q'):
                break
            elif tecla == 32:
                palabras.append("")
                ultima_agregada = None
            elif tecla == ord('b'):
                if palabras:
                    palabras.pop()
                ultima_agregada = palabras[-1] if palabras else None
            elif tecla == ord('c'):
                palabras.clear()
                ultima_agregada = None
            elif tecla == ord('r'):
                permitir_repeticion = True
    finally:
        camara.release()
        cv2.destroyAllWindows()
        for detector in detectores:
            detector.close()

if __name__ == "__main__":
    main()
