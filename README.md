# asynchronous-tenders

## Table of Contents
+ [About](#about)
+ [Getting Started](#getting_started)
+ [Usage](#usage)

## About <a name = "about"></a>
Скрипт для асинхронного завантаження даних з АРІ прозоро в `.json`

## Getting Started <a name = "getting_started"></a>
### Інструкція щодо використання бібліотеки

#### Віртуальне середовище
Після клонування репозиторію слід створити віртуальне середовище та встановити бібліотеки з `requirements.txt`
```bash
$ python -m venv env
$ source env/Scripts/activate
$ python -m pip install -r requirements.txt 
```

## Usage <a name = "usage"></a>
Заповнити `links.txt` унікальними ідентифікаторами тендерів, як-от:
```
efc53d5ccd244323a81b8b270eaa8217
305b566b66964d5cbca003ec61d47b1c
631a520e51cc4918b7d0ae1c2e1d36d6
d0061a2d4d2d4d2dbfc988c656eb0946
3346b06ea1cb4e6bb485333eec5a5e40
```
Після цього запустити скрипт з віртуального середовщиа
```bash
(env)$ python main.py
```

Відповіді АРІ будуть збережені у папку `data/`, в якій кожен файл буде названий за ідентифікатором тендера. 