import time
from typing import List
import requests
from threading import Event
from framework.error.exception import TimeoutException
from framework.manager.subscriber import ModemManagerSubscriber, ModemManagerSubscriberEvent
from framework.middleware.factory import MiddlewareFactory
from framework.models.modemdiagnose import ModemDiagnoseModel, ModemDiagnoseOwner, ModemDiagnoseType
from framework.models.modemthreadtask import TaskWizard, TaskWizardStep, TaskWizardStepType
from framework.models.iplabelfilter import IpLabelFilterModel
from framework.models.server import ServerModemModel
from framework.models.modemiphistory import ModemIpHistoryModel
from framework.models.iplabelhistory import IpLabelHistoryModel
from framework.models.modemlog import ModemLogModel, ModemLogOwner, ModemLogType
from framework.infra.netiface import NetIface
from framework.infra.usb import USB
from framework.infra.route import Route
from enum import Enum
from framework.proxy.factory import ProxyService
from framework.settings import Settings
from framework.util.wan import Wan
from datetime import datetime, timedelta

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
            callback = None,
            settings = None
    ):
        self.server_modem_model = server_modem_model   
        self.proxy_service = proxy_service     
        self.event_stop = event_stop
        self.callback = callback
        self._modem = None
        self._usb_port = None
        self.settings = settings


    def modem(self):
        if not self._modem: self._modem = self.server_modem_model.modem
        return self._modem

    def usb_port(self):
        if not self._usb_port: self._usb_port = self.server_modem_model.usb
        return self._usb_port

    def iface(self):
        addr_id = self.modem().addr_id
        return NetIface.get_iface_by_addr_id(addr_id)        

    def hard_reboot(self):
        USB(server=self.server_modem_model.server()).hard_reboot(usb_port=self.usb_port())

    def hard_turn_off(self):
        USB(server=self.server_modem_model.server()).hard_turn_off(usb_port=self.usb_port())

    def wan(self):
        iface = self.iface()
        if iface == None or iface.ifaddresses == None: return None
        return Wan(settings = self.settings, interface = iface.interface)

    def get_device_middleware(self):            
        params_transformed = {}
        params = self.server_modem_model.modem.device.middleware.params
        if params:
            for param in params: params_transformed[param.name] = param.value
        
        middleware_factory = MiddlewareFactory(
            middleware = self.modem().device.middleware,
            params = params_transformed,
            iface = self.iface(),
            settings = self.settings
        )
        middleware_instance = middleware_factory.instance()
        return middleware_instance

    def wait_until_modem_connection(self, timeout = 60):
        timeout_at = datetime.now() + timedelta(seconds = timeout)
        while(True):
            if self.event_stop_is_set(log = False): break

            inframodem_iface = self.iface()
            if inframodem_iface != None: break

            diff_timeout_now = int((datetime.now() - timeout_at).total_seconds())
            if diff_timeout_now >= timeout:
                raise TimeoutException('Timeout exception')

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

    # def resolve_proxy(self):
    #     if self.proxy_service: self.proxy_service.resolve()

    def resolve_route(self):
        inframodem_iface = self.iface()
        modem_ifaddress = inframodem_iface.ifaddresses[0]
        modem_gateway = NetIface.get_gateway_from_ipv4(ipv4 = modem_ifaddress['addr'])        
        route = Route(gateway=modem_gateway, interface=inframodem_iface.interface, ip=modem_ifaddress['addr'], table=self.modem().id)
        route.resolve_route()        

    def resolve_connectivity(self):
        # self.resolve_proxy()
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

        try:
            self.wait_until_modem_connection(self.settings.wait_until_modem_connection_timeout)
        except TimeoutException:
            modem_log_model = ModemLogModel(
                modem_id=self.modem().id, 
                owner=ModemLogOwner.SYSTEM, 
                type=ModemLogType.ERROR, 
                message='app.log.modem.reboot.error.connection.timeout',
                params={
                    'timeout': self.settings.wait_until_modem_connection_timeout
                }
            )
            modem_log_model.save_to_db()
            self.log(modem_log_model)
            return False
        
        return True
    
    def _diagnose_interfaces(self):
        ifaces = NetIface.get_all()
        interfaces = []
        for iface in ifaces:
            interfaces.append({
                'iface': iface.interface,
                'ifaddresses': iface.ifaddresses
            })

        return {
            'interfaces': interfaces
        }
    
    def wizard_wait_response(self, step: TaskWizardStep, data_callback = None):
        while True:
            if data_callback: step.data = data_callback()
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
            response = self.wizard_wait_response(step = step_list_interfaces, data_callback = lambda: self._diagnose_interfaces())

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
        ip_label_model = None,
        hard_reset = False, 
        not_changed_try_count = 3, 
        not_ip_try_count = 3,
        subscribers: List[ModemManagerSubscriber] = []
    ):
        modem_log_model = ModemLogModel(
            modem_id=self.modem().id, 
            owner=ModemLogOwner.SYSTEM, 
            type=ModemLogType.INFO, 
            message='app.log.modem.rotate.starting',
            params={
                'hard_reset': hard_reset,
                'ip_label': ip_label_model.label if ip_label_model else None,
                'filters': IpLabelFilterModel.schema().dump(filters, many=True) if filters else None                
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
                try:
                    old_ip = self.wan().try_get_current_ip(
                        event_stop = self.event_stop,
                        timeout = self.settings.external_ip_before_rotate_timeout if self.settings else 10
                    )
                except Exception: pass
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
                try:
                    new_ip = self.wan().try_get_current_ip(
                        event_stop = self.event_stop, 
                        timeout = self.settings.external_ip_after_rotate_timeout if self.settings else 30
                    )
                except Exception: pass

            else:
                if self.event_stop_is_set() == True: break            
                try:
                    self.wait_until_modem_connection(self.settings.wait_until_modem_connection_timeout)
                except TimeoutException:
                    modem_log_model = ModemLogModel(
                        modem_id=self.modem().id, 
                        owner=ModemLogOwner.SYSTEM, 
                        type=ModemLogType.ERROR, 
                        message='app.log.modem.reboot.error.connection.timeout',
                        params={
                            'timeout': self.settings.wait_until_modem_connection_timeout
                        }
                    )
                    modem_log_model.save_to_db()
                    self.log(modem_log_model)
                    break

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
                
            if self.event_stop_is_set() == True: break   

            modem_details = device_middleware.details()
            network_type = modem_details['network_type'] if modem_details else None
            network_provider = modem_details['network_provider'] if modem_details else None
            signalbar = modem_details['signalbar'] if modem_details else None

            if new_ip != None and new_ip != old_ip:
                modem_ip_history = ModemIpHistoryModel(modem_id = self.modem().id, ip = new_ip, network_type = network_type, network_provider = network_provider, signalbar = signalbar)
                modem_ip_history.save_to_db()

                inframodem_iface = self.iface()
                modem_ifaddress = inframodem_iface.ifaddresses[0]
                modem_gateway = NetIface.get_gateway_from_ipv4(ipv4 = modem_ifaddress['addr'])

                if ip_label_model and self.server_modem_model.prevent_same_ip_users == True:
                    is_ip_reserved_for_other = IpLabelHistoryModel.is_ip_reserved_for_other(ip = new_ip, ip_label_id = ip_label_model.id)

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
                                'filters': IpLabelFilterModel.schema().dump(filters, many=True)
                            },
                            logged_at = datetime.now()
                        )
                        modem_log_model.save_to_db()
                        self.log(modem_log_model)
                        
                        continue
                else:
                    done = True
            
                if done == True:
                    if ip_label_model:
                        proxy_user_ip_history_model = IpLabelHistoryModel(ip_label_id = ip_label_model.id, modem_ip_history_id = modem_ip_history.id)
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

                    ModemManagerSubscriber.notify(subscribers, ModemManagerSubscriberEvent.ON_ROTATE_SUCCESS, {
                        'modem': {
                            'id': self.server_modem_model.id
                        },
                        'connectivity': {
                            'external_ip': new_ip,
                            'network_type': network_type,
                            'network_provider': network_provider,
                            'signalbar': signalbar
                        }
                    })                    

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

    def external_ip_through_device(self, timeout = 60):
        return self.wan().try_get_current_ip(event_stop = self.event_stop, timeout = timeout)

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