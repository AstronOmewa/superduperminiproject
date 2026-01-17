# superduperminiproject
Мини-проект по python

# Инструкция по развертыванию
## Создание виртуального окружения и активация
0. Если не установлен ```pip``` и ```python```, то установите (зависит от ОС).
1. В терминале с проектом: 
    > ```python -m venv venv```
2. Активация
    1. Windows: 
        > ```cd venv/Scripts/activate.ps1``` (PS)

        ИЛИ
        
        >  ```cd venv/Scripts/activate.bat``` (Terminal)


    2. macOS/Linux/WSL:
        > ```source venv/bin/activate```
    
## Установка зависимостей

В корневом каталоге проекта:

> ```pip install -r requirements.txt```

## Запуск

1. > ```cd backend```

2. > ```python app.py```

3. В браузере введите ```ip``` из консоли (например, 127.0.0.1) и порт (5000). Таким образом, строка поиска должна выглядеть следующим образом: ```http://127.0.0.1:5000/```