import json
import time

#Abstract class for webcrawling from MixesDb
class AbstractSeeder:
    def __init__(self):
        self.start_time = time.time()
        self.db = json.load(open("db.json"))
        return

    def log_time(self):
        print("--- %s seconds to crawl---" % (time.time() - self.start_time))
