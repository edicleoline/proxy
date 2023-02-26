Git para o "firmware" do equipamento.

Neste documento, vou tratar como "equipamento" o composto por Raspberry, expandor I/O (PCF8574), módulo relay, hub USB e fontes de alimentação.

A solução é cada equipamento estar preparado para servir como servidor de proxy 4G.
A firmware é uma biblioteca escrita em Python, capaz de gerenciar o equipamento e disponibilizar uma API capaz de ser consumida por um segundo servidor, o principal, que gerenciará todos os equipamentos da rede.

Perceba que não há um banco de dados instalado em cada equipamento. O banco de dados, em MySQL, ficará "hospedado no servidor principal".

No diretório principal, o arquivo server-farm.py, preparado para gerenciar um modem específico - desde o ligamento/desligamento da porta USB, gerenciamento da interface, rotas, porta de proxy, teste de conexão, teste de conexão de proxy, identificação de problemas, solução de problemas e outros:


usage: server-farm.py [-h] --modem MODEM_ID (--diagnose | --rotate | --usb-reboot | --info) [--hard-reset] [--user USER] [--match IP_MATCH]


optional arguments:
  -h, --help        show this help message and exit
  --modem MODEM_ID  Modem ID
  --diagnose        Execute diagnose
  --rotate          Rotate IPv4
  --usb-reboot      Reboot USB
  --info            Show details about modem, connection and proxy
  --hard-reset      Use USB hard reset
  --user USER       User email
  --match IP_MATCH  IPv4 match

--modem: Recebe obrigatoriamente o ID do modem
--diagnose: Realiza um diagnóstico e resolve problemas de conexão, interface, rotas, proxy e outros problemas
--rotate: Rotaciona o IP
  --hard-reset: Rotaciona o IP desligando e ligando a porta USB
  Sem a opção --hard-reset ativada, o modem não é reiniciado. Em vez disso, a biblioteca acessa o firmware do modem, desconecta o modem da rede da operadora, e liga novamente, solicitando um novo IP. Funcionou bem por algum tempo, mas as operadoras começaram e devolver o mesmo IP.
--usb-reboot: Eeinicia a USB (desliga, aguarda 1s e liga)  
--info: Retorna informações sobre o estado do modem (ligado/desligado), a interface atribuída pelo Sistema Operacional, detalhes como IP, gateway, máscara, cálculo de tráfego de dados e outros, operadora, tipo de rede atual conectada (4G, 3G, 2G, limitado, desconectado), nível do sinal com a operadora, conexão com o proxy, porta do proxy, e outros
--user: Utilizado com a opção --rotate, atribui o IP rotacionado a um usuário específico. Solução para gerenciar quantos usuários utilizam o mesmo IP, se compartilhado, ou certificar de que seja utilizado exclusivamente a um usuário, se dedicado.
--math: O rotacionamento é interrompido quando o IP adquirido "casa" com o valor informado. Por exemplo, se informado "177", o rotacionamento será interrompido quando adquirir o IP "177.25.10.100", mas continuará rotacionando se receber o IP 178.X.X.X - ou se o IP adquirido já estiver sendo utilizado exclusivamente por usuário.
