# WhatsApp ChatGPT BOT

This will listen to your messages, when one of the trigger emojis are found, it will open a chatbot with a persona.

## Install

1. create an AWS ubuntu server
2. log in via SSH
3. install this project

```bash

sudo apt update
apt install python3-pip
sudo apt install python3.10-venv

wget https://github.com/jrd3n/WhatsApp_Chatgpt_BOT/archive/refs/heads/main.zip

sudo apt install unzip
unzip main.zip

cd WhatsApp_Chatgpt_BOT-main/

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

mv ./lib/PWDS_copy.py ./lib/PWDS.py

nano ./lib/PWDS.py

```

Add you apis details to the PWDS file.

### green API

https://green-api.com/en/

create account

scan the qr code with whatapp

look up the public ip address of your server and add the webhook to the acount

http://{public_ip}:5000/WhatsApp_webhook

get the IP and Number and add to the PWDs.py

### ChatGPT

https://platform.openai.com/

## Test the server

now that you have the API information save the file. CNTROL+X and yes

test the server

```bash

python3 app.py

```
run for a bit

close with cntrol+c

### To install and run forever

```bash

crontab -e
1 # select you favorite editor

```

add the following comand at the bottom of the file
```bash

@reboot cd /home/ubuntu/WhatsApp_Chatgpt_BOT-main && /home/ubuntu/WhatsApp_Chatgpt_BOT-main/venv/bin/python3 /home/ubuntu/WhatsApp_Chatgpt_BOT-main/app.py  >> /home/ubuntu/WhatsApp_Chatgpt_BOT-main/log.txt 2>&1
```
control x to save

```bash
sudo reboot

```
