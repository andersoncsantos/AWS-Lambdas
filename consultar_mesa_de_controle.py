import boto3
import os
import time
from datetime import date

def build_response(message):
    return {
        "dialogAction" : {
            "type" : "Close",
            "fulfillmentState": "Fulfilled",
            "message" : {
                "contentType": "PlainText",
                "content": message
            }
        }
    }
    
def lambda_handler(event, context):
    
    os.environ['TZ'] = 'America/Sao_Paulo'
    time.tzset()
    
    hora_atual = time.localtime()
    time_string = time.strftime("%H:%M:%S", hora_atual)
    
    #time_string = '14:50:00'
    
    turno = ""
    
    if time_string > '07:00:00' and time_string < '14:45:00':
        turno = "manha"
    
    if time_string > '14:45:00' and time_string < '23:00:00':
        turno = "tarde"
        
    if time_string > '23:00:00':
        turno = "noite"
        
    if time_string > '00:00:00' and time_string < '07:00:00':
        turno = "noite"
    
    #turno = event['currentIntent']['slots']["turno"]
    
    date_time = time.strftime("%Y-%m-%d")
    d = int(time.strftime("%d"))
    m = int(time.strftime("%m"))
    y = int(time.strftime("%Y"))

    f_date = date(1899, 12, 30)
    l_date = date(y, m, d)
    delta = l_date - f_date
    
    dt = delta.days
    
    sc_table = boto3.resource('dynamodb').Table('Mesa_de_Controle')
    
    if turno == "manha":
        members = sc_table.get_item(Key={'Id' : dt})['Item']['MembersT1']
        
    if turno == "tarde":
        members = sc_table.get_item(Key={'Id' : dt})['Item']['MembersT2']
        
    if turno == "noite":
        members = sc_table.get_item(Key={'Id' : dt})['Item']['MembersT3']
    
    try:
        response = sc_table.get_item(Key={'Id' : dt})['Item']
    except KeyError:
        msg = "Escala nao foi cadastrada:exclamation:"
        return build_response(msg)
    else:
        #if 'mesa_de_controle' == event['currentIntent']['name']:
        options = members
        sorted_op = sorted(options)
        #sorted_op_str = ''.join(sorted_op)
        msg = ""
        for i, option in enumerate(sorted_op):
            msg += ":point_right::skin-tone-3: {} :slack_call: 1056\n".format(option)
                
                
        return build_response(msg)