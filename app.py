from flask import Flask, render_template, request
from lib.GREEN_API import *
import pickle
import time

# from lib.PWDS import GREENAPI_ID

app = Flask(__name__)

from lib.CHATGPT_API import ChatManager

# Create an instance of the ChatManager
chat_manager = ChatManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/WhatsApp_webhook', methods=['POST'])
def webhook():

    data = request.get_json()

    print(data)

    Decypted_Message = readMSG(data)

    if Decypted_Message:

        [chat_id, sender_id, sender_name, message, type_webhook, idMessage] = Decypted_Message

        print(f"From : '{sender_id}', in chat '{chat_id}', type '{type_webhook}', message '{message}'")

        if ("stop" in message.lower() or "go away" in message.lower() or "fuck off" in message.lower()) and chat_manager.check_in_chat(chat_id):
            chat_manager_Response = chat_manager.close_chat(chat_id)
            Send_Message(chat_id,chat_manager_Response, idMessage)
            # Mark_as_Read(chat_id,idMessage)

            # time.sleep(60)

        if chat_manager.check_for_known_emoji(message):
            chat_manager_Response = chat_manager.start_chat(chat_id,message)
            Send_Message(chat_id,chat_manager_Response, idMessage)
            # Mark_as_Read(chat_id,idMessage)

            # time.sleep(60)

        if chat_manager.check_in_chat(chat_id):
            chat_manager_Response = chat_manager.chat_gpt_response(chat_id,message)
            Send_Message(chat_id,chat_manager_Response, idMessage)
            # Mark_as_Read(chat_id,idMessage)

            # time.sleep(60)

    return 'OK', 200

if __name__ == '__main__':
    # import time

    # time.sleep(5)
    app.run(host='0.0.0.0', port=5000,debug=False)