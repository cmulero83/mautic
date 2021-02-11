#########
# Pruebas de conexion a Mautic
########################

import base64

import urllib.request as urllib2
import json

import sys
import os
import hashlib

import datetime

os.system('clear')



def main():

    ### Credencial para la cabecera de autentificacion de Mautic...

    user = 'Admin:9yCMiVYry8ZpXxT%'
    encodedBytes = base64.b64encode(user.encode("utf-8"))
    autentificacion = str(encodedBytes, "utf-8")

    ##### - Funcionando
    # Listar contactos
    ######

    req = urllib2.Request('http://mautic.mailshield.com.mx/api/contacts')
    req.add_header('Authorization','Basic QWRtaW46OXlDTWlWWXJ5OFpwWHhUJQ==')
    resp = urllib2.urlopen(req)

    if resp.status == 200:
        
        ### Vamos a parserar la respuesta...
        raw_data = resp.read()
        data = json.loads(raw_data.decode("utf-8"))
        nTotal = data['total']
        print(str(datetime.datetime.now()) + nTotal)
        print(data['contacts']['95'])

        




    ######### - Funcionando
    # Crear contacto
    #############

    url = 'https://mautic.mailshield.com.mx/api/contacts/new?'
    parametros = 'firstname="testeandonombre"&lastname="testeandoapellido"&email="test1dddd45071@test.es"&Country="Spain"'
    cadena_bynary = parametros.encode()

    req = urllib2.Request(url)
    req.add_header('Authorization','Basic QWRtaW46OXlDTWlWWXJ5OFpwWHhUJQ==')
    resp = urllib2.urlopen(req, data=cadena_bynary)

    if resp.status == 201:

        print(str(datetime.datetime.now()) + ':Se añadio registro')
        
        ### Vamos a parserar la respuesta...
        raw_data = resp.read()
        data = json.loads(raw_data.decode("utf-8"))

        print(data['contact']['id'])
        print(data['contact']['fields'])
        print(data['contact']['fields']['all']['firstname'])
        print(data['contact']['fields']['all']['lastname'])
        print(data['contact']['fields']['all']['country'])


    else:
        print(str(datetime.datetime.now()) + ': No se pudo añadir...')



















if __name__ == "__main__":
    main()












