# asynchronous-tenders

## Table of Contents
+ [About](#about)
+ [Getting Started](#getting_started)
+ [Usage](#usage)

## About <a name = "about"></a>
Скрипт для асинхронного завантаження даних з АРІ прозоро

## Getting Started <a name = "getting_started"></a>
### Інструкція щодо використання бібліотеки

#### Віртуальне середовище
Після клонування репозиторію слід створити віртуальне середовище та встановити бібліотеки з `requirements.txt`
```bash
$ python -m venv env
$ env/Scripts/activate
(env)$ python -m pip install -r requirements.txt 
```

## Usage <a name = "usage"></a>
Заповнити `links.csv` унікальними ідентифікаторами тендерів (`tender_id`) та статусом (`status`):

|tender_id|status|
|---------|------|
|https://public.api.openprocurement.org/api/2.5/tenders/dfe1adc050ea4729832c6f148fd39555|0|
|https://public.api.openprocurement.org/api/2.5/tenders/b8cc699d53ef45f6a7daaf3bd9e7f904|0|
|https://public.api.openprocurement.org/api/2.5/tenders/7c685cb5459f4cae93c702923ee2525d|0|
|https://public.api.openprocurement.org/api/2.5/tenders/400ae661a1d744988db3dd2c1e72c281|0|
|https://public.api.openprocurement.org/api/2.5/tenders/b725907aac6b4883b5f345356b6a5cc7|0|


Після цього запустити `main.py` з віртуального середовища
```bash
(env)$ python main.py
```

Скрипт відфільтрує тендери із `status == 0` і почне виконувати запити. 
Відповіді АРІ будуть збережені у папку `data/` (кожна відповідь буде названа за ідентифікатором тендера, напр. `dfe1adc050ea4729832c6f148fd39555.json`). 

У завантажених тендерів в оригінальній таблиці `links.csv` `status` зміниться на `1`, коли скрипт успішно завершиться: 


|tender_id|status|
|---------|------|
|https://public.api.openprocurement.org/api/2.5/tenders/dfe1adc050ea4729832c6f148fd39555|1|
|https://public.api.openprocurement.org/api/2.5/tenders/b8cc699d53ef45f6a7daaf3bd9e7f904|1|
|https://public.api.openprocurement.org/api/2.5/tenders/7c685cb5459f4cae93c702923ee2525d|1|
|https://public.api.openprocurement.org/api/2.5/tenders/400ae661a1d744988db3dd2c1e72c281|0|
|https://public.api.openprocurement.org/api/2.5/tenders/b725907aac6b4883b5f345356b6a5cc7|0|


---

# TO-DO
* [ ] Виправити `aiohttp.client_exceptions.ServerDisconnectedError`
* [ ] Налаштувати аналог cron для windows server
* [ ] Визначити оптимальний ліміт на запити в секунду