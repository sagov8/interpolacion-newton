"""Tablas y gráficos auxiliares."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_dd_table(
    xs: np.ndarray,
    dd_table: np.ndarray,
    num_terms: int,
) -> None:
    """
    Muestra la tabla de diferencias divididas.
    """
    st.subheader("Tabla de diferencias divididas")

    n_points = len(xs)
    rows = []

    for i in range(n_points):
        row = {"xᵢ": f"x{i} = {xs[i]:.6g}"}

        for j in range(n_points):
            value = dd_table[i, j]
            row[f"Ord {j}"] = round(float(value), 6) if not np.isnan(value) else ""

        rows.append(row)

    df_table = pd.DataFrame(rows)

    def highlight_dd(_: pd.DataFrame) -> pd.DataFrame:
        styles = pd.DataFrame("", index=df_table.index, columns=df_table.columns)

        for j in range(n_points):
            column = f"Ord {j}"

            if column in df_table.columns:
                if j < num_terms:
                    styles.loc[0, column] = (
                        "background-color: #e8e6fa; color: #534AB7; font-weight: bold"
                    )
                else:
                    styles.loc[0, column] = "color: #cccccc"

        return styles

    st.dataframe(
        df_table.style.apply(highlight_dd, axis=None),
        use_container_width=True,
        height=min(60 + n_points * 38, 280),
    )

    st.caption("🟣 Resaltado = coeficiente aₖ activo en el polinomio actual")


def render_coefficients_table(
    xs: np.ndarray,
    coeffs: np.ndarray,
    num_terms: int,
) -> None:
    """
    Muestra los coeficientes a_k y sus factores asociados.
    """
    st.subheader("Coeficientes aₖ")

    n_points = len(xs)
    rows = []

    for k in range(n_points):
        factor = " · ".join([f"(x−{xs[j]:.6g})" for j in range(k)])

        rows.append(
            {
                "k": k,
                "aₖ": f"{coeffs[k]:.8g}" if not np.isnan(coeffs[k]) else "—",
                "Factor": factor if factor else "1",
                "": "✅" if k < num_terms else "⬜",
            }
        )

    df_coeffs = pd.DataFrame(rows)

    def highlight_coeff(_: pd.DataFrame) -> pd.DataFrame:
        styles = pd.DataFrame("", index=df_coeffs.index, columns=df_coeffs.columns)

        for i in range(len(df_coeffs)):
            styles.iloc[i] = (
                "background-color: #e8faf3; color: #085041"
                if i < num_terms
                else "color: #cccccc"
            )

        return styles

    st.dataframe(
        df_coeffs.style.apply(highlight_coeff, axis=None),
        use_container_width=True,
        hide_index=True,
        height=min(60 + n_points * 38, 250),
    )


def render_coefficients_bar_chart(
    coeffs: np.ndarray,
    num_terms: int,
) -> None:
    """
    Muestra la magnitud absoluta de los coeficientes.
    """
    st.subheader("Magnitud de los coeficientes")

    values = [abs(coeff) if not np.isnan(coeff) else 0 for coeff in coeffs]

    colors = [
        "#7F77DD" if k < num_terms else "rgba(136,135,128,0.3)"
        for k in range(len(coeffs))
    ]

    fig_bar = go.Figure(
        go.Bar(
            x=[f"a{k}" for k in range(len(coeffs))],
            y=values,
            marker_color=colors,
            text=[f"{value:.4g}" for value in values],
            textposition="outside",
        )
    )

    fig_bar.update_layout(
        height=210,
        margin=dict(l=10, r=10, t=10, b=20),
        plot_bgcolor="white",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="rgba(0,0,0,0.07)"),
        showlegend=False,
    )

    st.plotly_chart(fig_bar, use_container_width=True)