import updater
import queue
import threading
from telegram.data import Update

def test(q):
    while True:
        if not q.empty():
            u = q.get()
            print(u)

updates_queue = queue.Queue()

u = updater.Updater(updates_queue)
t1 = threading.Thread(target = u.start)
t2 = threading.Thread(target=lambda q=updates_queue: test(q))
t1.start()
t2.start()
