# Проверка свободных талончиков в ГорЗдрав

<table border="0" cellpadding="0" cellspacing="0" align="center">
    <tr>          
        <td rowspan="2">
            <img src="https://github.com/exp-ext/ticket_gorzdrav/blob/main/image/main.jpeg" width="400">
        </td>
        <td>
            <img src="https://github.com/exp-ext/ticket_gorzdrav/blob/main/image/up.jpeg" width="200">
        </td>
    </tr>
     <tr>
        <td>
            <img src="https://github.com/exp-ext/ticket_gorzdrav/blob/main/image/down.jpeg" width="200">
        </td>
    </tr>
</table>

<hr />

# Описание:

Проверяет наличие изменений на странице Медорганизации и вслучае изменений присылает сообщения в Телеграмм.


# Запуск:

### клонируйте репозиторий

```
git clone https://github.com/exp-ext/ticket_gorzdrav.git
```

### зайдите в папку, создайте виртуальное окружения

Unix / Linux / macOS:

```
python3 -m venv venv && source venv/bin/activate && python -m pip install --upgrade pip
```

Windows:

```
python -m venv venv && venv\Scripts\activate && python -m pip install --upgrade pip
```

### установите зависимости

```
python3 -m pip install -r requirements.txt
```

- создайте файл `.env` из образца `.env.example`, заполнив переменные своими данными.

- запустите программу находясь в папке сфайлом `main.py`

Unix / Linux / macOS:

```
python main.py
```

или в фоновом режиме

```
python main.py &
```

Windows:

```
start /B python main.py
```

<hr />

### Script author: Borokin Andrey

GITHUB: [exp-ext](https://github.com/exp-ext)

[![Join Telegram](https://img.shields.io/badge/My%20Telegram-Join-blue)](https://t.me/Borokin)
