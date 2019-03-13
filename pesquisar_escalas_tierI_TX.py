import boto3
import os
import time
from datetime import date
from datetime import datetime

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
    
    turno = event['currentIntent']['slots']["turno"]
    captured_date = event['currentIntent']['slots']["dia"]
    
    dt = datetime.strptime(captured_date, '%Y-%m-%d')
    y = int(dt.strftime("%Y"))
    m = int(dt.strftime("%m"))
    d = int(dt.strftime("%d"))
    
    f_date = date(1899, 12, 30)
    l_date = date(y, m, d)
    delta = l_date - f_date
    
    result = delta.days
    
    # date_time = time.strftime("%Y-%m-%d")
    # d = int(time.strftime("%d"))
    # m = int(time.strftime("%m"))
    # y = int(time.strftime("%Y"))

    # f_date = date(1899, 12, 30)
    # l_date = date(y, m, d)
    # delta = l_date - f_date
    
    # dt = delta.days
    
    sc_table = boto3.resource('dynamodb').Table('Escala_TierI_TX')
    
    if turno == "manha":
        members = sc_table.get_item(Key={'Id' : result})['Item']['MembersT1']
        
    if turno == "tarde":
        members = sc_table.get_item(Key={'Id' : result})['Item']['MembersT2']
        
    if turno == "noite":
        members = sc_table.get_item(Key={'Id' : result})['Item']['MembersT3']
    
    try:
        response = sc_table.get_item(Key={'Id' : result})['Item']
    except KeyError:
        msg = "Escala nao foi cadastrada:exclamation:"
        return build_response(msg)
    else:
        if 'pesquisar_escala_tierI_TX' == event['currentIntent']['name']:
            options = members
            sorted_op = sorted(options)
            #sorted_op_str = ''.join(sorted_op)
            msg = ""
            for i, option in enumerate(sorted_op):
                msg += ":point_right::skin-tone-3: {} :slack_call: 7206 | 7207\n".format(option)
                
                
        return build_response(msg)