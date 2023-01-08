#!/bin/python3

import shodan
import time
import requests
import sys
from termcolor import colored

print(colored("  ______  _____ _____   _____ ______          _____   _____ _    _",'cyan'))
print(colored(" |  ____|/ ____|  __ \ / ____|  ____|   /\   |  __ \ / ____| |  | |",'cyan'))
print(colored(" | |__  | (___ | |__) | (___ | |__     /  \  | |__) | |    | |__| |",'cyan'))
print(colored(" |  __|  \___ \|  ___/ \___ \|  __|   / /\ \ |  _  /| |    |  __  |",'cyan'))
print(colored(" | |____ ____) | |     ____) | |____ / ____ \| | \ \| |____| |  | |",'cyan'))
print(colored(" |______|_____/|_|    |_____/|______/_/    \_\_|  \_\ _____|_|  |_|\n",'cyan'))
print(colored("Este script utiliza la API de shodan para la búsqueda de dispositivos ESP8266 dentro de internet por lo que es necesario que tengas una API gratuita o de preferencia de pago desde shodan, si no tienes una cuenta, la puedes crear gratuitamente desde https://shodan.io/\n",'magenta'))
API=input(colored('Para conocer tu API, ingresa a la url https://account.shodan.io/ \nIngresa tu API: ','white'))

api_shodan=shodan.Shodan(API)
query1 = 'server: esp8266'
query2 = 'server: esp32'
query3 = 'server: arduino'

def request(ip, port):
    try:
        url=("http://"+ip)
        url1=(url+':'+port)
        request=requests.get(url1,timeout=0.5)
        print("\nIP [" + ip + "]")
        print(colored("[+]",'green'),colored(url1,'green'))
        respond_code=request.status_code
        if respond_code != 200:
            print(colored("[!] HTTP STATUS",'yellow') ,colored(request.status_code,'yellow'))
    except requests.exceptions.Timeout as error_time:
        #print(error_time)
        pass
    except requests.exceptions.RequestException as error_req:
        #print(error_req)
        pass

try:
    query_input=input('\nEscoge entre estas dos opciones de dispositivo ESP para realizar la búsqueda:\n\n 1)ESP8266\n 2)ESP32\n 3)Arduino \n\nOpción:')
    if query_input in ['1']:
        query=query1
    elif query_input in ['2']:
        query=query2
    elif query_input in ['3']:
        query=query3
    else:
        print(colored('Error: Valor incorrecto, digita el número 1 o 2','red'))
        sys.exit(1)
    results = api_shodan.search(query)
    print('Parámetro de búsqueda [',query,']')
    time.sleep(3)
    print('\nResultados encontrados: {}'.format(results['total']))
    show=input('¿Comprobar las direcciones IP encontradas? SI/NO:')
    
    if show in ['si', 'SI', 'sI', 'Si',]:
        for result in results['matches']:
            ip=(format(result['ip_str']))
            port=(format(result['port']))
            request(ip, port)
except shodan.APIError as e:
    print(colored('Error: {}'.format(e),'red'))
    sys.exit(1)
