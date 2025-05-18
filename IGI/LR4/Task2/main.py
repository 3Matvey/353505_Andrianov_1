import os
import sys

# чтобы Python нашёл наш пакет
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from text_analyzer import CombinedAnalyzer

def main():
    print("=== Text Analysis (Task 2) ===")
    while True:
        inp = input("Input file (или 'quit'): ")
        if inp.lower() == 'quit':
            break
        out = input("Output results file: ")
        zipf = input("Zip archive name: ")

        if not out.lower().endswith('.txt'):
            out += '.txt'
        if not zipf.lower().endswith('.zip'):
            zipf += '.zip'

        analyzer = CombinedAnalyzer(inp)
        try:
            analyzer.read_file()
            analyzer.process_text()
            analyzer.save_results(out)
            analyzer.zip_results(out, zipf)

            print("\n--- Результаты ---")
            for k, v in analyzer.results.items():
                print(f"{k}: {v}")
            print(f"\nФайл результатов '{out}' и архив '{zipf}' созданы.")
        except Exception as e:
            print("Ошибка:", e)

        if input("\nЕщё один файл? (yes/no): ").lower() != 'yes':
            break

if __name__ == "__main__":
    main()
