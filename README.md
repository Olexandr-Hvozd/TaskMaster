Task Master – це веб-застосунок для керування особистими завданнями, створений на Django. 
Додаток дозволяє користувачам реєструватися, створювати, редагувати, виконувати та видаляти завдання, 
а також відстежувати статистику продуктивності.

🚀 Функціонал
✅ Реєстрація та авторизація користувачів
✅ Додавання, редагування, виконання та видалення завдань
✅ Позначення завдання як виконаного
✅ Перегляд всіх наявних завдань
✅ Відстеження статистики виконаних завдань
✅ Зміна пароля та даних профілю
✅ Відновлення пароля через email

🛠️ Технології
Python 3.11.9
Django 5.1.4
SQLite
CSS
HTML

🔧 Встановлення

Клонуйте репозиторій:
git clone https://github.com/твій-юзернейм/task-master.git

cd taskmaster

Створіть віртуальне середовище та активуй його:
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows

Встанови залежності:
pip install -r requirements.txt

Виконайте міграції:
python manage.py migrate

Запустіть сервер:
python manage.py runserver

Відкрийте у браузері:
http://127.0.0.1:8000/
