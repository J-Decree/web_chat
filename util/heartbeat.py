import threading
import queue
from util.queue import message_queue, heartbeat_queue


class HeartbeatHelper(object):
    def __init__(self, m_queue=message_queue, h_queue=heartbeat_queue):
        self.m_queue = m_queue
        self.h_queue = h_queue

    def target_func(self, userinfo_id):
        while True:
            try:
                heartbeat_queue.site[userinfo_id].get(timeout=3)
            except queue.Empty:
                self.m_queue.publish_logout_message(userinfo_id)
                break

    def start_guard_thread(self, userinfo_id):
        t = threading.Thread(target=self.target_func, args=(userinfo_id,))
        t.start()
