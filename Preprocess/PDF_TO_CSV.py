import pdfplumber
import pandas as pd
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from pdf2image import convert_from_path
from pytesseract import image_to_string

DetectorFactory.seed = 0

def extract_text_from_pdf(pdf_path):
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                text.extend(page_text.splitlines())
    return text

def extract_text_with_ocr(pdf_path):
    pages = convert_from_path(pdf_path)
    text = []
    for page in pages:
        page_text = image_to_string(page)
        text.extend(page_text.splitlines())
    return text

def detect_language_and_separate(lines):
    source_sentences = []
    target_sentences = []
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue
        try:
            lang = detect(stripped_line)
            if lang == "en":
                source_sentences.append(stripped_line)
            elif lang == "yo":
                target_sentences.append(stripped_line)
        except LangDetectException:
            continue
    return source_sentences, target_sentences

def align_sentences(source, target):
    min_len = min(len(source), len(target))
    return source[:min_len], target[:min_len]

def save_to_csv(source, target, output_csv):
    df = pd.DataFrame({'source': source, 'target': target})
    df.to_csv(output_csv, index=False, encoding='utf-8')

def process_pdf_to_dataset(pdf_path, output_csv):
    lines = extract_text_from_pdf(pdf_path)
    if not lines:
        lines = extract_text_with_ocr(pdf_path)
    source, target = detect_language_and_separate(lines)
    source, target = align_sentences(source, target)
    save_to_csv(source, target, output_csv)

# Example usage
pdf_file = "geology1.0.pdf"
output_csv = "geology_dataset2.csv"
process_pdf_to_dataset(pdf_file, output_csv)
