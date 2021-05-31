Простейший опросник

Перед запуском необходимо установить зависимости командой  
```
install -r requirments.txt
```

Создать и накатить миграции командами
```
python3 manage.py makemigrations
python3 manage.py migrate
```

Также, для работы с админкой требуется создать пользователя командой
```
python manage.py createsuperuser --email admin@example.com --username admin
```

и запустить в корневой директории командой
```
python3 manage.py runserver
```