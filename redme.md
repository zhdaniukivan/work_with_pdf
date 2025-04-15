Следуйте этим шагам для установки проекта
mkdir work_with_pdf
cd work_with_pdf
git init
git remote add origin https://github.com/zhdaniukivan/work_with_pdf.git

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip 
pip install -r requirements.txt (pip freeze > requirements.txt)

структура проекта:



create database:
<!-- 
sudo -iu postgres psql CREATE DATABASE cryptonews;
create user cryptouser with password '100500';

ALTER DATABASE cryptonews OWNER TO cryptouser;

python manage.py makemigrations python manage.py migrate

python manage.py createsuperuser 80292819810 100500

python manage.py runserver -->

ci/cd: