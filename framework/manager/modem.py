from framework.infra.modem import Modem as IModem
from threading import Thread
from threading import Event
from enum import Enum
from framework.manager.error.exception import ModemLockedByOtherThreadException, ModemRebootException, NoTaskRunningException

class ModemManager():
    def __init__(self):
        self.threads = []

    def reboot(self, infra_modem: IModem, hard_reset = False, callback = None):
        thread_running = self.running(infra_modem)

        if thread_running:
            raise ModemLockedByOtherThreadException('We could running this task now because this modem is locked by another thread.')
        
        event_stop = Event()

        if hard_reset == True:
            try:
                process_thread = Thread(
                    target=infra_modem.hard_reboot_and_wait
                )
                process_thread.start()

                self.threads.append(
                    ModemThreadData(infra_modem, ModemThreadAction.REBOOT, process_thread, event_stop)
                )
            except OSError as error:
                raise ModemRebootException(str(error))
        else:
            device_middleware = infra_modem.get_device_middleware()
            if device_middleware:
                process_thread = Thread(
                    target=device_middleware.reboot_and_wait
                )
                process_thread.start()

                self.threads.append(
                    ModemThreadData(infra_modem, ModemThreadAction.REBOOT, process_thread, event_stop)
                )
            else:
                raise ModemRebootException('Modem is offline. Try hard-reset')

    def rotate(
            self, 
            infra_modem: IModem, 
            proxy_user_id = None, 
            filters = None, 
            hard_reset = False, 
            not_changed_try_count = 3, 
            not_ip_try_count = 6, 
            callback = None
    ):
        thread_running = self.running(infra_modem)

        if thread_running:
            raise ModemLockedByOtherThreadException('We could running this task now because this modem is locked by another thread.')

        event_stop = Event()

        process_thread = Thread(
            target=infra_modem.rotate, 
            args=(
                filters, 
                proxy_user_id, 
                hard_reset, 
                not_changed_try_count, 
                not_ip_try_count,
                callback,
                event_stop
            )
        )
        process_thread.start()

        self.threads.append(
            ModemThreadData(infra_modem, ModemThreadAction.ROTATE, process_thread, event_stop)
        )

    def stop_task(self, infra_modem: IModem, callback = None):
        thread_running = self.running(infra_modem)

        if not thread_running:
            raise NoTaskRunningException('We could find any task running for this modem.')
        
        thread_running.event_stop.set()
        print('stop event sent')

    def running(self, infra_modem: IModem):
        for t in self.threads:
            if t.infra_modem.modem.id != infra_modem.modem.id: continue

            if t.thread.is_alive(): return t
            
            if not t.thread.is_alive():
                pass #remove from list

        return None

        

class ModemThreadAction(Enum):
    REBOOT  = 1
    ROTATE  = 2


class ModemThreadStatus(Enum):
    RUNNING           = 1
    DONE              = 2
    SUSPENDED_BY_USER = 3


class ModemThreadData():
    def __init__(self, infra_modem: IModem, action: ModemThreadAction, thread: Thread, event_stop: Event):
        self.infra_modem = infra_modem
        self.action = action
        self.thread = thread
        self.event_stop = event_stop