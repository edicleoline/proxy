class Settings():
    def __init__(self):
        self.external_ip_before_rotate_timeout = 10
        self.external_ip_after_rotate_timeout = 30
        self.modem_status_external_ip_interval = 30
        self.modem_status_external_ip_timeout = 5
        self.wait_until_modem_connection_timeout = 60
        self.external_ip_url = 'https://ipecho.net/plain'
        # self.external_ip_url = 'https://api.ipify.org/'