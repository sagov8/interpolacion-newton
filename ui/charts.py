"""Gráficas principales de la aplicación."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core.newton import eval_newton, get_poly_label


def render_polynomial_chart(
    xs: np.ndarray,
    ys: np.ndarray,
    coeffs: np.ndarray,
    num_terms: int,
    x_eval: float,
    y_eval: float,
    preset: dict,
    show_ref: bool,
    show_prev: bool,
) -> None:
    """
    Renderiza la curva del polinomio y los puntos interpolados.
    """
    st.subheader("Construcción geométrica del polinomio")

    x_span = float(xs.max() - xs.min())
    margin = x_span * 0.25 if x_span > 0 else 1.0

    x_plot = np.linspace(xs.min() - margin, xs.max() + margin, 600)
    y_poly = eval_newton(x_plot, xs, coeffs, num_terms)

    fig = go.Figure()

    if show_ref and preset["ref"] is not None:
        y_ref = preset["ref"](x_plot)

        fig.add_trace(
            go.Scatter(
                x=x_plot,
                y=y_ref,
                mode="lines",
                name=preset["ref_label"],
                line=dict(
                    color="rgba(150,150,180,0.5)",
                    width=1.5,
                    dash="dash",
                ),
            )
        )

    if show_prev and num_terms > 1:
        for k in range(1, num_terms):
            y_k = eval_newton(x_plot, xs, coeffs, k)

            fig.add_trace(
                go.Scatter(
                    x=x_plot,
                    y=y_k,
                    mode="lines",
                    line=dict(
                        color="rgba(127,119,221,0.18)",
                        width=1,
                    ),
                    showlegend=False,
                )
            )

    fig.add_trace(
        go.Scatter(
            x=x_plot,
            y=y_poly,
            mode="lines",
            name=f"P{num_terms - 1}(x)  [{num_terms} término{'s' if num_terms > 1 else ''}]",
            line=dict(
                color="#7F77DD",
                width=3,
            ),
        )
    )

    done_idx = list(range(num_terms - 1))

    if done_idx:
        fig.add_trace(
            go.Scatter(
                x=xs[done_idx],
                y=ys[done_idx],
                mode="markers",
                name="Interpolados",
                marker=dict(
                    color="#1D9E75",
                    size=12,
                    line=dict(
                        color="white",
                        width=1.5,
                    ),
                ),
            )
        )

    new_idx = num_terms - 1

    fig.add_trace(
        go.Scatter(
            x=[xs[new_idx]],
            y=[ys[new_idx]],
            mode="markers",
            name=f"Nuevo: ({xs[new_idx]:.4g}, {ys[new_idx]:.4g})",
            marker=dict(
                color="#EF9F27",
                size=16,
                line=dict(
                    color="#BA7517",
                    width=2,
                ),
            ),
        )
    )

    pending_idx = list(range(num_terms, len(xs)))

    if pending_idx:
        fig.add_trace(
            go.Scatter(
                x=xs[pending_idx],
                y=ys[pending_idx],
                mode="markers",
                name="Pendientes",
                marker=dict(
                    color="rgba(136,135,128,0.4)",
                    size=10,
                    line=dict(
                        color="#888780",
                        width=1.5,
                    ),
                ),
            )
        )

    if num_terms >= 2:
        y_pred_prev = eval_newton(xs[new_idx], xs, coeffs, num_terms - 1)
        gap = abs(ys[new_idx] - y_pred_prev)

        if gap > 1e-10:
            fig.add_trace(
                go.Scatter(
                    x=[xs[new_idx], xs[new_idx]],
                    y=[y_pred_prev, ys[new_idx]],
                    mode="lines+markers",
                    name=f"Brecha: {gap:.4g}",
                    line=dict(
                        color="#D85A30",
                        width=2,
                        dash="dot",
                    ),
                    marker=dict(
                        color=[
                            "rgba(216,90,48,0.35)",
                            "rgba(0,0,0,0)",
                        ],
                        size=[9, 0],
                    ),
                )
            )

    fig.add_trace(
        go.Scatter(
            x=[x_eval],
            y=[y_eval],
            mode="markers+text",
            name=f"P({x_eval:.3g}) = {y_eval:.5g}",
            marker=dict(
                color="#D85A30",
                size=11,
                symbol="diamond",
            ),
            text=[f"  {y_eval:.4g}"],
            textposition="middle right",
            textfont=dict(
                size=11,
                color="#D85A30",
            ),
        )
    )

    fig.add_vline(
        x=x_eval,
        line_dash="dot",
        line_color="rgba(216,90,48,0.25)",
        line_width=1,
    )

    y_visible = np.concatenate([ys, np.asarray([y_eval], dtype=float)])
    y_min = float(np.nanmin(y_visible))
    y_max = float(np.nanmax(y_visible))
    y_range = max(y_max - y_min, 1.0)

    fig.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=20, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="left",
            x=0,
            font=dict(size=11),
        ),
        xaxis=dict(
            title="x",
            gridcolor="rgba(0,0,0,0.07)",
            zeroline=True,
            zerolinecolor="rgba(0,0,0,0.15)",
        ),
        yaxis=dict(
            title="y",
            gridcolor="rgba(0,0,0,0.07)",
            range=[
                y_min - y_range * 0.3,
                y_max + y_range * 0.4,
            ],
        ),
        plot_bgcolor="white",
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True)

    poly_str = get_poly_label(coeffs, xs, num_terms)

    st.markdown(
        f'<div style="background:#f0f0fa;border-left:4px solid #7F77DD;'
        f'border-radius:0 8px 8px 0;padding:10px 14px;'
        f'font-family:monospace;font-size:13px;line-height:1.8">{poly_str}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("")

    c1, c2, c3 = st.columns(3)

    c1.metric("x evaluado", f"{x_eval:.4g}")
    c2.metric("P(x)", f"{y_eval:.6g}")

    if show_ref and preset["ref"] is not None:
        try:
            y_real = float(preset["ref"](np.array([x_eval]))[0])
            c3.metric("Error |f(x) − P(x)|", f"{abs(y_eval - y_real):.2e}")
        except Exception:
            pass