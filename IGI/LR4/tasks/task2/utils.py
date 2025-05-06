"""
Task 2: File and Archive Utilities
This module contains functions for file and archive operations.
"""

import os
import zipfile
from typing import Optional
from .models import TextStatistics, TextAnalyzer, SentenceType

class FileHandler:
    """Class for handling file operations."""
    
    @staticmethod
    def read_file(filename: str) -> Optional[str]:
        """
        Read text from a file.
        
        Args:
            filename (str): Path to the input file (can be relative or absolute)
            
        Returns:
            Optional[str]: Text content or None if error occurred
        """
        try:
            # Convert to absolute path if it's relative
            abs_path = os.path.abspath(filename)
            with open(abs_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            print(f"Current working directory: {os.getcwd()}")
            return None
    
    @staticmethod
    def write_file(filename: str, content: str) -> bool:
        """
        Write text to a file.
        
        Args:
            filename (str): Path to the output file (can be relative or absolute)
            content (str): Content to write
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Convert to absolute path if it's relative
            abs_path = os.path.abspath(filename)
            with open(abs_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        except Exception as e:
            print(f"Error writing file: {e}")
            print(f"Current working directory: {os.getcwd()}")
            return False

class ArchiveHandler:
    """Class for handling archive operations."""
    
    @staticmethod
    def create_archive(source_file: str, archive_name: str) -> bool:
        """
        Create a ZIP archive containing the source file.
        
        Args:
            source_file (str): Path to the file to archive
            archive_name (str): Name of the archive to create
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(source_file, os.path.basename(source_file))
            return True
        except Exception as e:
            print(f"Error creating archive: {e}")
            return False
    
    @staticmethod
    def get_archive_info(archive_name: str) -> Optional[dict]:
        """
        Get information about files in the archive.
        
        Args:
            archive_name (str): Path to the archive
            
        Returns:
            Optional[dict]: Dictionary with file information or None if error occurred
        """
        try:
            with zipfile.ZipFile(archive_name, 'r') as zipf:
                info = {}
                for file_info in zipf.infolist():
                    info[file_info.filename] = {
                        'size': file_info.file_size,
                        'compressed_size': file_info.compress_size,
                        'date_time': file_info.date_time
                    }
                return info
        except Exception as e:
            print(f"Error reading archive: {e}")
            return None

def format_statistics(stats: TextStatistics) -> str:
    """
    Format statistics into a readable string.
    
    Args:
        stats (TextStatistics): Statistics to format
        
    Returns:
        str: Formatted statistics
    """
    return f"""Text Statistics:
Total sentences: {stats.total_sentences}
Sentence types:
  - Declarative: {stats.sentence_types[SentenceType.DECLARATIVE]}
  - Interrogative: {stats.sentence_types[SentenceType.INTERROGATIVE]}
  - Imperative: {stats.sentence_types[SentenceType.IMPERATIVE]}
Average sentence length: {stats.avg_sentence_length:.2f} words
Average sentence length in characters: {stats.avg_sentence_length_chars:.2f}
Average word length: {stats.avg_word_length:.2f} characters
Smiley count: {stats.smiley_count}"""

def format_analysis_results(analyzer: TextAnalyzer) -> str:
    """
    Format analysis results into a readable string.
    
    Args:
        analyzer (TextAnalyzer): Analyzer with results
        
    Returns:
        str: Formatted results
    """
    # Get capital letters
    capital_letters = analyzer.find_capital_letters()
    
    # Get max length words
    max_length, max_words = analyzer.find_max_length_words()
    
    # Get words before punctuation
    words_before_punctuation = analyzer.find_words_before_punctuation()
    
    # Get longest word ending with 'e'
    longest_word_e = analyzer.find_longest_word_ending_with_e()
    
    # Get text with replaced pattern
    replaced_text = analyzer.replace_pattern()
    
    return f"""Analysis Results:
Capital English letters: {', '.join(capital_letters)}
Words with maximum length ({max_length}): {', '.join(max_words)}
Words followed by punctuation: {', '.join(words_before_punctuation)}
Longest word ending with 'e': {longest_word_e}
Text with replaced pattern:
{replaced_text}""" 