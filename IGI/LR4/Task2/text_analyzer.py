import re
import zipfile
import os
from datetime import datetime

class BaseAnalyzer:
    """Базовый класс для чтения текста, сохранения результатов и архивации."""
    version = '1.0'

    def __init__(self, file_path: str):
        self._file_path = file_path
        self.text = ""
        self.results = {}

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        if not isinstance(value, str):
            raise ValueError("Путь к файлу должен быть строкой.")
        self._file_path = value

    def read_file(self):
        try:
            with open(self._file_path, 'r', encoding='utf-8') as f:
                self.text = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self._file_path} не найден.")
        except Exception as e:
            raise Exception(f"Ошибка чтения файла: {e}")

    def save_results(self, output_path: str):
        """Записывает все ключи/значения из self.results и, если есть, modified_text."""
        with open(output_path, 'w', encoding='utf-8') as f:
            for key, value in self.results.items():
                f.write(f"{key}: {value}\n")
            # Если была сделана замена – положим и сам текст
            if hasattr(self, 'modified_text'):
                f.write("\n--- Modified Text ---\n")
                f.write(self.modified_text)

    def zip_results(self, output_path: str, zip_path: str):
        """Запаковывает output_path в zip и добавляет в results информацию об архиве."""
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(output_path, arcname=os.path.basename(output_path))
        info = zipf.getinfo(os.path.basename(output_path))
        self.results['Zip File Info'] = {
            'file_name': info.filename,
            'file_size': info.file_size,
            'compressed_size': info.compress_size,
            'modified': datetime(*info.date_time).strftime('%Y-%m-%d %H:%M:%S')
        }


class GeneralAnalyzerMixin:
    """Общие задачи (кол-во предложений, средняя длина и т.п.)."""

    def count_sentences(self):
        lst = re.findall(r'[^.!?]*[.!?]', self.text, flags=re.MULTILINE)
        self.results['Total sentences'] = len(lst)

    def count_sentence_types(self):
        endings = re.findall(r'([.!?])', self.text)
        self.results['Declarative sentences']   = endings.count('.')
        self.results['Interrogative sentences'] = endings.count('?')
        self.results['Exclamatory sentences']   = endings.count('!')

    def average_sentence_length(self):
        sents = [s.strip() for s in re.split(r'[.!?]', self.text) if s.strip()]
        total_chars = sum(len(w) for sent in sents for w in re.findall(r'\w+', sent))
        avg = total_chars / len(sents) if sents else 0
        self.results['Average sentence length'] = round(avg, 2)

    def average_word_length(self):
        words = re.findall(r'\w+', self.text)
        avg = sum(len(w) for w in words) / len(words) if words else 0
        self.results['Average word length'] = round(avg, 2)

    def count_smileys(self):
        # : or ;  then zero-or-more -  then one-or-more of same bracket () or []
        patt = r'[:;]-*([\(\)\[\]])\1*'
        self.results['Smiley count'] = len(re.findall(patt, self.text))

    def process_general_tasks(self):
        self.count_sentences()
        self.count_sentence_types()
        self.average_sentence_length()
        self.average_word_length()
        self.count_smileys()


class SpecificAnalyzerMixin:
    """Задачи варианта 1:
     1) заглавные буквы, 2) замена a+ b{2,} c+ → qqq,
     3) сколько слов макс. длины,
     4) слова перед ',' или '.',
     5) самое длинное слово на 'e'.
    """

    def extract_uppercase_letters(self):
        letters = re.findall(r'[A-Z]', self.text)
        self.results['Uppercase letters'] = ''.join(letters)

    def replace_abc_pattern(self):
        patt = re.compile(r'a+b{2,}c+')
        # делаем замену
        self.modified_text = patt.sub('qqq', self.text)
        # считаем, сколько было замен
        count = len(patt.findall(self.text))
        self.results['Replacements count'] = count

    def count_max_length_words(self):
        words = re.findall(r'\b\w+\b', self.text)
        if not words:
            self.results['Max length words count'] = 0
            return
        max_len = max(len(w) for w in words)
        max_words = [w for w in words if len(w) == max_len]
        self.results['Max length words count'] = len(max_words)
        self.results['Max length words'] = max_words

    def extract_words_with_punct(self):
        lst = re.findall(r'\b\w+(?=[\.,])', self.text)
        self.results['Words before comma/dot'] = lst

    def find_longest_e_word(self):
        words = re.findall(r'\b\w+e\b', self.text, flags=re.IGNORECASE)
        if words:
            max_len = max(len(w) for w in words)
            longest = [w for w in words if len(w) == max_len]
            self.results['Longest e-ending word'] = longest
        else:
            self.results['Longest e-ending word'] = None

    def process_specific_tasks(self):
        self.extract_uppercase_letters()
        self.replace_abc_pattern()
        self.count_max_length_words()
        self.extract_words_with_punct()
        self.find_longest_e_word()


class CombinedAnalyzer(BaseAnalyzer, GeneralAnalyzerMixin, SpecificAnalyzerMixin):
    """Объединяем всё вместе."""
    def process_text(self):
        self.process_general_tasks()
        self.process_specific_tasks()
