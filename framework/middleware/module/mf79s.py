import requests
import time
import sys
import base64
import json
import sys
from framework.error.exception import MiddlewareAuthenticationException, MiddlewareCarrierConnectionException, MiddlewareException
from framework.infra.netiface import NetIface
from framework.settings import Settings

sys.path.append('..')
from framework.util.wan import Wan

class MF79S:
    def __init__(self, iface: NetIface, params: dict, settings: Settings):
        self.iface = iface
        self.params = params
        self.settings = settings
        self.wan = Wan(settings = settings, interface = iface.interface)
        self.session = requests.Session()

    @property
    def password(self):
        return base64.b64encode(str(self.params['password']).encode("utf-8"))
    
    @property
    def gateway(self):
        ifaddress = self.iface.ifaddresses[0]
        return NetIface.get_gateway_from_ipv4(ipv4 = ifaddress['addr'])
    
    @property
    def is_interface_connected(self):        
        return NetIface.get_iface_by_addr_id(self.gateway) != None

    def login(self):
        try:
            payload = { 'isTest': 'false', 'goformId': 'LOGIN', 'password': self.password }
            header = { 
                'Accept': 'application/json, text/javascript, */*; q=0.01', 
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en',
                'Connection': 'keep-alive',
                'Content-Length': '49',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
                'host': self.gateway, 
                'Origin': 'http://{ip}'.format(**{'ip': self.gateway}), 
                'Referer': 'http://{ip}/index.html'.format(**{'ip': self.gateway}),                                 
                'Sec-GPC': '1',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }
            r = requests.post('http://{ip}/goform/goform_set_cmd_process'.format(**{'ip': self.gateway}), headers=header, data=payload, timeout=5)
            resp = json.loads(r.text)            
            if resp['result'] == '0':
                return True
            else:
                raise MiddlewareAuthenticationException('Invalid password')
        except Exception as e:
            raise MiddlewareAuthenticationException(str(e))

    def disconnect(self):
        try:
            payload = { 'isTest': 'false', 'notCallback': 'true', 'goformId': 'DISCONNECT_NETWORK' }
            header = { 
                'Accept': 'application/json, text/javascript, */*; q=0.01', 
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en',
                'Connection': 'keep-alive',
                'Content-Length': '49',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
                'host': self.gateway, 
                'Origin': 'http://{ip}'.format(**{'ip': self.gateway}), 
                'Referer': 'http://{ip}/index.html'.format(**{'ip': self.gateway}),                                 
                'Sec-GPC': '1',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }
            r = requests.post('http://{ip}/goform/goform_set_cmd_process'.format(**{'ip': self.gateway}), headers=header, data=payload, timeout=15)
            resp = json.loads(r.text)  
            if resp['result'] == 'success':
                return True
            else:
                return False
        except:
            return False

    def connect(self):
        try:
            payload = { 'isTest': 'false', 'notCallback': 'true', 'goformId': 'CONNECT_NETWORK' }
            header = { 
                'Accept': 'application/json, text/javascript, */*; q=0.01', 
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en',
                'Connection': 'keep-alive',
                'Content-Length': '49',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
                'host': self.gateway, 
                'Origin': 'http://{ip}'.format(**{'ip': self.gateway}), 
                'Referer': 'http://{ip}/index.html'.format(**{'ip': self.gateway}),                                  
                'Sec-GPC': '1',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }
            r = requests.post('http://{ip}/goform/goform_set_cmd_process'.format(**{'ip': self.gateway}), headers=header, data=payload, timeout=15)
            resp = json.loads(r.text)            
            if resp['result'] == 'success':
                return True
            else:
                return False
        except:
            return False

    def release(self):        
        if not self.login():
            raise MiddlewareAuthenticationException('You are not authenticated')

        self.disconnect()
        time.sleep(7)

        retry = 0
        connected = False
        while True:          
            retry = retry + 1  
            connected = self.connect()
            if connected == True: break            
            else:
                time.sleep(1)           
                if retry >= 3: break

        if connected == False:
            raise MiddlewareCarrierConnectionException("We could create a connection with carrier")

        time.sleep(5) #TODO: try better solution

        return self.wan.try_get_current_ip(timeout = 30)


    def reboot(self):
        try:
            payload = { 'isTest': 'false', 'goformId': 'REBOOT_DEVICE' }
            header = { 
                'Accept': 'application/json, text/javascript, */*; q=0.01', 
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en',
                'Connection': 'keep-alive',
                'Content-Length': '35',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
                'host': self.gateway, 
                'Origin': 'http://{ip}'.format(**{'ip': self.gateway}), 
                'Referer': 'http://{ip}/index.html'.format(**{'ip': self.gateway}),                                  
                'Sec-GPC': '1',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }
            r = requests.post('http://{ip}/goform/goform_set_cmd_process'.format(**{'ip': self.gateway}), headers=header, data=payload, timeout=15)            
            return True
        except:
            raise MiddlewareException('We could reboot modem')
        
    def reboot_and_wait(self):
        self.reboot()

        while True:            
            if self.is_interface_connected == False: break
            time.sleep(1)

        while True:
            if self.is_interface_connected == True: break
            time.sleep(1)

    def details(self):
        try:
            header = { 
                'Accept': 'application/json, text/javascript, */*; q=0.01', 
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en',
                'Connection': 'keep-alive',
                'Content-Length': '35',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
                'host': self.gateway, 
                'Origin': 'http://{ip}'.format(**{'ip': self.gateway}), 
                'Referer': 'http://{ip}/index.html'.format(**{'ip': self.gateway}),                                  
                'Sec-GPC': '1',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }
            r = requests.get('http://{ip}/goform/goform_get_cmd_process?multi_data=1&isTest=false&sms_received_flag_flag=0&sts_received_flag_flag=0&cmd=modem_main_state%2Cpin_status%2Copms_wan_mode%2Cloginfo%2Cnew_version_state%2Ccurrent_upgrade_state%2Cis_mandatory%2Cwifi_dfs_status%2Cbattery_value%2Csignalbar%2Cnetwork_type%2Cnetwork_provider%2Cppp_status%2CEX_SSID1%2Csta_ip_status%2CEX_wifi_profile%2Cm_ssid_enable%2CRadioOff%2CSSID1%2Csimcard_roam%2Clan_ipaddr%2Cstation_mac%2Cbattery_charging%2Cbattery_vol_percent%2Cbattery_pers%2Cspn_name_data%2Cspn_b1_flag%2Cspn_b2_flag%2Crealtime_tx_bytes%2Crealtime_rx_bytes%2Crealtime_time%2Crealtime_tx_thrpt%2Crealtime_rx_thrpt%2Cmonthly_rx_bytes%2Cmonthly_tx_bytes%2Cmonthly_time%2Cdate_month%2Cdata_volume_limit_switch%2Cdata_volume_limit_size%2Cdata_volume_alert_percent%2Cdata_volume_limit_unit%2Croam_setting_option%2Cupg_roam_switch%2Cssid%2Cwifi_enable%2Cwifi_5g_enable%2Ccheck_web_conflict%2Cdial_mode%2Clac_code%2Csms_received_flag%2Csts_received_flag%2Csms_unread_num&_=1674578158276'.format(**{'ip': self.gateway}), headers=header, timeout=15)            
            resp = json.loads(r.text)

            return {
                'network_type': resp['network_type'],
                'network_provider': resp['network_provider'],
                'signalbar': resp['signalbar']
            }
        except:
            return None
