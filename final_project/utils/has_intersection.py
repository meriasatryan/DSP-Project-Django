def has_intersection(arr1, arr2):
    """
    Checks if two arrays have any common elements.

    Args:
    - arr1 (list): First array to compare.
    - arr2 (list): Second array to compare.

    Returns:
    - bool: True if the arrays have at least one common element, False otherwise.
    """
    set1 = set(arr1)
    set2 = set(arr2)
    return bool(set1 & set2)
