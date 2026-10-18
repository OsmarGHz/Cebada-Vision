"""Rellena reports/anexos.md con la tabla de las 59 predicciones (en 3 columnas) y los enlaces, y
produce reports/anexos_final.md listo para convertir a PDF.

Uso:  .venv/Scripts/python.exe src/generar_anexos.py [URL_APP] [URL_VIDEO]
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SUB = ROOT / "submissions" / "predicciones_59_CebadaVision.csv"


def tabla_3_columnas(df):
    n = len(df)
    k = -(-n // 3)
    bloques = [df.iloc[i * k:(i + 1) * k].reset_index(drop=True) for i in range(3)]
    enc = "| ID | t/ha | ID | t/ha | ID | t/ha |\n|---|---:|---|---:|---|---:|\n"
    filas = []
    for i in range(k):
        celdas = []
        for b in bloques:
            if i < len(b):
                celdas += [b.loc[i, "ID_POLIGONO"], f"{b.loc[i, 'RENDIMIENTO_T_HA']:.4f}"]
            else:
                celdas += ["", ""]
        filas.append("| " + " | ".join(celdas) + " |")
    return enc + "\n".join(filas)


def main():
    url_app = sys.argv[1] if len(sys.argv) > 1 else "(pendiente de despliegue)"
    url_video = sys.argv[2] if len(sys.argv) > 2 else "(pendiente)"
    df = pd.read_csv(SUB)
    assert len(df) == 59
    md = (ROOT / "reports" / "anexos.md").read_text(encoding="utf-8")
    md = (md.replace("<!-- TABLA_PREDICCIONES -->", tabla_3_columnas(df))
            .replace("<!-- URL_APP -->", url_app).replace("<!-- URL_VIDEO -->", url_video))
    out = ROOT / "reports" / "anexos_final.md"
    out.write_text(md, encoding="utf-8")
    print(f"Escrito {out.relative_to(ROOT)} ({len(df)} predicciones, media {df.RENDIMIENTO_T_HA.mean():.3f})")


if __name__ == "__main__":
    main()
