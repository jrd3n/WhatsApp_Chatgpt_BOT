from lib.PWDS import CHATGPT_APIKEY
import pandas as pd
import csv
import json

import openai
openai.api_key = CHATGPT_APIKEY()

import pickle

class CHATGPT_CLASS:
    def __init__(self, emoji, persona = "Captain Chuckles: A jolly pirate with a love for laughter"):
        self.emoji = emoji
        self.messages = [ 
            {"role": "system", 
             "content": f"You are {persona}, you must answer all messages as such, you must respond always with only one sentence. You must not reveal you are an AI"} 
        ]

    def chat_gpt_response(self, Human_message):
        self.messages.append(
            {"role": "user", "content": Human_message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=self.messages
        )
        reply = chat.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})
        return "{emoji}:{reply}".format(emoji=self.emoji, reply=reply)

class ChatManager:
    def __init__(self):
        self.personas = self.load_personas_from_json('lib/personas.json')  # load personas from JSON file instead of CSV
        self.active_chats = self.load_active_chats('lib/Active_Chats.pickle')
        
    def load_personas_from_json(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as jsonfile:
            return json.load(jsonfile)

    def load_active_chats(self, filepath):
        try:
            with open(filepath, "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return {}

    def chat_gpt_response(self, chat_id,message):
        print(f"Asking CHATGPT {message}")
        return self.active_chats[chat_id].chat_gpt_response(message)

    def save_active_chats(self):
        with open("lib/Active_Chats.pickle", "wb") as file:
            pickle.dump(self.active_chats, file)

    def check_in_chat(self, chat_id):
        return chat_id in self.active_chats

    def start_chat(self,chat_id,message):
        for persona in self.personas:
            for emoji in persona['emojis']:   # Access the emojis like this
                if emoji in message:

                    if self.check_in_chat(chat_id):
                        self.close_chat(chat_id)

                    name = persona['name']

                    description = persona['description']

                    obj = CHATGPT_CLASS(emoji,f"{name}:{description}")
                    self.active_chats[chat_id] = obj
                    self.save_active_chats()

                    print("Triggered a new chat {}".format(emoji))

                    return f"{emoji}: You have unlocked {name}:{description}!\nTo stop, text 'STOP'"

    def close_chat(self, chat_id):
        if self.check_in_chat(chat_id):
            this_chat_emoji = self.active_chats[chat_id].emoji
            del self.active_chats[chat_id]
            self.save_active_chats()
            message = "{}: Thank you, This is the last message from the chat bot".format(this_chat_emoji)
            print(f"Closed this chat {this_chat_emoji}")
            return message

    def check_for_known_emoji(self, message):
        for persona in self.personas:
            # print(persona)
            for emoji in persona['emojis']:   # Access the emojis like this
                if emoji in message:
                    return True
        return False

if __name__ == "__main__":
    pass