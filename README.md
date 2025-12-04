# XPriceComparer

Пример проекта с бэкендом FastAPI и фронтендом Vite/React. Цены обновляются через индивидуальные парсеры для каждого товара.

## Запуск

```bash
# Backend
python -m pip install -r requirements.txt
uvicorn backend.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Структура парсеров

- Директория: `backend/parsers/`
- Каждый файл-парсер содержит:
  - `PRODUCT_ID`: строка (например, `"hp-3053"`)
  - `parse()`: возвращает список словарей `{ "store": str, "name": str, "price": int|float }`
- Примеры: `backend/parsers/hp_3053.py`, `backend/parsers/canon_lbp2900.py`

## Формат товара

Каждая запись в `backend/data/prices.json` теперь состоит из полей:  
`id`, `store`, `name_original`, `price` (плюс пользовательские `name_user`, `tags`, `comment` через overrides).

## Обновление цен

Скрипт: `python backend/update_prices.py`
- Загружает все модули в `backend/parsers/`
- Для каждого парсера берёт офферы и собирает `prices.json`
- Если парсер не вернул данные, оставляет прошлые значения при их наличии

## Добавление нового товара

1. Создайте файл в `backend/parsers/`, например `new_product.py`
2. Задайте `PRODUCT_ID` и реализуйте `parse()` с реальным парсингом (requests + BeautifulSoup или API)
3. Запустите `python backend/update_prices.py` для обновления `backend/data/prices.json`

## Планировщик

Запускайте `python backend/update_prices.py` раз в сутки через cron/systemd/CI, чтобы обновлять цены автоматически.
