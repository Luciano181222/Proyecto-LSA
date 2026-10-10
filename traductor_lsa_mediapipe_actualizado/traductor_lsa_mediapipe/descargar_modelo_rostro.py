from pathlib import Path
from urllib.request import urlretrieve

URL = ("https://storage.googleapis.com/mediapipe-models/"
       "face_landmarker/face_landmarker/float16/1/face_landmarker.task")
DESTINO = Path("models/face_landmarker.task")

if __name__ == "__main__":
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    if not DESTINO.exists():
        print("Descargando modelo facial...")
        urlretrieve(URL, DESTINO)
    print(f"Modelo facial listo: {DESTINO}")
