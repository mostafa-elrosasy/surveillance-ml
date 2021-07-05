import time
class Timer:
    def __init__(self, period = 5):
        self.time = 0
        self.period = period
    
    def its_time(self) -> bool:
        return time.time() > self.time + self.period

    def mark_time(self):
        self.time = time.time()
