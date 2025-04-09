def count_uppercase_en_letters(text: str) -> int:
    """
    Count the number of uppercase English letters (A-Z) in the given string.
    Does not use any regular expressions.

    Parameters:
        text (str): The input string in which uppercase letters are to be counted.

    Returns:
        int: The number of uppercase English letters found in the input string.
    """
    count = 0
    for ch in text:
        if 'A' <= ch <= 'Z':
            count += 1
    return count
