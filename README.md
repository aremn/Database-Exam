
# DataBase Project

Данный проект представляет собой информационную систему для управления данными о видах, размещениях и помещениях в зоопарке. Приложение предоставляет REST API с использованием технологий **FastAPI**, **SQLAlchemy**, и **Alembic**, а также включает удобный пользовательский интерфейс.

![image](https://github.com/user-attachments/assets/c6b0f3d1-019f-4bda-a671-020eacd110e9)


---

## Технологии

- **Backend**: FastAPI, SQLAlchemy ORM
- **Frontend**: HTML с CSS
- **Database**: PostgreSQL
- **Миграции**: Alembic

---

## Основные возможности

1. **CRUD-операции**:
   - Создание, чтение, обновление и удаление данных о видах, размещениях и помещениях.
2. **Фильтрация данных**:
   - Удобная, гибкая и быстрая фильтрация данных по разным параматрам
3. **Экспорт данных**:
   - Экспорт данных в формате CSV для всех сущностей.
4. **Пагинация**:
   - Удобная навигация между страницами.
5. **REST API**:
   - Полный доступ к данным через API.
6. **JSON-поле и полнотекстовый поиск**:
   - Хранение и поиск данных с использованием индекса pg_trgm.

---

## Скриншоты

### Главная страница с видами (Species)
![Главная страница Subjects](https://github.com/user-attachments/assets/7e3181b5-8ed9-4831-8b2c-1324e40452cf)



### Страница размещениями (Enclosures)
![Страница с размещениями](https://github.com/user-attachments/assets/ae33fff2-cca3-4f6c-9a59-06d9ba5309b1)



### Страница помещений (Placements)

![Страница с помещениями](https://github.com/user-attachments/assets/45565d9f-ca4b-41ef-b886-602abed64d3c)


---

## Установка и запуск

### 1. Установите зависимости
```bash
pip install -r requirements.txt
```

### 2. Настройте базу данных
- Создайте базу данных в PostgreSQL.
- Обновите файл `.env` с вашими настройками базы данных.

Пример `.env`:
```
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/zoo_db
```

### 3. Выполните миграции
```bash
alembic upgrade head
```

### 4. Запустите приложение
```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: [http://127.0.0.1:8001](http://127.0.0.1:8001).

---

## API-эндпоинты

### 127.0.0.1:8001/docs

![API](https://github.com/user-attachments/assets/539a82a6-f107-4a15-9b22-4038f7906c5b)


---
