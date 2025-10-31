from pathlib import Path
import csv

base_dir = Path(__name__).resolve().parent

file_path = base_dir / "alx_csv_files_and_python_file" / "user.csv"
def read_csv():
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        data = list(reader)
    return data
