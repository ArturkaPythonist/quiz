import os
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
bind = "127.0.0.1:8000"
chdir = '/mnt/c/Users/Admin/PycharmProjects/quiz'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz.settings")

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

