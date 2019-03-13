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
    
    equipe = event['currentIntent']['slots']["equipe"]
    
    # captured_date = event['currentIntent']['slots']["Date_Input"]
   
    # dt = datetime.strptime(captured_date, '%Y-%m-%d')
    # y = int(dt.strftime("%Y"))
    # m = int(dt.strftime("%m"))
    # d = int(dt.strftime("%d"))
    
    # f_date = date(1899, 12, 30)
    # l_date = date(y, m, d)
    # delta = l_date - f_date
    
    # captured_date_result = delta.days
    
    date_time = time.strftime("%Y-%m-%d")
    d = int(time.strftime("%d"))
    m = int(time.strftime("%m"))
    y = int(time.strftime("%Y"))

    f_date = date(1899, 12, 30)
    l_date = date(y, m, d)
    delta = l_date - f_date
    
    dt = delta.days
    
    if equipe == "oss":
        sc_table = boto3.resource('dynamodb').Table('Sobreaviso_OSS')
               
    if equipe == "ps":
        sc_table = boto3.resource('dynamodb').Table('Sobreaviso_CorePS')
        
    if equipe == "cs":
        sc_table = boto3.resource('dynamodb').Table('Sobreaviso_CoreCS')
        
    if equipe == "datacom":
        sc_table = boto3.resource('dynamodb').Table('Sobreaviso_DataComm')
        
    if equipe == "ran":
        sc_table = boto3.resource('dynamodb').Table('Sobreaviso_RAN')
        
    if equipe == "security":
        sc_table = boto3.resource('dynamodb').Table('Sobreaviso_SOC')
        
    if equipe == "tx":
        sc_table = boto3.resource('dynamodb').Table('Sobreaviso_TX')
        
    if equipe == "datavas":
        sc_table = boto3.resource('dynamodb').Table('Sobreaviso_DataVas')
        
    try:
        response = sc_table.get_item(Key={'Id' : dt})['Item']
    except KeyError:
        msg = "Escala nao foi cadastrada:exclamation:"
        return build_response(msg)
    else:
        #if 'pesquisar_escalas' == event['currentIntent']['name']:
        options = sc_table.get_item(Key={'Id' : dt})['Item']['Members']
        sorted_op = sorted(options)
        #sorted_op_str = ''.join(sorted_op)
        msg = ""
        for i, option in enumerate(sorted_op):
            msg += "{}\n".format(option)
                
                
        return build_response(msg)
    
    