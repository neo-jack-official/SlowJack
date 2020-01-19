![alt text](https://raw.githubusercontent.com/neo-jack-official/SlowJack/master/Imagenes/Vista01.png)
![alt text](https://raw.githubusercontent.com/neo-jack-official/SlowJack/master/Imagenes/vista02.png)
# slowjack.py - SlowJack es un remake (nueva version) de SlowLoris, re editado por Neo-Jack DIC/2019
# ULTIMA ACTUALIZACION ---> ENE/2020
## ¿Qué es slowjack?
Es un testeador de denegación de servicio HTTP que afecta a servidores enhebrados.

## ¿Como funciona?
1. Realiza muchas peticiones HTTP, por medio de clientes pre asignados.(defecto: 150, recomendado de 100 a 200)
2. se envian encabezados periódicamente (cada ~ 15 seg.) para mantener las conexiones abiertas.(defecto: 15 seg, recomendado de 10 a 15 seg)
3. Nunca se cierra la conexión a menos que el servidor lo haga. Si el servidor cierra una conexión, se crea una nueva (se muestra como "Recrear") y seguimos haciendo lo mismo.

Esto llena el cupo de peticiones del servidor inundandolo y evita que pueda responder a peticiones externas de terceros.

## Seguridad de SlowJack

SlowJack cuenta con un verificador de seguridad para su proteccion.
notificando si esta en una red TOR.

## Problemas con mi red TOR.
# Tengo red TOR y SlowJack no la encuentra.
Cuando usted inicia SlowJack, se le informara su IP-HOST, Usualmente es 12.0.0.1.
Si su red TOR corre bajo el mismo IP-HOST, no tendra problemas.
Si su IP-HOST es distinta a 12.0.0.1
.
![alt text](https://raw.githubusercontent.com/neo-jack-official/SlowJack/master/Imagenes/iphost.png)

	1) Abra slowjack.py con algun editor de texto
	2) busque la siguiente linea de comandos:
	    * `socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)`
	3) Remplace "127.0.0.1"
	   por la IP-HOST que le muestra SlowJack, cuando lo corre desde terminal.
	4) Guarde SlowJack.py


## Como Instalar y correr PYTHON?

Slowjack es un archivo con extencion "Py", solo requiere tener pre instalado Python.

## Preparamos la instalacion para python

* `sudo apt-get update`
* `sudo apt-get install build-essential checkinstall`
* `sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev`
* `sudo apt-get install python2.7`
* `sudo apt-get install python3.6`

## Revisamos que python esta instalado correctamente

* `python -V | python3 -V`


### Soporte para proxy SOCKS5

Si planea usar la opción `-x` para usar un proxy SOCKS5 para conectarse en lugar de una conexión directa a través de su dirección IP, deberá instalar la biblioteca` PySocks`.
 [`PySocks`] (https://github.com/Anorov/PySocks)
 [` SocksiPy`] (http://socksipy.sourceforge.net/) by GitHub @Anorov y puede ser instalado fácilmente por comando ` pip` 

* `sudo pip3 install PySocks`

Luego puede usar la opción `-x` para activar el soporte SOCKS5 y las opciones` --proxy-host` y `--proxy-port` para especificar el host proxy SOCKS5 y su puerto, si son diferentes del estándar` 127.0.0.1: 8080`.

## Opciones de Configuracion

* `-h = Ayuda`
* `-p = Puerto, por defecto : 80`
* `-s = Clientes, por defecto : 150` recomendacion (entre 100 a 200)
* `-v = Muetsra clientes creados, por defecto : Activado`
* `-ua = Navegadores Aleatorios, por defecto: Activado`
* `-x = Usar SOCKS5 proxy para conectar`
* `--proxy-host = Usar SOCKS5 proxy host`
* `--proxy-port = Usar SOCKS5 proxy port`
* `--https = Usar HTTPS para la peticion`
* `--sleeptime = Tiempo de descanso entre cada envio header. por defecto: 15` recomendado (entre 10 a 15 seg)
* `-T = Habilitar el enrutamiento TOR, por defecto: Desactivado`

## Como lo utilizo?

Si `slowjack.py` esta en Escritorio
1) Abra terminal, Escriba `cd Escritorio`
2) Ejecute bajo Python `python slowjack.py www.ejemplo.com`

## Ejemplos de comandos.

  Cambiando cantidad de Clientes:
Para 180 Clientes
* `python slowjack.py www.ejemplo.com -s 180` 

  Cambiando tiempo de espera entre Headers:
Para reducir tiempo entre Headers a 10 Seg.
* `python slowjack.py www.ejemplo.com --sleeptime 10`

  Combinando comandos:
* `python slowjack.py www.ejemplo.com -s 180 --sleeptime 10`

  Activando Tor:
* `python slowjack.py www.ejemplo.com -T`


