def analyze_text(text: str) -> None:
    """
    Analyze the given text and print:
     1) The number of words.
     2) The longest word and its 1-based position in the sequence.
     3) Every even-numbered word (2nd, 4th, etc.).

    The text has words separated by spaces and commas. We do not use any regular expressions.

    Parameters:
        text (str): The input text to analyze.

    Returns:
        None
    """
    # для split
    cleaned_text = text.replace(",", " ").replace(".", " ").replace(";", " ")

    # разбить строку по пробелам
    words = cleaned_text.split()

    if not words:
        print("No words found in the text.")
        return

    num_words = len(words)

    longest_word = max(words, key=len)

    # если несколько слов одинаково длинные, вернётся позиция первого из них
    longest_word_index = words.index(longest_word) + 1

    even_words = []
    for i, w in enumerate(words, start=1):
        if i % 2 == 0:
            even_words.append(w)

    print(f"Text to analyze:\n{text}\n")
    print(f"1) Number of words: {num_words}")
    print(f"2) Longest word: \"{longest_word}\" (position: {longest_word_index})")
    print(f"3) Even-numbered words: {even_words}")
