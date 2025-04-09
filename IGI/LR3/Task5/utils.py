def sum_negative_elements(lst: list) -> float:
    """
    Calculate the sum of all negative elements in the list.

    Parameters:
        lst (list): A list of float numbers.

    Returns:
        float: The sum of negative elements.
    """
    return sum(x for x in lst if x < 0)


def product_between_min_max(lst: list) -> float:
    """
    Calculate the product of the elements located between the minimal and
    maximal elements in the list (exclusive).

    If the minimal and maximal elements are adjacent or if the list has fewer than 2 elements,
    the product is considered 1 by default (no elements between).

    Parameters:
        lst (list): A list of float numbers.

    Returns:
        float: The product of the elements between min and max (excluding them).
    """
    if len(lst) < 2:
        # If the list is too small, there's nothing to multiply
        return 1.0

    # Find indices of min and max
    min_val = min(lst)
    max_val = max(lst)

    min_idx = lst.index(min_val)
    max_idx = lst.index(max_val)

    # Determine the slice boundaries (exclusive)
    start = min(min_idx, max_idx) + 1  # one past the smaller index
    end = max(min_idx, max_idx)       # up to the larger index but not including

    # If start >= end, it means min and max are adjacent or out of range => product is 1
    if start >= end:
        return 1.0

    product = 1.0
    for x in lst[start:end]:
        product *= x
    
    return product
