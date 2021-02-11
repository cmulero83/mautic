
###########
# Se conecta al CRM y nos trae los registros que no estan en Mautic
####################

import base64

import urllib.request as urllib2
import json

import sys
import os
import time

import datetime
import hashlib

from urllib.parse import urlencode
from urllib.request import urlopen
import urllib.parse

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def md5(s):
    return hashlib.md5(s.encode()).hexdigest()


def main():
    
    ####
    ### Vamos a realizar la conexión con el CRM
    ####
    ### Si exito, retorna un array con 0 -> sessionID, 1 -> userId
    session = vtiger_conexion()

    ######################
    # Vamos a buscar en el CRM los registros que no han sido procesados por MAUTIC y que el campo NOMBRE <> Pendiente
    ######################
    filtrar_leads_mautic(session)


def filtrar_leads_mautic(session):


    sessionId = session[0]

    url = 'https://www.mailshield.tech/vtigercrm/webservice.php?'
    #parametros = urllib.parse.quote("select id, website from Leads where website='" + dominio + "';")
    parametros = urllib.parse.quote("select id, firstname, lastname, website, email, cf_852, country, cf_874 from Leads where cf_874=False AND firstname != 'Pendiente' LIMIT 90;")
    test = url +  "operation=query&sessionName=" + sessionId + "&query=" + parametros

    while True:

        try:
            resp = urlopen(test)

            if resp.status == 200:

            ### Comprobamos el exito...
                raw_data = resp.read()
                data = json.loads(raw_data.decode("utf-8"))    
                exito = data['success']


                if exito == True:
                    print(str(datetime.datetime.now()) + ": Retrive Correcto.....")
                    print("Total de registros " + str(len(data['result'])))
                    
                    for i in data['result']:
                        
                        ####### Vamos añadirlo a Mautic
                        ####### Pasamos como parametro la fila que vamos a procesar

                        resp = anadir_mautic(i)
                        
                        if resp == True:
                            print(str(datetime.datetime.now()) + " : " + i['email']+" : se añadio a MAUTIC .....")
                        else:
                             print(str(datetime.datetime.now()) + " : " + i['email']+" : NO se añadio a MAUTIC .....")

                        
                        actualizar_vtiger_campo_mautic(i['id'], sessionId)


                
                    
                    break

                else:
                    print(print(str(datetime.datetime.now()) + ": Retrive FALLO....."))

    
        except:

            print(str(datetime.datetime.now()) + ": Error en la busqueda, se reintenta")
            time.sleep(2)



### Esta funcion añade a Mautic la fila que se esta procesando, recibo como parametro un JSON con toda la informacion...
def anadir_mautic( JSONData):

    cNombre = JSONData['firstname']
    cApellido = JSONData['lastname']
    website = JSONData['website']
    email = JSONData['email']
    mx = JSONData['cf_852']
    country = JSONData['country']



    url = 'http://mautic.mailshield.com.mx/api/contacts/new?'
    parametros = 'firstname=' + cNombre + '&lastname=' + cApellido +'&website=' + website  + '&mx=' + mx  + '&email=' + email + '&country=' + country
    cadena_bynary = parametros.encode()

    req = urllib2.Request(url)
    req.add_header('Authorization','Basic QWRtaW46OXlDTWlWWXJ5OFpwWHhUJQ==')

    try:

        resp = urllib2.urlopen(req, data=cadena_bynary)

        if resp.status == 201:

            print(str(datetime.datetime.now()) + ': Se añadio registro')
        
            ### Vamos a parserar la respuesta...
            raw_data = resp.read()
            data = json.loads(raw_data.decode("utf-8"))

            return True


        else:

            print(str(datetime.datetime.now()) + 'No se puedo realizar la carga en MAUTI: status = ' + str( resp.status) )
        
            return False

    except:
        print(str(datetime.datetime.now()) +  'Error en la conexion con Matuic')



def actualizar_vtiger_campo_mautic(id, sessionId):
    

    print(id)


    pythonDictionary = dict(id=id, cf_874=1)
    jsondata = json.dumps(pythonDictionary)

    parametros = 'operation=revise&sessionName=' + sessionId + '&elementType=Leads&element=' + jsondata
    parametros_bynary = parametros.encode()

    url = 'https://www.mailshield.tech/vtigercrm/webservice.php?'

    contador = 0
    while True:
        try:
            updatelead = urlopen(url, data = parametros_bynary)

            if updatelead.status == 200:

                #### Comprobamos el exito

                raw_data = updatelead.read()
                data = json.loads(raw_data.decode("utf-8"))  

                exito = data['success']

                if exito == True:

                    print(str(datetime.datetime.now()) + id + ':Se actualizo registro en el CRM')
                    return True


        except:
            print(str(datetime.datetime.now()) + id + ':ERROR EN acceso al CRM...')
            contador = contador + 1
            if contador < 5:
                time.sleep(2)
            else:
                ### Abortamos la apliacion
                sys.exit()




def vtiger_conexion():

    contador = 0

    while True:

        try:
      
            response = urlopen('https://www.mailshield.tech/vtigercrm/webservice.php?operation=getchallenge&username=admin')


            if response.status == 200:


                raw_data = response.read()
                data = json.loads(raw_data.decode("utf-8"))    
                exito = data['success']

                if exito == True:
                    print(str(datetime.datetime.now()) + "Challenge correcto....")

                    ######## Tuvimos exito tomamos el token 

                    token = data['result']['token']
                    encodedKey = md5(token + 'davYhwRrtWamv4wR')

     
                    url = 'https://www.mailshield.tech/vtigercrm/webservice.php?'
                    parametros = 'operation=login&username=admin&accessKey=' + encodedKey
                    cadena_bynary = parametros.encode()


                    loginResponse = urlopen(url, data = cadena_bynary)

                    if loginResponse.status == 200:

                        raw_data = loginResponse.read()
                        #print(raw_data)
                        login_data = json.loads(raw_data.decode("utf-8"))
                        exito = login_data['success']

                        if exito == True:
                            print(str(datetime.datetime.now()) + 'Acceso al CRM Correcto....')

                            sessionId = login_data['result']['sessionName']
                            userId = login_data['result']['userId']


                            return(sessionId, userId)


        except:

            print(str(datetime.datetime.now()) + "Error en el Challenge conexion se reintentara")
            contador = contador + 1
            if contador < 5:
                time.sleep(2)
            else:
                print(str(datetime.datetime.now()) + ": No se puedo realizar la conexion la aplicacion termino...")
                sys.exit()
            









if __name__ == "__main__":



    main()





