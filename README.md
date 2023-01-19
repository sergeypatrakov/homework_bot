# Бот-ассистент

### Описание:

Telegram-бот, который обращается к API сервиса Практикум.Домашка и узнает статус домашней работы: взята ли домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку. 

### Технологии:

Python 3.7, API, Telegram, Dotenv

### Инструкция по установке:

Клонируй репозиторий и перейди в него в командной строке:

```git clone https://github.com/sergeypatrakov/homework_bot```

```cd homework_bot```

Cоздай и активируй виртуальное окружение:

```python3 -m venv venv```

* Если у тебя Linux/macOS
    ```
    source venv/bin/activate
    ```

* Если у тебя windows
    ```
    source env/scripts/activate
    ```
    ```
    python3 -m pip install --upgrade pip
    ```

Установи зависимости из файла requirements.txt:

```pip install -r requirements.txt```

Выполни миграции:

```python3 manage.py migrate```

Запусти проект:

```python3 manage.py runserver```

Развлекайся)


### Автор:

[Сергей Патраков](https://github.com/sergeypatrakov)

___

# Assistent bot

### Description:

Telegram-bot use API of the service Practicum.Domashka and finds homework status: homework was taken in the review, homework was checked, and if homework was checked, then the reviewer accepted it or returned it for revision.

### Tech:

Python 3.7, API, Telegram, Dotenv

### Installation instructions:

Clone the repository and go to the command line:

```git clone https://github.com/sergeypatrakov/homework_bot```

```cd homework_bot```

Create and activate a virtual environment:

```python 3 -m venv venv```

* If you have Linux/mac OS

    ```
    source venv/bin/activate
    ```

* If you have windows
    ```
    source env/scripts/activate
    ```
    ```
    python3 -m pip install --upgrade pip
    ```

Install the dependencies from the file requirements.txt:

```pip install -r requirements.txt```

Perform migrations:

```python3 manage.py migrate```

Launch the project:

```python3 manage.py runserver```

Enjoy)

### Author:

[Sergey Patrakov](https://github.com/sergeypatrakov)