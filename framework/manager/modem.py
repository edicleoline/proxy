from datetime import datetime
from framework.infra.modem import Modem as IModem
from threading import Thread
from threading import Event
from enum import Enum
from framework.manager.error.exception import ModemLockedByOtherThreadException, ModemRebootException, NoTaskRunningException
from framework.models.modemthreadtask import TaskWizard
from framework.proxy.factory import ProxyService
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from marshmallow import fields
import uuid
from framework.settings import Settings

class ModemManager():
    def __init__(self, proxy_service: ProxyService, settings: Settings):
        self.proxy_service = proxy_service
        self.settings = settings
        self.threads = []

    def reboot(self, infra_modem: IModem, hard_reset = False):
        thread_running = self.running(infra_modem)

        if thread_running:
            raise ModemLockedByOtherThreadException('We could running this task now because this modem is locked by another thread.')
        
        self.remove_thread_from_list(infra_modem=infra_modem)
        
        event_stop = Event()
        infra_modem.event_stop = event_stop
        infra_modem.proxy_service = self.proxy_service

        process_thread = Thread(
            target=infra_modem.reboot,
            args=(
                hard_reset,
            )
        )
        process_thread.start()

        self.threads.append(
            ModemThreadData(infra_modem, ModemThreadAction.REBOOT, process_thread, event_stop)
        )        

    def rotate(
            self, 
            infra_modem: IModem, 
            proxy_user_id = None, 
            proxy_username = None,
            filters = None, 
            hard_reset = False, 
            not_changed_try_count = 3, 
            not_ip_try_count = 6
    ):
        thread_running = self.running(infra_modem)

        if thread_running:
            raise ModemLockedByOtherThreadException('We could running this task now because this modem is locked by another thread.')

        self.remove_thread_from_list(infra_modem=infra_modem)

        event_stop = Event()
        infra_modem.event_stop = event_stop
        infra_modem.proxy_service = self.proxy_service

        process_thread = Thread(
            target=infra_modem.rotate, 
            args=(
                filters, 
                proxy_user_id, 
                proxy_username,
                hard_reset, 
                not_changed_try_count, 
                not_ip_try_count,
                lambda: self.get_threads()
            )
        )
        process_thread.start()

        self.threads.append(
            ModemThreadData(infra_modem, ModemThreadAction.ROTATE, process_thread, event_stop)
        )

    def diagnose(self, infra_modem: IModem):
        thread_running = self.running(infra_modem)

        if thread_running:
            raise ModemLockedByOtherThreadException('We could running this task now because this modem is locked by another thread.')
        
        self.remove_thread_from_list(infra_modem=infra_modem)
        
        event_stop = Event()
        infra_modem.event_stop = event_stop
        infra_modem.proxy_service = self.proxy_service

        process_thread = Thread(
            target=infra_modem.diagnose,
            args=(
                lambda: self.get_threads(),
            )
        )
        process_thread.start()

        self.threads.append(
            ModemThreadData(infra_modem, ModemThreadAction.DIAGNOSE, process_thread, event_stop, None)
        )

    def stop_task(self, infra_modem: IModem, callback = None):
        thread_running = self.running(infra_modem)

        if not thread_running:
            raise NoTaskRunningException('We could find any task running for this modem.')
        
        thread_running.event_stop.set()

    def running(self, infra_modem: IModem):
        for t in self.threads:
            if t.infra_modem.modem().id != infra_modem.modem().id: continue

            if t.thread.is_alive(): return t

        return None
    
    def remove_thread_from_list(self, infra_modem: IModem):
        self.threads[:] = [x for x in self.threads if not x.infra_modem.server_modem_model.id == infra_modem.server_modem_model.id]

    def get_threads(self):
        return self.threads

    def thread_by_id(self, id):
        for thread in self.threads:
            if str(thread.id) == str(id):
                return thread

        return None
        

class ModemThreadAction(Enum):
    REBOOT   = 1
    ROTATE   = 2
    DIAGNOSE = 3


class ModemThreadStatus(Enum):
    RUNNING           = 1
    DONE              = 2
    SUSPENDED_BY_USER = 3


@dataclass_json
@dataclass
class ModemThreadData():
    id: str = None
    task: dict
    wizard: TaskWizard = None

    def __init__(self, infra_modem: IModem, action: ModemThreadAction, thread: Thread, event_stop: Event, wizard: TaskWizard = None):
        self.id = uuid.uuid4()
        self.infra_modem = infra_modem
        self.action = action
        self.thread = thread
        self.event_stop = event_stop
        self.started_at = datetime.now()
        self.wizard = wizard
        self.post_task = None

    @property
    def task(self):
        return {
            'name': self.action.name,
            'stopping': True if self.event_stop.is_set() else False
        }