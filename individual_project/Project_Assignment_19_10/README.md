# HTTP Client & Server (GUI)

Десктопное приложение на Python с графическим интерфейсом (tkinter). Внутри — собственный HTTP-клиент и HTTP-сервер, написанные на сокетах, без сторонних сетевых библиотек (`requests`, `flask` и т.п. не используются).

## Возможности

- **Клиент:** GET и POST, таблица заголовков, тело запроса, таймауты, разбор `Content-Length` и `Transfer-Encoding: chunked`, `Host` по умолчанию, `Content-Type` и `Content-Length` для POST, обработка ошибок `HttpError`.
- **Сервер:** маршруты `/`, `/echo`, `/time`, `/headers`, `/status/{code}`, 404; keep-alive и `Connection: close`; защита от переполнения заголовков (> 8 КБ → 400); запуск и остановка в отдельном потоке.
- **GUI:** вкладки «Клиент» и «Сервер», лог запросов в реальном времени, индикатор состояния, кнопка «Открыть в браузере».
- **Тесты:** 47 unit и интеграционных тестов (pytest).
- **Логирование:** файл `app.log` и вывод в консоль через модуль `logging`.

## Требования

- Python 3.10+
- tkinter (входит в стандартную поставку Python; на Linux — `sudo apt install python3-tk`)
- pytest, flake8, pylint — только для тестов и линтеров

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

Через Python:

```bash
python -m src.main
```

Через Makefile:

```bash
make run
```

Откроется окно с двумя вкладками: «Клиент» и «Сервер».

## Использование клиента

1. Введите URL, например `http://example.com/`.
2. Выберите метод: GET или POST.
3. Для POST заполните поле «Тело (POST)».
4. При необходимости добавьте заголовки через кнопку «Добавить».
5. Нажмите «Отправить».

В области «Ответ» появятся статус, заголовки и тело. Запрос выполняется в фоновом потоке — интерфейс не замерзает.

## Использование сервера

1. Укажите порт (по умолчанию `8080`).
2. Нажмите «Запустить». Индикатор станет зелёным.
3. Откройте в браузере `http://localhost:8080/` или используйте `curl`.

Доступные маршруты:
- `/` (GET) — HTML-страница «Hello».
- `/echo` (POST) — возвращает тело запроса, `Content-Type` сохраняется.
- `/time` (GET) — текущее время в JSON.
- `/headers` (GET) — все заголовки запроса в JSON.
- `/status/{code}` (GET) — ответ с указанным статус-кодом.
- любой другой маршрут — 404 Not Found.

Кнопка «Остановить» освобождает порт.

## Примеры curl

```bash
curl.exe -v http://localhost:8080/
curl.exe -v http://localhost:8080/time
curl.exe -v http://localhost:8080/headers
curl.exe -v http://localhost:8080/status/418
curl.exe -v -X POST -d "hello" http://localhost:8080/echo
curl.exe -v http://localhost:8080/nonexistent
```

## Тесты

```bash
pytest tests/ -v
```

- Unit-тесты: URL-парсер, HTTP-парсер, сериализатор.
- Интеграционные: клиент ↔ сервер в одном процессе.
- Всего: 47 тестов, включая вспомогательные тесты клиента и TCP-слоя.

## Линтеры

```bash
flake8 src/ tests/ --max-line-length=120
pylint src/ --disable=C0111,C0103,R0913,R0914,W0611,W0613,R0902,R0903,R0801,W0718,C0415 --max-line-length=120 --init-hook="import sys; sys.path.insert(0, '.')"
```

## Структура проекта

```text
src/
├── http/
│   ├── url.py          # Url, ParseError
│   ├── request.py      # Request
│   ├── response.py     # Response
│   ├── parser.py       # Parser (parse_request, parse_response)
│   ├── serializer.py   # serialize_request, serialize_response
│   ├── errors.py       # HttpError
│   └── abc.py          # AbstractParser, AbstractHandler
├── net/
│   ├── socket_wrapper.py  # Socket (контекстный менеджер)
│   ├── tcp_client.py      # TcpClient
│   └── tcp_server.py      # TcpServer
├── client/
│   └── http_client.py     # HttpClient
├── server/
│   ├── http_server.py     # HttpServer (поток)
│   ├── router.py          # Router
│   └── handlers.py        # RootHandler, EchoHandler, TimeHandler, HeadersHandler
├── gui/
│   └── app.py             # App (tkinter)
├── log_config.py          # настройка logging
└── main.py                # точка входа
tests/
├── test_url.py
├── test_parser.py
├── test_serializer.py
├── test_tcp_client.py
├── test_http_client.py
├── test_server.py
└── test_integration.py
requirements.txt
Makefile
README.md
report.md
```

## Особенности реализации

- **HTTP/1.1**: обязательный `Host`, keep-alive, `Content-Length`, `Transfer-Encoding: chunked`.
- **Таймауты** соединения и чтения (секунды внутри, миллисекунды в API `set_timeout`).
- **Защита от переполнения** заголовков: > 8 КБ → `ParseError` → 400 Bad Request.
- **Многопоточность**: сервер в фоновом потоке, GUI обновляется только из главного потока через `queue.Queue` и `root.after`.
- **Исключения вместо кодов возврата**: `ParseError`, `ConnectionError`, `TimeoutError`, `HttpError(status)`.
- **Контекстные менеджеры** для сокетов (`with`).
- **Логирование** через `logging` в файл и консоль.