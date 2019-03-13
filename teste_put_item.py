import boto3

sc_table = boto3.resource('dynamodb').Table('escalas')
#sc_table.get_item(Key={'team' : 'Security'})['Item']['members']
sc_table.put_item(Item={'team': 'OSS', 'members': {
    'Victor', 
    'Anderson', 
    'Mario', 
    'Klug', 
    'Leonardo Guerreiro', 
    'Leonardo Pedro'}})