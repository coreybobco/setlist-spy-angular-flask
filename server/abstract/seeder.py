import time

#Abstract class for webcrawling from MixesDb
class AbstractSeeder(AbstractParent):
    def __init__(self):
                AbstractCrawler.__init__(self)
        self.start_time = time.time()
        return

    def log_time(self):
        print("--- %s seconds to crawl---" % (time.time() - self.start_time))
