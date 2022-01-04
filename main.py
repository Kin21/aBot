import updater
import queue
import threading
import responder




updates_queue = queue.Queue()

u = updater.Updater(updates_queue)
r = responder.Responder(updates_queue, None)

t1 = threading.Thread(target = u.start)
t2 = threading.Thread(target = r.start)
t1.start()
t2.start()
