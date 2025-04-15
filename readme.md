# Установка проекта

Следуйте этим шагам для установки проекта:

```bash
# Создание рабочей директории
mkdir work_with_pdf
cd work_with_pdf

# Клонирование репозитория
git clone https://github.com/zhdaniukivan/work_with_pdf.git

# Создание и активация виртуального окружения
python3 -m venv venv
source venv/bin/activate  # Для Linux/MacOS
# venv\Scripts\activate  # Для Windows

# Обновление pip и установка зависимостей
pip install --upgrade pip
pip install -r requirements.txt


# Запуск проекта
python main1.py

путь к обрабатываемому PDF-файлу указан в main1.py в переменной:
pdf_path = "temporary/1.pdf"