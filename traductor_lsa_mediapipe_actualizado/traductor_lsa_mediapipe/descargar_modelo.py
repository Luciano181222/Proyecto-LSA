from pathlib import Path
from urllib.request import urlretrieve

URL = ("https://storage.googleapis.com/mediapipe-models/"
       "hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task")
DESTINO = Path("models/hand_landmarker.task")

if __name__ == "__main__":
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    if not DESTINO.exists():
        print("Descargando modelo de manos...")
        urlretrieve(URL, DESTINO)
    print(f"Modelo de manos listo: {DESTINO}")
