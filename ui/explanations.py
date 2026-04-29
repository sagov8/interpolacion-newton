"""Textos didácticos e iteración manual."""

from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

from core.newton import build_iteration_rows, eval_newton


def render_step_explanation(
    xs: np.ndarray,
    ys: np.ndarray,
    coeffs: np.ndarray,
    num_terms: int,
) -> None:
    """
    Explica qué aporta el término activo del polinomio.
    """
    st.subheader("¿Qué ocurre en este paso?")

    k = num_terms - 1

    if num_terms == 1:
        message = (
            f"**Polinomio constante** P₀(x) = {coeffs[0]:.6g}.\n\n"
            f"Solo captura la altura en el primer nodo x₀ = {xs[0]:.6g}. "
            f"Geométricamente es una recta horizontal."
        )

    elif not np.isnan(coeffs[k]) and abs(coeffs[k]) < 1e-10:
        message = (
            f"**a{k} ≈ 0** — el término de grado {k} no aporta nada.\n\n"
            f"Confirma que el polinomio tiene grado efectivo ≤ {k - 1}."
        )

    else:
        y_pred = eval_newton(xs[k], xs, coeffs, num_terms - 1)
        gap = ys[k] - y_pred

        new_factor_value = float(np.prod([xs[k] - xs[j] for j in range(k)]))
        correction = coeffs[k] * new_factor_value

        previous_nodes = ", ".join([f"x{j}={xs[j]:.6g}" for j in range(k)])

        message = (
            f"**Nuevo coeficiente:** a{k} = {coeffs[k]:.6g}\n\n"
            f"Predicción anterior en x{k} = {xs[k]:.6g}: **{y_pred:.6g}**  \n"
            f"Valor real f(x{k}) = **{ys[k]:.6g}** → brecha = **{gap:.6g}**\n\n"
            f"El nuevo factor se anula en los nodos anteriores ({previous_nodes}). "
            f"Por eso el nuevo término corrige el punto actual sin mover los anteriores.\n\n"
            f"Aporte del nuevo término en x{k}: **{correction:.6g}**."
        )

    st.info(message)


def render_algorithm_explanation() -> None:
    """
    Explica el algoritmo iterativo de Newton.
    """
    with st.expander("Explicación del algoritmo iterativo"):
        st.markdown(
            """
El método de interpolación de Newton construye el polinomio de forma incremental.

Primero se parte de un polinomio constante:
            """
        )

        st.code(
            "P₀(x) = a₀",
            language="text",
        )

        st.markdown("Luego se agregan términos uno por uno:")

        st.code(
            """
P₁(x) = a₀ + a₁(x - x₀)

P₂(x) = a₀ + a₁(x - x₀) + a₂(x - x₀)(x - x₁)

P₃(x) = a₀ + a₁(x - x₀) + a₂(x - x₀)(x - x₁)
        + a₃(x - x₀)(x - x₁)(x - x₂)
            """.strip(),
            language="text",
        )

        st.markdown("En general:")

        st.code(
            """
Pₖ(x) = a₀ + a₁(x - x₀) + a₂(x - x₀)(x - x₁)
        + ... + aₖ(x - x₀)(x - x₁)...(x - xₖ₋₁)
            """.strip(),
            language="text",
        )

        st.markdown(
            """
La idea principal es que el nuevo término:
            """
        )

        st.code(
            "aₖ(x - x₀)(x - x₁)...(x - xₖ₋₁)",
            language="text",
        )

        st.markdown(
            """
vale cero en todos los nodos anteriores:
            """
        )

        st.code(
            "x₀, x₁, ..., xₖ₋₁",
            language="text",
        )

        st.markdown(
            """
Por eso, cuando agregamos el término `k`, el polinomio puede ajustarse al nuevo punto `xₖ`
sin modificar los puntos que ya interpolaba correctamente.

---

### Tabla de diferencias divididas

La primera columna de la tabla contiene los valores originales:
            """
        )

        st.code(
            "T[i, 0] = f(xᵢ)",
            language="text",
        )

        st.markdown("Luego cada columna se calcula con:")

        st.code(
            "T[i, j] = (T[i + 1, j - 1] - T[i, j - 1]) / (x[i + j] - x[i])",
            language="text",
        )

        st.markdown("Los coeficientes del polinomio de Newton son la primera fila:")

        st.code(
            """
a₀ = T[0, 0]
a₁ = T[0, 1]
a₂ = T[0, 2]
...
aₖ = T[0, k]
            """.strip(),
            language="text",
        )

        st.markdown("Por eso en el código se hace:")

        st.code(
            "coeffs = dd_table[0, :]",
            language="python",
        )

        st.markdown(
            """
---

### Evaluación iterativa

Para evaluar el polinomio no hace falta expandirlo. Se usa un producto acumulado:
            """
        )

        st.code(
            """
result = 0.0
product = 1.0

for k in range(num_terms):
    result += coeffs[k] * product
    product *= x - xs[k]
            """.strip(),
            language="python",
        )

        st.markdown("Esto va construyendo sucesivamente:")

        st.code(
            """
1
(x - x₀)
(x - x₀)(x - x₁)
(x - x₀)(x - x₁)(x - x₂)
...
            """.strip(),
            language="text",
        )

        st.markdown(
            """
Así el polinomio se evalúa en orden, término por término.
            """
        )


def render_manual_iteration(
    xs: np.ndarray,
    dd_table: np.ndarray,
) -> None:
    """
    Muestra una tabla con el cálculo manual de cada diferencia dividida.
    """
    with st.expander("Ver iteración manual detallada"):
        st.markdown("### Cálculo de cada diferencia dividida")

        rows = build_iteration_rows(xs, dd_table)

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )