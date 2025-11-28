# gunicorn.conf.py
import multiprocessing

# Number of worker processes
workers = multiprocessing.cpu_count() * 2 + 1

# Use the 'gthread' worker class for handling concurrent I/O-bound requests
worker_class = 'gthread'

# Number of threads per worker
threads = 4

# Timeout for workers
timeout = 120

# Bind to all network interfaces on the port provided by Render
bind = "0.0.0.0:10000"

# Log to stdout
accesslog = "-"
errorlog = "-"
