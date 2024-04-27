import os
import requests
import random
import time
from loguru import logger


# logging configs
dir_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(dir_path, 'faucet.log')

logger.remove()
logger.add(log_path, format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | '
                              '<level>{level: ^7}</level> | '
                              '<level>{message}</level>')
logger.info('Starting.......')


# core configs
account_token = 'YOUR DISCORD ACCOUNT TOKEN'
channel_id = 'DISCORD CHANNEL ID'
message_text = 'MESSAGE TO SEND'

# proxy config
debug_mode = False
if debug_mode == True:
    proxies = {
    'https': 'http://127.0.0.1:7890/',
    'http': 'http://127.0.0.1:7890/'
    }
else:
    proxies = None

header = {
    "Authorization": account_token,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
  };

while True:
    nonce = str(random.randint(10**18, 10**18 + 2*(10**17)))
    payload = {"mobile_network_type":"unknown","content":message_text,"nonce":nonce,"tts":False, "flags":0}
    url = "https://discord.com/api/v9/channels/" + channel_id + "/messages"
    response = requests.post(url=url, headers=header, json=payload, proxies=proxies).json()
    if 'code' in response:
        logger.error(response['message'])
        time.sleep(random.uniform(60*60, 60*60*2))
    else:
        logger.info('success')
        time.sleep(random.uniform(60*60*6, 60*60*6.5))
