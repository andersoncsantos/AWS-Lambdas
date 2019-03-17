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
    
    equipe = event['currentIntent']['slots']["equipe"]
    colaborador = event['currentIntent']['slots']["worker"]
    captured_date = event['currentIntent']['slots']["dia"]
    periodo = event['currentIntent']['slots']["periodo"]
    
    if colaborador == "teste1":
        contato = "11 91234-5678"
    
    dt = datetime.strptime(captured_date, '%Y-%m-%d')
    y = int(dt.strftime("%Y"))
    m = int(dt.strftime("%m"))
    d = int(dt.strftime("%d"))
    
    f_date = date(1899, 12, 30)
    l_date = date(y, m, d)
    delta = l_date - f_date
    
    result = delta.days
    
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
    
    # sc_table = boto3.resource('dynamodb').Table('Sobreaviso_OSS')
    # sc_table.update_item(Key={'Id': 43831},
    # UpdateExpression='SET Members = :m',
    # ExpressionAttributeValues={':m': {colaborador}})
    
    sc_table.put_item(Item={'Id': result, 'Date': captured_date, 'Members': {
        ":date: " + periodo,
        ":point_right::skin-tone-3: " + colaborador,
        ":slack_call: " + contato
        
    }})
    
    msg = "Update realizado com sucesso!\n up!"
                      

    return build_response(msg)