from kombu import Queue

broker_url = "pyamqp://guest@localhost//"
result_backend = "redis://localhost:6379/0"

result_chord_retry_interval = 300
worker_prefetch_multiplier = 1
worker_concurrency = 1
worker_pool = "prefork"
task_queues = [
    Queue("first_testing"),
    Queue("second_testing")
]
