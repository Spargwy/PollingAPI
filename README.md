Простейший опросник

Перед запуском необходимо установить зависимости командой  
```
pipenv install
```

Создать и накатить миграции командами
```
./manage.py makemigrations
./manage.py migrate
```

Также, для работы с админкой требуется создать пользователя командой
```
./manage.py createsuperuser --email admin@example.com --username admin
```

и запустить в корневой директории командой
```
./manage.py runserver
```
