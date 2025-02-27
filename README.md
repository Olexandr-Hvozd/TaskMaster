# Task Master

Task Master is a web application for managing personal tasks, built with Django. 
The application allows users to register, create, edit, complete, and delete tasks, 
as well as track performance statistics.

## 🚀 Features

- ✅ User registration and login
- ✅ Adding, editing, completing, and deleting tasks
- ✅ Viewing all existing tasks
- ✅ Tracking completed task statistics
- ✅ Changing password and profile details
- ✅ Password recovery via email

## 🛠️ Technologies

- Python 3.11.9
- Django 5.1.4
- SQLite
- CSS
- HTML

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Olexandr-Hvozd/TaskMaster.git


2. **Navigate to the project directory:**:
    ```cmd
    cd taskmaster

3. **Create a virtual environment and activate it: Create a virtual environment:**
    ```cmd
    python -m venv venv

    Activation for Windows:
    venv\Scripts\activate 

    Activation for Mac/Linux:
    source venv/bin/activate

4. **Install dependencies:**
    ```cmd
    pip install -r requirements.txt

5. **Run migrations:**
    ```cmd
    python manage.py migrate

6. **Start the server:**
    ```cmd
    python manage.py runserver

7. **Open the application in your browser:**
    ```cmd
    Go to the following address: http://127.0.0.1:8000/