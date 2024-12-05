from Database import Database
import json
import binascii


def handler(event, context):
    database = Database()
    result = {}
    print(event)

    if event['multiValueQueryStringParameters']["type"][0] == '0':
        barcode = database.get_item_by_barcode(event['multiValueQueryStringParameters']['barcode'][0])
        if barcode:
            result = barcode.get_json()
        else:
            result = {
                "statusCode": 202,
                "body": "not found"
            }
    elif event['multiValueQueryStringParameters']["type"][0] == '1':
        barcode = (event['multiValueQueryStringParameters']['barcode'][0])
        name = binascii.hexlify((event['multiValueQueryStringParameters']['name'][0]).encode()).decode()
        p1 = (event['multiValueQueryStringParameters']['p1'][0])
        p2 = (event['multiValueQueryStringParameters']['p2'][0])
        p3 = (event['multiValueQueryStringParameters']['p3'][0])
        p4 = (event['multiValueQueryStringParameters']['p4'][0])
        database.add_new_barcode(barcode, name, p1, p2, p3, p4)

        result = {
            'statusCode': 200,
            'body': "ok"}


    else:
        result = {
            'statusCode': 404,
            'body': event}
        


    return result

