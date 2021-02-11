###########################################################################################################
#
# Pruebas API con MAUTIC
#
###########################################################################################################


from requests_oauthlib import OAuth1Session

from urllib.parse import urlencode
from urllib.request import urlopen
import urllib.parse

from urllib.request import *

import json
import hashlib
import time



CONSUMER_KEY = '6658i0kmwvocowggk40wo4484skwkggkgooogwowggskwso0k0'
CONSUMER_SECRET = '13vff1j1mduoog0wwgg88k4ws8ow08o4co0o40408w4080c0kg'

oauthRequest = OAuth1Session(CONSUMER_KEY,
                    client_secret=CONSUMER_SECRET)

url = 'https://mautic.mailshield.com.mx/oauth/v1/request_token'

headers = {
        'Accept': "application/json",
        'Accept-Encoding': "gzip, deflate",
    }

r = oauthRequest.get(url, headers=headers)

if r.status_code == 200:


    #### Vamos a sacar de la cadena que nos devuelve, unicamente el valor : oauth_token, el cual vamos a usar en la autirzacion
    ### El split va a devolver un array, el cual dividimos 1 vez.

    texto = str(r.content)
    x = texto.split("&", 1)
    oauth_token = x[0][14:]

    print(oauth_token)

    #### Paso 2 Authorization

    url = 'https://mautic.mailshield.com.mx/oauth/v1/authorize?'
    parametros = 'oauth_token=' + oauth_token
    cadena_bynary = parametros.encode()


    AutorizeResponse = urlopen(url, data = cadena_bynary)

    if AutorizeResponse.status == 200:

        raw_data = AutorizeResponse.read()

        ### Vamos a comparar que nos la respuesta incluye el mismo valor qeu pasamos en la peticion
        ###########################################################################################

        texto = str(raw_data)
        x = texto.split("&",1)
        out_request = x[0][15:]

        #### Vamos a obtener el oauth_verifier
        #######################################

        posicion_final = len(x[1]) - 1
        oauth_verifier = x[1][15:posicion_final]

        print(oauth_verifier)


        if out_request == oauth_token:
            print('exito')

            #### Vamos al paso 3 - Obtener el Access Token
            ###############################################

            oauthRequest = OAuth1Session(CONSUMER_KEY,
                    client_secret=CONSUMER_SECRET,
                    )

            url = ' '
    
            headers = {
            'Accept': "application/json",
            'Accept-Encoding': "gzip, deflate",
            'oauth_consumer_key': "6658i0kmwvocowggk40wo4484skwkggkgooogwowggskwso0k0",
            'oauth_nonce':'',
            'oauth_signature':"GENERATED_REQUEST_SIGNATURE",
            'oauth_signature_method':"HMAC-SHA1",
            'oauth_timestamp':"1318467427",
            'oauth_version':"1.0"
            }

            r = oauthRequest.get(url, headers=headers)

            print(r)



        else:
            print('Fallo el Autorize')



        







