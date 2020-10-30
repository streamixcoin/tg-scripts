#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import os, sys
import csv
import traceback
import time
import random

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

def banner():
    print(f"""
\__    ___/___ |  |   ____   ________________    _____    /   _____/ ________________  ______ ______   ___________ 
  |    |_/ __ \|  | _/ __ \ / ___\_  __ \__  \  /     \   \_____  \_/ ___\_  __ \__  \ \____ \\____ \_/ __ \_  __ \
  |    |\  ___/|  |_\  ___// /_/  >  | \// __ \|  Y Y  \  /        \  \___|  | \// __ \|  |_> >  |_> >  ___/|  | \/
  |____| \___  >____/\___  >___  /|__|  (____  /__|_|  / /_______  /\___  >__|  (____  /   __/|   __/ \___  >__|   
             \/          \/_____/            \/      \/          \/     \/           \/|__|   |__|        \/    
     
     Recoded By Raghav
        """)

cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    banner()
    print(re+"[!] run python3 setup.py first !!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')
    banner()
    client.sign_in(phone, input(gr+'[+] Enter the code: '+re))
 
os.system('clear')
banner()
 
chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
 
for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
 
i=0
for group in groups:
    print(gr+'['+cy+str(i)+gr+']'+cy+' - '+group.title)
    i+=1

print(gr+'[+] Choose a group to add members')
g_index = input(gr+"[+] Enter a Number : "+re)
target_group=groups[int(g_index)]
 
target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)
receiver = InputPeerUser(target_group.id,target_group.access_hash)

try:
    client.send_message(target_group_entity, 'testing message')
except PeerFloodError:
    print(re+"[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
except UserPrivacyRestrictedError:
    print(re+"[!] The user's privacy settings do not allow you to do this. Skipping.")
except:
    traceback.print_exc()
    print(re+"[!] Unexpected Error")
print("finished !!\n")