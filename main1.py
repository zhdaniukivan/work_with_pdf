import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

# Подключаемся к Mistral API
api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-small-latest"
client = Mistral(api_key=api_key)

# 1. Загружаем PDF и получаем OCR-документ
def upload_pdf_for_ocr(path_to_pdf: str) -> str:
    with open(path_to_pdf, "rb") as f:
        uploaded_pdf = client.files.upload(
            file={"file_name": os.path.basename(path_to_pdf), "content": f},
            purpose="ocr"
        )
    signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)
    return signed_url.url

# 2. Составляем сообщение для извлечения данных из сертификатов
def extract_certified_materials(document_url: str) -> str:
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Ты ассистент, который помогает анализировать PDF-документы. "
                        "Пожалуйста, найди ВСЕ СЕРТИФИКАТЫ КАЧЕСТВА в документе. "
                        "Затем из каждого сертификата выдели СЕРТИФИЦИРУЕМЫЕ МАТЕРИАЛЫ. "
                        "Выведи результат в виде нумерованного списка:"
                        "\n\n1. Название сертификата\n   - Материал 1\n   - Материал 2 и т.д."
                    )
                },
                {
                    "type": "document_url",
                    "document_url": document_url
                }
            ]
        }
    ]

    response = client.chat.complete(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content

# 3. Основной код
if __name__ == "__main__":
    pdf_path = "temporary/1.pdf"
    url = upload_pdf_for_ocr(pdf_path)
    result = extract_certified_materials(url)
    print(result)
