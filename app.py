from __future__ import annotations

import streamlit as st

from core.newton import build_dd_table, eval_newton, get_newton_coefficients
from data.presets import PRESETS
from ui.charts import render_polynomial_chart
from ui.explanations import (
    render_algorithm_explanation,
    render_manual_iteration,
    render_step_explanation,
)
from ui.sidebar import render_sidebar
from ui.tables import (
    render_coefficients_bar_chart,
    render_coefficients_table,
    render_dd_table,
)


st.set_page_config(
    page_title="Interpolación de Newton",
    layout="wide",
)


st.title("📐 Interpolación de Newton — Diferencias Divididas")
st.markdown(
    "Construye el polinomio interpolante paso a paso a partir de puntos definidos por el usuario."
)

config = render_sidebar(PRESETS)

xs = config["xs"]
ys = config["ys"]
num_terms = config["num_terms"]
x_eval = config["x_eval"]

# Cálculo principal
D = build_dd_table(xs, ys)
coeffs = get_newton_coefficients(D)
y_eval = eval_newton(x_eval, xs, coeffs, num_terms)

col_left, col_right = st.columns([3, 2], gap="large")

with col_left:
    render_polynomial_chart(
        xs=xs,
        ys=ys,
        coeffs=coeffs,
        num_terms=num_terms,
        x_eval=x_eval,
        y_eval=y_eval,
        preset=config["preset"],
        show_ref=config["show_ref"],
        show_prev=config["show_prev"],
    )

with col_right:
    render_dd_table(xs=xs, dd_table=D, num_terms=num_terms)
    render_coefficients_table(xs=xs, coeffs=coeffs, num_terms=num_terms)

    if config["show_bars"]:
        render_coefficients_bar_chart(coeffs=coeffs, num_terms=num_terms)

    render_step_explanation(xs=xs, ys=ys, coeffs=coeffs, num_terms=num_terms)

render_algorithm_explanation()
render_manual_iteration(xs=xs, dd_table=D)

st.divider()
st.caption(
    "Implementación: Método de Newton con diferencias divididas. "
    "Tabla triangular y coeficientes aₖ = f[x₀,…,xₖ] calculados en O(n²)."
)