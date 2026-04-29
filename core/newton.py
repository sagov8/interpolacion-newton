"""Lógica numérica del método de interpolación de Newton."""

from __future__ import annotations

import numpy as np


def parse_float_list(raw_text: str) -> np.ndarray:
    """
    Convierte un texto tipo '1, 2, 3' en un arreglo numérico.
    """
    values = []

    for item in raw_text.split(","):
        item = item.strip()

        if item:
            values.append(float(item))

    if len(values) == 0:
        raise ValueError("Debes ingresar al menos un valor.")

    return np.array(values, dtype=float)


def validate_interpolation_data(xs: np.ndarray, ys: np.ndarray) -> None:
    """
    Verifica que los datos sean válidos para interpolar.
    """
    if len(xs) != len(ys):
        raise ValueError("La cantidad de xᵢ y f(xᵢ) debe ser igual.")

    if len(xs) < 2:
        raise ValueError("Se necesitan al menos 2 puntos.")

    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            if xs[i] == xs[j]:
                raise ValueError("Los nodos xᵢ deben ser todos distintos.")


def build_dd_table(xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
    """
    Construye la tabla de diferencias divididas de Newton.

    Esta función sigue estos pasos:

    1. La primera columna contiene los valores yᵢ.
    2. Cada nueva columna se calcula usando diferencias divididas.
    3. La primera fila contiene los coeficientes del polinomio de Newton.
    """
    n = len(xs) - 1

    dd_table = []

    for i in range(n + 1):
        row = []

        for j in range(n + 1):
            row.append(np.nan)

        dd_table.append(row)

    for i in range(n + 1):
        dd_table[i][0] = ys[i]

    for j in range(1, n + 1):
        for i in range(0, n - j + 1):
            numerator = dd_table[i + 1][j - 1] - dd_table[i][j - 1]
            denominator = xs[i + j] - xs[i]

            dd_table[i][j] = numerator / denominator

    return np.array(dd_table, dtype=float)


def get_newton_coefficients(dd_table: np.ndarray) -> np.ndarray:
    """
    Extrae los coeficientes a₀, a₁, ..., aₙ.

    En el método de Newton, los coeficientes están en la primera fila
    de la tabla de diferencias divididas.
    """
    n = len(dd_table)
    coeffs = []

    for j in range(n):
        coeffs.append(dd_table[0][j])

    return np.array(coeffs, dtype=float)


def eval_newton_scalar(
    x: float,
    xs: np.ndarray,
    coeffs: np.ndarray,
    num_terms: int,
) -> float:
    """
    Evalúa el polinomio de Newton en un solo valor x.

    P(x) = a₀
         + a₁(x - x₀)
         + a₂(x - x₀)(x - x₁)
         + ...
    """
    result = coeffs[0]
    product = 1.0

    for k in range(1, num_terms):
        product = product * (x - xs[k - 1])
        result = result + coeffs[k] * product

    return float(result)


def eval_newton(
    x: float | np.ndarray,
    xs: np.ndarray,
    coeffs: np.ndarray,
    num_terms: int,
) -> float | np.ndarray:
    """
    Evalúa el polinomio de Newton.

    Si x es un número, devuelve un número.
    Si x es un arreglo, evalúa el polinomio punto por punto.
    """
    if np.isscalar(x):
        return eval_newton_scalar(float(x), xs, coeffs, num_terms)

    results = []

    for value in x:
        y = eval_newton_scalar(float(value), xs, coeffs, num_terms)
        results.append(y)

    return np.array(results, dtype=float)


def format_number(value: float, digits: int = 4) -> str:
    """
    Formatea números para mostrarlos en la expresión del polinomio.
    """
    if abs(value) < 1e-12:
        value = 0.0

    return f"{value:.{digits}g}"


def get_poly_label(coeffs: np.ndarray, xs: np.ndarray, num_terms: int) -> str:
    """
    Construye la expresión textual del polinomio de Newton.
    """
    terms = []

    for k in range(num_terms):
        coefficient = coeffs[k]

        if np.isnan(coefficient) or abs(coefficient) < 1e-12:
            continue

        coefficient_text = format_number(coefficient)

        if k == 0:
            terms.append(coefficient_text)
        else:
            factors = []

            for j in range(k):
                factors.append(f"(x − {format_number(xs[j])})")

            factor_text = " · ".join(factors)
            terms.append(f"{coefficient_text} · {factor_text}")

    if len(terms) == 0:
        return "P(x) = 0"

    return "P(x) = " + "  +  ".join(terms)


def build_iteration_rows(xs: np.ndarray, dd_table: np.ndarray) -> list[dict[str, object]]:
    """
    Genera las filas explicativas para mostrar el cálculo manual
    de cada diferencia dividida.
    """
    n = len(xs) - 1
    rows = []

    for j in range(1, n + 1):
        for i in range(0, n - j + 1):
            numerator = dd_table[i + 1][j - 1] - dd_table[i][j - 1]
            denominator = xs[i + j] - xs[i]
            result = dd_table[i][j]

            rows.append(
                {
                    "Diferencia": f"f[x{i}, …, x{i + j}]",
                    "Numerador": (
                        f"{dd_table[i + 1][j - 1]:.6g} − "
                        f"{dd_table[i][j - 1]:.6g} = {numerator:.6g}"
                    ),
                    "Denominador": (
                        f"x{i + j} − x{i} = "
                        f"{xs[i + j]:.6g} − {xs[i]:.6g} = {denominator:.6g}"
                    ),
                    "Resultado": round(float(result), 8),
                }
            )

    return rows

def build_error_rows(
    xs: np.ndarray,
    ys: np.ndarray,
    coeffs: np.ndarray,
) -> list[dict[str, object]]:
    """
    Calcula el error iterativo de Newton en cada paso.

    Para cada punto x_k, calcula cuánto se equivoca el polinomio anterior
    P_{k-1}(x) antes de agregar el nuevo término.

    e_k = y_k - P_{k-1}(x_k)
    """
    rows = []
    n = len(xs) - 1

    for k in range(1, n + 1):
        x_k = xs[k]
        y_k = ys[k]

        prediction = eval_newton_scalar(
            x=float(x_k),
            xs=xs,
            coeffs=coeffs,
            num_terms=k,
        )

        error = y_k - prediction
        abs_error = abs(error)

        product = 1.0

        for j in range(k):
            product = product * (x_k - xs[j])

        calculated_coefficient = error / product

        rows.append(
            {
                "Iteración": k,
                "Punto agregado": f"({x_k:.6g}, {y_k:.6g})",
                "P anterior": f"P{k - 1}(x{k})",
                "Predicción": prediction,
                "Valor real": y_k,
                "Error": error,
                "|Error|": abs_error,
                "Producto": product,
                "aₖ = Error / Producto": calculated_coefficient,
                "aₖ tabla": coeffs[k],
            }
        )

    return rows