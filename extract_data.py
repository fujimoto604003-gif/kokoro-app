import pandas as pd
from docx import Document
import sys
import os

def read_excel(f):
    f.write("--- EXCEL CONTENT ---\n")
    try:
        file_path = "(質問文）２５問.xlsx"
        f.write(f"Reading {file_path}\n")
        df = pd.read_excel(file_path)
        f.write(df.to_string())
        f.write("\n")
    except Exception as e:
        f.write(f"Error reading excel: {e}\n")

def read_docx(f):
    f.write("\n--- DOCX CONTENT ---\n")
    try:
        file_path = "(資料）VARYオリジナル質問の学術的根拠付与.docx"
        f.write(f"Reading {file_path}\n")
        doc = Document(file_path)
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                f.write(text + "\n")
    except Exception as e:
        f.write(f"Error reading docx: {e}\n")

if __name__ == "__main__":
    with open("extraction_output.txt", "w", encoding="utf-8") as f:
        read_excel(f)
        read_docx(f)
