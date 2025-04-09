"""
Module: series_functions
Purpose: Contains functions for computing function values using power series expansion.
This module includes a function for computing sin(x) using its power series expansion.
"""

import math

def calculate_sin_series(x: float, eps: float, max_iter: int = 500) -> tuple:
    """
    Calculate sin(x) using its power series expansion.

    sin(x) = x - x^3/3! + x^5/5! - ... 

    Parameters:
        x (float): The input value (in radians) for which sin(x) is computed.
        eps (float): The desired precision for the calculation. The series stops when the next term's magnitude is below eps.
        max_iter (int): Maximum number of iterations (terms) allowed. Default is 500.
    
    Returns:
        tuple: A tuple containing:
            - approximation (float): The computed sin(x) value from the series.
            - terms_used (int): The number of terms used in the series.
    
    Raises:
        ValueError: If eps is not positive.
        RuntimeError: If the desired precision is not reached within max_iter iterations.
    """
    if eps <= 0:
        raise ValueError("Precision epsilon must be positive.")
    
    term = x          # first term of the series for sin(x)
    sum_val = 0.0     # accumulator for the series sum
    terms_used = 0    # counter for the number of terms added

    while terms_used < max_iter:
        sum_val += term
        terms_used += 1
        
        # Compute the next term using the recurrence relation:
        # term_next = -term * x^2 / ((2*terms_used)*(2*terms_used+1))
        next_term = -term * x * x / ((2 * terms_used) * (2 * terms_used + 1))
        
        if abs(next_term) < eps:
            break
        
        term = next_term

    # If we reached the maximum number of iterations without meeting precision:
    if terms_used == max_iter and abs(next_term) >= eps:
        raise RuntimeError("Desired precision not reached within maximum iterations.")
    
    return sum_val, terms_used
