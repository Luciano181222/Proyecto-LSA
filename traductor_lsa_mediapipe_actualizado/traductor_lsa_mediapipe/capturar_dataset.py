import csv
import time
from pathlib import Path
import cv2
from mediapipe_utils import (crear_detectores, detectar_en_frame, dibujar_resultados,
                             TOTAL_CARACTERISTICAS)

DATASET = Path("dataset")
MUESTRAS_POR_CLASE = 250
INTERVALO_SEGUNDOS = 0.08


def capturar_clase(etiqueta):
    DATASET.mkdir(parents=True, exist_ok=True)
    archivo = DATASET / f"{etiqueta}.csv"
    # Si ya existe, no agregamos datos con posibles formatos anteriores por accidente.
    modo = "a" if archivo.exists() else "w"
    escribir_cabecera = modo == "w"
    detectores = crear_detectores()
    camara = cv2.VideoCapture(0)
    if not camara.isOpened():
        for detector in detectores:
            detector.close()
        raise RuntimeError("No se pudo abrir la cámara.")

    cantidad = 0
    ultima_muestra = 0.0
    pausado = False
    try:
        with archivo.open(modo, newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            if escribir_cabecera:
                escritor.writerow(["label"] + [f"f{i}" for i in range(TOTAL_CARACTERISTICAS)])
            print(f"Capturando {etiqueta}: objetivo {MUESTRAS_POR_CLASE} muestras. P pausa, Q/Esc salir.")
            while cantidad < MUESTRAS_POR_CLASE:
                ok, frame = camara.read()
                if not ok:
                    break
                frame = cv2.flip(frame, 1)
                manos, rostro, vector = detectar_en_frame(detectores, frame)
                frame = dibujar_resultados(frame, manos, rostro)
                ahora = time.time()
                # Evitar muestras vacías: requerimos al menos una mano y una cara.
                hay_mano = bool(manos.hand_landmarks)
                hay_rostro = bool(rostro.face_landmarks)
                if not pausado and hay_mano and hay_rostro and ahora - ultima_muestra >= INTERVALO_SEGUNDOS:
                    escritor.writerow([etiqueta] + vector.tolist())
                    f.flush()
                    cantidad += 1
                    ultima_muestra = ahora
                estado = "PAUSADO" if pausado else f"{etiqueta}: {cantidad}/{MUESTRAS_POR_CLASE}"
                cv2.putText(frame, estado, (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                            (0, 0, 255) if pausado else (0, 255, 0), 2)
                cv2.putText(frame, f"Manos: {len(manos.hand_landmarks or [])} | Cara: {int(hay_rostro)}",
                            (15, 68), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 0), 2)
                cv2.imshow("Captura del dataset", frame)
                tecla = cv2.waitKey(1) & 0xFF
                if tecla in (27, ord('q')):
                    break
                if tecla == ord('p'):
                    pausado = not pausado
    finally:
        camara.release()
        cv2.destroyAllWindows()
        for detector in detectores:
            detector.close()
    print(f"Muestras capturadas para {etiqueta}: {cantidad}")


def main():
    print("CAPTURA DE SEÑAS ESTÁTICAS: mantené la seña quieta unos instantes.")
    print("Para cada clase se guardan landmarks de hasta 2 manos y 1 rostro.")
    while True:
        etiqueta = input("Etiqueta (por ejemplo HOLA; ENTER termina): ").strip().upper()
        if not etiqueta:
            break
        etiqueta = "".join(c if c.isalnum() or c == "_" else "_" for c in etiqueta)
        capturar_clase(etiqueta)

if __name__ == "__main__":
    main()
