from threading import Thread

class helper:

    thread = Thread()

    def set_thread(self, t):
        helper.thread = t

    def get_thread(self):
        return helper.thread