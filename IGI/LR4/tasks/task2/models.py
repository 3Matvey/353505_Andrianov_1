"""
Task 2: Text Analysis System
This module contains classes for analyzing text according to the requirements.
"""

import re
from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum, auto

class SentenceType(Enum):
    """Types of sentences in the text."""
    DECLARATIVE = auto()  # Повествовательное
    INTERROGATIVE = auto()  # Вопросительное
    IMPERATIVE = auto()  # Побудительное

@dataclass
class TextStatistics:
    """Class for storing text statistics."""
    total_sentences: int
    sentence_types: dict[SentenceType, int]
    avg_sentence_length: float  # in words
    avg_sentence_length_chars: float  # in characters
    avg_word_length: float
    smiley_count: int

class TextAnalyzer:
    """Class for analyzing text according to the requirements."""
    
    def __init__(self, text: str):
        """
        Initialize the text analyzer.
        
        Args:
            text (str): Text to analyze
        """
        self._text = text
        self._words = self._extract_words()
        self._sentences = self._extract_sentences()
    
    def _extract_words(self) -> List[str]:
        """Extract all words from the text."""
        return re.findall(r'\b\w+\b', self._text)
    
    def _extract_sentences(self) -> List[str]:
        """Extract all sentences from the text."""
        # Split by common sentence endings
        sentences = re.split(r'[.!?]+', self._text)
        return [s.strip() for s in sentences if s.strip()]
    
    def get_statistics(self) -> TextStatistics:
        """Calculate and return text statistics."""
        # Count total sentences
        total_sentences = len(self._sentences)
        
        # Count sentence types
        sentence_types = {
            SentenceType.DECLARATIVE: len(re.findall(r'[^.!?]+\.', self._text)),
            SentenceType.INTERROGATIVE: len(re.findall(r'[^.!?]+\?', self._text)),
            SentenceType.IMPERATIVE: len(re.findall(r'[^.!?]+!', self._text))
        }
        
        # Calculate average sentence length (in words)
        total_words_in_sentences = sum(len(self._extract_words_from_sentence(s)) 
                                     for s in self._sentences)
        avg_sentence_length = (total_words_in_sentences / total_sentences 
                             if total_sentences > 0 else 0)
        
        # Calculate average sentence length in characters
        total_chars_in_sentences = sum(len(re.sub(r'[^\w\s]', '', s)) 
                                     for s in self._sentences)
        avg_sentence_length_chars = (total_chars_in_sentences / total_sentences 
                                   if total_sentences > 0 else 0)
        
        # Calculate average word length
        total_word_length = sum(len(word) for word in self._words)
        avg_word_length = total_word_length / len(self._words) if self._words else 0
        
        # Count smileys according to the specified pattern
        # Pattern: [;:] followed by any number of '-' followed by one or more identical brackets
        smiley_pattern = r'[:;]-*([([\])\]])\1*'
        smiley_count = len(re.findall(smiley_pattern, self._text))
        
        return TextStatistics(
            total_sentences=total_sentences,
            sentence_types=sentence_types,
            avg_sentence_length=avg_sentence_length,
            avg_sentence_length_chars=avg_sentence_length_chars,
            avg_word_length=avg_word_length,
            smiley_count=smiley_count
        )
    
    def _extract_words_from_sentence(self, sentence: str) -> List[str]:
        """Extract words from a single sentence."""
        return re.findall(r'\b\w+\b', sentence)
    
    def find_capital_letters(self) -> List[str]:
        """
        Find all capital letters in the text.
        
        Returns:
            List[str]: List of capital letters
        """
        # Find all capital letters
        return re.findall(r'[A-Z]', self._text)
    
    def replace_pattern(self) -> str:
        """
        Replace pattern 'a' followed by 'b' with 'c'.
        
        Returns:
            str: Text with replaced pattern
        """
        # Replace 'a' followed by 'b' with 'c'
        return re.sub(r'a(?=b)', 'c', self._text)
    
    def find_max_length_words(self) -> Tuple[int, List[str]]:
        """
        Find words with maximum length.
        
        Returns:
            Tuple[int, List[str]]: (max_length, list_of_words)
        """
        if not self._words:
            return 0, []
        
        max_length = max(len(word) for word in self._words)
        max_words = [word for word in self._words if len(word) == max_length]
        return max_length, max_words
    
    def find_words_before_punctuation(self) -> List[str]:
        """
        Find words that are followed by punctuation marks.
        
        Returns:
            List[str]: List of words followed by punctuation
        """
        # Find words followed by punctuation
        pattern = r'\b\w+\b(?=[.,!?])'
        return re.findall(pattern, self._text)
    
    def find_longest_word_ending_with_e(self) -> str:
        """
        Find the longest word that ends with 'e'.
        
        Returns:
            str: The longest word ending with 'e'
        """
        # Find all words ending with 'e'
        words_ending_with_e = re.findall(r'\b\w*e\b', self._text)
        if not words_ending_with_e:
            return ""
        # Return the longest word
        return max(words_ending_with_e, key=len)
    
    def find_words_with_digits(self) -> List[str]:
        """
        Find all words that contain digits.
        
        Returns:
            List[str]: List of words containing digits
        """
        # Find all words containing digits
        return re.findall(r'\b\w*\d\w*\b', self._text)
    
    def find_words_with_repeated_letters(self) -> List[str]:
        """
        Find all words that contain repeated letters.
        
        Returns:
            List[str]: List of words containing repeated letters
        """
        # Find all words containing repeated letters
        return re.findall(r'\b\w*(\w)\1\w*\b', self._text)
    
    def find_words_with_special_characters(self) -> List[str]:
        """
        Find all words that contain special characters.
        
        Returns:
            List[str]: List of words containing special characters
        """
        # Find all words containing special characters
        return re.findall(r'\b\w*[^\w\s]\w*\b', self._text)
    
    def find_words_with_vowels(self) -> List[str]:
        """
        Find all words that contain vowels.
        
        Returns:
            List[str]: List of words containing vowels
        """
        # Find all words containing vowels
        return re.findall(r'\b\w*[aeiouAEIOU]\w*\b', self._text)
    
    def find_words_with_consonants(self) -> List[str]:
        """
        Find all words that contain consonants.
        
        Returns:
            List[str]: List of words containing consonants
        """
        # Find all words containing consonants
        return re.findall(r'\b\w*[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]\w*\b', self._text) 