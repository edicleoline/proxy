from framework.settings import Settings
from typing import List
from datetime import datetime, timedelta

class Cloacker():
    id: str
    interval: int
    ready_at: datetime
    suspended: bool = False
    locked: bool = False
    inverted: bool = False

    def __init__(self, id: str, interval: int):
        self.id = id
        self.interval = interval   
        self.reset()     

    def ready(self):
        if self.suspended == True or self.locked == True: return False

        if self.inverted == True:
            self.inverted = False
            self.reset()
            return True

        diff = int((self.ready_at - datetime.now()).total_seconds())
        print('difffffffff {0} ready_at {1}'.format(diff, self.ready_at))
        ready = True if diff <= 0 and diff > -1 else False
        if diff < 0: self.reset()
        if ready: self.locked = True
        return ready
    
    def reset(self):
        self.ready_at = datetime.now() + timedelta(seconds = self.interval)
        self.locked = False
    
    def suspend(self):
        self.suspended = True

    def unsuspend(self):
        self.suspended = False

    def invert(self):
        self.inverted = True


class CloackerService():
    settings: Settings = None
    cloackers: List[Cloacker] = []

    def __init__(self, settings: Settings = None):
        self.settings = settings

    def add_or_update(self, cloacker: Cloacker):
        _cloacker = self.cloacker_by_id(cloacker.id)
        if _cloacker:
            _cloacker.interval = cloacker.interval
            _cloacker.reset()
        else:
            self.add(cloacker = cloacker)

    def add(self, cloacker: Cloacker):
        self.cloackers.append(cloacker)

    def remove_by_id(self, cloacker_id: str):
        self.cloackers[:] = [x for x in self.cloackers if not x.id == cloacker_id]

    def exist(self, cloacker_id: str):
        return True if self.cloacker_by_id(cloacker_id) else False

    def cloacker_by_id(self, cloacker_id: str):
        if not self.cloackers: return None

        for cloacker in self.cloackers:
            if cloacker.id == cloacker_id: return cloacker

        return None

