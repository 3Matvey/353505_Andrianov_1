"""
Task 2: Text Analysis System
This module provides the main interface for text analysis operations.
"""
from common.user_input import get_user_choice
from .models import TextAnalyzer
from .utils import FileHandler, ArchiveHandler, format_statistics, format_analysis_results

def display_menu():
    """Display the main menu for task 2."""
    print("\n=== Text Analysis System ===")
    print("1. Analyze text from file")
    print("2. Show analysis results")
    print("3. Save results to file")
    print("4. Create archive with results")
    print("5. Show archive information")
    print("0. Return to main menu")
    print("===========================")


def analyze_text():
    """Analyze text from a file."""
    filename = input("Enter input filename: ").strip()
    if not filename:
        print("Filename cannot be empty.")
        return None
    
    text = FileHandler.read_file(filename)
    if text is None:
        print(f"Could not read file: {filename}")
        return None
    
    if not text.strip():
        print("File is empty.")
        return None
    
    print("File read successfully.")
    return TextAnalyzer(text)

def save_results(analyzer: TextAnalyzer):
    """Save analysis results to a file."""
    if analyzer is None:
        print("No analysis results to save.")
        return
    
    filename = input("Enter output filename: ").strip()
    if not filename:
        print("Filename cannot be empty.")
        return
    
    # Get statistics and analysis results
    stats = analyzer.get_statistics()
    stats_text = format_statistics(stats)
    analysis_text = format_analysis_results(analyzer)
    
    # Combine all results
    content = f"{stats_text}\n\n{analysis_text}"
    
    if FileHandler.write_file(filename, content):
        print(f"Results saved to {filename}")
        return filename
    return None

def create_archive(source_file: str):
    """Create an archive with the results file."""
    if not source_file:
        print("No results file to archive.")
        return
    
    archive_name = input("Enter archive name (without extension): ").strip()
    if not archive_name:
        print("Archive name cannot be empty.")
        return
    
    archive_name = f"{archive_name}.zip"
    if ArchiveHandler.create_archive(source_file, archive_name):
        print(f"Archive created: {archive_name}")
        return archive_name
    return None

def show_archive_info(archive_name: str):
    """Display information about the archive."""
    if not archive_name:
        print("No archive to show information about.")
        return
    
    info = ArchiveHandler.get_archive_info(archive_name)
    if info is None:
        return
    
    print(f"\nArchive information for {archive_name}:")
    for filename, details in info.items():
        print(f"\nFile: {filename}")
        print(f"Size: {details['size']} bytes")
        print(f"Compressed size: {details['compressed_size']} bytes")
        print(f"Date: {details['date_time']}")

def main():
    """Main function for task 2."""
    analyzer = None
    results_file = None
    archive_file = None
    
    while True:
        display_menu()
        choice = get_user_choice(5)
        
        if choice == 0:
            break
        elif choice == 1:
            analyzer = analyze_text()
        elif choice == 2:
            if analyzer is None:
                print("Please analyze text first.")
                continue
            stats = analyzer.get_statistics()
            print(format_statistics(stats))
            print("\n" + format_analysis_results(analyzer))
        elif choice == 3:
            results_file = save_results(analyzer)
        elif choice == 4:
            archive_file = create_archive(results_file)
        elif choice == 5:
            show_archive_info(archive_file)

if __name__ == "__main__":
    main() 