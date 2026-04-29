"""Ejemplos predefinidos para la aplicación."""

from __future__ import annotations

import numpy as np


PRESETS = {
    "f(x) = x³  (puntos 1–5)": {
        "x": "1, 2, 3, 4, 5",
        "y": "1, 8, 27, 64, 125",
        "ref": lambda x: x**3,
        "ref_label": "f(x) = x³",
    },
    "f(x) = sin(x)": {
        "x": "0.0, 0.5, 1.0, 1.5, 2.0",
        "y": ", ".join(f"{np.sin(v):.6f}" for v in [0.0, 0.5, 1.0, 1.5, 2.0]),
        "ref": np.sin,
        "ref_label": "f(x) = sin(x)",
    },
    "f(x) = 1/x": {
        "x": "1, 2, 3, 4, 5",
        "y": "1.0, 0.5, 0.33333, 0.25, 0.2",
        "ref": lambda x: np.where(np.abs(x) > 0.05, 1.0 / x, np.nan),
        "ref_label": "f(x) = 1/x",
    },
    "Personalizado": {
        "x": "0, 1, 2, 3",
        "y": "1, 3, 2, 5",
        "ref": None,
        "ref_label": "",
    },
}