### Установка проекта

- установить версию python 3.10
- создать виртуальное окружение 
```shell script
python3.10 -m venv venv
```
- активировать виртуальное окружение
```shell script
source venv/bin/activate
```
- установить зависимости
```shell script
pip install -r requirements.txt
pip install -r requirements_dev.txt
```
- запустить
```shell script
./manage.py runserver
```
- открыть в браузере http://localhost:8000 

### Документация по API
#### Endpoints:
- /forms/ - получение списка активных опросов
- /forms/{id: int} - получение списка вопросов по ID опроса
- /questions/{id: int}/answer/ - прохождение опроса (отправка ответа на вопрос)
- /users/{id: int}/forms/ - получение пройденных пользователем опросов с детализацией по ответам по ID уникальному пользователя
