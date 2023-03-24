import sys, time
import requests
from threading import Event
from framework.models.proxyuseripfilter import ProxyUserIPFilterModel

from framework.models.server import ServerModemModel
from framework.models.modemiphistory import ModemIPHistoryModel
from framework.models.proxyuseriphistory import ProxyUserIPHistoryModel
from framework.models.modemlog import ModemLogModel, ModemLogOwner, ModemLogType

from framework.infra.netiface import NetIface
from framework.infra.usb import USB
from framework.infra.route import Route
from framework.infra.proxyservice import ProxyService

from framework.device.zte.mf79s import MF79S
from framework.device.zte.error.exception import ConnectException

from datetime import datetime
from enum import Enum

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

class Owner(Enum):
    SYSTEM  = 1
    USER    = 2

class Modem:
    def __init__(self, server_modem_model: ServerModemModel, callback = None):
        self.server_modem_model = server_modem_model
        self.modem = self.server_modem_model.modem()
        self.usb_port = server_modem_model.usb_port()
        self.callback = callback

    def iface(self):
        addr_id = self.modem.addr_id
        return NetIface.get_iface_by_addr_id(addr_id)        

    def hard_reboot(self):
        """Reboot USB port by cut power.       
        """                
        sys.stdout.write('{0}[!] Let''s reboot USB port {1}...{2}'.format(CYELLOW, self.usb_port.port, CEND))
        sys.stdout.flush()
        USB(server=self.server_modem_model.server()).hard_reboot(usb_port=self.usb_port)
        sys.stdout.write('{0} OK{1}\n'.format(CGREEN, CEND))
        sys.stdout.flush()

    def hard_reboot_and_wait(self):
        self.hard_reboot()
        self.wait_until_modem_connection(print_alert = False)

    def hard_turn_off(self):
        """Turn off USB port.
        """        
        sys.stdout.write('{0}[!] Let''s turn off USB port {1}...{2}'.format(CYELLOW, self.usb_port.port, CEND))
        sys.stdout.flush()
        USB(server=self.server_modem_model.server()).hard_turn_off(usb_port=self.usb_port)
        sys.stdout.write('{0} OK{1}\n'.format(CGREEN, CEND))
        sys.stdout.flush()

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
                middleware = MF79S(addr_id = self.modem.addr_id, interface = iface.interface, gateway = gateway, password = 'vivo', retries_ip = retries_ip)

        return middleware

    def wait_until_modem_connection(self, print_alert = False):
        write_alert = True
        while(True):
            inframodem_iface = self.iface()

            if inframodem_iface != None:
                break
            else:
                if print_alert and write_alert:
                    sys.stdout.write('{0}[!] This modem is offline. Let''s wait until get online back...{1}\n'.format(CRED, CEND))
                    sys.stdout.flush()

            write_alert = False
            time.sleep(1)

    def event_stop_is_set(self, event_stop: Event):
        if event_stop and event_stop.is_set():
            modem_log_model = ModemLogModel(
                modem_id=self.modem.id, 
                owner=ModemLogOwner.SYSTEM, 
                type=ModemLogType.WARNING, 
                message='Processo interrompido pelo usuário'
            )
            modem_log_model.save_to_db()
            self.log(modem_log_model)
            return True
        else:
            return False

    def log(self, log: ModemLogModel):
        if self.callback: self.callback(log)

    def rotate(
            self, 
            filters = None, 
            proxy_user_id = None, 
            proxy_username = None,
            hard_reset = False, 
            not_changed_try_count = 3, 
            not_ip_try_count = 3, 
            event_stop: Event = None):

        modem_log_model = ModemLogModel(
            modem_id=self.modem.id, 
            owner=ModemLogOwner.SYSTEM, 
            type=ModemLogType.INFO, 
            message='app.log.modem.rotate.starting',
            params={
                'filters': ProxyUserIPFilterModel.schema().dump(filters, many=True) if filters else None,
                'hard_reset': hard_reset,
                'proxy_username': proxy_username
            },
            logged_at = datetime.now()
        )
        modem_log_model.save_to_db()
        self.log(modem_log_model)

        device_middleware, not_changed_count, not_ip_count = None, 0, 0

        while True:
            old_ip, new_ip, done = None, None, False

            modem_log_model = ModemLogModel(
                modem_id=self.modem.id, 
                owner=ModemLogOwner.SYSTEM, 
                type=ModemLogType.INFO, 
                message='Iniciando middleware',
                logged_at = datetime.now()              
            )
            modem_log_model.save_to_db()
            self.log(modem_log_model)

            device_middleware = self.get_device_middleware()
            if device_middleware:
                old_ip = device_middleware.wan.try_get_current_ip(retries=2)
            else:
                modem_log_model = ModemLogModel(
                    modem_id=self.modem.id, 
                    owner=ModemLogOwner.SYSTEM, 
                    type=ModemLogType.ERROR, 
                    message='Middleware não encontrado',
                    code=Error.MIDDLEWARE_NOT_FOUND.value,
                    logged_at = datetime.now()
                )
                modem_log_model.save_to_db()
                self.log(modem_log_model)
                break
        
            if hard_reset == True:
                self.hard_reboot()

                modem_log_model = ModemLogModel(
                    modem_id=self.modem.id, 
                    owner=ModemLogOwner.SYSTEM, 
                    type=ModemLogType.INFO, 
                    message='Porta USB reiniciada. Aguardando modem', 
                    params={
                        'usb_port': self.usb_port.port
                    },
                    logged_at = datetime.now()
                )
                modem_log_model.save_to_db()
                self.log(modem_log_model)

                #verificar event thread cancel neste metodo, pois chegou a travar
                self.wait_until_modem_connection(False)

                if self.event_stop_is_set(event_stop) == True: break

                modem_log_model = ModemLogModel(
                    modem_id=self.modem.id, 
                    owner=ModemLogOwner.SYSTEM, 
                    type=ModemLogType.INFO, 
                    message='Modem reiniciado. Aguardando conexão com a operadora',
                    logged_at = datetime.now()
                )
                modem_log_model.save_to_db()
                self.log(modem_log_model)

                time.sleep(30)

                self.wait_until_modem_connection(True)
                
                device_middleware = self.get_device_middleware()
                new_ip = device_middleware.wan.try_get_current_ip(retries=30)

            else:
                if self.event_stop_is_set(event_stop) == True: break            
                self.wait_until_modem_connection(True)                                
                if self.event_stop_is_set(event_stop) == True: break                            
                device_middleware = self.get_device_middleware()

                modem_log_model = ModemLogModel(
                    modem_id=self.modem.id, 
                    owner=ModemLogOwner.SYSTEM, 
                    type=ModemLogType.INFO, 
                    message='Reiniciando conexão com a operadora usando middleware',
                    logged_at = datetime.now()             
                )
                modem_log_model.save_to_db()
                self.log(modem_log_model)

                try:                    
                    new_ip = device_middleware.release()
                except ConnectException as e:
                    modem_log_model = ModemLogModel(
                        modem_id=self.modem.id, 
                        owner=ModemLogOwner.SYSTEM, 
                        type=ModemLogType.ERROR, 
                        message='Erro ao reiniciar conexão com a operadora usando middleware',
                        code=Error.MIDDLEWARE_IP_RELEASE_FAIL.value,
                        logged_at = datetime.now()
                    )
                    modem_log_model.save_to_db()
                    self.log(modem_log_model)
                    break

                # new_ip = '189.40.89.35' #TESTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT  
                
            if self.event_stop_is_set(event_stop) == True: break              

            if new_ip != None and new_ip != old_ip:
                modem_log_model = ModemLogModel(
                    modem_id=self.modem.id, 
                    owner=ModemLogOwner.SYSTEM, 
                    type=ModemLogType.INFO, 
                    message='Novo IP recebido com sucesso',
                    params={
                        'ipv4': new_ip
                    },
                    logged_at = datetime.now()
                )
                modem_log_model.save_to_db()
                self.log(modem_log_model)

                modem_details = device_middleware.details()
                network_type = modem_details['network_type'] if modem_details else None
                network_provider = modem_details['network_provider'] if modem_details else None
                signalbar = modem_details['signalbar'] if modem_details else None

                modem_ip_history = ModemIPHistoryModel(modem_id = self.modem.id, ip = new_ip, network_type = network_type, network_provider = network_provider, signalbar = signalbar)
                modem_ip_history.save_to_db()

                inframodem_iface = self.iface()
                modem_ifaddress = inframodem_iface.ifaddresses[0]
                modem_gateway = NetIface.get_gateway_from_ipv4(ipv4 = modem_ifaddress['addr'])

                if proxy_user_id:
                    is_ip_reserved_for_other = ProxyUserIPHistoryModel.is_ip_reserved_for_other(ip=new_ip, proxy_user_id=proxy_user_id)

                    if self.event_stop_is_set(event_stop) == True: break

                    if is_ip_reserved_for_other:
                        modem_log_model = ModemLogModel(
                            modem_id=self.modem.id, 
                            owner=ModemLogOwner.SYSTEM, 
                            type=ModemLogType.INFO, 
                            message='Vamos rotacionar novamente porque este IP está reservado para outro usuário',
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
                        if filter.type == 'ip' and new_ip.startswith(filter.value.strip()):
                            done = True
                            ip_match_found = True
                        
                    if ip_match_found == False:
                        modem_log_model = ModemLogModel(
                            modem_id=self.modem.id, 
                            owner=ModemLogOwner.SYSTEM, 
                            type=ModemLogType.INFO, 
                            message='Vamos rotacionar novamente porque este IP não combina com nenhum filtro fornecido',
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

                    proxyService = ProxyService(ip=modem_ifaddress['addr'], proxy_ipv4_http_port=self.server_modem_model.proxy_ipv4_http_port)
                    proxyService.resolve_proxy()

                    route = Route(gateway=modem_gateway, interface=inframodem_iface.interface, ip=modem_ifaddress['addr'], table=self.modem.id)
                    route.resolve_route()

                    break

            elif (new_ip != None and new_ip == old_ip) and (not_changed_count < not_changed_try_count):
                not_changed_count = not_changed_count + 1

                modem_log_model = ModemLogModel(
                    modem_id=self.modem.id, 
                    owner=ModemLogOwner.SYSTEM, 
                    type=ModemLogType.WARNING, 
                    message='Vamos rotacionar novamente porque o IP recebido pela operadora não foi alterado',
                    params={
                        'ipv4': new_ip
                    },
                    logged_at = datetime.now()
                )
                modem_log_model.save_to_db()
                self.log(modem_log_model)

            elif (not_ip_count < not_ip_try_count) and new_ip == None:
                not_ip_count = not_ip_count + 1
                
                modem_log_model = ModemLogModel(
                    modem_id=self.modem.id, 
                    owner=ModemLogOwner.SYSTEM, 
                    type=ModemLogType.WARNING, 
                    message='Vamos rotacionar novamente porque não conseguimos receber um IP válido',
                    params={
                        'ipv4': new_ip
                    },
                    logged_at = datetime.now()
                )
                modem_log_model.save_to_db()
                self.log(modem_log_model)

            if not_changed_count >= not_changed_try_count:
                modem_details = device_middleware.details()
                network_type = modem_details['network_type'] if modem_details else None
                network_provider = modem_details['network_provider'] if modem_details else None
                signalbar = modem_details['signalbar'] if modem_details else None

                modem_log_model = ModemLogModel(
                    modem_id=self.modem.id, 
                    owner=ModemLogOwner.SYSTEM, 
                    type=ModemLogType.ERROR, 
                    message='Interrompemos a tarefa porque depois de algumas tentativas a operadora insiste atribuir o mesmo IP para este modem',
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
                    modem_id=self.modem.id, 
                    owner=ModemLogOwner.SYSTEM, 
                    type=ModemLogType.ERROR, 
                    message='Interrompemos a tarefa porque depois de algumas tentativas não conseguimos receber um IP válido. Verifique seu plano de dados',
                    params={
                        'ipv4': new_ip,
                        'times': not_ip_try_count
                    },
                    code=Error.NO_IP_TRY_COUNT_EXCEEDED.value,
                    logged_at = datetime.now()
                )
                modem_log_model.save_to_db()
                self.log(modem_log_model)

                break

            if self.event_stop_is_set(event_stop) == True: break
            # time.sleep(1)

    def external_ip_through_device(self, silence_mode = False, retries=2):
        device_middleware = self.get_device_middleware()
        if device_middleware == None:
            return None
        return device_middleware.wan.try_get_current_ip(retries=retries, silence_mode=silence_mode)

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