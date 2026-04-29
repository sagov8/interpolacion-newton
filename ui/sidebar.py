"""Controles laterales de Streamlit."""

from __future__ import annotations

import numpy as np
import streamlit as st

from core.newton import parse_float_list, validate_interpolation_data


def render_sidebar(presets: dict) -> dict:
    """
    Renderiza el sidebar y devuelve la configuración seleccionada.
    """
    with st.sidebar:
        st.header("⚙️ Configuración")

        preset_name = st.selectbox("Ejemplo predefinido", list(presets.keys()))
        preset = presets[preset_name]

        x_input = st.text_input("Nodos xᵢ (separados por comas)", value=preset["x"])
        y_input = st.text_input("Valores f(xᵢ) (separados por comas)", value=preset["y"])

    try:
        xs = parse_float_list(x_input)
        ys = parse_float_list(y_input)
        validate_interpolation_data(xs, ys)
    except Exception as exc:
        st.error(f"Error en los datos de entrada: {exc}")
        st.stop()

    n_points = len(xs)

    with st.sidebar:
        st.divider()

        num_terms = st.slider(
            "Construir hasta el término:",
            min_value=1,
            max_value=n_points,
            value=n_points,
            step=1,
            help="Arrastra para ver la construcción término a término.",
        )

        st.divider()

        x_eval = st.number_input(
            "Evaluar P(x) en x =",
            value=float(np.mean(xs)),
            step=0.1,
            format="%.4f",
        )

        st.divider()

        show_ref = st.checkbox(
            "Función de referencia",
            value=(preset["ref"] is not None),
        )

        show_prev = st.checkbox(
            "Curvas previas (semitransparente)",
            value=True,
        )

        show_bars = st.checkbox(
            "Magnitud de coeficientes",
            value=False,
        )

    return {
        "preset_name": preset_name,
        "preset": preset,
        "xs": xs,
        "ys": ys,
        "num_terms": num_terms,
        "x_eval": x_eval,
        "show_ref": show_ref,
        "show_prev": show_prev,
        "show_bars": show_bars,
    }