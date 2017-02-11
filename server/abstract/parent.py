import time

#Abstract Parent Class. Invoke this to time functions
class AbstractParent():
    def __init__(self):
        self.start_time = time.time()

    def log_time(self, reset_timer=False):
        print("---Runtime: %s seconds---" % (time.time() - self.start_time))
        if reset_timer:
            print("---Resetting timer---")
            self.start_time = time.time()
