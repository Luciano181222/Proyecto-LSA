import cv2
from mediapipe_utils import crear_detectores, detectar_en_frame, dibujar_resultados


def main():
    detectores = crear_detectores()
    camara = cv2.VideoCapture(0)
    if not camara.isOpened():
        for detector in detectores:
            detector.close()
        raise RuntimeError("No se pudo abrir la cámara. Revisá los permisos o probá VideoCapture(1).")
    try:
        print("Detector activo. Presioná Q para salir.")
        while True:
            ok, frame = camara.read()
            if not ok:
                break
            frame = cv2.flip(frame, 1)
            manos, rostro, _ = detectar_en_frame(detectores, frame)
            frame = dibujar_resultados(frame, manos, rostro)
            n_manos = len(manos.hand_landmarks or [])
            n_rostros = len(rostro.face_landmarks or [])
            cv2.putText(frame, f"Manos: {n_manos} | Rostros: {n_rostros}", (15, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            cv2.imshow("Detector de dos manos y rostro", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        camara.release()
        cv2.destroyAllWindows()
        for detector in detectores:
            detector.close()

if __name__ == "__main__":
    main()
