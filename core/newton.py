"""Lógica numérica del metodo de interpolación de Newton."""
from __future__ import annotations

import numpy as np


def parse_float_list(raw_text: str) -> np.ndarray:
    """
    Convierte un texto tipo '1, 2, 3' en un arreglo de floats.
    """
    values = [value.strip() for value in raw_text.split(",") if value.strip()]

    if not values:
        raise ValueError("Debes ingresar al menos un valor.")

    return np.array([float(value) for value in values], dtype=float)


def validate_interpolation_data(xs: np.ndarray, ys: np.ndarray) -> None:
    """
    Valida que los datos permitan construir un polinomio interpolante.
    """
    if len(xs) != len(ys):
        raise ValueError("La cantidad de xᵢ y f(xᵢ) debe ser igual.")

    if len(xs) < 2:
        raise ValueError("Se necesitan al menos 2 puntos.")

    if len(np.unique(xs)) != len(xs):
        raise ValueError("Los nodos xᵢ deben ser todos distintos.")


def build_dd_table(xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
    """
    Construye la tabla triangular de diferencias divididas.

    table[i, 0] = f[x_i]
    table[i, j] = f[x_i, ..., x_{i+j}]
    """
    n_points = len(xs)

    table = np.full((n_points, n_points), np.nan, dtype=float)
    table[:, 0] = ys

    for order in range(1, n_points):
        for row in range(n_points - order):
            numerator = table[row + 1, order - 1] - table[row, order - 1]
            denominator = xs[row + order] - xs[row]
            table[row, order] = numerator / denominator

    return table


def get_newton_coefficients(dd_table: np.ndarray) -> np.ndarray:
    """
    Los coeficientes a_k del polinomio de Newton están en la primera fila.
    """
    return dd_table[0, :]


def eval_newton(
    x: float | np.ndarray,
    xs: np.ndarray,
    coeffs: np.ndarray,
    num_terms: int,
) -> float | np.ndarray:
    """
    Evalúa el polinomio de Newton usando producto acumulado.

    P_k(x) = a_0
           + a_1(x - x_0)
           + a_2(x - x_0)(x - x_1)
           + ...
           + a_k(x - x_0)(x - x_1)...(x - x_{k-1})
    """
    x_arr = np.asarray(x, dtype=float)

    result = np.zeros_like(x_arr, dtype=float)
    product = np.ones_like(x_arr, dtype=float)

    for k in range(num_terms):
        result = result + coeffs[k] * product
        product = product * (x_arr - xs[k])

    if np.isscalar(x):
        return float(result)

    return result


def format_number(value: float, digits: int = 4) -> str:
    """
    Formatea números para mostrarlos en expresiones legibles.
    """
    if abs(value) < 1e-12:
        value = 0.0

    return f"{value:.{digits}g}"


def get_poly_label(coeffs: np.ndarray, xs: np.ndarray, num_terms: int) -> str:
    """
    Construye una etiqueta textual del polinomio de Newton activo.
    """
    terms: list[str] = []

    for k in range(num_terms):
        coefficient = coeffs[k]

        if np.isnan(coefficient) or abs(coefficient) < 1e-12:
            continue

        factors = [f"(x − {format_number(xs[j])})" for j in range(k)]
        factor_text = " · ".join(factors)
        coefficient_text = format_number(coefficient)

        if factor_text:
            terms.append(f"{coefficient_text} · {factor_text}")
        else:
            terms.append(coefficient_text)

    return "P(x) = " + "  +  ".join(terms) if terms else "P(x) = 0"


def build_iteration_rows(xs: np.ndarray, dd_table: np.ndarray) -> list[dict[str, object]]:
    """
    Genera las filas explicativas para mostrar el cálculo manual.
    """
    n_points = len(xs)
    rows: list[dict[str, object]] = []

    for order in range(1, n_points):
        for row in range(n_points - order):
            numerator = dd_table[row + 1, order - 1] - dd_table[row, order - 1]
            denominator = xs[row + order] - xs[row]

            rows.append(
                {
                    "Diferencia": f"f[x{row}, …, x{row + order}]",
                    "Numerador": (
                        f"{dd_table[row + 1, order - 1]:.6g} − "
                        f"{dd_table[row, order - 1]:.6g} = {numerator:.6g}"
                    ),
                    "Denominador": (
                        f"x{row + order} − x{row} = "
                        f"{xs[row + order]:.6g} − {xs[row]:.6g} = {denominator:.6g}"
                    ),
                    "Resultado": round(float(dd_table[row, order]), 8),
                }
            )

    return rows