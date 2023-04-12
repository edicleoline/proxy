import sys, time
import requests
from threading import Event
from framework.error.exception import TimeoutException
from framework.models.modemdiagnose import ModemDiagnoseModel, ModemDiagnoseOwner, ModemDiagnoseType
from framework.models.modemthreadtask import TaskWizard, TaskWizardStep, TaskWizardStepType
from framework.models.proxyuseripfilter import ProxyUserIPFilterModel
from framework.models.server import ServerModemModel
from framework.models.modemiphistory import ModemIPHistoryModel
from framework.models.proxyuseriphistory import ProxyUserIPHistoryModel
from framework.models.modemlog import ModemLogModel, ModemLogOwner, ModemLogType
from framework.infra.netiface import NetIface
from framework.infra.usb import USB
from framework.infra.route import Route
from framework.device.zte.mf79s import MF79S
from framework.device.zte.error.exception import ConnectException
from datetime import datetime
from enum import Enum
from framework.proxy.factory import ProxyService

CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLAC = '\033[90m'
CEND = '\033[0m'

class Error(Enum):
    IP_NOT_CHANGED  = 300
    NO_PUBLIC_IP    = 301
    MIDDLEWARE_NOT_FOUND = 201
    MIDDLEWARE_IP_RELEASE_FAIL = 202
    NOT_CHANGED_IP_TRY_COUNT_EXCEEDED = 303
    NO_IP_TRY_COUNT_EXCEEDED = 306
    USB_HARD_RESET_EXCEPTION = 408

class Owner(Enum):
    SYSTEM  = 1
    USER    = 2

class Modem:
    def __init__(
            self, 
            server_modem_model: ServerModemModel, 
            proxy_service: ProxyService = None, 
            event_stop: Event = None, 
            callback = None
    ):
        self.server_modem_model = server_modem_model   
        self.proxy_service = proxy_service     
        self.event_stop = event_stop
        self.callback = callback
        self._modem = None
        self._usb_port = None

    def modem(self):
        if not self._modem:
            self._modem = self.server_modem_model.modem

        return self._modem

    def usb_port(self):
        if not self._usb_port:
            self._usb_port = self.server_modem_model.usb

        return self._usb_port

    def iface(self):
        addr_id = self.modem().addr_id
        return NetIface.get_iface_by_addr_id(addr_id)        

    def hard_reboot(self):
        USB(server=self.server_modem_model.server()).hard_reboot(usb_port=self.usb_port())

    def hard_turn_off(self):
        USB(server=self.server_modem_model.server()).hard_turn_off(usb_port=self.usb_port())

    def get_device_middleware(self, retries_ip = 5):
        middleware = None

        iface = self.iface()
        if iface == None:
            return None

        if iface.ifaddresses == None:
            return None

        ifaddress = iface.ifaddresses[0]
        gateway = NetIface.get_gateway_from_ipv4(ipv4 = ifaddress['addr'])

        if True:#device != None:
            if True:#modem.model == 'MF79S':
                middleware = MF79S(addr_id = self.modem().addr_id, interface = iface.interface, gateway = gateway, password = 'vivo', retries_ip = retries_ip)

        return middleware

    def wait_until_modem_connection(self):
        while(True):
            if self.event_stop_is_set(log = False): break

            inframodem_iface = self.iface()
            if inframodem_iface != None:
                break

            time.sleep(1)

    def wait_until_modem_disconnection(self):
        while(True):
            if self.event_stop_is_set(log = False): break

            inframodem_iface = self.iface()
            if inframodem_iface == None:
                break

            time.sleep(1)

    def event_stop_is_set(self, log = True):
        if self.event_stop and self.event_stop.is_set():
            if log == True:
                modem_log_model = ModemLogModel(
                    modem_id=self.modem().id, 
                    owner=ModemLogOwner.SYSTEM, 
                    type=ModemLogType.WARNING, 
                    message='app.log.modem.rotate.stopped.by_user'
                )
                modem_log_model.save_to_db()
                self.log(modem_log_model)
            return True
        else:
            return False

    def log(self, log: ModemLogModel):
        if self.callback: self.callback(log)

    def log_diagnose(self, log: ModemDiagnoseModel):
        if self.callback: self.callback(log)

    def resolve_proxy(self):
        if self.proxy_service:
            self.proxy_service.resolve(self.server_modem_model)

    def resolve_route(self):
        inframodem_iface = self.iface()
        modem_ifaddress = inframodem_iface.ifaddresses[0]
        modem_gateway = NetIface.get_gateway_from_ipv4(ipv4 = modem_ifaddress['addr'])        
        route = Route(gateway=modem_gateway, interface=inframodem_iface.interface, ip=modem_ifaddress['addr'], table=self.modem().id)
        route.resolve_route()
        

    def resolve_connectivity(self):
        self.resolve_proxy()
        self.resolve_route()

    def reboot(self, hard_reset = False, write_params = True):
        rebooted = self.reboot_and_wait(hard_reset=hard_reset, write_params=write_params)
        if rebooted == True:
            modem_log_model = ModemLogModel(
                modem_id=self.modem().id, 
                owner=ModemLogOwner.SYSTEM, 
                type=ModemLogType.SUCCESS, 
                message='app.log.modem.reboot.done.success'
            )
            modem_log_model.save_to_db()
            self.log(modem_log_model)

        return rebooted

    def reboot_and_wait(self, hard_reset = False, write_params = True):
        modem_log_model = ModemLogModel(
            modem_id=self.modem().id, 
            owner=ModemLogOwner.SYSTEM, 
            type=ModemLogType.INFO, 
            message='app.log.modem.rebooting',
            params={
                'hard_reset': hard_reset
            } if write_params == True else None,
            logged_at = datetime.now()
        )
        modem_log_model.save_to_db()
        self.log(modem_log_model)

        if hard_reset == True:
            try:
                self.hard_reboot()
                self.wait_until_modem_disconnection()
            except OSError as error:
                modem_log_model = ModemLogModel(
                    modem_id=self.modem().id, 
                    owner=ModemLogOwner.SYSTEM, 
                    type=ModemLogType.ERROR, 
                    message='app.log.modem.reboot.stop.error.hard_reboot',
                    code=Error.USB_HARD_RESET_EXCEPTION.value,
                    logged_at = datetime.now(),
                    params={
                        'usb_port': self.usb_port().port,
                        'error': str(error)
                    }
                )
                modem_log_model.save_to_db()
                self.log(modem_log_model)

                return False
            
            modem_log_model = ModemLogModel(
                modem_id=self.modem().id, 
                owner=ModemLogOwner.SYSTEM, 
                type=ModemLogType.INFO, 
                message='app.log.modem.usb.rebooted_wait_modem', 
                params={
                    'usb_port': self.usb_port().port
                },
                logged_at = datetime.now()
            )
            modem_log_model.save_to_db()
            self.log(modem_log_model)

        else:
            device_middleware = self.get_device_middleware()
            if device_middleware == None:
                modem_log_model = ModemLogModel(
                    modem_id=self.modem().id, 
                    owner=ModemLogOwner.SYSTEM, 
                    type=ModemLogType.ERROR, 
                    message='app.log.modem.reboot.stop.error.middleware_not_found',
                    code=Error.MIDDLEWARE_NOT_FOUND.value,
                    logged_at = datetime.now()
                )
                modem_log_model.save_to_db()
                self.log(modem_log_model)

                return False
            else:
                device_middleware.reboot_and_wait()

        self.wait_until_modem_connection()
        return True
    
    def wizard_wait_response(self, step: TaskWizardStep):
        while True:
            if self.event_stop and self.event_stop.is_set():
                return None
            
            if step.response:
                return step.response

            time.sleep(1)
    
    def diagnose(self, get_threads):
        modem_diagnose_model = ModemDiagnoseModel(
            modem_id=self.modem().id,
            owner=ModemDiagnoseOwner.SYSTEM, 
            type=ModemDiagnoseType.INFO, 
            message='app.modem.diagnose.starting',
            logged_at = datetime.now()
        )
        self.log_diagnose(modem_diagnose_model)

        time.sleep(0.2)

        threads = get_threads()
        self_thread = None
        for thread in threads:
            if thread.infra_modem.server_modem_model.id == self.server_modem_model.id:
                self_thread = thread

        self_thread.wizard = TaskWizard()

        self_thread.wizard.add_step(TaskWizardStep(type = TaskWizardStepType.CHECKING_CONNECTION))
        
        is_connected = self.is_connected()

        time.sleep(4)

        response = None
        if not is_connected:
            step_check_connection = TaskWizardStep(type = TaskWizardStepType.CHECK_CONNECTION, require_response = True)
            self_thread.wizard.add_step(step_check_connection)
            response = self.wizard_wait_response(step = step_check_connection)

        if not response:
            return False

        if 'confirm_modem_on' not in response:
            print('invalid response')
            return False
        
        if response['confirm_modem_on'] == True:
            step_list_interfaces = TaskWizardStep(type = TaskWizardStepType.SELECT_INTERFACE, require_response = True)
            self_thread.wizard.add_step(step_list_interfaces)
            response = self.wizard_wait_response(step = step_list_interfaces)

        else:
            # step_list_interfaces = TaskWizardStep(type = TaskWizardStepType.LIST_INTERFACES, require_response = True)
            # self_thread.wizard.add_step(step_list_interfaces)
            # response = self.wizard_wait_response(step = step_list_interfaces)
            print('nothing to do fuck')

        print('lets continue !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

        # time.sleep(5)
        return True

        
    def rotate(
            self, 
            filters = None, 
            proxy_user_id = None, 
            proxy_username = None,
            hard_reset = False, 
            not_changed_try_count = 3, 
            not_ip_try_count = 3
    ):
        modem_log_model = ModemLogModel(
            modem_id=self.modem().id, 
            owner=ModemLogOwner.SYSTEM, 
            type=ModemLogType.INFO, 
            message='app.log.modem.rotate.starting',
            params={
                'hard_reset': hard_reset,
                'proxy_username': proxy_username,
                'filters': ProxyUserIPFilterModel.schema().dump(filters, many=True) if filters else None                
            },
            logged_at = datetime.now()
        )
        modem_log_model.save_to_db()
        self.log(modem_log_model)

        device_middleware, not_changed_count, not_ip_count = None, 0, 0

        while True:
            old_ip, new_ip, done = None, None, False

            modem_log_model = ModemLogModel(
                modem_id=self.modem().id, 
                owner=ModemLogOwner.SYSTEM, 
                type=ModemLogType.INFO, 
                message='app.log.modem.middleware.starting',
                logged_at = datetime.now()              
            )
            modem_log_model.save_to_db()
            self.log(modem_log_model)

            device_middleware = self.get_device_middleware()
            if device_middleware:
                try: old_ip = device_middleware.wan.try_get_current_ip(timeout = 10)
                except TimeoutException: pass
            else:
                modem_log_model = ModemLogModel(
                    modem_id=self.modem().id, 
                    owner=ModemLogOwner.SYSTEM, 
                    type=ModemLogType.ERROR, 
                    message='app.log.modem.rotate.stop.error.middleware_not_found',
                    code=Error.MIDDLEWARE_NOT_FOUND.value,
                    logged_at = datetime.now()
                )
                modem_log_model.save_to_db()
                self.log(modem_log_model)
                break
        
            if hard_reset == True:
                if self.reboot_and_wait(hard_reset=True, write_params=False) == False:
                    break

                if self.event_stop_is_set() == True: break

                modem_log_model = ModemLogModel(
                    modem_id=self.modem().id, 
                    owner=ModemLogOwner.SYSTEM, 
                    type=ModemLogType.INFO, 
                    message='app.log.modem.rebooted_wait_provider',
                    logged_at = datetime.now()
                )
                modem_log_model.save_to_db()
                self.log(modem_log_model)
                
                device_middleware = self.get_device_middleware()
                try: new_ip = device_middleware.wan.try_get_current_ip(event_stop = self.event_stop, timeout = 30)
                except TimeoutException: pass

            else:
                if self.event_stop_is_set() == True: break            
                self.wait_until_modem_connection()                                
                if self.event_stop_is_set() == True: break   
                                         
                device_middleware = self.get_device_middleware()

                modem_log_model = ModemLogModel(
                    modem_id=self.modem().id, 
                    owner=ModemLogOwner.SYSTEM, 
                    type=ModemLogType.INFO, 
                    message='app.log.modem.middleware.rebooting',
                    logged_at = datetime.now()             
                )
                modem_log_model.save_to_db()
                self.log(modem_log_model)

                try:
                    new_ip = device_middleware.release()
                except ConnectException as e:
                    modem_log_model = ModemLogModel(
                        modem_id=self.modem().id, 
                        owner=ModemLogOwner.SYSTEM, 
                        type=ModemLogType.ERROR, 
                        message='app.log.modem.reboot.stop.error.middleware_reboot',
                        code=Error.MIDDLEWARE_IP_RELEASE_FAIL.value,
                        logged_at = datetime.now()
                    )
                    modem_log_model.save_to_db()
                    self.log(modem_log_model)
                    break

                # new_ip = '189.40.89.35' #TESTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT  
                
            if self.event_stop_is_set() == True: break   

            modem_details = device_middleware.details()
            network_type = modem_details['network_type'] if modem_details else None
            network_provider = modem_details['network_provider'] if modem_details else None
            signalbar = modem_details['signalbar'] if modem_details else None

            if new_ip != None and new_ip != old_ip:
                modem_ip_history = ModemIPHistoryModel(modem_id = self.modem().id, ip = new_ip, network_type = network_type, network_provider = network_provider, signalbar = signalbar)
                modem_ip_history.save_to_db()

                inframodem_iface = self.iface()
                modem_ifaddress = inframodem_iface.ifaddresses[0]
                modem_gateway = NetIface.get_gateway_from_ipv4(ipv4 = modem_ifaddress['addr'])

                if proxy_user_id and self.server_modem_model.prevent_same_ip_users == True:
                    is_ip_reserved_for_other = ProxyUserIPHistoryModel.is_ip_reserved_for_other(ip=new_ip, proxy_user_id=proxy_user_id)

                    if self.event_stop_is_set() == True: break

                    if is_ip_reserved_for_other:
                        modem_log_model = ModemLogModel(
                            modem_id=self.modem().id, 
                            owner=ModemLogOwner.SYSTEM, 
                            type=ModemLogType.WARNING, 
                            message='app.log.modem.rotate.ip.new.reserved_other_user',
                            params={
                                'ipv4': new_ip
                            },
                            logged_at = datetime.now()
                        )
                        modem_log_model.save_to_db()
                        self.log(modem_log_model)
                        
                        continue 

                if filters != None and len(filters) > 0:
                    ip_match_found = False
                    for filter in filters:                        
                        if filter.type == 'ip' and filter.value and new_ip.startswith(filter.value.strip()):
                            done = True
                            ip_match_found = True
                        
                    if ip_match_found == False:
                        modem_log_model = ModemLogModel(
                            modem_id=self.modem().id, 
                            owner=ModemLogOwner.SYSTEM, 
                            type=ModemLogType.WARNING, 
                            message='app.log.modem.rotate.ip.new.filter_not_match',
                            params={
                                'ipv4': new_ip,
                                'filters': ProxyUserIPFilterModel.schema().dump(filters, many=True)
                            },
                            logged_at = datetime.now()
                        )
                        modem_log_model.save_to_db()
                        self.log(modem_log_model)
                        
                        continue
                else:
                    done = True
            
                if done == True:
                    if proxy_user_id:
                        proxy_user_ip_history_model = ProxyUserIPHistoryModel(proxy_user_id = proxy_user_id, modem_ip_history_id = modem_ip_history.id)
                        proxy_user_ip_history_model.save_to_db()

                    self.resolve_connectivity()
                    
                    modem_log_model = ModemLogModel(
                        modem_id=self.modem().id, 
                        owner=ModemLogOwner.SYSTEM, 
                        type=ModemLogType.SUCCESS, 
                        message='app.log.modem.rotate.done.success',
                        logged_at = datetime.now(),
                        params={
                            'ipv4': new_ip,                        
                            'network_type': network_type,
                            'network_provider': network_provider,
                            'signalbar': signalbar
                        },
                    )
                    modem_log_model.save_to_db()
                    self.log(modem_log_model)

                    break

            elif new_ip != None and new_ip == old_ip:
                not_changed_count = not_changed_count + 1

                if not_changed_count < not_changed_try_count:
                    modem_log_model = ModemLogModel(
                        modem_id=self.modem().id, 
                        owner=ModemLogOwner.SYSTEM, 
                        type=ModemLogType.WARNING, 
                        message='app.log.modem.rotate.ip.new.not_change',
                        params={
                            'ipv4': new_ip
                        },
                        logged_at = datetime.now()
                    )
                    modem_log_model.save_to_db()
                    self.log(modem_log_model)

            elif new_ip == None:
                not_ip_count = not_ip_count + 1
                
                if not_ip_count < not_ip_try_count:
                    modem_log_model = ModemLogModel(
                        modem_id=self.modem().id, 
                        owner=ModemLogOwner.SYSTEM, 
                        type=ModemLogType.WARNING, 
                        message='app.log.modem.rotate.ip.new.not_valid',
                        params={
                            'ipv4': new_ip
                        },
                        logged_at = datetime.now()
                    )
                    modem_log_model.save_to_db()
                    self.log(modem_log_model)

            if not_changed_count >= not_changed_try_count:               
                modem_log_model = ModemLogModel(
                    modem_id=self.modem().id, 
                    owner=ModemLogOwner.SYSTEM, 
                    type=ModemLogType.ERROR, 
                    message='app.log.modem.rotate.stop.ip.not_change',
                    params={
                        'times': not_changed_try_count,
                        'ipv4': new_ip,                        
                        'network_type': network_type,
                        'network_provider': network_provider,
                        'signalbar': signalbar
                    },
                    code=Error.NOT_CHANGED_IP_TRY_COUNT_EXCEEDED.value,
                    logged_at = datetime.now()
                )
                modem_log_model.save_to_db()
                self.log(modem_log_model)

                break

            if not_ip_count >= not_ip_try_count:
                modem_log_model = ModemLogModel(
                    modem_id=self.modem().id, 
                    owner=ModemLogOwner.SYSTEM, 
                    type=ModemLogType.ERROR, 
                    message='app.log.modem.rotate.stop.ip.not_valid',
                    params={
                        'times': not_ip_try_count,
                        'ipv4': new_ip,     
                        'network_type': network_type,
                        'network_provider': network_provider,
                        'signalbar': signalbar                   
                    },
                    code=Error.NO_IP_TRY_COUNT_EXCEEDED.value,
                    logged_at = datetime.now()
                )
                modem_log_model.save_to_db()
                self.log(modem_log_model)

                break

            if self.event_stop_is_set() == True: break
            # time.sleep(1)

    def external_ip_through_device(self, timeout=60):
        device_middleware = self.get_device_middleware()
        if device_middleware == None: return None
        return device_middleware.wan.try_get_current_ip(timeout = timeout)

    def external_ip_through_proxy(self):
        proxies = { 
              "http" : 'http://{0}:{1}'.format('127.0.0.1', self.server_modem_model.proxy_ipv4_http_port), 
              "https": 'https://{0}:{1}'.format('127.0.0.1', self.server_modem_model.proxy_ipv4_http_port), 
        }

        r = requests.get('https://ipecho.net/plain', headers=None, proxies=proxies, timeout=3)
        return r.text
    
    def is_connected(self):
        inframodem_iface = self.iface()
        return True if inframodem_iface != None else False

    def ussd(self):
        """Send USSD to SIM card.
        """
        pass

    def install(self):
        pass

    def uninstall(self):
        pass