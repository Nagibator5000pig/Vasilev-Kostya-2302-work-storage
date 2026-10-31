import queue
import threading
import tkinter as tk
import webbrowser
from tkinter import ttk
from datetime import datetime

from src.client.http_client import HttpClient
from src.http.url import ParseError
from src.server.handlers import RootHandler, EchoHandler, TimeHandler, HeadersHandler
from src.server.http_server import HttpServer
from src.log_config import setup_logging
from src.server.router import Router


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HTTP Client/Server")
        self.geometry("900x600")

        self._queue = queue.Queue()
        self._client = HttpClient(timeout=5.0)
        self._logger = setup_logging()
        self._server: HttpServer | None = None

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.client_tab = ttk.Frame(notebook, padding=10)
        self.server_tab = ttk.Frame(notebook, padding=10)
        notebook.add(self.client_tab, text="Клиент")
        notebook.add(self.server_tab, text="Сервер")

        self._build_client_tab()
        self._build_server_tab()

        self.after(100, self._poll_queue)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_client_tab(self):
        frame = self.client_tab

        top = ttk.Frame(frame)
        top.pack(fill="x", pady=5)

        ttk.Label(top, text="Метод:").pack(side="left")
        self.method_var = tk.StringVar(value="GET")
        method_box = ttk.Combobox(top, textvariable=self.method_var, values=["GET", "POST"], width=8, state="readonly")
        method_box.pack(side="left", padx=5)
        method_box.bind("<<ComboboxSelected>>", self._on_method_change)

        ttk.Label(top, text="URL:").pack(side="left", padx=(10, 0))
        self.url_var = tk.StringVar(value="http://example.com/")
        ttk.Entry(top, textvariable=self.url_var).pack(side="left", fill="x", expand=True, padx=5)

        self.send_btn = ttk.Button(top, text="Отправить", command=self._on_send)
        self.send_btn.pack(side="left", padx=5)

        self.clear_btn = ttk.Button(top, text="Очистить", command=self._on_clear)
        self.clear_btn.pack(side="left")

        self.loading_label = ttk.Label(frame, text="")
        self.loading_label.pack(anchor="w")

        headers_frame = ttk.LabelFrame(frame, text="Заголовки")
        headers_frame.pack(fill="both", expand=False, pady=5)

        headers_inner = ttk.Frame(headers_frame)
        headers_inner.pack(fill="both", expand=True, padx=5, pady=5)

        self.headers_tree = ttk.Treeview(
            headers_inner, columns=("name", "value"), show="headings", height=4
        )
        self.headers_tree.heading("name", text="Имя")
        self.headers_tree.heading("value", text="Значение")
        self.headers_tree.column("name", width=200)
        self.headers_tree.column("value", width=500)
        self.headers_tree.pack(side="left", fill="both", expand=True)

        h_btns = ttk.Frame(headers_inner)
        h_btns.pack(side="right", fill="y", padx=(5, 0))

        ttk.Button(h_btns, text="Добавить", command=self._add_header_dialog).pack(fill="x", pady=2)
        ttk.Button(h_btns, text="Удалить", command=self._remove_header).pack(fill="x", pady=2)

        body_frame = ttk.LabelFrame(frame, text="Тело (POST)")
        body_frame.pack(fill="both", expand=False, pady=5)

        self.body_text = tk.Text(body_frame, height=5)
        self.body_text.pack(fill="both", expand=True, padx=5, pady=5)

        response_frame = ttk.LabelFrame(frame, text="Ответ")
        response_frame.pack(fill="both", expand=True, pady=5)

        self.status_label = ttk.Label(response_frame, text="Статус: —")
        self.status_label.pack(anchor="w", padx=5, pady=2)

        self.response_text = tk.Text(response_frame, height=15)
        self.response_text.pack(fill="both", expand=True, padx=5, pady=5)

        self._on_method_change()

    def _build_server_tab(self):
        frame = self.server_tab

        top = ttk.Frame(frame)
        top.pack(fill="x", pady=5)

        ttk.Label(top, text="Порт:").pack(side="left")
        self.port_var = tk.StringVar(value="8080")
        ttk.Entry(top, textvariable=self.port_var, width=8).pack(side="left", padx=5)

        self.start_btn = ttk.Button(top, text="Запустить", command=self._on_start_server)
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = ttk.Button(top, text="Остановить", command=self._on_stop_server, state="disabled")
        self.stop_btn.pack(side="left")

        self.state_label = ttk.Label(top, text="● Остановлен", foreground="red")
        self.state_label.pack(side="left", padx=15)

        log_frame = ttk.LabelFrame(frame, text="Лог запросов")
        log_frame.pack(fill="both", expand=True, pady=5)

        columns = ("time", "method", "path", "status")
        self.log_tree = ttk.Treeview(log_frame, columns=columns, show="headings", height=15)
        self.log_tree.heading("time", text="Время")
        self.log_tree.heading("method", text="Метод")
        self.log_tree.heading("path", text="Путь")
        self.log_tree.heading("status", text="Статус")
        self.log_tree.column("time", width=150)
        self.log_tree.column("method", width=80)
        self.log_tree.column("path", width=400)
        self.log_tree.column("status", width=80)
        self.log_tree.pack(fill="both", expand=True, padx=5, pady=5)

        bottom = ttk.Frame(log_frame)
        bottom.pack(fill="x", padx=5, pady=(0, 5))

        ttk.Button(bottom, text="Открыть в браузере", command=self._open_in_browser).pack(side="left")
        ttk.Button(bottom, text="Очистить лог", command=self._clear_log).pack(side="right")

    def _on_method_change(self, event=None):
        if self.method_var.get() == "POST":
            self.body_text.config(state="normal", background="white")
        else:
            self.body_text.config(state="disabled", background="#e0e0e0")

    def _add_header_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Добавить заголовок")
        dialog.geometry("400x120")
        dialog.transient(self)
        dialog.grab_set()

        ttk.Label(dialog, text="Имя:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var, width=40).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Значение:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        value_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=value_var, width=40).grid(row=1, column=1, padx=5, pady=5)

        def on_ok():
            name = name_var.get().strip()
            value = value_var.get().strip()
            if name:
                self.headers_tree.insert("", "end", values=(name, value))
            dialog.destroy()

        ttk.Button(dialog, text="OK", command=on_ok).grid(row=2, column=1, padx=5, pady=10, sticky="e")

    def _remove_header(self):
        for item in self.headers_tree.selection():
            self.headers_tree.delete(item)

    def _on_send(self):
        method = self.method_var.get()
        url = self.url_var.get().strip()
        self._logger.info("Sending %s %s", method, url)
        headers = self._parse_headers()
        body = b""
        if method == "POST":
            body = self.body_text.get("1.0", "end-1c").encode("utf-8")

        self.send_btn.config(state="disabled")
        self.loading_label.config(text="Отправка...")
        self.status_label.config(text="Статус: —")
        self.response_text.delete("1.0", "end")

        threading.Thread(target=self._do_request, args=(method, url, headers, body), daemon=True).start()

    def _do_request(self, method, url, headers, body):
        try:
            if method == "GET":
                resp = self._client.get(url, headers=headers)
            else:
                content_type = headers.pop("Content-Type", "text/plain")
                resp = self._client.post(url, body=body, content_type=content_type, headers=headers)
            self._queue.put(("ok", resp))
        except ParseError as e:
            self._queue.put(("error", f"ParseError: {e}"))
        except Exception as e:
            self._queue.put(("error", f"{type(e).__name__}: {e}"))

    def _poll_queue(self):
        try:
            while True:
                kind, payload = self._queue.get_nowait()
                if kind == "ok":
                    self._render_response(payload)
                elif kind == "error":
                    self._render_error(payload)
                elif kind == "log":
                    self._append_log(payload)
        except queue.Empty:
            pass
        self.after(100, self._poll_queue)

    def _render_response(self, resp):
        self.status_label.config(text=f"Статус: {resp.status} {resp.reason}")
        headers = "\r\n".join(f"{k}: {v}" for k, v in resp.headers.items())
        try:
            body = resp.body.decode("utf-8")
        except UnicodeDecodeError:
            body = repr(resp.body)
        self.response_text.delete("1.0", "end")
        self.response_text.insert("1.0", f"{headers}\r\n\r\n")
        start = self.response_text.index("end-1c")
        self.response_text.insert("end", body)
        self._highlight(body, start)
        self._finish()

    def _highlight(self, body: str, start: str):
        self.response_text.tag_configure("json_key", foreground="blue")
        self.response_text.tag_configure("json_str", foreground="green")
        self.response_text.tag_configure("html_tag", foreground="purple")
        if body.strip().startswith(("{", "[")):
            import re
            for m in re.finditer(r'"[^"]+"\s*:', body):
                self.response_text.tag_add("json_key", f"{start}+{m.start()}c", f"{start}+{m.end()}c")
            for m in re.finditer(r':\s*"([^"]*)"', body):
                s, e = m.start(1), m.end(1)
                self.response_text.tag_add("json_str", f"{start}+{s}c", f"{start}+{e}c")
        elif body.strip().startswith("<"):
            import re
            for m in re.finditer(r'<[^>]+>', body):
                self.response_text.tag_add("html_tag", f"{start}+{m.start()}c", f"{start}+{m.end()}c")

    def _render_error(self, message):
        self._logger.error("Request failed: %s", message)
        self.status_label.config(text="Ошибка")
        self.response_text.delete("1.0", "end")
        self.response_text.insert("1.0", message)
        self._finish()

    def _finish(self):
        self.send_btn.config(state="normal")
        self.loading_label.config(text="")

    def _on_clear(self):
        for item in self.headers_tree.get_children():
            self.headers_tree.delete(item)
        self.body_text.delete("1.0", "end")
        self.response_text.delete("1.0", "end")
        self.status_label.config(text="Статус: —")

    def _parse_headers(self):
        result = {}
        for item in self.headers_tree.get_children():
            name, value = self.headers_tree.item(item, "values")
            if name:
                result[name] = value
        return result

    def _log_request(self, req, resp):
        t = datetime.now().strftime("%H:%M:%S")
        m = req.method if req else "?"
        p = req.path if req else "?"
        self._queue.put(("log", (t, m, p, resp.status)))

    def _on_start_server(self):
        try:
            port = int(self.port_var.get())
        except ValueError:
            self.state_label.config(text="Неверный порт", foreground="red")
            return

        router = Router()
        router.route("GET", "/", RootHandler().handle)
        router.route("POST", "/echo", EchoHandler().handle)
        router.route("GET", "/time", TimeHandler().handle)
        router.route("GET", "/headers", HeadersHandler().handle)

        self._server = HttpServer(router, host="0.0.0.0", port=port)
        self._server.on_request = self._log_request
        try:
            self._logger.info("Starting server on port %d", port)
            self._server.start()
        except OSError as e:
            self.state_label.config(text=f"Ошибка: {e}", foreground="red")
            self._server = None
            return

        self.state_label.config(text=f"● Запущен на {port}", foreground="green")
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")

    def _on_stop_server(self):
        if self._server is not None:
            self._logger.info("Stopping server")
            self._server.stop()
            self._server = None
        self.state_label.config(text="● Остановлен", foreground="red")
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

    def _append_log(self, row):
        self.log_tree.insert("", "end", values=row)

    def _open_in_browser(self):
        try:
            port = int(self.port_var.get())
        except ValueError:
            port = 8080
        webbrowser.open(f"http://localhost:{port}/")

    def _clear_log(self):
        for item in self.log_tree.get_children():
            self.log_tree.delete(item)

    def _on_close(self):
        if self._server is not None:
            self._server.stop()
        self.destroy()
