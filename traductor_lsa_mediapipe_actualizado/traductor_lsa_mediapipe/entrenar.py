import csv
from pathlib import Path
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from mediapipe_utils import TOTAL_CARACTERISTICAS

DATASET = Path("dataset")
CARPETA_MODELOS = Path("modelos")


def cargar_dataset():
    X, y = [], []
    for archivo in sorted(DATASET.glob("*.csv")):
        with archivo.open("r", newline="", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            requeridas = [f"f{i}" for i in range(TOTAL_CARACTERISTICAS)]
            if not lector.fieldnames or not all(c in lector.fieldnames for c in requeridas):
                print(f"Aviso: se omite {archivo}; no tiene las {TOTAL_CARACTERISTICAS} características nuevas.")
                continue
            for fila in lector:
                try:
                    valores = [float(fila[c]) for c in requeridas]
                    etiqueta = fila["label"].strip()
                except (ValueError, KeyError, TypeError):
                    continue
                if etiqueta:
                    X.append(valores)
                    y.append(etiqueta)
    if not X:
        raise RuntimeError("No hay datos válidos. Ejecutá capturar_dataset.py para crear el dataset actualizado.")
    return np.asarray(X, dtype=np.float32), np.asarray(y)


def main():
    X, y = cargar_dataset()
    clases, conteos = np.unique(y, return_counts=True)
    print(f"Muestras: {len(X)} | Características por muestra: {X.shape[1]}")
    for clase, n in zip(clases, conteos):
        print(f"  {clase}: {n}")
    if len(clases) < 2:
        raise RuntimeError("Necesitás al menos dos clases diferentes.")
    if np.min(conteos) < 2:
        raise RuntimeError("Cada clase necesita al menos 2 muestras para dividir entrenamiento y prueba.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    modelo = RandomForestClassifier(n_estimators=300, random_state=42,
                                    n_jobs=-1, class_weight="balanced")
    modelo.fit(X_train, y_train)
    pred = modelo.predict(X_test)
    print(f"\nExactitud de prueba: {accuracy_score(y_test, pred):.2%}")
    print(classification_report(y_test, pred, zero_division=0))
    CARPETA_MODELOS.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, CARPETA_MODELOS / "modelo.pkl")
    print("Modelo guardado en modelos/modelo.pkl")
    print("Nota: la prueba aleatoria por frames puede sobreestimar el rendimiento; probá también con sesiones/personas distintas.")

if __name__ == "__main__":
    main()
