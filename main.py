import os
import tempfile
from typing import List, Tuple, Optional
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import PyPDF2


class PDFProcessor:
    def __init__(self):
        self.text_pages: List[int] = []
        self.scanned_pages: List[int] = []

    def analyze_pdf(self, pdf_path: str) -> Tuple[List[int], List[int]]:
        """Определяет текстовые и сканированные страницы PDF"""
        self.text_pages.clear()
        self.scanned_pages.clear()

        with open(pdf_path, 'rb') as file:
            pdf = PyPDF2.PdfReader(file)

            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text and len(text.strip()) > 100:
                    self.text_pages.append(i + 1)
                else:
                    self.scanned_pages.append(i + 1)

        return self.text_pages, self.scanned_pages

    def extract_page_as_image(self, pdf_path: str, page_num: int) -> Optional[Image.Image]:
        """Конвертирует страницу PDF в изображение"""
        try:
            images = convert_from_path(pdf_path, first_page=page_num, last_page=page_num)
            return images[0] if images else None
        except Exception as e:
            print(f"Ошибка конвертации страницы {page_num} в изображение: {e}")
            return None

    def process_image_with_ocr(self, image: Image.Image) -> str:
        """Распознаёт текст с изображения"""
        return pytesseract.image_to_string(image, lang="rus+eng")

    def process_pdf(self, input_pdf: str, text_output: str, ocr_output: str) -> None:
        text_pages, scanned_pages = self.analyze_pdf(input_pdf)
        print(f"Найдено {len(text_pages)} текстовых и {len(scanned_pages)} сканированных страниц")

        text_writer = PyPDF2.PdfWriter()
        with open(input_pdf, 'rb') as file:
            pdf = PyPDF2.PdfReader(file)
            for page_num in text_pages:
                text_writer.add_page(pdf.pages[page_num - 1])

        with open(text_output, 'wb') as f:
            text_writer.write(f)

        ocr_texts = []
        for page_num in scanned_pages:
            print(f"OCR страница {page_num}...")
            image = self.extract_page_as_image(input_pdf, page_num)
            if image:
                text = self.process_image_with_ocr(image)
                ocr_texts.append((page_num, text))

        with open(ocr_output, 'w', encoding='utf-8') as f:
            for page_num, text in ocr_texts:
                f.write(f"## Страница {page_num}\n\n{text}\n\n")

        print(f"Текстовые страницы сохранены в: {text_output}")
        print(f"OCR результаты сохранены в: {ocr_output}")


def main():
    input_pdf = "temporary/1.pdf"
    text_output = "text_pages.pdf"
    ocr_output = "ocr_results.md"

    processor = PDFProcessor()
    processor.process_pdf(input_pdf, text_output, ocr_output)


if __name__ == "__main__":
    main()
