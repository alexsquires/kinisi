"""
A small module to find the nearest positive definite matrix.
"""

# Copyright (c) Andrew R. McCluskey and Benjamin J. Morgan
# Distributed under the terms of the MIT License
# author: Andrew R. McCluskey (arm61)

import warnings
import numpy as np
from statsmodels.stats import correlation_tools


def find_nearest_positive_definite(matrix: np.ndarray) -> np.ndarray:
    """
    Find the nearest positive-definite matrix to that given, using the method from N.J. Higham, "Computing a nearest
    symmetric positive semidefinite matrix" (1988): 10.1016/0024-3795(88)90223-6

    :param matrix: Matrix to find nearest positive-definite for.
    :return: Nearest positive-definite matrix.
    """

    if check_positive_definite(matrix):
        return matrix

    warnings.warn("The estimated covariance matrix was not positive definite, the nearest positive "
                  "definite matrix has been found and will be used.")

    A3 = correlation_tools.cov_nearest(matrix, method='clipped')

    if check_positive_definite(A3):
        return A3

    spacing = np.spacing(np.linalg.norm(matrix))
    eye = np.eye(matrix.shape[0])
    k = 1
    while not check_positive_definite(A3):
        mineig = np.min(np.real(np.linalg.eigvals(A3)))
        A3 += eye * (-mineig * k**2 + spacing)
        k += 1

    return A3


def check_positive_definite(matrix: np.ndarray) -> bool:
    """
    Checks if a matrix is positive-definite via Cholesky decomposition.

    :param matrix: Matrix to check.
    :return: True for a positive-definite matrix.
    """
    try:
        _ = np.linalg.cholesky(matrix)
        return True
    except np.linalg.LinAlgError:
        return False
