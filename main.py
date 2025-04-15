import os
import PyPDF2
from typing import List, Tuple

class PDFSplitter:
    def __init__(self, input_pdf_path: str):
        """
        Инициализация PDFSplitter с путем к входному PDF-файлу
        
        :param input_pdf_path: Путь к исходному PDF-файлу
        """
        self.input_pdf_path = input_pdf_path
        self.text_pages = []
        self.scanned_pages = []
        
    def analyze_pdf(self) -> Tuple[List[int], List[int]]:
        """
        Анализирует PDF-файл и определяет, какие страницы содержат текст, а какие являются сканированными
        
        :return: Кортеж (номера текстовых страниц, номера сканированных страниц)
        """
        try:
            with open(self.input_pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    
                    # Если текст извлекается и его достаточно много - считаем текстовой страницей
                    if text and len(text.strip()) > 100:
                        self.text_pages.append(page_num + 1)  # +1 т.к. нумерация с 1
                    else:
                        # Проверяем, есть ли изображения на странице
                        if '/XObject' in page.get('/Resources', {}):
                            x_object = page['/Resources']['/XObject'].get_object()
                            for obj in x_object:
                                if x_object[obj]['/Subtype'] == '/Image':
                                    self.scanned_pages.append(page_num + 1)
                                    break
        except Exception as e:
            print(f"Ошибка при анализе PDF: {e}")
        
        return self.text_pages, self.scanned_pages
    
    def split_pdf(self, text_output_path: str, scanned_output_path: str) -> None:
        """
        Разделяет PDF на два файла: с текстовыми страницами и со сканированными страницами
        
        :param text_output_path: Путь для сохранения PDF с текстовыми страницами
        :param scanned_output_path: Путь для сохранения PDF со сканированными страницами
        """
        try:
            # Сначала анализируем файл, если еще не сделали этого
            if not self.text_pages and not self.scanned_pages:
                self.analyze_pdf()
            
            # Создаем писателей для выходных файлов
            text_writer = PyPDF2.PdfWriter()
            scanned_writer = PyPDF2.PdfWriter()
            
            with open(self.input_pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    if (page_num + 1) in self.text_pages:
                        text_writer.add_page(pdf_reader.pages[page_num])
                    elif (page_num + 1) in self.scanned_pages:
                        scanned_writer.add_page(pdf_reader.pages[page_num])
            
            # Сохраняем результаты
            if text_writer.pages:
                with open(text_output_path, 'wb') as f:
                    text_writer.write(f)
            
            if scanned_writer.pages:
                with open(scanned_output_path, 'wb') as f:
                    scanned_writer.write(f)
                    
        except Exception as e:
            print(f"Ошибка при разделении PDF: {e}")
    
    def get_text_pages(self) -> List[int]:
        """Возвращает номера текстовых страниц"""
        return self.text_pages
    
    def get_scanned_pages(self) -> List[int]:
        """Возвращает номера сканированных страниц"""
        return self.scanned_pages


def main():
    # Пример использования
    input_pdf = "temporary/1.pdf"
    text_output = "text_pages.pdf"  # Исправлено имя файла
    scanned_output = "scanned_pages.pdf"
    
    if not os.path.exists(input_pdf):
        print(f"Файл {input_pdf} не найден!")
        return
    
    splitter = PDFSplitter(input_pdf)
    
    # Анализируем PDF
    text_pages, scanned_pages = splitter.analyze_pdf()
    print(f"Текстовые страницы: {text_pages}")
    print(f"Сканированные страницы: {scanned_pages}")
    
    if not text_pages and not scanned_pages:
        print("Не удалось определить типы страниц. Возможно, файл поврежден или имеет нестандартный формат.")
        return
    
    # Разделяем PDF
    splitter.split_pdf(text_output, scanned_output)
    
    # Проверяем результаты
    if os.path.exists(text_output):
        print(f"Текстовые страницы сохранены в {text_output}")
    else:
        print("Не удалось сохранить текстовые страницы")
    
    if os.path.exists(scanned_output):
        print(f"Сканированные страницы сохранены в {scanned_output}")
    else:
        print("Не удалось сохранить сканированные страницы")


if __name__ == "__main__":
    main()