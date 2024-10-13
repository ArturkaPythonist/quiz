import os
import multiprocessing

# Определение числа воркеров
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"

# Привязка к интерфейсу, если нужен внешний доступ, измените на 0.0.0.0
bind = "0.0.0.0:8000"

# Переход в рабочую директорию
os.chdir("/app")

# Устанавливаем настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz.settings")

# Логирование
loglevel = 'info'
errorlog = '-'  # Логи ошибок выводятся в стандартный вывод
accesslog = '-'  # Логи доступа также выводятся в стандартный вывод

# Функции хуков для Gunicorn
def post_fork(server, worker):
    server.log.info(f"Worker spawned (pid: {worker.pid})")

def worker_int(worker):
    worker.log.info(f"Worker exiting (pid: {worker.pid})")

def worker_abort(worker):
    worker.log.info(f"Worker aborting (pid: {worker.pid})")

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    server.log.info("Server is ready to accept requests.")
