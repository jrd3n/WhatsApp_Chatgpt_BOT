from lib.PWDS import GREENAPI_APIKEY, GREENAPI_ID
from whatsapp_api_client_python import API
import time

#http://52.56.245.5:5000/WhatsApp_webhook

def readMSG(data):
    try:
        type_webhook = data.get('typeWebhook')

        if type_webhook == "NONE" or type_webhook == "outgoingAPIMessageReceived":
            return False

        chat_id = data.get('senderData', {}).get('chatId')
        sender_id = data['senderData']['sender']
        sender_name = data['senderData']['senderName']
        message_data = data.get('messageData', {})

        message = None
        if 'textMessageData' in message_data:
            message = message_data['textMessageData'].get('textMessage')
        elif 'extendedTextMessageData' in message_data:
            message = message_data['extendedTextMessageData'].get('text')

        id_message = data.get('idMessage')
        # sendByApi  = data.get('sendByApi')

        # print(f"Send by API = {sendByApi}")

        # if sendByApi != False:
        #     return False

        if message is None:
            return False
            
        return [chat_id, sender_id, sender_name, message, type_webhook, id_message]
    
    except:
        return False
    
greenAPI = API.GreenApi(
    GREENAPI_ID(),GREENAPI_APIKEY()
)

def Mark_as_Read(chat_id,Message_id):

    response = greenAPI.marking.readChat(chatId=chat_id,idMessage=Message_id)

    print(response.data)

def Send_Message(chat_id, Message, idMessage):
    #Send_Message(Recipient,Message,Message_id,chat_id):
    print(f"Sending the message {Message}")
    # print("Now here")
    response = greenAPI.sending.sendMessage(chat_id, "{MESSAGE}".format(MESSAGE=Message))
    print(f"The response from the server {response.data}")

    while response.data == None:
        time.sleep(3)
        response = greenAPI.sending.sendMessage(chat_id, "{MESSAGE}".format(MESSAGE=Message))
        print(f"The response from the server {response.data}")

    Mark_as_Read(chat_id,idMessage)

    pass

if __name__ == "__main__":

    Send_Message('447986843737@c.us',"Hello")

    pass